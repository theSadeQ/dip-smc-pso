# Example from: docs\controllers\mpc_technical_guide.md
# Index: 15
# Runnable: True
# Hash: 08480d04

@dataclass
class MPCWeights:
    q_x: float = 1.0          # Cart position weight
    q_theta: float = 10.0     # Angle weight (each)
    q_xdot: float = 0.1       # Velocity weight
    q_thetadot: float = 0.5   # Angular velocity weight
    r_u: float = 1e-2         # Input effort penalty