# Example from: docs\configuration_integration_documentation.md
# Index: 22
# Runnable: True
# Hash: 27a951a3

#!/usr/bin/env python3
"""Complete configuration integration example."""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class ComprehensiveConfigurationExample:
    """Demonstrate comprehensive configuration integration."""

    def __init__(self):
        self.config_manager = self._setup_configuration_manager()

    def _setup_configuration_manager(self):
        """Setup configuration management system."""

        class ConfigManager:
            def __init__(self):
                self.base_config = self._load_base_config()
                self.validator = ConfigurationValidator()
                self.migrator = ConfigurationMigrationManager()

            def _load_base_config(self):
                """Load base configuration."""
                config_path = Path("config.yaml")
                if config_path.exists():
                    from src.config import load_config
                    return load_config(config_path)
                else:
                    return self._create_default_config()

            def _create_default_config(self):
                """Create default configuration."""
                return {
                    'physics': {
                        'm1': 0.5, 'm2': 0.5, 'M': 2.0,
                        'l1': 0.5, 'l2': 0.5,
                        'b1': 0.1, 'b2': 0.1,
                        'I1': 0.1, 'I2': 0.1
                    },
                    'simulation': {
                        'duration': 5.0,
                        'dt': 0.001,
                        'initial_state': [0.1, 0.05, 0.0, 0.0, 0.0, 0.0]
                    },
                    'controllers': {
                        'classical_smc': {
                            'gains': [20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
                            'max_force': 150.0,
                            'boundary_layer': 0.02,
                            'dt': 0.001
                        }
                    }
                }

            def get_controller_config(self, controller_type: str, **overrides) -> Dict[str, Any]:
                """Get validated controller configuration."""

                # Get base configuration
                base_controller_config = self.base_config['controllers'].get(controller_type, {})

                # Apply overrides
                controller_config = {**base_controller_config, **overrides}

                # Migrate deprecated parameters
                controller_config = self.migrator.check_deprecated_config(
                    controller_type, controller_config
                )

                # Validate configuration
                if not self.validator.validate_configuration(controller_type, controller_config):
                    report = self.validator.get_validation_report()
                    raise ValueError(f"Configuration validation failed: {report['errors']}")

                return controller_config

        return ConfigManager()

    def demonstration_1_basic_usage(self):
        """Demonstrate basic configuration usage."""

        print("=== Demonstration 1: Basic Configuration Usage ===")

        # Get configuration for different controllers
        for controller_type in ['classical_smc', 'adaptive_smc', 'sta_smc']:
            try:
                config = self.config_manager.get_controller_config(controller_type)
                print(f"\n{controller_type.upper()} Configuration:")
                print(f"  Gains: {config.get('gains', 'Not specified')}")
                print(f"  Max Force: {config.get('max_force', 'Not specified')}")
                print(f"  Timestep: {config.get('dt', 'Not specified')}")

                # Create controller with configuration
                controller = create_controller(controller_type, **config)
                print(f"  ✅ Controller created successfully")

            except Exception as e:
                print(f"  ❌ Failed to create {controller_type}: {e}")

    def demonstration_2_parameter_override(self):
        """Demonstrate parameter override patterns."""

        print("\n=== Demonstration 2: Parameter Override Patterns ===")

        # Original configuration
        print("Original gains:", self.config_manager.base_config['controllers']['classical_smc']['gains'])

        # Override with explicit parameters
        config = self.config_manager.get_controller_config(
            'classical_smc',
            gains=[25, 20, 15, 10, 40, 6],
            max_force=160.0
        )
        print("Overridden gains:", config['gains'])
        print("Overridden max_force:", config['max_force'])

        # Create controller with overrides
        controller = create_controller('classical_smc', **config)
        print("✅ Controller created with overrides")

    def demonstration_3_validation_and_migration(self):
        """Demonstrate validation and migration features."""

        print("\n=== Demonstration 3: Validation and Migration ===")

        # Test deprecated parameter migration
        old_config = {
            'k_gain': 35.0,                    # Deprecated
            'lambda_gains': [12.0, 8.0],       # Deprecated
            'sat_limit': 150.0,                # Deprecated
            'boundary_thickness': 0.02,        # Deprecated
            'dt': 0.001
        }

        print("Old configuration (with deprecated parameters):")
        for key, value in old_config.items():
            print(f"  {key}: {value}")

        # Apply migration
        migrated_config = self.config_manager.migrator.check_deprecated_config(
            'classical_smc', old_config
        )

        print("\nMigrated configuration:")
        for key, value in migrated_config.items():
            print(f"  {key}: {value}")

        print("\nMigration warnings:")
        for warning in self.config_manager.migrator.get_deprecation_warnings():
            print(f"  ⚠️  {warning}")

    def demonstration_4_environment_configuration(self):
        """Demonstrate environment-based configuration."""

        print("\n=== Demonstration 4: Environment Configuration ===")

        # Simulate different environments
        environments = ['development', 'testing', 'production']

        for env in environments:
            print(f"\nEnvironment: {env}")

            # Environment-specific overrides
            env_overrides = {
                'development': {'gains': [15, 10, 8, 5, 25, 3]},      # Conservative
                'testing': {'gains': [20, 15, 12, 8, 35, 5]},         # Standard
                'production': {'gains': [25, 20, 15, 10, 45, 7]}      # Aggressive
            }

            config = self.config_manager.get_controller_config(
                'classical_smc',
                **env_overrides.get(env, {})
            )

            print(f"  Gains: {config['gains']}")

            # Validate for specific environment
            validator = ConfigurationValidator()
            is_valid = validator.validate_configuration('classical_smc', config)

            if is_valid:
                print(f"  ✅ Configuration valid for {env}")
            else:
                print(f"  ❌ Configuration invalid for {env}")
                for error in validator.get_validation_report()['errors']:
                    print(f"    Error: {error}")

    def demonstration_5_pso_integration(self):
        """Demonstrate PSO integration with configuration."""

        print("\n=== Demonstration 5: PSO Integration ===")

        # Create PSO-optimized configuration
        base_config = self.config_manager.get_controller_config('classical_smc')

        print("Base configuration for PSO:")
        print(f"  Initial gains: {base_config['gains']}")

        # Create PSO factory with configuration
        from src.controllers.factory import create_pso_controller_factory, SMCType

        factory = create_pso_controller_factory(
            SMCType.CLASSICAL,
            **{k: v for k, v in base_config.items() if k != 'gains'}
        )

        print(f"  PSO factory created: {factory.n_gains} gains required")

        # Simulate PSO optimization
        import numpy as np

        # Generate random gain variations
        base_gains = np.array(base_config['gains'])

        for i in range(3):
            # Add random variation
            variation = 0.1 * np.random.randn(len(base_gains))
            test_gains = base_gains * (1 + variation)
            test_gains = np.clip(test_gains, 0.1, 100.0)  # Keep positive

            print(f"\n  PSO Iteration {i+1}:")
            print(f"    Test gains: {test_gains.tolist()}")

            try:
                controller = factory(test_gains)
                print(f"    ✅ Controller created successfully")

                # Simulate fitness evaluation
                fitness = np.sum(test_gains**2)  # Simple fitness function
                print(f"    Fitness: {fitness:.2f}")

            except Exception as e:
                print(f"    ❌ Controller creation failed: {e}")

    def run_all_demonstrations(self):
        """Run all configuration demonstrations."""

        print("Configuration Integration Demonstrations")
        print("=" * 50)

        try:
            self.demonstration_1_basic_usage()
            self.demonstration_2_parameter_override()
            self.demonstration_3_validation_and_migration()
            self.demonstration_4_environment_configuration()
            self.demonstration_5_pso_integration()

            print("\n" + "=" * 50)
            print("All demonstrations completed successfully!")

        except Exception as e:
            print(f"\nDemonstration failed: {e}")
            import traceback
            traceback.print_exc()

# Run demonstrations
if __name__ == "__main__":
    demo = ComprehensiveConfigurationExample()
    demo.run_all_demonstrations()