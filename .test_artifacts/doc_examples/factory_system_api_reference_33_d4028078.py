# Example from: docs\api\factory_system_api_reference.md
# Index: 33
# Runnable: True
# Hash: d4028078

def get_expected_gain_count(smc_type: SMCType) -> int:
    """Get expected number of gains for a controller type."""
    expected_counts = {
        SMCType.CLASSICAL: 6,
        SMCType.ADAPTIVE: 5,
        SMCType.SUPER_TWISTING: 6,
        SMCType.HYBRID: 4,
    }
    return expected_counts.get(smc_type, 6)