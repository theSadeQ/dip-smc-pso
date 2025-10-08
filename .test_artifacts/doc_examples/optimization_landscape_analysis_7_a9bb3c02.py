# Example from: docs\mathematical_foundations\optimization_landscape_analysis.md
# Index: 7
# Runnable: False
# Hash: a9bb3c02

def compute_fitness(gains):
    result = simulate(gains)

    ise_norm = result.ise / reference_values['ise']
    chattering_norm = result.chattering / reference_values['chattering']
    effort_norm = result.effort / reference_values['effort']

    fitness = (
        objective_weights['ise'] * ise_norm +
        objective_weights['chattering'] * chattering_norm +
        objective_weights['effort'] * effort_norm
    )

    return fitness