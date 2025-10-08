# Example from: docs\theory\pso_algorithm_foundations.md
# Index: 5
# Runnable: False
# Hash: 6b43526f

# example-metadata:
# runnable: false

import numpy as np

def fast_non_dominated_sort(
    objectives: np.ndarray
) -> dict:
    """
    Fast non-dominated sorting for multi-objective optimization.

    Implements Algorithm 5.1 (Deb et al. 2002) to partition solutions
    into Pareto fronts.

    Parameters
    ----------
    objectives : np.ndarray, shape (N, M)
        Objective function values for N solutions and M objectives

    Returns
    -------
    dict
        Fronts with indices and dominance relationships
    """
    N, M = objectives.shape

    # Domination count and dominated sets
    domination_count = np.zeros(N, dtype=int)
    dominated_solutions = [set() for _ in range(N)]

    # Compare all pairs
    for i in range(N):
        for j in range(i+1, N):
            # Check if i dominates j
            i_dominates_j = np.all(objectives[i] <= objectives[j]) and \
                           np.any(objectives[i] < objectives[j])

            # Check if j dominates i
            j_dominates_i = np.all(objectives[j] <= objectives[i]) and \
                           np.any(objectives[j] < objectives[i])

            if i_dominates_j:
                dominated_solutions[i].add(j)
                domination_count[j] += 1
            elif j_dominates_i:
                dominated_solutions[j].add(i)
                domination_count[i] += 1

    # Extract fronts
    fronts = []
    current_front = []

    for i in range(N):
        if domination_count[i] == 0:
            current_front.append(i)

    fronts.append(current_front)

    # Build subsequent fronts
    while len(fronts[-1]) > 0:
        next_front = []
        for i in fronts[-1]:
            for j in dominated_solutions[i]:
                domination_count[j] -= 1
                if domination_count[j] == 0:
                    next_front.append(j)

        if len(next_front) > 0:
            fronts.append(next_front)

    # Remove empty last front
    if len(fronts[-1]) == 0:
        fronts = fronts[:-1]

    return {
        "fronts": fronts,
        "n_fronts": len(fronts),
        "front_sizes": [len(f) for f in fronts],
        "pareto_front": fronts[0] if len(fronts) > 0 else [],
    }

def compute_crowding_distance(
    objectives: np.ndarray,
    front_indices: list
) -> np.ndarray:
    """
    Compute crowding distance for solutions in a Pareto front.

    Parameters
    ----------
    objectives : np.ndarray, shape (N, M)
        Objective function values
    front_indices : list
        Indices of solutions in current front

    Returns
    -------
    np.ndarray
        Crowding distances for each solution in front
    """
    N_front = len(front_indices)
    M = objectives.shape[1]

    if N_front <= 2:
        # Boundary solutions have infinite crowding distance
        return np.full(N_front, np.inf)

    crowding_distances = np.zeros(N_front)

    for m in range(M):
        # Extract objective m values for front
        obj_m = objectives[front_indices, m]

        # Sort solutions by objective m
        sorted_indices = np.argsort(obj_m)

        # Boundary solutions
        crowding_distances[sorted_indices[0]] = np.inf
        crowding_distances[sorted_indices[-1]] = np.inf

        # Normalization
        obj_range = obj_m[sorted_indices[-1]] - obj_m[sorted_indices[0]]
        if obj_range > 1e-10:
            # Interior solutions
            for i in range(1, N_front - 1):
                idx = sorted_indices[i]
                crowding_distances[idx] += (
                    (obj_m[sorted_indices[i+1]] - obj_m[sorted_indices[i-1]]) / obj_range
                )

    return crowding_distances

# Example usage for ZDT1 test function (2 objectives):
# objectives_zdt1 = ...  # N x 2 array
# result = fast_non_dominated_sort(objectives_zdt1)
# Expected: Pareto front clearly identified, crowding distances computed