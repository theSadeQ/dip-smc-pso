# Example from: docs\reports\DOCUMENTATION_EXPERT_TECHNICAL_ASSESSMENT_REPORT.md
# Index: 3
# Runnable: False
# Hash: b0211db0

# example-metadata:
# runnable: false

"""
Particle Swarm Optimisation (PSO) tuner for sliding-mode controllers.

This module defines the high-throughput, vectorised `PSOTuner` class that wraps
a particle swarm optimisation algorithm around the vectorised simulation...
It incorporates improvements from design review steps, including decoupling of
global state, explicit random number generation, dynamic instability penalties
and configurable cost normalisation.
"""