# Example from: docs\pso_troubleshooting_maintenance_manual.md
# Index: 8
# Runnable: True
# Hash: 2d8f2d5c

def diagnose_controller_stability(gains, controller_type):
    """Diagnose controller stability issues."""
    from src.controllers.factory import ControllerFactory
    import numpy as np

    # Create controller
    controller = ControllerFactory.create_controller(controller_type, gains)

    # Test with various states
    test_states = [
        np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),  # Equilibrium
        np.array([0.1, 0.1, 0.0, 0.0, 0.0, 0.0]),  # Small perturbation
        np.array([0.5, 0.3, 0.1, 0.0, 0.0, 0.0]),  # Large perturbation
        np.array([0.1, 0.1, 0.0, 0.2, 0.2, 0.0])   # With velocities
    ]

    print(f"🔍 Stability diagnosis for {controller_type}")
    print(f"Gains: {gains}")

    for i, state in enumerate(test_states):
        try:
            control = controller.compute_control(state)
            status = "✅" if np.isfinite(control) and abs(control) <= controller.max_force else "❌"
            print(f"Test {i+1}: {status} u = {control:.3f}, |u| <= {controller.max_force}")
        except Exception as e:
            print(f"Test {i+1}: ❌ Error: {e}")

    # Check gain ratios (controller-specific)
    if controller_type == 'classical_smc':
        lambda1, lambda2 = gains[1], gains[3]
        K = gains[4]
        print(f"λ₁/λ₂ ratio: {lambda1/lambda2:.2f} (should be 0.5-2.0)")
        print(f"K/λ₁ ratio: {K/lambda1:.2f} (should be 5-50)")

# Usage
diagnose_controller_stability([5.0, 3.0, 7.0, 2.0, 25.0, 1.0], 'classical_smc')