# Example from: docs\analysis\HYBRID_SMC_FIX_TECHNICAL_DOCUMENTATION.md
# Index: 12
# Runnable: False
# Hash: e3b1953c

# example-metadata:
# runnable: false

class ControllerValidator:
    @staticmethod
    def validate_control_output(output, controller_name: str):
        """Validate controller output structure and types."""
        if output is None:
            raise ValueError(f"{controller_name}: compute_control returned None")

        if not hasattr(output, 'control'):
            raise ValueError(f"{controller_name}: Missing control attribute")

        if not np.isfinite(output.control):
            raise ValueError(f"{controller_name}: Non-finite control value")