# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 25
# Runnable: False
# Hash: 2afcb049

# example-metadata:
# runnable: false

# Aggressive stabilizer for near-upright
stabilizer_near = SuperTwistingSMC(gains=[...], max_force=20.0)

# Conservative stabilizer for larger angles
stabilizer_far = ClassicalSMC(gains=[...], max_force=20.0)

# Hybrid swing-up with region-based stabilizer selection
class AdaptiveSwingUpSMC(SwingUpSMC):
    def _select_stabilizer(self, θ₁, θ₂):
        if abs(θ₁) < 0.2 and abs(θ₂) < 0.2:
            return stabilizer_near
        else:
            return stabilizer_far

    def compute_control(self, state, state_vars, history):
        # Override to dynamically select stabilizer
        self.stabilizer = self._select_stabilizer(state[1], state[2])
        return super().compute_control(state, state_vars, history)