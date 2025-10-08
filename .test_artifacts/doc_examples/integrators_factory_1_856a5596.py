# Example from: docs\reference\simulation\integrators_factory.md
# Index: 1
# Runnable: True
# Hash: 856a5596

IntegratorConfig = {
    'method': str,           # 'euler', 'rk2', 'rk4', 'rk45'
    'dt': float,             # Fixed step size (for fixed-step methods)
    'rtol': float,           # Relative tolerance (adaptive only)
    'atol': float,           # Absolute tolerance (adaptive only)
    'min_step': float,       # Minimum step size (adaptive only)
    'max_step': float,       # Maximum step size (adaptive only)
    'safety_factor': float,  # Step size safety factor (adaptive only)
}