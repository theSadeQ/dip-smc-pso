# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 6
# Runnable: False
# Hash: 4c615fac

# example-metadata:
# runnable: false

class SMCFactory:
    """
    Type-safe factory for creating SMC controllers.

    Provides unified interface for all 4 core SMC types with:
    - Mathematical constraint validation
    - Performance optimization
    - PSO integration support
    - Configuration management
    """

    @staticmethod
    def create_controller(smc_type: SMCType,
                         config: SMCConfig) -> SMCProtocol:
        """
        Create SMC controller with validation and optimization.

        Args:
            smc_type: Controller type from SMCType enum
            config: Type-safe configuration object

        Returns:
            Initialized SMC controller implementing SMCProtocol

        Raises:
            ValueError: If gains violate mathematical constraints
            FactoryConfigurationError: If configuration is invalid
        """
        # Validate mathematical constraints
        if not validate_smc_gains(smc_type, config.gains):
            raise ValueError(f"Gains violate stability constraints for {smc_type}")

        # Create controller based on type
        controller_map = {
            SMCType.CLASSICAL: ClassicalSMC,
            SMCType.ADAPTIVE: AdaptiveSMC,
            SMCType.SUPER_TWISTING: SuperTwistingSMC,
            SMCType.HYBRID: HybridAdaptiveSTASMC
        }

        controller_class = controller_map[smc_type]
        return controller_class(**config.to_controller_params())