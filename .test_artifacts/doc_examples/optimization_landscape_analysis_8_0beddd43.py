# Example from: docs\mathematical_foundations\optimization_landscape_analysis.md
# Index: 8
# Runnable: True
# Hash: 0beddd43

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.problems import Problem

class SMCMultiObjective(Problem):
    def __init__(self):
        super().__init__(
            n_var=6,                    # 6 gains
            n_obj=3,                    # ISE, chattering, effort
            n_constr=1,                 # K > 10
            xl=[0.1, 0.1, 0.1, 0.1, 1.0, 0.0],
            xu=[50, 50, 50, 50, 200, 50]
        )

    def _evaluate(self, x, out, *args, **kwargs):
        # x: (n_population, 6) - gains
        ise = []
        chattering = []
        effort = []

        for gains in x:
            result = simulate(gains)
            ise.append(result.ise)
            chattering.append(result.chattering)
            effort.append(result.effort)

        out["F"] = np.column_stack([ise, chattering, effort])
        out["G"] = 10 - x[:, 4]  # Constraint: K > 10

# Run MOPSO
problem = SMCMultiObjective()
algorithm = NSGA2(pop_size=50)
result = minimize(problem, algorithm, termination=('n_gen', 100))

pareto_set = result.X  # Pareto-optimal gains
pareto_front = result.F  # Objective values