# Example from: docs\plans\documentation\week_3_optimization_simulation.md
# Index: 10
# Runnable: False
# Hash: 3047a0cb

class MultiObjectiveFitness:
    def __init__(self, weights):
        self.w_ise = weights['ise']
        self.w_chattering = weights['chattering']
        self.w_effort = weights['effort']
        self.w_violations = weights['violations']

    def evaluate(self, simulation_result):
        J = (
            self.w_ise * simulation_result.ise +
            self.w_chattering * simulation_result.chattering_index +
            self.w_effort * simulation_result.control_effort +
            self.w_violations * simulation_result.constraint_violations
        )
        return J