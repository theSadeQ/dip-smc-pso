# Example from: docs\factory\troubleshooting_guide.md
# Index: 14
# Runnable: False
# Hash: c2df9664

# example-metadata:
# runnable: false

def categorize_problem(error_message):
    """Categorize problem based on error message."""

    categories = {
        'creation': ['Unknown controller type', 'requires.*gains', 'Invalid parameter'],
        'configuration': ['Config validation', 'Missing.*parameter', 'Deprecated parameter'],
        'pso': ['PSO factory', 'bounds validation', 'n_gains'],
        'threading': ['lock timeout', 'deadlock', 'thread'],
        'import': ['ModuleNotFoundError', 'ImportError', 'No module named'],
        'performance': ['timeout', 'slow', 'memory']
    }

    error_lower = error_message.lower()

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in error_lower:
                return category

    return 'unknown'

# Example usage
error = "Controller 'classical_smc' requires 6 gains, got 5"
category = categorize_problem(error)
print(f"Problem category: {category}")