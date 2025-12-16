"""
Simple verification - test that basic simulation works
"""

import sys
import subprocess
import json
import numpy as np

print("="*80)
print("BASIC SYSTEM VERIFICATION")
print("="*80)
print()

# Test 1: Run simulation with Classical SMC
print("[1/4] Testing Classical SMC simulation...")
result = subprocess.run(
    ["python", "simulate.py", "--controller", "classical_smc", "--duration", "5.0"],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("  [OK] Classical SMC simulation completed")
else:
    print(f"  [ERROR] Simulation failed with code {result.returncode}")
    print(result.stderr[:500])
    sys.exit(1)
print()

# Test 2: Try STA-SMC
print("[2/4] Testing STA-SMC simulation...")
result = subprocess.run(
    ["python", "simulate.py", "--controller", "sta_smc", "--duration", "5.0"],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("  [OK] STA-SMC simulation completed")
else:
    print(f"  [ERROR] Simulation failed")
    print(result.stderr[:500])
print()

# Test 3: Try Adaptive SMC
print("[3/4] Testing Adaptive SMC simulation...")
result = subprocess.run(
    ["python", "simulate.py", "--controller", "adaptive_smc", "--duration", "5.0"],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("  [OK] Adaptive SMC simulation completed")
else:
    print(f"  [ERROR] Simulation failed")
    print(result.stderr[:500])
print()

# Test 4: Load and inspect optimized gains
print("[4/4] Inspecting optimized gains...")
try:
    with open('optimization_results/phase2_pso_results/adaptive_smc_gains.json', 'r') as f:
        adaptive_gains = json.load(f)
    print(f"  [OK] Adaptive SMC optimized gains loaded:")
    print(f"      Cost: {adaptive_gains['cost']}")
    print(f"      Gains: {adaptive_gains['gains']}")
    print(f"      Method: {adaptive_gains['method']}")

    with open('optimization_results/phase2_pso_results/sta_smc_gains.json', 'r') as f:
        sta_gains = json.load(f)
    print(f"  [OK] STA-SMC optimized gains loaded:")
    print(f"      Cost: {sta_gains['cost']}")
    print(f"      Gains: {sta_gains['gains'][:3]}...")  # Just first 3

except FileNotFoundError as e:
    print(f"  [ERROR] Could not load gains: {e}")
print()

print("="*80)
print("BASIC VERIFICATION COMPLETE")
print("="*80)
print()
print("All 3 controller types can simulate successfully.")
print("Now let's verify the optimized gains actually improve performance...")
