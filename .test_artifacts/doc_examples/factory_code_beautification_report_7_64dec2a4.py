# Example from: docs\reports\factory_code_beautification_report.md
# Index: 7
# Runnable: False
# Hash: 64dec2a4

class SMCGainSpec:
    """SMC gain specification with expected interface."""
    def __init__(self, gain_names: List[str], gain_bounds: List[Tuple[float, float]],
                 controller_type: str, n_gains: int):
        self.gain_names = gain_names
        self.gain_bounds = gain_bounds
        self.controller_type = controller_type
        self.n_gains = n_gains

SMC_GAIN_SPECS = {
    SMCType.CLASSICAL: SMCGainSpec(
        gain_names=['k1', 'k2', 'lambda1', 'lambda2', 'K', 'kd'],
        gain_bounds=[(1.0, 30.0), (1.0, 30.0), (1.0, 20.0), (1.0, 20.0), (5.0, 50.0), (0.1, 10.0)],
        controller_type='classical_smc',
        n_gains=6
    )
}