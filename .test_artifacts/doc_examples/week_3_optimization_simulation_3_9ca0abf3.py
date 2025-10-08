# Example from: docs\plans\documentation\week_3_optimization_simulation.md
# Index: 3
# Runnable: True
# Hash: 9ca0abf3

BaseOptimizer (ABC)
  ├── SwarmOptimizer (ABC)
  │   ├── PSOCore
  │   ├── AdaptivePSO
  │   └── MultiObjectivePSO
  ├── EvolutionaryOptimizer (ABC)
  │   ├── GeneticAlgorithm
  │   └── DifferentialEvolution
  └── BayesianOptimizer