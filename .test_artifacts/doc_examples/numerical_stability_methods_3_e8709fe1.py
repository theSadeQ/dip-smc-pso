# Example from: docs\theory\numerical_stability_methods.md
# Index: 3
# Runnable: True
# Hash: e8709fe1

# Boundary layer saturation function
sat_sigma = saturate(sigma, eps_dyn, method=self.switch_method)
u_robust = -self.K * sat_sigma - self.kd * sigma