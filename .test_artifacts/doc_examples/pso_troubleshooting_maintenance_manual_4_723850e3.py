# Example from: docs\pso_troubleshooting_maintenance_manual.md
# Index: 4
# Runnable: True
# Hash: 723850e3

# Check if Numba is available
   try:
       import numba
       print("✅ Numba available for acceleration")
   except ImportError:
       print("❌ Numba not available - install with: pip install numba")