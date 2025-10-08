# Example from: docs\configuration_schema_validation.md
# Index: 18
# Runnable: False
# Hash: 766843b1

class ConfigurationTestSuite:
    """Comprehensive configuration validation test suite."""

    def test_valid_configurations(self):
        """Test all valid configuration combinations."""
        test_configs = [
            'config_minimal.yaml',
            'config_development.yaml',
            'config_testing.yaml',
            'config_production.yaml'
        ]

        for config_file in test_configs:
            with open(config_file) as f:
                config_data = yaml.safe_load(f)

            # Should validate without errors
            config = MasterConfig(**config_data)
            assert config is not None

    def test_invalid_configurations(self):
        """Test configuration validation catches invalid inputs."""
        invalid_configs = [
            {'system': {'version': '0.9.0'}},  # Version too old
            {'physics': {'pendulum_length_1': -1.0}},  # Negative length
            {'controllers': {'classical_smc': {'gains': [0, 1, 2, 3, 4, 5]}}},  # Zero gain
            {'optimization': {'pso': {'c1': 2.0, 'c2': 1.0}}},  # c1 + c2 <= 4
            {'simulation': {'dt': 1.0}}}  # Time step too large
        ]

        for invalid_config in invalid_configs:
            with pytest.raises(ValidationError):
                MasterConfig(**invalid_config)

    def test_mathematical_constraints(self):
        """Test mathematical constraint validation."""
        # Test SMC stability constraints
        smc_config = {
            'type': 'classical_smc',
            'gains': [10.0, 8.0, 15.0, 12.0, 50.0, 5.0]
        }
        physics_config = {
            'pendulum_length_1': 0.5,
            'pendulum_length_2': 0.3,
            'cart_mass': 1.0,
            'pendulum_mass_1': 0.2,
            'pendulum_mass_2': 0.1,
            'gravity': 9.81
        }

        assert validate_lyapunov_stability_constraints(smc_config, physics_config)

        # Test PSO convergence constraints
        pso_config = {
            'w': 0.7298,
            'c1': 1.49618,
            'c2': 1.49618,
            'n_particles': 30,
            'bounds': {
                'classical_smc': [[0.1, 50.0]] * 6
            }
        }

        assert validate_pso_convergence_constraints(pso_config)

    def test_runtime_validation(self):
        """Test runtime parameter validation."""
        base_config = load_test_config('config_production.yaml')
        validator = RuntimeConfigValidator(base_config)

        # Test valid parameter update
        assert validator.validate_parameter_update('controllers.classical_smc.gains.0', 12.0)

        # Test invalid parameter update
        with pytest.raises(ValueError):
            validator.validate_parameter_update('controllers.classical_smc.gains.0', -5.0)

    def test_configuration_migration(self):
        """Test configuration version migration."""
        migrator = ConfigurationMigrator()

        # Load old version configuration
        old_config = load_test_config('config_v1_0.yaml')

        # Migrate to current version
        migrated_config = migrator.migrate_config(old_config, '2.1.0')

        # Validate migrated configuration
        config = MasterConfig(**migrated_config)
        assert config.system.version == '2.1.0'