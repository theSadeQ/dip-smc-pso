# Example from: docs\api\factory_reference.md
# Index: 8
# Runnable: False
# Hash: 6878caef

SMC_GAIN_SPECS = {
    SMCType.CLASSICAL: SMCGainSpec(
        gain_names=['k1', 'k2', 'lambda1', 'lambda2', 'K', 'kd'],
        gain_bounds=[(1.0, 30.0), (1.0, 30.0), (1.0, 20.0), (1.0, 20.0), (5.0, 50.0), (0.1, 10.0)],
        controller_type='classical_smc',
        n_gains=6
    ),
    # ... additional specifications
}