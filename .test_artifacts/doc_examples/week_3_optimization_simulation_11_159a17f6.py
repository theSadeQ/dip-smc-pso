# Example from: docs\plans\documentation\week_3_optimization_simulation.md
# Index: 11
# Runnable: True
# Hash: 159a17f6

def pareto_front(objectives):
    """Compute non-dominated solutions."""
    is_pareto = np.ones(len(objectives), dtype=bool)
    for i, obj_i in enumerate(objectives):
        for j, obj_j in enumerate(objectives):
            if i != j and dominates(obj_j, obj_i):
                is_pareto[i] = False
                break
    return objectives[is_pareto]