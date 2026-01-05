"""
TRL (Technology Readiness Level) Classification Script for PSO Gains

Automatically classifies PSO optimization files by maturity level and generates
shortcuts in Framework 2 (By Maturity) directory structure.

TRL Levels (NASA/EU adaptation for PSO optimization):
- Level 1: Theoretical bounds (config.yaml bounds, not empirically validated)
- Level 2: Simulation-validated (Phase 2, Phase 53 gains on nominal conditions)
- Level 3: Statistical validation (MT-7 multi-seed Monte Carlo)
- Level 4: Robustness-validated (MT-8 disturbances, LT-6 uncertainty)
- Level 5: Hardware-validated (HIL testing results)
- Level 6: Production-deployed (Currently in config.yaml controller_defaults)
- Level 7: Archived/superseded (Historical gains in archive/)

Usage:
    python classify_by_trl.py [--validate-only]
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Tuple
import sys

# Project paths
PROJECT_ROOT = Path("D:/Projects/main")
FRAMEWORK_1_ROOT = PROJECT_ROOT / ".ai_workspace/pso/by_purpose"
FRAMEWORK_2_ROOT = PROJECT_ROOT / ".ai_workspace/pso/by_maturity"
EXPERIMENTS_ROOT = PROJECT_ROOT / "academic/paper/experiments"

# TRL classification rules
TRL_RULES = {
    "level_1_theoretical": {
        "description": "Theoretical bounds from configuration",
        "paths": ["config.yaml"],
        "keywords": ["bounds", "theoretical"],
    },
    "level_2_simulation": {
        "description": "Simulation-validated on nominal conditions",
        "paths": ["phase2", "phase53", "phases/phase"],
        "keywords": ["phase2", "phase53", "standard", "nominal"],
    },
    "level_3_statistical": {
        "description": "Statistical validation via multi-seed Monte Carlo",
        "paths": ["mt7_validation", "multi_seed"],
        "keywords": ["mt7", "seed", "statistical", "monte_carlo"],
    },
    "level_4_robustness": {
        "description": "Robustness-validated (disturbances, uncertainty)",
        "paths": ["mt8", "disturbance", "robust", "lt6", "uncertainty"],
        "keywords": ["mt8", "disturbance", "robust", "lt6", "uncertainty"],
    },
    "level_5_hardware": {
        "description": "Hardware-validated via HIL testing",
        "paths": ["hil", "hardware"],
        "keywords": ["hil", "hardware", "validation"],
    },
    "level_6_production": {
        "description": "Production-deployed (config.yaml defaults)",
        "paths": ["config.yaml"],
        "keywords": ["production", "deployed", "default"],
    },
    "level_7_archived": {
        "description": "Archived/superseded gains",
        "paths": ["archive"],
        "keywords": ["archive", "old", "superseded"],
    },
}

# Controller names
CONTROLLERS = ["classical_smc", "sta_smc", "adaptive_smc", "hybrid_adaptive_sta"]


def classify_file_by_trl(file_path: str, file_name: str) -> Tuple[str, int]:
    """
    Classify a file by TRL level based on path and filename.

    Returns:
        Tuple[str, int]: (TRL level, confidence score 0-100)
    """
    file_path_lower = file_path.lower()
    file_name_lower = file_name.lower()

    # Priority order (higher priority first)
    priority = [
        "level_6_production",  # Highest priority
        "level_5_hardware",
        "level_4_robustness",
        "level_3_statistical",
        "level_2_simulation",
        "level_1_theoretical",
        "level_7_archived",  # Lowest priority
    ]

    for level in priority:
        rules = TRL_RULES[level]

        # Check path matches
        for path_pattern in rules["paths"]:
            if path_pattern in file_path_lower:
                # Check keywords for confidence boost
                keyword_matches = sum(
                    1 for kw in rules["keywords"]
                    if kw in file_name_lower or kw in file_path_lower
                )
                confidence = 70 + min(keyword_matches * 10, 30)
                return level, confidence

    # Fallback: Level 2 (simulation) with low confidence
    return "level_2_simulation", 30


def create_shortcut(
    target_path: Path,
    shortcut_path: Path,
    trl_level: str,
    controller: str,
    description: str,
) -> None:
    """Create a Windows-compatible shortcut file (.txt)"""
    shortcut_path.parent.mkdir(parents=True, exist_ok=True)

    trl_desc = TRL_RULES[trl_level]["description"]

    content = f"""# Shortcut to: {target_path.relative_to(PROJECT_ROOT)}
# Framework: Maturity-Based (TRL) Classification
# TRL Level: {trl_level.replace('_', ' ').title()}
# Description: {trl_desc}
# Controller: {controller}

Target Path:
{target_path}

TRL Classification:
{trl_desc}

