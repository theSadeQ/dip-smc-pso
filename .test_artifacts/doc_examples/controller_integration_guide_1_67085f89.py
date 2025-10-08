# Example from: docs\factory\controller_integration_guide.md
# Index: 1
# Runnable: False
# Hash: 67085f89

class EnterpriseControllerFactory:
    """
    Enterprise-grade controller factory with comprehensive integration support.

    Features:
    - Type-safe controller creation
    - Automatic parameter validation
    - Plant model integration
    - PSO optimization support
    - Thread-safe operations
    - Comprehensive error handling
    """

    @staticmethod
    def create_controller(
        controller_type: str,
        config: Optional[Any] = None,
        gains: Optional[GainsArray] = None,
        **kwargs: Any
    ) -> ControllerProtocol:
        """
        Create controller with enhanced integration support.

        Args:
            controller_type: Type of controller to create
            config: Configuration object or dictionary
            gains: Controller gains array
            **kwargs: Additional parameters for flexibility

        Returns:
            Configured controller instance

        Raises:
            ValueError: Invalid controller type or configuration
            TypeError: Invalid parameter types
        """