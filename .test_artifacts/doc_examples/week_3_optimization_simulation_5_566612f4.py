# Example from: docs\plans\documentation\week_3_optimization_simulation.md
# Index: 5
# Runnable: False
# Hash: 566612f4

# example-metadata:
# runnable: false

def evaluate_fitness(self, gains):
    # Create controller from gains
    controller = self.factory.create(gains)

    # Run simulation
    result = self.simulator.run(controller)

    # Compute multi-objective fitness
    fitness = (
        self.w1 * result.ise +
        self.w2 * result.chattering_index +
        self.w3 * result.control_effort
    )

    return fitness