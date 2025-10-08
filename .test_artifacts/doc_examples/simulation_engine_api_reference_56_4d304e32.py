# Example from: docs\api\simulation_engine_api_reference.md
# Index: 56
# Runnable: True
# Hash: 4d304e32

k1 = f(x_n, u_n, t_n)
k2 = f(x_n + dt/2 * k1, u_n, t_n + dt/2)
k3 = f(x_n + dt/2 * k2, u_n, t_n + dt/2)
k4 = f(x_n + dt * k3, u_n, t_n + dt)
x_{n+1} = x_n + dt/6 * (k1 + 2*k2 + 2*k3 + k4)