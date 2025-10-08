# Example from: docs\architecture\controller_system_architecture.md
# Index: 10
# Runnable: False
# Hash: 68284d64

# example-metadata:
# runnable: false

class ErrorHandlingFramework:
    """Comprehensive error handling with recovery strategies."""

    @staticmethod
    def handle_controller_error(
        error: Exception,
        controller_type: str,
        context: Dict[str, Any]
    ) -> ControllerErrorResult:
        """Handle controller-specific errors with recovery."""

        if isinstance(error, ControllerCreationError):
            return ErrorHandlingFramework._handle_creation_error(
                error, controller_type, context
            )
        elif isinstance(error, ComputationError):
            return ErrorHandlingFramework._handle_computation_error(
                error, controller_type, context
            )
        elif isinstance(error, ConfigurationError):
            return ErrorHandlingFramework._handle_configuration_error(
                error, controller_type, context
            )
        else:
            return ErrorHandlingFramework._handle_unknown_error(
                error, controller_type, context
            )

    @staticmethod
    def _handle_creation_error(
        error: ControllerCreationError,
        controller_type: str,
        context: Dict[str, Any]
    ) -> ControllerErrorResult:
        """Handle controller creation failures with fallback."""

        # Attempt fallback to default configuration
        try:
            fallback_config = DefaultConfigurations.get_config(controller_type)
            fallback_controller = create_controller(controller_type, fallback_config)

            return ControllerErrorResult(
                success=True,
                controller=fallback_controller,
                error_type='creation_error_recovered',
                recovery_action='fallback_to_default_config'
            )

        except Exception as fallback_error:
            return ControllerErrorResult(
                success=False,
                error_type='creation_error_unrecoverable',
                original_error=error,
                fallback_error=fallback_error
            )