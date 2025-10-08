# Example from: docs\api\factory_system_api_reference.md
# Index: 63
# Runnable: False
# Hash: f7902ba5

# Add to SMCType enum
class SMCType(Enum):
    CLASSICAL = "classical_smc"
    ADAPTIVE = "adaptive_smc"
    SUPER_TWISTING = "sta_smc"
    HYBRID = "hybrid_adaptive_sta_smc"
    NEW_CONTROLLER = "new_controller"  # Add new type

# Add to gain count mapping
def get_expected_gain_count(smc_type: SMCType) -> int:
    expected_counts = {
        SMCType.CLASSICAL: 6,
        SMCType.ADAPTIVE: 5,
        SMCType.SUPER_TWISTING: 6,
        SMCType.HYBRID: 4,
        SMCType.NEW_CONTROLLER: 4,  # Add expected count
    }
    return expected_counts.get(smc_type, 6)

# Add PSO bounds
def get_gain_bounds_for_pso(smc_type: SMCType) -> Tuple[List[float], List[float]]:
    bounds_map = {
        # ... existing bounds ...
        SMCType.NEW_CONTROLLER: {
            'lower': [1.0, 1.0, 0.5, 0.5],
            'upper': [30.0, 30.0, 20.0, 20.0]
        }
    }
    return (bounds_map[smc_type]['lower'], bounds_map[smc_type]['upper'])