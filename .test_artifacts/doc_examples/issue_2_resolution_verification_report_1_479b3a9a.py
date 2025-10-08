# Example from: docs\issue_2_resolution_verification_report.md
# Index: 1
# Runnable: True
# Hash: 479b3a9a

optimized_gains = [8.0, 5.0, 12.0, 6.0, 4.85, 3.43]
controller = SuperTwistingSMC(gains=optimized_gains, dt=0.01, max_force=150.0)