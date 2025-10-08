# Example from: docs\optimization\pso_core_algorithm_guide.md
# Index: 7
# Runnable: False
# Hash: dded3699

def evaluate_population(self) -> np.ndarray:
    """Evaluate fitness for all particles.

    Returns:
        Fitness values for all particles
    """
    fitness = np.zeros(self.population_size)

    for i, position in enumerate(self.positions):
        try:
            # Validate position
            if not self._is_valid_position(position):
                fitness[i] = np.inf
                continue

            # Evaluate objective function
            fitness[i] = self.objective_function(position)

            # Constraint penalty (if any)
            if self.has_constraints:
                penalty = self._compute_constraint_penalty(position)
                fitness[i] += penalty

        except Exception as e:
            # Robust error handling
            self.logger.warning(f"Fitness evaluation failed for particle {i}: {e}")
            fitness[i] = np.inf

    return fitness