Additional Context:
{description}
"""

    with open(shortcut_path, "w") as f:
        f.write(content)


def load_framework1_mapping() -> List[Dict]:
    """Load existing Framework 1 file mapping"""
    mapping_file = FRAMEWORK_1_ROOT / "FRAMEWORK_1_FILE_MAPPING.csv"

    if not mapping_file.exists():
        print(f"[WARNING] Framework 1 mapping not found: {mapping_file}")
        return []

    with open(mapping_file, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)


def extract_controller_from_filename(filename: str) -> str:
    """Extract controller name from filename"""
    filename_lower = filename.lower()

    # Priority: Most specific first
    if "hybrid_adaptive_sta" in filename_lower or "hybrid" in filename_lower:
        return "hybrid_adaptive_sta"
    if "adaptive_smc" in filename_lower or "adaptive" in filename_lower:
        return "adaptive_smc"
    if "sta_smc" in filename_lower or "sta" in filename_lower:
        return "sta_smc"
    if "classical_smc" in filename_lower or "classical" in filename_lower:
        return "classical_smc"

    return "unknown"


def generate_framework2_shortcuts(validate_only: bool = False) -> Dict:
    """
    Generate Framework 2 shortcuts based on TRL classification.

    Args:
        validate_only: If True, only validate classification without creating files

    Returns:
        Dict with statistics
    """
    stats = {
        "total_files": 0,
        "classified": 0,
        "shortcuts_created": 0,
        "errors": 0,
        "by_level": {level: 0 for level in TRL_RULES.keys()},
        "by_controller": {ctrl: 0 for ctrl in CONTROLLERS},
    }

    # Load Framework 1 mapping (if available)
    framework1_files = load_framework1_mapping()

    # If no mapping, scan Framework 1 directly
    if not framework1_files:
        print("[INFO] Scanning Framework 1 shortcuts directly...")
        framework1_files = []

        for shortcut_file in FRAMEWORK_1_ROOT.rglob("*.txt"):
            # Skip create_shortcuts.py and other non-shortcut files
            if shortcut_file.name.endswith(".py") or shortcut_file.name.endswith(".csv"):
                continue

            # Read target path from shortcut
            try:
                with open(shortcut_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    # Find the line with actual path (after "Target Path:" header)
                    target_path = None
                    found_header = False
                    for line in lines:
                        if "Target Path:" in line:
                            found_header = True
                            continue
                        if found_header and line.strip() and not line.startswith("#"):
                            target_path = line.strip()
                            break

                    if target_path:
                        framework1_files.append({
                            "shortcut": str(shortcut_file),
                            "target": target_path,
                            "filename": shortcut_file.name,
                        })
            except Exception as e:
                print(f"[ERROR] Failed to read {shortcut_file}: {e}")
                stats["errors"] += 1

    stats["total_files"] = len(framework1_files)

    # Classify and create shortcuts
    for file_entry in framework1_files:
        target_path = file_entry.get("target", "")
        filename = file_entry.get("filename", "")

        if not target_path or not filename:
            print(f"[DEBUG] Skipping file_entry (no path/name): {file_entry}")
            continue

        # Classify by TRL
        trl_level, confidence = classify_file_by_trl(target_path, filename)
        stats["classified"] += 1
        stats["by_level"][trl_level] += 1

        # Extract controller
        controller = extract_controller_from_filename(filename)
        if controller in stats["by_controller"]:
            stats["by_controller"][controller] += 1

        if validate_only and stats["classified"] <= 5:
            print(f"[DEBUG] Classified: {filename} -> {trl_level} (confidence: {confidence}%)")

        # Create shortcut
        if not validate_only:
            shortcut_name = filename.replace(".txt", f"_trl{trl_level[6]}.txt")
            shortcut_path = (
                FRAMEWORK_2_ROOT
                / trl_level
                / controller
                / shortcut_name
            )

            try:
                create_shortcut(
                    target_path=Path(target_path),
                    shortcut_path=shortcut_path,
                    trl_level=trl_level,
                    controller=controller,
                    description=f"Auto-classified from Framework 1 (confidence: {confidence}%)",
                )
                stats["shortcuts_created"] += 1
            except Exception as e:
                print(f"[ERROR] Failed to create shortcut for {filename}: {e}")
                stats["errors"] += 1

    return stats


def print_statistics(stats: Dict) -> None:
    """Print classification statistics"""
    print("\n" + "=" * 60)
    print("TRL Classification Statistics")
    print("=" * 60)
    print(f"Total files processed: {stats['total_files']}")
    print(f"Successfully classified: {stats['classified']}")
    print(f"Shortcuts created: {stats['shortcuts_created']}")
    print(f"Errors: {stats['errors']}")

    print("\n" + "-" * 60)
    print("By TRL Level:")
    print("-" * 60)
    for level, count in stats["by_level"].items():
        level_name = level.replace("_", " ").title()
        print(f"  {level_name}: {count} files")

    print("\n" + "-" * 60)
    print("By Controller:")
    print("-" * 60)
    for controller, count in stats["by_controller"].items():
        print(f"  {controller}: {count} files")

    print("\n" + "=" * 60)


def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Classify PSO files by TRL maturity level"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate classification without creating shortcuts",
    )
    args = parser.parse_args()

    print("TRL Classification Script for PSO Optimization")
    print("=" * 60)

    if args.validate_only:
        print("[MODE] Validation only (no shortcuts created)")
    else:
        print("[MODE] Full execution (shortcuts will be created)")

    print(f"\nFramework 1 Root: {FRAMEWORK_1_ROOT}")
    print(f"Framework 2 Root: {FRAMEWORK_2_ROOT}")

    # Generate shortcuts
    stats = generate_framework2_shortcuts(validate_only=args.validate_only)

    # Print statistics
    print_statistics(stats)

    # Success message
    if not args.validate_only and stats["shortcuts_created"] > 0:
        print(f"\n[OK] Created {stats['shortcuts_created']} shortcuts in Framework 2")
        print(f"     Location: {FRAMEWORK_2_ROOT}")
    elif args.validate_only:
        print(f"\n[OK] Validation complete, no files created")

    if stats["errors"] > 0:
        print(f"\n[WARNING] {stats['errors']} errors encountered")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
