# Example from: docs\pso_troubleshooting_maintenance_manual.md
# Index: 9
# Runnable: False
# Hash: ab06ce39

def validate_gain_ratios(particles, controller_type):
       """Enhanced gain validation with ratio constraints."""
       valid = np.ones(particles.shape[0], dtype=bool)

       if controller_type == 'classical_smc':
           c1, lambda1, c2, lambda2, K, kd = particles.T

           # Ratio constraints
           valid &= (lambda1 / lambda2 > 0.5) & (lambda1 / lambda2 < 2.0)
           valid &= (K / lambda1 > 5) & (K / lambda1 < 50)
           valid &= (kd / K > 0.01) & (kd / K < 0.5)

       return valid