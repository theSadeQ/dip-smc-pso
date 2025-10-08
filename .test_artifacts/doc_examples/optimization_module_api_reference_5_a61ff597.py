# Example from: docs\api\optimization_module_api_reference.md
# Index: 5
# Runnable: True
# Hash: a61ff597

{
    'best_cost': float,              # Final best fitness value
    'best_pos': np.ndarray,          # Best gain vector (1D array)
    'cost_history': np.ndarray,      # Best cost per iteration (1D array)
    'pos_history': np.ndarray,       # Best position per iteration (2D array: iters × dims)
}