---
description: Automated log analysis for simulations, PSO, and tests
tags: [debugging, logs, analysis, pso, pytest]
---

# Automated Log Analysis

I'll analyze your simulation, optimization, and test logs to identify errors, patterns, and performance issues.

## What I'll do:

1. **Search for Errors**
   - ERROR/WARNING level messages
   - Exception stack traces (LinAlgError, ValueError, RuntimeError)
   - Failed test cases (pytest)
   - PSO convergence failures
   - Simulation instabilities

2. **Identify Patterns**
   - Frequency of numerical errors
   - Affected controllers/modules
   - PSO iteration patterns
   - Test failure trends
   - Performance bottlenecks

3. **Extract Key Information**
   - Timestamps
   - Error messages (with context)
   - Stack traces
   - PSO iteration numbers
   - Test case names
   - Controller types
   - Simulation parameters

4. **Generate Report**
   - Error summary by category
   - Top failing tests
   - PSO convergence analysis
   - Numerical stability issues
   - Recommended fixes

## Please provide:

1. **Log file location** (e.g., `logs/pso_optimization.log`, `tests/logs/pytest.log`, `pso_lyapunov_run.log`)
2. **Time range** (optional: "last hour", "last run", "since 2025-10-05")
3. **Specific errors** (optional: "LinAlgError", "PSO convergence", "test failures")

**Examples:**
- "Analyze pso_lyapunov_run.log for convergence issues"
- "Analyze tests/logs/pytest.log for the last 24 hours"
- "Search logs/ for LinAlgError exceptions"
