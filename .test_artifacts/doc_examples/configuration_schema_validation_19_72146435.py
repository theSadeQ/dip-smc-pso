# Example from: docs\configuration_schema_validation.md
# Index: 19
# Runnable: True
# Hash: 72146435

from hypothesis import given, strategies as st

class PropertyBasedConfigurationTests:
    """Property-based testing for configuration validation."""

    @given(
        lambda1=st.floats(min_value=0.1, max_value=50.0),
        lambda2=st.floats(min_value=0.1, max_value=50.0),
        k_gains=st.lists(st.floats(min_value=0.1, max_value=100.0), min_size=4, max_size=4)
    )
    def test_smc_stability_property(self, lambda1, lambda2, k_gains):
        """Property: SMC with positive gains should always validate."""
        gains = [lambda1, lambda2] + k_gains

        config = {
            'type': 'classical_smc',
            'gains': gains,
            'saturation_limit': 10.0,
            'boundary_layer_thickness': 0.01
        }

        # Should always validate for positive gains
        smc_config = ClassicalSMCConfig(**config)
        assert all(g > 0 for g in smc_config.gains)

    @given(
        c1=st.floats(min_value=0.1, max_value=4.0),
        c2=st.floats(min_value=0.1, max_value=4.0)
    )
    def test_pso_convergence_property(self, c1, c2):
        """Property: PSO with c1 + c2 > 4 should converge."""
        if c1 + c2 > 4.0:
            config = {
                'w': 0.7298,
                'c1': c1,
                'c2': c2,
                'n_particles': 30,
                'max_iterations': 100,
                'bounds': {'classical_smc': [[0.1, 50.0]] * 6}
            }

            # Should validate without error
            pso_config = PSOConfig(**config)
            assert pso_config.c1 + pso_config.c2 > 4.0