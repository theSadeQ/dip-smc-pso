# Example from: docs\api\factory_system_api_reference.md
# Index: 36
# Runnable: False
# Hash: c74f5f38

# example-metadata:
# runnable: false

SMC_GAIN_SPECS = {
    SMCType.CLASSICAL: SMCGainSpec(
        gain_names=['k1', 'k2', 'lambda1', 'lambda2', 'K', 'kd'],
        gain_bounds=[(1.0, 30.0), (1.0, 30.0), (1.0, 20.0), (1.0, 20.0), (5.0, 50.0), (0.1, 10.0)],
        controller_type='classical_smc',
        n_gains=6
    ),
    SMCType.ADAPTIVE: SMCGainSpec(
        gain_names=['k1', 'k2', 'lambda1', 'lambda2', 'gamma'],
        gain_bounds=[(2.0, 40.0), (2.0, 40.0), (1.0, 25.0), (1.0, 25.0), (0.5, 10.0)],
        controller_type='adaptive_smc',
        n_gains=5
    ),
    # ... etc.
}