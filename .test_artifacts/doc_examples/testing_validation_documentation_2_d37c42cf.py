# Example from: docs\factory\testing_validation_documentation.md
# Index: 2
# Runnable: True
# Hash: d37c42cf

class TestParameterValidation:
    """Comprehensive parameter validation testing."""

    def setup_method(self):
        """Setup validation test environment."""
        self.validator = ParameterValidator()

    @pytest.mark.parametrize("controller_type,valid_gains", [
        ('classical_smc', [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]),
        ('adaptive_smc', [25.0, 18.0, 15.0, 10.0, 4.0]),
        ('sta_smc', [35.0, 20.0, 25.0, 18.0, 12.0, 8.0]),
        ('hybrid_adaptive_sta_smc', [18.0, 12.0, 10.0, 8.0])
    ])
    def test_valid_gain_validation(self, controller_type: str, valid_gains: List[float]):
        """Test validation passes for valid gain configurations."""
        controller_info = CONTROLLER_REGISTRY[controller_type]

        # Should not raise any exceptions
        _validate_controller_gains(valid_gains, controller_info)

        # Test with numpy array input
        _validate_controller_gains(np.array(valid_gains), controller_info)

    def test_adaptive_smc_gamma_validation(self):
        """Test specific validation for adaptive SMC gamma parameter."""
        # Valid gamma values
        valid_configs = [
            [10.0, 5.0, 8.0, 3.0, 2.0],    # Normal gamma
            [10.0, 5.0, 8.0, 3.0, 0.5],   # Low gamma
            [10.0, 5.0, 8.0, 3.0, 8.0],   # High gamma
        ]

        for gains in valid_configs:
            controller_info = CONTROLLER_REGISTRY['adaptive_smc']
            _validate_controller_gains(gains, controller_info)

        # Invalid gamma values should trigger warnings but not errors
        # (Warnings are handled at higher level)
        extreme_gamma_gains = [10.0, 5.0, 8.0, 3.0, 15.0]  # Very high gamma
        controller_info = CONTROLLER_REGISTRY['adaptive_smc']
        _validate_controller_gains(extreme_gamma_gains, controller_info)

    def test_super_twisting_k1_k2_relationship(self):
        """Test STA-SMC K1/K2 relationship validation."""
        # Optimal relationship: K1 > K2
        optimal_gains = [35.0, 20.0, 25.0, 18.0, 12.0, 8.0]  # K1=35 > K2=20
        controller_info = CONTROLLER_REGISTRY['sta_smc']
        _validate_controller_gains(optimal_gains, controller_info)

        # Suboptimal but valid: K1 <= K2 (should warn but not fail)
        suboptimal_gains = [20.0, 25.0, 25.0, 18.0, 12.0, 8.0]  # K1=20 < K2=25
        _validate_controller_gains(suboptimal_gains, controller_info)

    def test_parameter_bounds_validation(self):
        """Test parameter bounds checking."""
        from src.controllers.factory.smc_factory import validate_parameter_ranges

        # Test within bounds
        controller_type = 'classical_smc'
        gains = [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
        bounds = [(5.0, 50.0), (5.0, 40.0), (3.0, 30.0), (3.0, 25.0), (10.0, 80.0), (1.0, 15.0)]

        # Should not raise exception
        validate_parameter_ranges(gains, controller_type, bounds)

        # Test outside bounds
        out_of_bounds_gains = [100.0, 15.0, 12.0, 8.0, 35.0, 5.0]  # First gain too high
        with pytest.raises(ValueError):
            validate_parameter_ranges(out_of_bounds_gains, controller_type, bounds)

    def test_configuration_migration_validation(self):
        """Test validation of migrated configurations."""
        # Test deprecated parameter handling
        deprecated_config = {
            'gains': [10.0, 5.0, 8.0, 3.0, 15.0, 2.0],
            'max_force': 100.0,
            'gamma': 0.1,  # Should be deprecated for classical_smc
        }

        # Should handle gracefully without crashing
        from src.controllers.factory.deprecation import check_deprecated_config
        migrated_config = check_deprecated_config('classical_smc', deprecated_config)

        # Gamma should be removed for classical_smc
        assert 'gamma' not in migrated_config

    def test_hybrid_smc_sub_configuration_validation(self):
        """Test validation of hybrid SMC sub-configurations."""
        # Create valid sub-configurations
        from src.controllers.smc.algorithms.classical.config import ClassicalSMCConfig
        from src.controllers.smc.algorithms.adaptive.config import AdaptiveSMCConfig

        classical_config = ClassicalSMCConfig(
            gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
            max_force=150.0,
            dt=0.001,
            boundary_layer=0.02
        )

        adaptive_config = AdaptiveSMCConfig(
            gains=[25.0, 18.0, 15.0, 10.0, 4.0],
            max_force=150.0,
            dt=0.001
        )

        # Test hybrid controller creation with sub-configs
        controller = create_controller(
            'hybrid_adaptive_sta_smc',
            config={
                'classical_config': classical_config,
                'adaptive_config': adaptive_config
            },
            gains=[18.0, 12.0, 10.0, 8.0]
        )

        assert controller is not None