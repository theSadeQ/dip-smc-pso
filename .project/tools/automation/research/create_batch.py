#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
#  .dev_tools/research/create_batch.py
# ═══════════════════════════════════════════════════════════════════════════
"""
Create batch input files for research pipeline.

Extracts claims by module and/or priority from claims_inventory.json
and formats them for research_pipeline.py.

Usage:
    python create_batch.py --module optimization --output batch_optimization.json
    python create_batch.py --priority HIGH --output batch_high_all.json
    python create_batch.py --module controllers --priority HIGH --output batch_controllers_high.json
"""

import json
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any, Optional


def extract_module_from_path(file_path: str) -> str:
    """
    Extract module name from file path.

    Args:
        file_path: Path like "src/optimization/pso_optimizer.py"

    Returns:
        Module name like "optimization", or "other" if not matched
    """
    if not file_path:
        return "unknown"

    # Normalize path separators
    path = file_path.replace("\\", "/")
    parts = path.split("/")

    # Extract module from src/ paths
    if len(parts) >= 2 and parts[0] == "src":
        return parts[1]

    # Extract module from docs/ paths
    if len(parts) >= 2 and parts[0] == "docs":
        return parts[1] if len(parts) >= 2 else "docs"

    return "other"


def filter_claims(
    inventory: Dict[str, Any],
    module: Optional[str] = None,
    priority: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Filter claims by module and/or priority.

    Args:
        inventory: Loaded claims_inventory.json
        module: Module name to filter (e.g., "optimization", "controllers")
        priority: Priority level to filter (e.g., "HIGH", "CRITICAL", "MEDIUM")

    Returns:
        Filtered list of claim objects
    """
    filtered = []

    for claim in inventory["claims"]:
        # Priority filter
        if priority and claim.get("priority") != priority:
            continue

        # Module filter
        if module:
            claim_module = extract_module_from_path(claim.get("file_path", ""))
            if claim_module != module:
                continue

        filtered.append(claim)

    return filtered


def create_batch_file(
    claims: List[Dict[str, Any]],
    output_path: str,
) -> Dict[str, Any]:
    """
    Create batch JSON file in research pipeline format.

    Args:
        claims: List of claim objects
        output_path: Path to save batch file

    Returns:
        Batch data structure
    """
    # Count by priority
    by_priority = defaultdict(int)
    for claim in claims:
        priority = claim.get("priority", "UNKNOWN")
        by_priority[priority] += 1

    # Build research queue (claim IDs organized by priority)
    research_queue = defaultdict(list)
    for claim in claims:
        priority = claim.get("priority", "UNKNOWN")
        research_queue[priority].append(claim["id"])

    # Ensure all priority levels exist (even if empty)
    for priority in ["CRITICAL", "HIGH", "MEDIUM"]:
        if priority not in research_queue:
            research_queue[priority] = []

    # Create batch structure
    batch = {
        "metadata": {
            "total_claims": len(claims),
            "by_priority": dict(by_priority),
        },
        "research_queue": dict(research_queue),
        "claims": claims,
    }

    # Save to file
    output_path_obj = Path(output_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path_obj, "w", encoding="utf-8") as f:
        json.dump(batch, f, indent=2, ensure_ascii=False)

    return batch


def main():
    parser = argparse.ArgumentParser(
        description="Create batch input files for research pipeline"
    )
    parser.add_argument(
        "--inventory",
        type=str,
        default=".artifacts/claims_inventory.json",
        help="Path to claims inventory (default: .artifacts/claims_inventory.json)",
    )
    parser.add_argument(
        "--module",
        type=str,
        help="Filter by module (e.g., optimization, controllers, analysis)",
    )
    parser.add_argument(
        "--priority",
        type=str,
        choices=["CRITICAL", "HIGH", "MEDIUM"],
        help="Filter by priority level",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output batch file path (e.g., .artifacts/batch_optimization.json)",
    )
    parser.add_argument(
        "--list-modules",
        action="store_true",
        help="List all available modules and exit",
    )

    args = parser.parse_args()

    # Load inventory
    inventory_path = Path(args.inventory)
    if not inventory_path.exists():
        print(f"Error: Inventory file not found: {inventory_path}")
        return 1

    with open(inventory_path, "r", encoding="utf-8") as f:
        inventory = json.load(f)

    # List modules mode
    if args.list_modules:
        modules = defaultdict(int)
        for claim in inventory["claims"]:
            module = extract_module_from_path(claim.get("file_path", ""))
            modules[module] += 1

        print("Available modules:")
        print("=" * 60)
        for module, count in sorted(modules.items(), key=lambda x: -x[1]):
            print(f"  {module:20s}: {count:4d} claims")
        print("=" * 60)
        return 0

    # Validate arguments
    if not args.module and not args.priority:
        print("Error: Must specify at least --module or --priority")
        return 1

    # Filter claims
    filtered = filter_claims(inventory, module=args.module, priority=args.priority)

    if not filtered:
        print(
            f"Warning: No claims found matching filters (module={args.module}, priority={args.priority})"
        )
        return 1

    # Create batch file
    batch = create_batch_file(filtered, args.output)

    # Print summary
    print("=" * 60)
    print("BATCH FILE CREATED")
    print("=" * 60)
    print(f"Output: {args.output}")
    print(f"Total claims: {batch['metadata']['total_claims']}")
    print(f"By priority: {batch['metadata']['by_priority']}")
    if args.module:
        print(f"Module filter: {args.module}")
    if args.priority:
        print(f"Priority filter: {args.priority}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    exit(main())
