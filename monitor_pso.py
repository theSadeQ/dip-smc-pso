#!/usr/bin/env python
"""
Real-time PSO Optimization Monitor
Displays live progress of Phase 2 PSO optimization
"""

import os
import sys
import time
import json
from datetime import datetime, timedelta

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def parse_progress(stderr_line):
    """Extract iteration and cost from PySwarms progress line"""
    # Format: "pyswarms.single.global_best:   3%|3         |6/200, best_cost=94.7"
    import re
    match = re.search(r'(\d+)/(\d+), best_cost=([\d.]+)', stderr_line)
    if match:
        current = int(match.group(1))
        total = int(match.group(2))
        cost = float(match.group(3))
        return current, total, cost
    return None, None, None

def format_time(seconds):
    """Format seconds as human-readable duration"""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        return f"{int(seconds/60)}m {int(seconds%60)}s"
    else:
        hours = int(seconds / 3600)
        mins = int((seconds % 3600) / 60)
        return f"{hours}h {mins}m"

def monitor_pso():
    """Monitor PSO optimization progress"""
    controllers = ['sta_smc', 'adaptive_smc', 'hybrid_adaptive_sta_smc']

    print("\n" + "="*70)
    print("  Phase 2 PSO Optimization Monitor")
    print("="*70)
    print("\nMonitoring: optimization_results/phase2_pso_results/\n")

    start_time = time.time()
    last_update = None

    while True:
        clear_screen()
        print("\n" + "="*70)
        print(f"  Phase 2 PSO Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        print(f"Runtime: {format_time(time.time() - start_time)}")
        print("-"*70)

        for ctrl in controllers:
            json_path = f'optimization_results/phase2_pso_results/{ctrl}_gains.json'

            # Check if completed
            if os.path.exists(json_path):
                with open(json_path) as f:
                    data = json.load(f)
                    cost = data.get('cost', 'N/A')
                    gains = data.get('gains', [])
                    print(f"\n[OK] {ctrl.upper()}")
                    print(f"  Status: COMPLETE")
                    print(f"  Final cost: {cost:.6f}")
                    print(f"  Gains: {gains}")
            else:
                print(f"\n[...] {ctrl.upper()}")
                print(f"  Status: OPTIMIZING or PENDING")
                print(f"  Output: Waiting for optimization to complete...")

        print("\n" + "-"*70)
        print("Press Ctrl+C to exit monitor")
        print("="*70)

        # Check every 30 seconds
        time.sleep(30)

if __name__ == '__main__':
    try:
        monitor_pso()
    except KeyboardInterrupt:
        print("\n\n[INFO] Monitor stopped by user")
        sys.exit(0)
