# Example from: docs\troubleshooting\hybrid_smc_runtime_fix.md
# Index: 7
# Runnable: False
# Hash: de9a812b

# PSO fitness function error handling
def fitness_function(gains):
    try:
        result = evaluate_controller(gains)
        if isinstance(result, str):  # Error message received
            # String gets converted to float - typically 0.0
            return float(result) if result.replace('.','').isdigit() else 0.0
        return result
    except:
        return float('inf')  # Invalid fitness