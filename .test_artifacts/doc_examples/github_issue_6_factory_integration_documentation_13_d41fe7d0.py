# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 13
# Runnable: False
# Hash: d41fe7d0

class SMCFactory:
    """
    Main factory class for creating SMC controllers.

    Methods:
        create_controller: Create controller with full configuration
        get_gain_specification: Get gain requirements for controller type
        validate_configuration: Validate configuration parameters
    """

    @staticmethod
    def create_controller(smc_type: SMCType, config: SMCConfig) -> SMCProtocol:
        """Create validated SMC controller."""

    @staticmethod
    def get_gain_specification(smc_type: SMCType) -> SMCGainSpec:
        """Get gain specification for controller type."""

    @staticmethod
    def validate_configuration(smc_type: SMCType, config: SMCConfig) -> bool:
        """Validate configuration for controller type."""