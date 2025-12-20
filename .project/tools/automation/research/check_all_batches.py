#!/usr/bin/env python3
"""Check progress of all running batches."""
import re
import sys
from pathlib import Path
from collections import defaultdict

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Centralized log paths
from src.utils.infrastructure.logging.paths import LOG_DIR

def parse_log(log_file):
    """Parse a batch log file and extract metrics."""
    if not Path(log_file).exists():
        return None

    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    total_claims = 0
    completed = []
    current_claim = None
    rate_limits = 0
    errors = 0

    for line in lines:
        if 'Loaded' in line and 'claims for research' in line:
            match = re.search(r'Loaded (\d+) claims', line)
            if match:
                total_claims = int(match.group(1))

        if 'Completed' in line and 'citations in' in line:
            match = re.search(r'Completed ([A-Z-]+\d+):', line)
            if match:
                completed.append(match.group(1))

        if 'Processing' in line and '...' in line:
            match = re.search(r'Processing ([A-Z-]+\d+):', line)
            if match:
                current_claim = match.group(1)

        if '[ERROR]' in line:
            errors += 1
        if '[WARNING]' in line and 'Rate limit' in line:
            rate_limits += 1

    num_completed = len(completed)
    progress_pct = (num_completed / total_claims * 100) if total_claims else 0

    return {
        'total': total_claims,
        'completed': num_completed,
        'progress_pct': progress_pct,
        'current': current_claim,
        'rate_limits': rate_limits,
        'errors': errors
    }

def main():
    batches = [
        ('Batch 1: Optimization', LOG_DIR / 'batch_01_optimization.log'),
        ('Batch 2: Controllers', LOG_DIR / 'batch_02_controllers.log'),
        ('Batch 3: Analysis', LOG_DIR / 'batch_03_analysis.log'),
        ('Batch 4: Simulation', LOG_DIR / 'batch_04_simulation.log'),
        ('Batch 5: Plant', LOG_DIR / 'batch_05_plant.log'),
        ('Batch 6: Interfaces', LOG_DIR / 'batch_06_interfaces.log'),
        ('Batch 7: Utils', LOG_DIR / 'batch_07_utils.log'),
        ('Batch 8: Other', LOG_DIR / 'batch_08_other.log'),
        ('Batch 9: MEDIUM', LOG_DIR / 'batch_09_medium.log'),
    ]

    print("=" * 80)
    print("ALL BATCHES PROGRESS SUMMARY")
    print("=" * 80)

    total_claims = 0
    total_completed = 0

    for name, log_file in batches:
        stats = parse_log(log_file)
        if stats:
            total_claims += stats['total']
            total_completed += stats['completed']
            status = 'RUNNING' if stats['progress_pct'] < 100 else 'COMPLETE'
            print(f"{name:25} {stats['completed']:3}/{stats['total']:3} ({stats['progress_pct']:5.1f}%) [{status}]")
        else:
            print(f"{name:25} NOT STARTED or log not found")

    print("=" * 80)
    overall_pct = (total_completed / total_claims * 100) if total_claims else 0
    print(f"{'OVERALL PROGRESS':25} {total_completed:3}/{total_claims:3} ({overall_pct:5.1f}%)")
    print("=" * 80)

if __name__ == '__main__':
    main()
