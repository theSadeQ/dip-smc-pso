# Example from: docs\PATTERNS.md
# Index: 10
# Runnable: False
# Hash: d2621895

# OLD APPROACH (Inheritance - 427 lines, hard to test):
class AdaptiveSMC(BaseSMC):
    def compute_control(self, state):
        # 427 lines of monolithic code
        # - Surface computation
        # - Switching logic
        # - Adaptation law
        # - Uncertainty estimation
        # - Control computation
        # All tightly coupled, hard to test independently

# NEW APPROACH (Composition - 4 focused modules):

# src/controllers/smc/algorithms/adaptive/controller.py
class ModularAdaptiveSMC:
    """Adaptive SMC using composed components."""

    def __init__(self, config: AdaptiveSMCConfig):
        # Compose from focused modules
        self.surface = LinearSlidingSurface(config.k1, config.k2,
                                            config.lam1, config.lam2)
        self.adaptation = AdaptationLaw(config.gamma, config.leak_rate)
        self.estimator = UncertaintyEstimator(config.K_min, config.K_max)
        self.switching = SwitchingFunction(method='boundary_layer',
                                          epsilon=config.boundary_layer)

    def compute_control(self, state):
        """Compute control using composed modules."""
        # Each module is independently testable
        s = self.surface.compute(state)
        K_adapted = self.adaptation.update(s, self.K_current)
        uncertainty = self.estimator.estimate(state, s)
        u_switch = self.switching.compute(s, K_adapted)

        return u_switch