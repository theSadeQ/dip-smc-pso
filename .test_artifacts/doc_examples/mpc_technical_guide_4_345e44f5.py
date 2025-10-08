# Example from: docs\controllers\mpc_technical_guide.md
# Index: 4
# Runnable: False
# Hash: 345e44f5

# example-metadata:
# runnable: false

# Decision variables
X = cp.Variable((6, N+1))  # State trajectory
U = cp.Variable((1, N))    # Control sequence

# Cost function
Q = diag([q_x, q_θ, q_θ, q_ẋ, q_θ̇, q_θ̇])
R = r_u

obj = 0
constraints = [X[:, 0] == x₀]

for k in range(N):
    # Stage cost
    e_k = X[:, k] - x_ref[:, k]
    obj += cp.quad_form(e_k, Q) + cp.quad_form(U[:, k], R)

    # Dynamics constraint
    constraints += [X[:, k+1] == A_d @ X[:, k] + B_d @ U[:, k]]

    # Input bounds
    constraints += [cp.abs(U[0, k]) <= max_force]

    # State bounds
    constraints += [
        cp.abs(X[0, k]) <= max_cart_pos,
        cp.abs(X[1, k] - π) <= max_theta_dev,
        cp.abs(X[2, k] - π) <= max_theta_dev
    ]

# Terminal cost
e_N = X[:, N] - x_ref[:, N]
obj += cp.quad_form(e_N, Q)

problem = cp.Problem(cp.Minimize(obj), constraints)