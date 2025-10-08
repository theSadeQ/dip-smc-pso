# Example from: docs\testing\testing_workflows_best_practices.md
# Index: 7
# Runnable: False
# Hash: 760b5b53

# Install mutpy
pip install mutpy

# Run mutation testing
mut.py --target src.controllers.smc.classic_smc --unit-test tests.test_controllers.smc.algorithms.classical.test_classical_smc --report-html mutation_report.html

# Example mutation: Change + to -
# Original: control = u_eq + u_switch
# Mutant:   control = u_eq - u_switch

# If tests still pass → weak test suite
# If tests fail → strong test suite (mutation killed)

# Target: >80% mutation score