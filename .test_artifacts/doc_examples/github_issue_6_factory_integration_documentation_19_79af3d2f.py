# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 19
# Runnable: True
# Hash: 79af3d2f

# Performance benchmark results from test_simulation_integration.py
Controller Performance Rankings (Lower RMS Error = Better):

1. Adaptive SMC:        RMS Error: 1.54    Max Control: 12.0N   ⭐ BEST
2. Hybrid Adaptive:     RMS Error: 2.22    Max Control: 25.5N
3. Classical SMC:       RMS Error: 2.93    Max Control: 35.0N
4. Super-Twisting:      RMS Error: 14.65   Max Control: 150.0N

Simulation Time: 5.0s
Timestep: 0.01s (500 steps)
All controllers met real-time constraints (<2ms per step)