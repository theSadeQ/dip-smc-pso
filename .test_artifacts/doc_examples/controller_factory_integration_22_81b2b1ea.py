# Example from: docs\technical\controller_factory_integration.md
# Index: 22
# Runnable: False
# Hash: 81b2b1ea

def validate_lyapunov_stability(controller, test_states):
    """Validate Lyapunov stability for controller."""

    for state in test_states:
        # Compute Lyapunov function
        V = compute_lyapunov_function(state, controller.config)

        # Compute time derivative
        dV_dt = compute_lyapunov_derivative(state, controller)

        # Verify stability condition
        if dV_dt > 0:
            logger.warning(f"Lyapunov condition violated at state {state}")
            return False

    return True