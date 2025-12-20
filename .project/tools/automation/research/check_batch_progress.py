#!/usr/bin/env python3
"""Quick progress checker for batch research runs."""
import sys
import re
from pathlib import Path

def check_progress(log_file: str):
    """Parse log file and report progress."""
    log_path = Path(log_file)
    if not log_path.exists():
        print(f"Log file not found: {log_file}")
        return

    with open(log_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Extract key metrics
    total_claims = None
    completed = []
    current_claim = None
    errors = []
    warnings = []

    for line in lines:
        # Total claims loaded
        if 'Loaded' in line and 'claims for research' in line:
            match = re.search(r'Loaded (\d+) claims', line)
            if match:
                total_claims = int(match.group(1))

        # Completed claims
        if 'Completed' in line and 'citations in' in line:
            match = re.search(r'Completed ([A-Z-]+\d+):', line)
            if match:
                completed.append(match.group(1))

        # Current claim being processed
        if 'Processing' in line and '...' in line:
            match = re.search(r'Processing ([A-Z-]+\d+):', line)
            if match:
                current_claim = match.group(1)

        # Errors and warnings
        if '[ERROR]' in line:
            errors.append(line.strip())
        if '[WARNING]' in line and 'Rate limit' in line:
            warnings.append(line.strip())

    # Calculate progress
    num_completed = len(completed)
    progress_pct = (num_completed / total_claims * 100) if total_claims else 0

    # Print report
    print("=" * 70)
    print("BATCH RESEARCH PROGRESS")
    print("=" * 70)
    print(f"Total claims: {total_claims}")
    print(f"Completed: {num_completed}/{total_claims} ({progress_pct:.1f}%)")
    print(f"Current: {current_claim or 'N/A'}")
    print(f"Rate limit warnings: {len(warnings)}")
    print(f"Errors: {len(errors)}")

    if completed:
        print(f"\nLast 3 completed: {', '.join(completed[-3:])}")

    if errors:
        print(f"\nRecent errors ({min(3, len(errors))}):")
        for err in errors[-3:]:
            print(f"  {err[:100]}...")

    print("\n" + "=" * 70)

if __name__ == '__main__':
    from src.utils.infrastructure.logging.paths import LOG_DIR
    log_file = sys.argv[1] if len(sys.argv) > 1 else str(LOG_DIR / 'batch_01_optimization.log')
    check_progress(log_file)
