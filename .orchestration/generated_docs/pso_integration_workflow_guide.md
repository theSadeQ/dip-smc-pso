# PSO Integration Workflow Guide

## Overview
This guide describes the complete workflow for integrating PSO optimization with SMC controllers.

## Workflow Steps

### 1. Initialize PSO Environment
```python
from src.controllers.factory import SMCType, create_smc_for_pso, get_gain_bounds_for_pso, validate_smc_gains
from src.plant.configurations import ConfigurationFactory

# Initialize plant configuration
plant_config = ConfigurationFactory.create_default_config("simplified")
```

### 2. Define Controller Type and Get Bounds
```python
# Select SMC controller type
smc_type = SMCType.CLASSICAL

# Get optimization bounds for the controller
bounds = get_gain_bounds_for_pso(smc_type)
lower_bounds, upper_bounds = bounds
```

### 3. Create Fitness Function
```python
def fitness_function(gains):
    # Validate gains
    if not validate_smc_gains(smc_type, gains):
        return float('inf')  # Invalid gains penalty

    # Create controller
    controller = create_smc_for_pso(smc_type, gains, plant_config)

    # Evaluate performance
    # ... implementation specific to your optimization goals

    return cost_value
```

### 4. Execute PSO Optimization
```python
# Use your preferred PSO library (e.g., PySwarms)
import pyswarms as ps

# Configure PSO
options = {'c1': 2.0, 'c2': 2.0, 'w': 0.9}
optimizer = ps.single.GlobalBestPSO(
    n_particles=30,
    dimensions=len(lower_bounds),
    options=options,
    bounds=(lower_bounds, upper_bounds)
)

# Run optimization
best_cost, best_gains = optimizer.optimize(fitness_function, iters=100)
```

### 5. Validate and Deploy Results
```python
# Validate optimized gains
if validate_smc_gains(smc_type, best_gains):
    # Create optimized controller
    optimized_controller = create_smc_for_pso(smc_type, best_gains, plant_config)

    # Test performance
    state = np.array([0.1, 0.2, 0.3, 0.0, 0.0, 0.0])
    control = optimized_controller.compute_control(state)

    print(f"Optimization successful! Best cost: {best_cost}")
    print(f"Optimized gains: {best_gains}")
else:
    print("Optimization failed - invalid gains")
```

## Best Practices
- Always validate gains before and after optimization
- Use appropriate fitness function design
- Monitor convergence criteria
- Test optimized controllers thoroughly
