# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 22
# Runnable: False
# Hash: a6dc7122

# Single trajectory → SequentialOrchestrator
# PSO (30 particles) → BatchOrchestrator (25x faster)
# Monte Carlo (1000 runs) → ParallelOrchestrator (4 cores)
# HIL testing → RealTimeOrchestrator