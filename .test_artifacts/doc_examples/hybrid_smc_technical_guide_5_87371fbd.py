# Example from: docs\controllers\hybrid_smc_technical_guide.md
# Index: 5
# Runnable: True
# Hash: 87371fbd

# Primary PSO parameters [c1, λ1, c2, λ2]
gains = [77.6216, 44.449, 17.3134, 14.25]  # Optimal PSO result

# Fixed internal parameters (not PSO-tuned)
k1_init = 2.0      # Initial adaptive gain 1
k2_init = 1.0      # Initial adaptive gain 2
gamma1 = 0.5       # Adaptation rate 1
gamma2 = 0.3       # Adaptation rate 2
dead_zone = 0.01   # Adaptation dead zone