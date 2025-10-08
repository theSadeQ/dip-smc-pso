# Example from: docs\workflows\complete_integration_guide.md
# Index: 16
# Runnable: True
# Hash: acba88c5

# Debug PSO optimization problems
from src.utils.debugging import PSODebugger

def debug_pso_optimization():
    """Debug PSO optimization issues."""

    debugger = PSODebugger()

    # Common PSO issues and solutions
    issues = {
        'slow_convergence': {
            'symptoms': ['high iteration count', 'plateau in cost'],
            'solutions': ['increase particles', 'adjust cognitive/social parameters', 'check bounds']
        },
        'premature_convergence': {
            'symptoms': ['early plateau', 'low diversity'],
            'solutions': ['increase inertia', 'add mutation', 'diversify initialization']
        },
        'no_convergence': {
            'symptoms': ['cost increases', 'unstable behavior'],
            'solutions': ['check fitness function', 'validate bounds', 'reduce parameter count']
        }
    }

    # Automated diagnosis
    diagnosis = debugger.diagnose_pso_issues(
        controller_type='hybrid_adaptive_sta_smc',
        pso_history=load_pso_history(),
        known_issues=issues
    )

    return diagnosis