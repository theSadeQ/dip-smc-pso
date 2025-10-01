#!/usr/bin/env python3
"""
Systematic analyzer for .copy() patterns across codebase.
Classifies each copy as UNNECESSARY, NECESSARY, or CONVERTIBLE.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Root directory
ROOT = Path(__file__).parent.parent

# Categories
UNNECESSARY = "UNNECESSARY"
NECESSARY = "NECESSARY"
CONVERTIBLE = "CONVERTIBLE"

def analyze_copy_context(file_path: Path, line_num: int, line_content: str,
                         context_before: List[str], context_after: List[str]) -> Dict[str, Any]:
    """Analyze a single .copy() occurrence and classify it."""

    # Extract variable name
    match = re.search(r'(\w+)\s*=\s*(.+)\.copy\(\)', line_content)
    if not match:
        match = re.search(r'\.copy\(\)', line_content)
        var_name = "inline"
    else:
        var_name = match.group(1)

    full_context = '\n'.join(context_before + [line_content] + context_after)

    # Classification logic
    confidence = 0.0
    category = NECESSARY  # Default to safe classification
    reason = ""

    # UNNECESSARY patterns
    if "return" in line_content and ".copy()" in line_content:
        # Return statements with copy - likely defensive programming
        if "self." in line_content:
            category = NECESSARY
            reason = "Public getter returning internal state (defensive copy required)"
            confidence = 0.95
        elif any("error" in ctx.lower() or "fail" in ctx.lower() for ctx in context_before):
            category = NECESSARY
            reason = "Error result construction (copy required for immutability)"
            confidence = 0.9
        else:
            category = UNNECESSARY
            reason = "Return copy of local variable (can return directly)"
            confidence = 0.7

    elif "config_dict = config_dict.copy()" in line_content:
        category = NECESSARY
        reason = "Config dict mutation safety (prevents side effects on caller's dict)"
        confidence = 0.95

    elif ".broadcast_to(" in full_context and ".copy()" in line_content:
        category = NECESSARY
        reason = "broadcast_to returns read-only view, copy makes it writable"
        confidence = 1.0

    elif var_name == "init_b" and ".copy()" in line_content:
        if "broadcast_to" in line_content:
            category = NECESSARY
            reason = "broadcast_to returns read-only view"
            confidence = 1.0
        else:
            category = UNNECESSARY
            reason = "Local variable immediately assigned to preallocated array"
            confidence = 0.85

    elif "x_curr = x0.copy()" in line_content:
        # Check if x_curr is mutated or just reassigned
        if any("x_curr = " in line for line in context_after[:10]):
            category = UNNECESSARY
            reason = "x_curr immediately reassigned in loop (no mutation)"
            confidence = 0.95
        else:
            category = NECESSARY
            reason = "State variable may be mutated"
            confidence = 0.7

    elif ".append({" in full_context and ".copy()" in line_content:
        category = NECESSARY
        reason = "Storing in history/list (copy prevents aliasing)"
        confidence = 0.95

    elif "perturbed_params = " in line_content and ".copy()" in line_content:
        category = NECESSARY
        reason = "Parameter perturbation (mutation follows)"
        confidence = 0.95

    elif "state_plus = " in line_content or "state_minus = " in line_content:
        category = NECESSARY
        reason = "Numerical differentiation (element mutation follows)"
        confidence = 1.0

    elif "trial = target.copy()" in line_content:
        category = NECESSARY
        reason = "Crossover operation (mutation follows)"
        confidence = 1.0

    elif "penalized_fitness = fitness.copy()" in line_content:
        category = NECESSARY
        reason = "Constraint penalty application (mutation follows)"
        confidence = 0.95

    elif any("diagnostics" in ctx for ctx in context_before + context_after):
        if ".copy()" in line_content and ("state" in line_content or "control" in line_content):
            category = UNNECESSARY
            reason = "Diagnostic copy for result dict (read-only snapshot, no mutation risk)"
            confidence = 0.8

    elif ".astype()" in line_content and ".copy()" in line_content:
        category = CONVERTIBLE
        reason = ".astype() already creates copy, .copy() redundant"
        confidence = 1.0

    elif ".reshape(" in line_content and ".copy()" in line_content:
        category = CONVERTIBLE
        reason = ".reshape() returns view by default, .copy() can be removed if view acceptable"
        confidence = 0.7

    elif "fitness_history.copy()" in line_content or "convergence_history.copy()" in line_content:
        category = NECESSARY
        reason = "History list copy for result isolation"
        confidence = 0.9

    elif "_create_failure_result" in full_context or "_create_success_result" in full_context:
        category = UNNECESSARY
        reason = "Result dict construction (immutable after return, no mutation risk)"
        confidence = 0.85

    elif "'position': position.copy()" in line_content or "'objectives': objectives.copy()" in line_content:
        category = NECESSARY
        reason = "Archive storage (prevents external mutation)"
        confidence = 0.95

    elif "self.personal_best_positions[i] = self.positions[i].copy()" in line_content:
        category = NECESSARY
        reason = "PSO personal best tracking (independent from current position)"
        confidence = 1.0

    elif "self._last_state = state.copy()" in line_content:
        category = NECESSARY
        reason = "State caching for next iteration (prevents aliasing)"
        confidence = 0.95

    elif "stats = " in line_content and ".copy()" in line_content:
        category = UNNECESSARY
        reason = "Stats dict copy for read-only access (no mutation needed)"
        confidence = 0.8

    return {
        "file": str(file_path.relative_to(ROOT)),
        "line": line_num,
        "pattern": line_content.strip(),
        "category": category,
        "reason": reason,
        "confidence": confidence,
        "context": full_context
    }

def scan_file(file_path: Path) -> List[Dict[str, Any]]:
    """Scan a single file for .copy() occurrences."""
    results = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if '.copy()' in line:
                context_before = lines[max(0, i-3):i]
                context_after = lines[i+1:min(len(lines), i+4)]

                analysis = analyze_copy_context(
                    file_path, i+1, line,
                    context_before, context_after
                )
                results.append(analysis)

    except Exception as e:
        print(f"Error scanning {file_path}: {e}")

    return results

def main():
    """Main analysis entry point."""
    print("Scanning codebase for .copy() patterns...")

    # Scan all Python files
    all_files = list(ROOT.glob("src/**/*.py")) + list(ROOT.glob("tests/**/*.py"))

    all_results = []
    files_scanned = 0

    for file_path in sorted(all_files):
        if file_path.name.startswith('.'):
            continue

        file_results = scan_file(file_path)
        if file_results:
            all_results.extend(file_results)
            files_scanned += 1
            print(f"  {file_path.relative_to(ROOT)}: {len(file_results)} copies")

    # Categorize results
    by_category = {
        UNNECESSARY: [],
        NECESSARY: [],
        CONVERTIBLE: []
    }

    for result in all_results:
        by_category[result['category']].append(result)

    # Generate hotspots
    file_counts = {}
    for result in all_results:
        file_path = result['file']
        file_counts[file_path] = file_counts.get(file_path, 0) + 1

    hotspots = [
        {
            "file": file_path,
            "copy_count": count,
            "impact": "high" if count >= 10 else "medium" if count >= 5 else "low"
        }
        for file_path, count in sorted(file_counts.items(), key=lambda x: -x[1])[:20]
    ]

    # Create inventory
    inventory = {
        "agent": "code-beautification-directory-specialist",
        "issue": "#16",
        "timestamp": datetime.now().isoformat(),
        "scan_summary": {
            "files_scanned": files_scanned,
            "total_copies": len(all_results),
            "unnecessary_copies": len(by_category[UNNECESSARY]),
            "necessary_copies": len(by_category[NECESSARY]),
            "convertible_to_views": len(by_category[CONVERTIBLE])
        },
        "by_category": by_category,
        "hotspots": hotspots
    }

    # Save inventory
    output_file = ROOT / "copy_pattern_inventory.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(inventory, f, indent=2)

    print(f"\n{'='*70}")
    print("SCAN COMPLETE")
    print(f"{'='*70}")
    print(f"Files scanned: {files_scanned}")
    print(f"Total .copy() occurrences: {len(all_results)}")
    print(f"  UNNECESSARY: {len(by_category[UNNECESSARY])} ({len(by_category[UNNECESSARY])/len(all_results)*100:.1f}%)")
    print(f"  NECESSARY: {len(by_category[NECESSARY])} ({len(by_category[NECESSARY])/len(all_results)*100:.1f}%)")
    print(f"  CONVERTIBLE: {len(by_category[CONVERTIBLE])} ({len(by_category[CONVERTIBLE])/len(all_results)*100:.1f}%)")
    print(f"\nInventory saved to: {output_file}")
    print(f"\nTop 5 hotspots:")
    for hotspot in hotspots[:5]:
        print(f"  {hotspot['file']}: {hotspot['copy_count']} copies ({hotspot['impact']} impact)")

if __name__ == "__main__":
    main()
