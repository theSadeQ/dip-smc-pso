#!/usr/bin/env python
"""
======================================================================================
FILE: .ai_workspace/tools/migration/migrate_docs_structure.py
PROJECT: Double Inverted Pendulum - SMC & PSO
DESCRIPTION: Automated migration script for docs/ reorganization (Dec 19, 2025)
AUTHOR: Claude Code
DATE: 2025-12-19
======================================================================================

Reorganizes docs/ directory from 102 cluttered root files to 6 essential files,
categorizing content into 8 domain-specific subdirectories.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List

# ====================================================================================
# CORE FILES TO KEEP AT ROOT (6 files)
# ====================================================================================

CORE_ROOT_FILES = [
    "index.md",           # Sphinx entry point
    "conf.py",            # Sphinx configuration
    "Makefile",           # Build automation
    "README.md",          # Docs directory guide
    "CODEOWNERS",         # GitHub governance
    "requirements.txt"    # Sphinx dependencies
]

# ====================================================================================
# MARKDOWN FILE CATEGORIZATION (71 files → 8 subdirectories)
# ====================================================================================

MARKDOWN_CATEGORIES = {
    "theory": [
        "pso_algorithm_mathematical_foundations.md",
        "mathematical_validation_procedures.md",
        "quality_gate_independence_framework.md",
        "safety_critical_testing_framework.md",
        "testing_standards_framework.md",
        "controller_testing_standards.md",
        "statistical_validation_frameworks.md",
        "reproducibility_validation_framework.md",
        "safety_validation_procedures.md",
        "test_quality_gates.md",
        "quality_gates_specification.md",
        "vectorized_simulation_testing_standards.md",
        "hypothesis_testing_integration.md",
        "hypothesis_testing_standards.md"
    ],
    "optimization": [
        "pso_integration_technical_specification.md",
        "pso_troubleshooting_maintenance_manual.md",
        "factory_integration_documentation.md",
        "pso_optimizer_integration.md",
        "pso_swarm_simulation_integration.md",
        "optimization_workflow.md",
        "optimization_results_specification.md",
        "pso_visualization_guide.md",
        "pso_advanced_usage.md",
        "pso_config_schema.md",
        "pso_usage_guide.md"
    ],
    "production": [
        "production_readiness_framework.md",
        "deployment_validation_checklists.md",
        "hil_quickstart.md",
        "streamlit_troubleshooting_guide.md",
        "streamlit_interface_guide.md",
        "production_considerations.md"
    ],
    "testing": [
        "test_execution_guide.md",
        "test_execution_execution_guide.md",  # Duplicate - will note
        "fault_detection_system_documentation.md",
        "test_infrastructure_guide.md",
        "testing_best_practices.md",
        "benchmark_testing_framework.md",
        "fault_detection_integration.md",
        "fault_detection_testing.md"
    ],
    "architecture": [
        "architecture.md",
        "architecture_control_room.md",
        "context.md",
        "memory_management_architecture.md",
        "controller_memory_management.md"
    ],
    "guides": [
        "FAQ.md",
        "memory_management_quick_reference.md",
        "DEPENDENCIES.md",
        "TROUBLESHOOTING.md",
        "simulation_guide.md",
        "getting_started_guide.md",
        "controller_guide.md",
        "QUICK_START.md"
    ],
    "reference": [
        "configuration_schema_validation.md",
        "CONTROLLER_FACTORY.md",
        "PLANT_MODEL.md",
        "CONFIG_SCHEMA.md"
    ],
    "meta": [
        "CHANGELOG.md",
        "LICENSES.md",
        "NAVIGATION.md",  # Critical navigation hub
        "SITEMAP.md",
        "INDEX.md",
        "CONTRIBUTING.md",
        "citations.md",
        "sitemap_theory_foundations.md",
        "sitemap_testing_validation.md",
        "sitemap_optimization.md",
        "attribution.md",
        "doc_conventions.md",
        "claude-backup.md"  # Check if obsolete
    ]
}

# ====================================================================================
# BUILD ARTIFACTS (11 files → .artifacts/docs_build/logs/)
# ====================================================================================

BUILD_ARTIFACTS = [
    "build_log.txt",
    "build_log_week2.txt",
    "build_output.txt",
    "build_week2.txt",
    "build_week34.txt",
    "build_week5.txt",
    "dry_run_output.txt",
    "fix_log.txt",
    "sphinx_build_log.txt",
    "week2_build_log.txt",
    "week34_build.txt"
]

# ====================================================================================
# PYTHON SCRIPTS (6 files, excluding conf.py)
# ====================================================================================

VALIDATION_SCRIPTS = [
    "validate_week2.py",
    "validate_week34.py",
    "validate_week5.py"
]

UTILITY_SCRIPTS = [
    "find_broken_file.py",
    "fix_all_markdown_headings.py",
    "replace_citations.py"
]

# ====================================================================================
# DATA FILES (10 files)
# ====================================================================================

DATA_FILES = {
    "docs/_data/citations": [
        "citation_map.json",
        "citation_validation_report.json",
        "citations.csv"
    ],
    "docs/_data/specs": [
        "io_contracts.csv"
    ],
    "docs/bib": [
        "refs.bib"
    ],
    "docs/_static/pwa": [
        "offline.html"
    ],
    ".artifacts/docs_build/reports": [
        "validation_report.json",
        "requirements_traceability.csv"
    ]
}

# ====================================================================================
# FILES TO DELETE
# ====================================================================================

FILES_TO_DELETE = [
    "index.md.bak"  # Obsolete backup
]

# ====================================================================================
# MIGRATION FUNCTIONS
# ====================================================================================

def create_directory_structure():
    """Create all necessary directories for reorganized docs."""
    print("[INFO] Creating directory structure...")

    directories = [
        # Markdown category directories
        "docs/theory",
        "docs/optimization",
        "docs/production",
        "docs/testing",
        "docs/architecture",
        "docs/guides",
        "docs/reference",
        "docs/meta",

        # Data directories
        "docs/_data/citations",
        "docs/_data/specs",
        "docs/bib",
        "docs/_static/pwa",

        # Build artifacts
        ".artifacts/docs_build/logs",
        ".artifacts/docs_build/reports",

        # Script destinations
        ".ai_workspace/tools/validation/docs",
        ".ai_workspace/tools/docs"
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  [OK] Created {directory}")

def move_markdown_files():
    """Move markdown files to categorized subdirectories."""
    print("\n[INFO] Categorizing and moving markdown files...")

    moved_count = 0
    for category, files in MARKDOWN_CATEGORIES.items():
        print(f"\n  Category: {category}/ ({len(files)} files)")
        for file in files:
            source = f"docs/{file}"
            destination = f"docs/{category}/{file}"

            if os.path.exists(source):
                shutil.move(source, destination)
                moved_count += 1
                print(f"    [OK] Moved {file}")
            else:
                print(f"    [WARNING] Not found: {file}")

    print(f"\n  [OK] Moved {moved_count} markdown files to categorized subdirectories")
    return moved_count

def move_build_artifacts():
    """Move build artifacts to .artifacts/docs_build/logs/."""
    print("\n[INFO] Moving build artifacts...")

    moved_count = 0
    for file in BUILD_ARTIFACTS:
        source = f"docs/{file}"
        destination = f".artifacts/docs_build/logs/{file}"

        if os.path.exists(source):
            shutil.move(source, destination)
            moved_count += 1
            print(f"  [OK] Moved {file}")
        else:
            print(f"  [WARNING] Not found: {file}")

    print(f"\n  [OK] Moved {moved_count} build artifacts")
    return moved_count

def move_scripts():
    """Move validation and utility scripts to .ai_workspace/tools/."""
    print("\n[INFO] Moving Python scripts...")

    moved_count = 0

    # Validation scripts
    print("  Validation scripts:")
    for file in VALIDATION_SCRIPTS:
        source = f"docs/{file}"
        destination = f".ai_workspace/tools/validation/docs/{file}"

        if os.path.exists(source):
            shutil.move(source, destination)
            moved_count += 1
            print(f"    [OK] Moved {file}")
        else:
            print(f"    [WARNING] Not found: {file}")

    # Utility scripts
    print("  Utility scripts:")
    for file in UTILITY_SCRIPTS:
        source = f"docs/{file}"
        destination = f".ai_workspace/tools/docs/{file}"

        if os.path.exists(source):
            shutil.move(source, destination)
            moved_count += 1
            print(f"    [OK] Moved {file}")
        else:
            print(f"    [WARNING] Not found: {file}")

    print(f"\n  [OK] Moved {moved_count} scripts")
    return moved_count

def move_data_files():
    """Move data files to organized locations."""
    print("\n[INFO] Moving data files...")

    moved_count = 0
    for destination_dir, files in DATA_FILES.items():
        print(f"  Destination: {destination_dir}/")
        for file in files:
            source = f"docs/{file}"
            destination = f"{destination_dir}/{file}"

            if os.path.exists(source):
                shutil.move(source, destination)
                moved_count += 1
                print(f"    [OK] Moved {file}")
            else:
                print(f"    [WARNING] Not found: {file}")

    print(f"\n  [OK] Moved {moved_count} data files")
    return moved_count

def delete_obsolete_files():
    """Delete obsolete backup and temporary files."""
    print("\n[INFO] Deleting obsolete files...")

    deleted_count = 0
    for file in FILES_TO_DELETE:
        filepath = f"docs/{file}"

        if os.path.exists(filepath):
            os.remove(filepath)
            deleted_count += 1
            print(f"  [OK] Deleted {file}")
        else:
            print(f"  [WARNING] Not found: {file}")

    print(f"\n  [OK] Deleted {deleted_count} obsolete files")
    return deleted_count

def verify_core_files():
    """Verify core files remain at docs/ root."""
    print("\n[INFO] Verifying core files at docs/ root...")

    missing = []
    for file in CORE_ROOT_FILES:
        filepath = f"docs/{file}"
        if os.path.exists(filepath):
            print(f"  [OK] {file}")
        else:
            print(f"  [ERROR] Missing: {file}")
            missing.append(file)

    if missing:
        print(f"\n  [ERROR] {len(missing)} core files missing!")
        return False
    else:
        print(f"\n  [OK] All {len(CORE_ROOT_FILES)} core files present")
        return True

def count_remaining_root_files():
    """Count files remaining at docs/ root after migration."""
    print("\n[INFO] Counting remaining files at docs/ root...")

    root_files = [f for f in os.listdir("docs") if os.path.isfile(f"docs/{f}")]
    count = len(root_files)

    print(f"  Files at docs/ root: {count}")
    print(f"  Target: {len(CORE_ROOT_FILES)} core files")

    if count > len(CORE_ROOT_FILES):
        print(f"\n  [WARNING] {count - len(CORE_ROOT_FILES)} unexpected files remain:")
        for file in root_files:
            if file not in CORE_ROOT_FILES:
                print(f"    - {file}")
    else:
        print(f"\n  [OK] docs/ root cleaned successfully!")

    return count

# ====================================================================================
# MAIN EXECUTION
# ====================================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("DOCS/ DIRECTORY REORGANIZATION MIGRATION")
    print("=" * 80)
    print("\nTarget: 102 files -> 6 core files (94% reduction)")
    print("\n" + "=" * 80)

    # Phase 1: Create directories
    create_directory_structure()

    # Phase 2: Move markdown files
    markdown_count = move_markdown_files()

    # Phase 3: Move build artifacts
    artifacts_count = move_build_artifacts()

    # Phase 4: Move scripts
    scripts_count = move_scripts()

    # Phase 5: Move data files
    data_count = move_data_files()

    # Phase 6: Delete obsolete files
    deleted_count = delete_obsolete_files()

    # Phase 7: Verify core files
    core_ok = verify_core_files()

    # Phase 8: Count remaining files
    remaining_count = count_remaining_root_files()

    # Summary
    print("\n" + "=" * 80)
    print("MIGRATION SUMMARY")
    print("=" * 80)
    print(f"Markdown files moved: {markdown_count}")
    print(f"Build artifacts moved: {artifacts_count}")
    print(f"Scripts moved: {scripts_count}")
    print(f"Data files moved: {data_count}")
    print(f"Obsolete files deleted: {deleted_count}")
    print(f"Total files processed: {markdown_count + artifacts_count + scripts_count + data_count + deleted_count}")
    print(f"\nCore files verified: {'YES' if core_ok else 'NO'}")
    print(f"Remaining at docs/ root: {remaining_count} (target: {len(CORE_ROOT_FILES)})")

    if remaining_count == len(CORE_ROOT_FILES) and core_ok:
        print("\n[OK] MIGRATION SUCCESSFUL!")
    else:
        print("\n[WARNING] Manual review required")

    print("=" * 80)
