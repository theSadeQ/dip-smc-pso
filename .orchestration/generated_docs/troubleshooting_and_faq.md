# PSO Integration Troubleshooting Guide

## Common Issues and Solutions

### 1. PSO Convergence Failures

**Symptoms**:
- PSO doesn't find good solutions
- Fitness remains high after many iterations
- Solutions are infeasible

**Possible Causes**:
- Poor fitness function design
- Inadequate PSO parameters
- Restrictive bounds

**Solutions**:
- Simplify fitness function
- Increase population size or iterations
- Review and adjust bounds
- Check for numerical issues

### 2. Invalid Gain Validation Errors

**Symptoms**:
- `validate_smc_gains()` returns False
- High penalty values in fitness function

**Possible Causes**:
- Gains outside specified bounds
- Wrong number of gains for SMC type
- NaN or infinite values

**Solutions**:
```python
# Check gain bounds
bounds = get_gain_bounds_for_pso(smc_type)
print(f"Expected bounds: {bounds}")

# Verify gain count
expected_count = len(bounds[0])
print(f"Expected {expected_count} gains, got {len(gains)}")

# Check for invalid values
if any(np.isnan(gains)) or any(np.isinf(gains)):
    print("Invalid gain values detected")
```

### 3. Controller Creation Failures

**Symptoms**:
- `create_smc_for_pso()` raises exceptions
- Controller object is None

**Possible Causes**:
- Invalid plant configuration
- Incompatible gain specifications
- Missing dependencies

**Solutions**:
- Verify plant configuration is valid
- Check SMC type and gain compatibility
- Test with known good parameters

### 4. Performance Optimization Issues

**Symptoms**:
- PSO runs very slowly
- Memory usage grows over time
- System becomes unresponsive

**Possible Causes**:
- Inefficient fitness function
- Memory leaks in optimization loop
- Excessive logging or debugging

**Solutions**:
- Profile fitness function performance
- Use vectorized operations where possible
- Limit data storage during optimization
- Implement periodic garbage collection

## Debugging Strategies

### Step-by-Step Debugging
1. **Test individual components**:
   ```python
   # Test bounds retrieval
   bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)

   # Test gain validation
   valid = validate_smc_gains(SMCType.CLASSICAL, test_gains)

   # Test controller creation
   controller = create_smc_for_pso(SMCType.CLASSICAL, test_gains, config)
   ```

2. **Validate fitness function**:
   ```python
   # Test with known gains
   test_gains = [10.0, 5.0, 8.0, 3.0, 15.0, 2.0]
   fitness = fitness_function(test_gains)
   print(f"Test fitness: {fitness}")
   ```

3. **Check PSO configuration**:
   ```python
   # Verify PSO parameters
   print(f"Population size: {n_particles}")
   print(f"Dimensions: {dimensions}")
   print(f"Bounds: {bounds}")
   ```

### Logging and Monitoring
```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Log PSO progress
def fitness_function_with_logging(gains):
    logger.debug(f"Evaluating gains: {gains}")
    fitness = compute_fitness(gains)
    logger.debug(f"Fitness: {fitness}")
    return fitness
```

## FAQ

### Q: How many PSO iterations should I use?
**A**: Start with 50-100 iterations. Monitor convergence and adjust based on problem complexity.

### Q: What if PSO finds invalid gains?
**A**: Implement constraint handling in your PSO algorithm or use penalty methods in the fitness function.

### Q: How do I handle multiple objectives?
**A**: Use weighted sum, Pareto optimization, or convert to single objective with constraints.

### Q: PSO is too slow, how can I speed it up?
**A**: Reduce population size, simplify fitness function, use parallel evaluation, or implement early stopping.

### Q: How do I validate optimized controllers?
**A**: Test on multiple scenarios, verify stability margins, and compare against baseline controllers.

## Contact and Support
- Check documentation and examples first
- Review common issues in this guide
- Test with simplified configurations
- Report persistent issues with minimal reproducible examples
