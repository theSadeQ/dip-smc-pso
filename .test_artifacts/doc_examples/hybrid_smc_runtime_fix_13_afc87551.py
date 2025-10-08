# Example from: docs\troubleshooting\hybrid_smc_runtime_fix.md
# Index: 13
# Runnable: False
# Hash: afc87551

# .mypy.ini configuration
[mypy]
python_version = 3.9
strict = True
warn_return_any = True
warn_unused_ignores = True
warn_redundant_casts = True
warn_unused_configs = True
disallow_untyped_defs = True

# Specific checks for return statements
check_untyped_defs = True
disallow_incomplete_defs = True