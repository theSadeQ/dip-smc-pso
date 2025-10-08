# Example from: docs\troubleshooting\hybrid_smc_runtime_fix_final.md
# Index: 8
# Runnable: False
# Hash: 9a78172c

class ControllerValidator:
    """Validate controller outputs meet interface contracts."""

    @staticmethod
    def validate_control_output(output, controller_name: str):
        """Validate controller output structure and types."""
        if output is None:
            raise ValueError(f"{controller_name}: compute_control returned None")

        if not hasattr(output, 'control'):
            raise ValueError(f"{controller_name}: Missing control attribute")

        if not np.isfinite(output.control):
            raise ValueError(f"{controller_name}: Non-finite control value")