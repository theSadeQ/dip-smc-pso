# Example from: docs\reference\controllers\factory_smc_factory.md
# Index: 7
# Runnable: True
# Hash: 030ca56a

def validate_gains(ctrl_type: SMCType, gains: List[float]) -> bool:
    spec = get_gain_specification(ctrl_type)
    if len(gains) != spec.n_gains:
        return False
    return all(lb <= g <= ub for g, (lb, ub) in zip(gains, spec.bounds))