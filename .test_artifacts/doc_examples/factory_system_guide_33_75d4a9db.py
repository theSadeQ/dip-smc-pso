# Example from: docs\controllers\factory_system_guide.md
# Index: 33
# Runnable: False
# Hash: 75d4a9db

# Solution: Ensure K1 > K2 in gain array
gains = [25.0, 15.0, ...]  # K1=25 > K2=15 ✓
gains = [15.0, 25.0, ...]  # K1=15 < K2=25 ✗