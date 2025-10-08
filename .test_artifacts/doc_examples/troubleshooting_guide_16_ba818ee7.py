# Example from: docs\factory\troubleshooting_guide.md
# Index: 16
# Runnable: False
# Hash: ba818ee7

def apply_solutions(category, error_details):
    """Apply category-specific solutions."""

    solutions = {
        'creation': [
            "Check controller type spelling and available types",
            "Verify gain array length matches controller requirements",
            "Ensure all gains are positive finite numbers"
        ],
        'configuration': [
            "Add missing required parameters",
            "Update deprecated parameter names",
            "Validate parameter types and ranges"
        ],
        'pso': [
            "Use SMCType enum instead of string",
            "Check PSO bounds and particle validation",
            "Verify factory function has required attributes"
        ],
        'threading': [
            "Reduce lock hold time",
            "Check for nested lock acquisition",
            "Use timeouts for lock operations"
        ],
        'import': [
            "Check PYTHONPATH includes src/ directory",
            "Verify all required files exist",
            "Install missing dependencies"
        ],
        'performance': [
            "Profile controller creation times",
            "Check for memory leaks",
            "Optimize hot code paths"
        ]
    }

    category_solutions = solutions.get(category, ["Unknown category - manual investigation required"])

    print(f"Recommended solutions for {category} problems:")
    for i, solution in enumerate(category_solutions, 1):
        print(f"  {i}. {solution}")

    return category_solutions

# Example usage
category = 'creation'
solutions = apply_solutions(category, "gain count mismatch")