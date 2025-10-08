# Example from: docs\controllers\mpc_technical_guide.md
# Index: 13
# Runnable: False
# Hash: 90744ffb

# Decision variables
X = cp.Variable((nx, N+1))  # States: 6 × (N+1)
U = cp.Variable((nu, N))    # Controls: 1 × N

# Cost matrices
Q = np.diag([w.q_x, w.q_theta, w.q_theta, w.q_xdot, w.q_thetadot, w.q_thetadot])
R = np.array([[w.r_u]])

# Build cost function and constraints
obj = 0
cons = [X[:, 0] == x0]  # Initial condition

for k in range(N):
    # Dynamics: x_{k+1} = A_d x_k + B_d u_k
    cons += [X[:, k+1] == Ad @ X[:, k] + Bd @ U[:, k]]

    # Input bounds: |u_k| ≤ u_max
    cons += [cp.abs(U[0, k]) <= self.max_force]

    # Stage cost: ||x_k - x_ref||²_Q + ||u_k||²_R
    e = X[:, k] - Xref[:, k]
    obj += cp.quad_form(e, Q) + cp.quad_form(U[:, k], R)

    # State constraints
    cons += [cp.abs(X[0, k]) <= self.max_cart_pos]  # Cart position
    cons += [cp.abs(X[1, k] - np.pi) <= self.max_theta_dev]  # θ₁
    cons += [cp.abs(X[2, k] - np.pi) <= self.max_theta_dev]  # θ₂

# Terminal cost: ||x_N - x_ref||²_Q
eN = X[:, N] - Xref[:, N]
obj += cp.quad_form(eN, Q)

# Solve
prob = cp.Problem(cp.Minimize(obj), cons)
prob.solve(solver=cp.OSQP, warm_start=True)