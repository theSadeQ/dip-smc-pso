# Example from: docs\guides\api\simulation.md
# Index: 3
# Runnable: False
# Hash: 8a56f490

# example-metadata:
# runnable: false

result = {
    't': np.ndarray,          # Time vector, shape (N+1,)
    'state': np.ndarray,      # State trajectories, shape (N+1, 6)
                              # [x, dx, θ₁, dθ₁, θ₂, dθ₂] at each timestep
    'control': np.ndarray,    # Control inputs, shape (N+1,)
    'metrics': {
        'ise': float,         # Integral of Squared Error
        'itae': float,        # Integral of Time-weighted Absolute Error
        'max_theta1': float,  # Maximum first pendulum angle (rad)
        'max_theta2': float,  # Maximum second pendulum angle (rad)
        'control_effort': float,  # Total control energy
        'settling_time': float    # Time to settle within 2% of target
    },
    'stability': {
        'converged': bool,    # Did system stabilize?
        'final_error': float  # Final tracking error
    }
}