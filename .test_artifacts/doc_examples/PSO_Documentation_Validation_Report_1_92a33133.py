# Example from: docs\PSO_Documentation_Validation_Report.md
# Index: 1
# Runnable: False
# Hash: 92a33133

"""
Particle Swarm Optimisation (PSO) tuner for sliding-mode controllers.

This module defines the high-throughput, vectorised `PSOTuner` class that wraps
a particle swarm optimisation algorithm around the vectorised simulation of a
double inverted pendulum (DIP) system.  It incorporates improvements from
design review steps, including decoupling of global state, explicit random
number generation, dynamic instability penalties and configurable cost
normalisation.  The implementation follows robust control theory practices
and is fully documented with theoretical backing.

References used throughout this module are provided in the accompanying
design-review report.
"""