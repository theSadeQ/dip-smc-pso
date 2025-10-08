# Example from: docs\guides\user-guide.md
# Index: 7
# Runnable: True
# Hash: 65b95c58

import time
start = time.time()
# Run simulation
subprocess.run(['python', 'simulate.py', '--ctrl', 'classical_smc'])
elapsed = time.time() - start
print(f"Simulation took {elapsed:.2f} seconds")