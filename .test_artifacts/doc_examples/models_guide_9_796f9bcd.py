# Example from: docs\plant\models_guide.md
# Index: 9
# Runnable: False
# Hash: 796f9bcd

# example-metadata:
# runnable: false

class SimplifiedPhysicsComputer:
    """Simplified physics computation for DIP."""

    def __init__(self, config: SimplifiedDIPConfig):
        self.config = config

        # Physics matrix computers
        self.full_matrices = DIPPhysicsMatrices(config)
        self.simplified_matrices = SimplifiedDIPPhysicsMatrices(config)

        # Numerical stability
        self.regularizer = AdaptiveRegularizer(config)
        self.matrix_inverter = MatrixInverter(self.regularizer)

        # Performance flags
        self.use_simplified_inertia = True
        self.cache_matrices = False