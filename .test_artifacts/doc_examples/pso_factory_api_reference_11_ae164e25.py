# Example from: docs\factory\pso_factory_api_reference.md
# Index: 11
# Runnable: False
# Hash: ae164e25

# Global registry of SMC gain specifications
SMC_GAIN_SPECS: Dict[SMCType, SMCGainSpec] = {

    SMCType.CLASSICAL: SMCGainSpec(
        controller_type=SMCType.CLASSICAL,
        n_gains=6,
        gain_names=['k1', 'k2', 'λ1', 'λ2', 'K', 'kd'],
        gain_descriptions=[
            'Position gain for pendulum 1',
            'Position gain for pendulum 2',
            'Surface gain for pendulum 1',
            'Surface gain for pendulum 2',
            'Switching gain for robustness',
            'Damping gain for chattering reduction'
        ],
        mathematical_constraints=[
            'k1 > 0 (controllability)',
            'k2 > 0 (controllability)',
            'λ1 > 0 (stability)',
            'λ2 > 0 (stability)',
            'K > 0 (reachability)',
            'kd ≥ 0 (non-negative damping)'
        ],
        pso_bounds=[
            (0.1, 50.0),   # k1
            (0.1, 50.0),   # k2
            (1.0, 50.0),   # λ1
            (1.0, 50.0),   # λ2
            (1.0, 200.0),  # K
            (0.0, 50.0)    # kd
        ],
        default_gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0]
    ),

    SMCType.SUPER_TWISTING: SMCGainSpec(
        controller_type=SMCType.SUPER_TWISTING,
        n_gains=6,
        gain_names=['K1', 'K2', 'λ1', 'λ2', 'α1', 'α2'],
        gain_descriptions=[
            'Primary twisting gain',
            'Secondary twisting gain',
            'Surface gain for pendulum 1',
            'Surface gain for pendulum 2',
            'Higher-order surface parameter 1',
            'Higher-order surface parameter 2'
        ],
        mathematical_constraints=[
            'K1 > K2 (finite-time convergence)',
            'K2 > 0 (convergence requirement)',
            'λ1 > 0 (stability)',
            'λ2 > 0 (stability)',
            'α1 > 0 (higher-order stability)',
            'α2 > 0 (higher-order stability)'
        ],
        pso_bounds=[
            (2.0, 100.0),  # K1 (must be > K2)
            (1.0, 99.0),   # K2 (must be < K1)
            (1.0, 50.0),   # λ1
            (1.0, 50.0),   # λ2
            (1.0, 50.0),   # α1
            (1.0, 50.0)    # α2
        ],
        default_gains=[25.0, 10.0, 15.0, 12.0, 20.0, 15.0]
    ),

    SMCType.ADAPTIVE: SMCGainSpec(
        controller_type=SMCType.ADAPTIVE,
        n_gains=5,
        gain_names=['k1', 'k2', 'λ1', 'λ2', 'γ'],
        gain_descriptions=[
            'Position gain for pendulum 1',
            'Position gain for pendulum 2',
            'Surface gain for pendulum 1',
            'Surface gain for pendulum 2',
            'Adaptation rate'
        ],
        mathematical_constraints=[
            'k1 > 0 (controllability)',
            'k2 > 0 (controllability)',
            'λ1 > 0 (stability)',
            'λ2 > 0 (stability)',
            '0.1 ≤ γ ≤ 20.0 (bounded adaptation)'
        ],
        pso_bounds=[
            (0.1, 50.0),   # k1
            (0.1, 50.0),   # k2
            (1.0, 50.0),   # λ1
            (1.0, 50.0),   # λ2
            (0.1, 20.0)    # γ
        ],
        default_gains=[10.0, 8.0, 15.0, 12.0, 0.5]
    ),

    SMCType.HYBRID: SMCGainSpec(
        controller_type=SMCType.HYBRID,
        n_gains=4,
        gain_names=['k1', 'k2', 'λ1', 'λ2'],
        gain_descriptions=[
            'Surface gain for pendulum 1',
            'Surface gain for pendulum 2',
            'Higher-order surface gain 1',
            'Higher-order surface gain 2'
        ],
        mathematical_constraints=[
            'k1 > 0 (stability)',
            'k2 > 0 (stability)',
            'λ1 > 0 (stability)',
            'λ2 > 0 (stability)'
        ],
        pso_bounds=[
            (1.0, 50.0),   # k1
            (1.0, 50.0),   # k2
            (1.0, 50.0),   # λ1
            (1.0, 50.0)    # λ2
        ],
        default_gains=[15.0, 12.0, 18.0, 15.0]
    )
}