# Example from: docs\architecture\controller_system_architecture.md
# Index: 4
# Runnable: False
# Hash: 75d823a4

class TypeSafetyValidator:
    """Comprehensive type safety validation for controller interfaces."""

    @staticmethod
    def validate_controller_interface(
        controller: Any,
        expected_type: str
    ) -> None:
        """Validate controller implements required interface."""

        required_methods = ['compute_control', 'reset', 'initialize_state']

        for method_name in required_methods:
            if not hasattr(controller, method_name):
                raise InterfaceError(
                    f"{expected_type} missing required method: {method_name}"
                )

            method = getattr(controller, method_name)
            if not callable(method):
                raise InterfaceError(
                    f"{expected_type}.{method_name} is not callable"
                )

    @staticmethod
    def validate_control_output(
        output: Any,
        controller_type: str
    ) -> None:
        """Validate controller output structure and types."""

        if output is None:
            raise ControllerError(f"{controller_type} returned None")

        # Type-specific validation based on expected output structure
        expected_attributes = ['control', 'state_vars', 'history']

        for attr in expected_attributes:
            if not hasattr(output, attr):
                raise ControllerError(
                    f"{controller_type} output missing attribute: {attr}"
                )