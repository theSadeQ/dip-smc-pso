# Example from: docs\testing\validation_methodology_guide.md
# Index: 13
# Runnable: True
# Hash: 4e1b5fe4

class TestMatrixConditioning:
    """Validate matrix conditioning for numerical stability."""

    def test_mass_matrix_conditioning(self):
        """Test mass matrix is well-conditioned."""
        from src.core.dynamics_full import FullNonlinearDynamics

        physics_cfg = {
            'M': 1.0, 'm1': 0.1, 'm2': 0.1,
            'L1': 0.5, 'L2': 0.5, 'g': 9.81
        }
        dynamics = FullNonlinearDynamics(physics_cfg)

        # Test various states
        states = [
            np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),      # Equilibrium
            np.array([0.0, np.pi/4, np.pi/6, 0.0, 0.0, 0.0]),  # Angled
            np.array([0.0, np.pi/2, np.pi/3, 0.0, 0.0, 0.0])   # Large angles
        ]

        for state in states:
            M = dynamics.compute_mass_matrix(state)

            # Compute condition number
            cond_number = np.linalg.cond(M)

            assert cond_number < 1e6, (
                f"Mass matrix poorly conditioned at {state}: "
                f"condition number = {cond_number:.2e}"
            )

    def test_mass_matrix_positive_definite(self):
        """Test mass matrix is positive definite."""
        from src.core.dynamics_full import FullNonlinearDynamics

        physics_cfg = {
            'M': 1.0, 'm1': 0.1, 'm2': 0.1,
            'L1': 0.5, 'L2': 0.5, 'g': 9.81
        }
        dynamics = FullNonlinearDynamics(physics_cfg)

        state = np.array([0.0, np.pi/4, np.pi/6, 0.0, 0.0, 0.0])
        M = dynamics.compute_mass_matrix(state)

        # Check positive definiteness via eigenvalues
        eigenvalues = np.linalg.eigvals(M)

        assert np.all(eigenvalues > 0), (
            f"Mass matrix not positive definite: eigenvalues = {eigenvalues}"
        )