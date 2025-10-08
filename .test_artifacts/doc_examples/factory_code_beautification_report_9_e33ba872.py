# Example from: docs\reports\factory_code_beautification_report.md
# Index: 9
# Runnable: False
# Hash: e33ba872

# example-metadata:
# runnable: false

class SMCType(Enum):
    """SMC Controller types enumeration."""
    CLASSICAL = "classical_smc"
    ADAPTIVE = "adaptive_smc"
    SUPER_TWISTING = "sta_smc"
    HYBRID = "hybrid_adaptive_sta_smc"

class SMCFactory:
    """Factory class for creating SMC controllers."""

    @staticmethod
    def create_controller(smc_type: SMCType, config: SMCConfig) -> ControllerProtocol:
        """Create controller using SMCType enum."""
        return create_controller(smc_type.value, config, config.gains)