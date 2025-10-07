#==========================================================================================\\\
#==================== docs/pso_factory_integration_patterns.md ======================\\\
#==========================================================================================\\\

# PSO-Factory Integration Patterns Documentation

## Overview

This document provides comprehensive guidance on integrating the factory system with Particle Swarm Optimization (PSO) workflows. The DIP SMC-PSO project features native PSO integration patterns that streamline controller optimization while maintaining scientific rigor and performance.

## Table of Contents

1. [PSO Integration Architecture](#pso-integration-architecture)
2. [Controller Factory Patterns](#controller-factory-patterns)
3. [Gain Optimization Workflows](#gain-optimization-workflows)
4. [Performance Optimization](#performance-optimization)
5. [Scientific Validation](#scientific-validation)
6. [Advanced PSO Patterns](#advanced-pso-patterns)
7. [Best Practices](#best-practices)
8. [Examples and Use Cases](#examples-and-use-cases)

---

## PSO Integration Architecture

### Design Philosophy

The PSO integration follows several key principles:

1. **Native Integration**: PSO optimization is a first-class citizen in the factory system
2. **Performance Optimized**: Minimal overhead for PSO fitness evaluation loops
3. **Type Safety**: Full type safety with domain-specific validation
4. **Scientific Rigor**: Control theory-based gain bounds and validation
5. **Flexible Configuration**: Support for various PSO algorithms and strategies

### Architecture Overview

```
PSO Integration Layer
├── Factory Functions
│   ├── create_smc_for_pso()           # Direct controller creation for PSO
│   ├── create_pso_controller_factory() # Factory function creation
│   └── create_all_smc_controllers()    # Batch controller creation
├── Wrapper System
│   ├── PSOControllerWrapper           # PSO-compatible interface wrapper
│   ├── gain validation methods        # Domain-specific validation
│   └── standardized compute_control   # Unified control computation
├── Gain Management
│   ├── get_gain_bounds_for_pso()      # Control theory-based bounds
│   ├── validate_smc_gains()           # Pre-optimization validation
│   └── SMC_GAIN_SPECS                 # Complete gain specifications
└── Configuration Integration
    ├── PSO parameter resolution       # Multi-source parameter resolution
    ├── optimization-specific configs  # PSO-optimized configurations
    └── performance monitoring         # Real-time optimization metrics
```

---

## Controller Factory Patterns

### Pattern 1: Direct Controller Creation

**Use Case:** Simple PSO fitness functions with straightforward controller evaluation.

```python
from src.controllers.factory import create_smc_for_pso, SMCType
import numpy as np

def simple_fitness_function(gains_array: np.ndarray) -> float:
    """Simple PSO fitness evaluation using direct controller creation."""

    # Create controller directly from gains
    controller = create_smc_for_pso(
        SMCType.CLASSICAL,
        gains=gains_array,
        max_force=150.0,
        dt=0.001
    )

    # Evaluate controller performance
    performance_metrics = evaluate_controller_performance(controller)

    # Return fitness value (minimize)
    return performance_metrics['total_cost']

# PSO optimization setup
from src.optimization.algorithms.pso_optimizer import PSOTuner

bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)
tuner = PSOTuner(
    controller_factory=simple_fitness_function,
    config=config
)
best_gains, best_fitness = tuner.optimize()
```

**Advantages:**
- ✅ Simple and straightforward
- ✅ Minimal setup code
- ✅ Direct control over parameters

**Disadvantages:**
- ❌ Recreates factory overhead for each evaluation
- ❌ Less efficient for high-frequency PSO calls

### Pattern 2: Factory Function Pattern (Recommended)

**Use Case:** High-performance PSO optimization with thousands of fitness evaluations.

```python
from src.controllers.factory import create_pso_controller_factory, SMCType

def optimized_pso_workflow():
    """High-performance PSO workflow using factory function pattern."""

    # Create factory function once (expensive operation)
    controller_factory = create_pso_controller_factory(
        SMCType.CLASSICAL,
        plant_config=config.physics,
        max_force=150.0,
        dt=0.001
    )

    # Factory function has required PSO attributes
    assert hasattr(controller_factory, 'n_gains')         # Number of gains required
    assert hasattr(controller_factory, 'controller_type') # Controller type string
    assert hasattr(controller_factory, 'max_force')       # Force saturation limit

    # Define fitness function using pre-created factory
    def fitness_function(gains_array: np.ndarray) -> float:
        """Fast fitness evaluation using factory function."""

        # Create controller (fast operation)
        controller = controller_factory(gains_array)

        # Evaluate performance
        return evaluate_controller_performance(controller)['total_cost']

    # PSO optimization with optimized factory
    tuner = PSOTuner(
        controller_factory=fitness_function,
        config=config
    )

    return tuner.optimize()
```

**Advantages:**
- ✅ Maximum performance for PSO loops
- ✅ Factory overhead paid only once
- ✅ Built-in PSO metadata (n_gains, controller_type)
- ✅ Thread-safe operation

**Disadvantages:**
- ❌ Slightly more complex setup

### Pattern 3: Batch Controller Creation

**Use Case:** Comparative studies, batch optimization, multi-objective PSO.

```python
from src.controllers.factory import create_all_smc_controllers

def multi_controller_optimization():
    """Optimize gains for multiple controller types simultaneously."""

    # Define gain sets for all controller types
    gains_dict = {
        'classical': [20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
        'adaptive': [25.0, 18.0, 15.0, 10.0, 4.0],
        'sta': [25.0, 15.0, 20.0, 12.0, 8.0, 6.0],
        'hybrid': [18.0, 12.0, 10.0, 8.0]
    }

    # Create all controllers efficiently
    controllers = create_all_smc_controllers(
        gains_dict,
        max_force=150.0,
        dt=0.001
    )

    # Evaluate all controllers
    performance_results = {}
    for controller_type, controller in controllers.items():
        performance_results[controller_type] = evaluate_controller_performance(controller)

    return performance_results

def parallel_multi_objective_pso():
    """Multi-objective PSO across different controller types."""

    controller_types = [SMCType.CLASSICAL, SMCType.ADAPTIVE, SMCType.SUPER_TWISTING]

    # Create factory functions for each type
    factories = {
        ctrl_type: create_pso_controller_factory(ctrl_type)
        for ctrl_type in controller_types
    }

    def multi_objective_fitness(gains_dict: Dict[str, np.ndarray]) -> List[float]:
        """Multi-objective fitness evaluation."""
        objectives = []

        for ctrl_type, gains in gains_dict.items():
            controller = factories[ctrl_type](gains)
            performance = evaluate_controller_performance(controller)
            objectives.append(performance['total_cost'])

        return objectives  # Pareto optimization

    # Run multi-objective PSO
    return run_multi_objective_pso(multi_objective_fitness)
```

**Advantages:**
- ✅ Efficient for multiple controller types
- ✅ Unified configuration management
- ✅ Parallel evaluation support

---

## Gain Optimization Workflows

### Basic PSO Workflow

```python
# example-metadata:
# runnable: false

def basic_pso_optimization(controller_type: SMCType) -> Tuple[np.ndarray, float]:
    """Standard PSO optimization workflow for SMC controllers."""

    # Step 1: Get gain bounds based on control theory
    lower_bounds, upper_bounds = get_gain_bounds_for_pso(controller_type)

    # Step 2: Create optimized factory function
    controller_factory = create_pso_controller_factory(
        controller_type,
        plant_config=load_config("config.yaml").physics
    )

    # Step 3: Define fitness function with validation
    def fitness_function(gains: np.ndarray) -> float:
        """PSO fitness function with robust error handling."""

        # Pre-validate gains
        if not validate_smc_gains(controller_type, gains):
            return float('inf')  # Invalid gains get worst fitness

        try:
            # Create controller
            controller = controller_factory(gains)

            # Evaluate performance
            metrics = evaluate_controller_performance(controller)

            # Combine multiple objectives
            fitness = (
                0.4 * metrics['control_effort'] +
                0.3 * metrics['tracking_error'] +
                0.2 * metrics['settling_time'] +
                0.1 * metrics['overshoot_penalty']
            )

            return fitness

        except Exception as e:
            logger.warning(f"Controller evaluation failed: {e}")
            return float('inf')

    # Step 4: Configure and run PSO
    pso_config = {
        'n_particles': 30,
        'max_iter': 100,
        'bounds': (lower_bounds, upper_bounds),
        'w': 0.9,       # Inertia weight
        'c1': 2.0,      # Cognitive coefficient
        'c2': 2.0       # Social coefficient
    }

    tuner = PSOTuner(
        controller_factory=fitness_function,
        config=config,
        **pso_config
    )

    # Step 5: Run optimization
    best_gains, best_fitness = tuner.optimize()

    # Step 6: Validate results
    final_controller = controller_factory(best_gains)
    final_metrics = evaluate_controller_performance(final_controller)

    logger.info(f"Optimization complete:")
    logger.info(f"Best gains: {best_gains}")
    logger.info(f"Best fitness: {best_fitness}")
    logger.info(f"Final metrics: {final_metrics}")

    return best_gains, best_fitness
```

### Advanced PSO Workflow with Constraints

```python
# example-metadata:
# runnable: false

def constrained_pso_optimization(controller_type: SMCType) -> Tuple[np.ndarray, float]:
    """Advanced PSO with stability constraints and adaptive bounds."""

    # Get base bounds
    lower_bounds, upper_bounds = get_gain_bounds_for_pso(controller_type)

    # Create constraint functions based on control theory
    def stability_constraint(gains: np.ndarray) -> bool:
        """Verify closed-loop stability constraints."""

        if controller_type == SMCType.CLASSICAL:
            k1, k2, lam1, lam2, K, kd = gains

            # Sliding surface stability (Hurwitz condition)
            if lam1 <= 0 or lam2 <= 0:
                return False

            # Reaching condition constraint
            if K <= 0:
                return False

            # Practical stability margins
            if lam1/k1 > 20 or lam2/k2 > 20:  # Avoid overly aggressive surfaces
                return False

            # Chattering prevention
            if K > 100:  # Excessive switching gain
                return False

        elif controller_type == SMCType.ADAPTIVE:
            k1, k2, lam1, lam2, gamma = gains

            # Adaptation rate constraints
            if gamma <= 0 or gamma > 20:
                return False

            # Surface stability
            if lam1 <= 0 or lam2 <= 0:
                return False

        return True

    # Create factory with constraint checking
    base_factory = create_pso_controller_factory(controller_type)

    def constrained_factory(gains: np.ndarray):
        """Factory with built-in constraint checking."""

        # Check stability constraints
        if not stability_constraint(gains):
            raise ValueError("Stability constraints violated")

        return base_factory(gains)

    # Enhanced fitness function
    def constrained_fitness_function(gains: np.ndarray) -> float:
        """Fitness function with constraint penalties."""

        try:
            # Check basic validity
            if not validate_smc_gains(controller_type, gains):
                return 1e6

            # Check stability constraints
            if not stability_constraint(gains):
                return 1e6

            # Create and evaluate controller
            controller = constrained_factory(gains)
            metrics = evaluate_controller_performance(controller)

            # Multi-objective fitness with penalties
            base_fitness = (
                0.4 * metrics['ise'] +                    # Control performance
                0.3 * metrics['settling_time'] +          # Speed
                0.2 * metrics['control_effort'] +         # Efficiency
                0.1 * metrics['overshoot']                # Stability margin
            )

            # Add constraint penalties
            penalty = 0.0

            # Chattering penalty
            if 'chattering_index' in metrics and metrics['chattering_index'] > 0.1:
                penalty += 100 * metrics['chattering_index']

            # Control saturation penalty
            if 'saturation_ratio' in metrics and metrics['saturation_ratio'] > 0.05:
                penalty += 50 * metrics['saturation_ratio']

            return base_fitness + penalty

        except Exception as e:
            return 1e6  # Severe penalty for failed evaluations

    # Adaptive PSO configuration
    adaptive_config = {
        'n_particles': 50,
        'max_iter': 150,
        'bounds': (lower_bounds, upper_bounds),
        'w': 0.9,
        'c1': 2.0,
        'c2': 2.0,
        'early_stopping': True,
        'patience': 20,
        'min_improvement': 1e-6
    }

    # Run constrained optimization
    tuner = PSOTuner(
        controller_factory=constrained_fitness_function,
        config=config,
        **adaptive_config
    )

    return tuner.optimize()
```

### Multi-Stage PSO Optimization

```python
# example-metadata:
# runnable: false

def multi_stage_pso_optimization(controller_type: SMCType) -> Tuple[np.ndarray, float]:
    """Multi-stage PSO with progressive refinement."""

    # Stage 1: Coarse optimization with wide bounds
    logger.info("Stage 1: Coarse optimization")

    lower_bounds, upper_bounds = get_gain_bounds_for_pso(controller_type)

    # Expand bounds for exploration
    exploration_lower = [0.5 * lb for lb in lower_bounds]
    exploration_upper = [2.0 * ub for ub in upper_bounds]

    coarse_config = {
        'n_particles': 40,
        'max_iter': 50,
        'bounds': (exploration_lower, exploration_upper),
        'w': 0.9,  # High inertia for exploration
        'c1': 1.5,
        'c2': 1.5
    }

    coarse_factory = create_pso_controller_factory(controller_type)
    coarse_tuner = PSOTuner(
        controller_factory=lambda gains: evaluate_basic_performance(coarse_factory(gains)),
        config=config,
        **coarse_config
    )

    stage1_gains, stage1_fitness = coarse_tuner.optimize()

    # Stage 2: Fine optimization around best solution
    logger.info("Stage 2: Fine optimization")

    # Narrow bounds around stage 1 result
    bound_margin = 0.2  # 20% margin
    fine_lower = [max(lb, (1 - bound_margin) * g) for lb, g in zip(lower_bounds, stage1_gains)]
    fine_upper = [min(ub, (1 + bound_margin) * g) for ub, g in zip(upper_bounds, stage1_gains)]

    fine_config = {
        'n_particles': 30,
        'max_iter': 100,
        'bounds': (fine_lower, fine_upper),
        'w': 0.4,  # Low inertia for exploitation
        'c1': 2.0,
        'c2': 2.0
    }

    fine_factory = create_pso_controller_factory(controller_type)
    fine_tuner = PSOTuner(
        controller_factory=lambda gains: evaluate_detailed_performance(fine_factory(gains)),
        config=config,
        **fine_config
    )

    stage2_gains, stage2_fitness = fine_tuner.optimize()

    # Stage 3: Validation and robustness testing
    logger.info("Stage 3: Robustness validation")

    final_controller = fine_factory(stage2_gains)
    robustness_metrics = evaluate_robustness(final_controller)

    logger.info(f"Multi-stage optimization complete:")
    logger.info(f"Stage 1 (coarse): {stage1_fitness}")
    logger.info(f"Stage 2 (fine): {stage2_fitness}")
    logger.info(f"Final gains: {stage2_gains}")
    logger.info(f"Robustness score: {robustness_metrics['robustness_index']}")

    return stage2_gains, stage2_fitness
```

---

## Performance Optimization

### Memory-Efficient PSO Patterns

```python
def memory_efficient_pso():
    """Memory-optimized PSO for large-scale optimization."""

    # Pattern 1: Reuse controller instances
    controller_pool = {}

    def pooled_factory(gains: np.ndarray, controller_type: SMCType):
        """Factory with controller pooling."""
        gains_key = tuple(gains)

        if gains_key not in controller_pool:
            # Create new controller only if not in pool
            controller_pool[gains_key] = create_smc_for_pso(controller_type, gains)

        return controller_pool[gains_key]

    # Pattern 2: Batch evaluation for parallel PSO
    def batch_fitness_evaluation(gains_batch: List[np.ndarray]) -> List[float]:
        """Evaluate multiple gain sets in batch."""

        # Create controllers in batch
        controllers = [
            create_smc_for_pso(SMCType.CLASSICAL, gains)
            for gains in gains_batch
        ]

        # Parallel evaluation
        from concurrent.futures import ProcessPoolExecutor

        with ProcessPoolExecutor(max_workers=4) as executor:
            fitness_values = list(executor.map(
                evaluate_controller_performance,
                controllers
            ))

        return [f['total_cost'] for f in fitness_values]

    # Pattern 3: Incremental evaluation
    class IncrementalEvaluator:
        """Incremental controller evaluation with caching."""

        def __init__(self, controller_type: SMCType):
            self.controller_type = controller_type
            self.evaluation_cache = {}
            self.factory = create_pso_controller_factory(controller_type)

        def evaluate(self, gains: np.ndarray) -> float:
            """Evaluate with caching."""
            gains_key = tuple(np.round(gains, 6))  # Round for cache efficiency

            if gains_key not in self.evaluation_cache:
                controller = self.factory(gains)
                performance = evaluate_controller_performance(controller)
                self.evaluation_cache[gains_key] = performance['total_cost']

            return self.evaluation_cache[gains_key]

        def clear_cache(self):
            """Clear evaluation cache to manage memory."""
            self.evaluation_cache.clear()
```

### High-Performance PSO Integration

```python
def high_performance_pso_integration():
    """High-performance PSO integration with optimizations."""

    # Pre-compile Numba functions for controller evaluation
    from numba import jit

    @jit(nopython=True)
    def fast_control_computation(state, gains, max_force):
        """Numba-compiled control computation."""
        # Simplified controller logic for speed
        k1, k2, lam1, lam2, K, kd = gains

        # Sliding surface
        s = lam1 * state[0] + lam2 * state[1] + state[3] + state[4]

        # Control law
        u = -K * np.tanh(s / 0.01)

        # Saturation
        return np.clip(u, -max_force, max_force)

    # Vectorized fitness evaluation
    @jit(nopython=True)
    def vectorized_fitness_evaluation(gains_matrix, states_batch):
        """Vectorized evaluation for multiple gain sets."""
        n_particles, n_gains = gains_matrix.shape
        n_states, state_dim = states_batch.shape

        fitness_values = np.zeros(n_particles)

        for i in range(n_particles):
            gains = gains_matrix[i]
            total_cost = 0.0

            for j in range(n_states):
                state = states_batch[j]
                control = fast_control_computation(state, gains, 150.0)
                total_cost += np.sum(state**2) + 0.1 * control**2

            fitness_values[i] = total_cost / n_states

        return fitness_values

    # High-performance PSO workflow
    def optimized_pso_workflow():
        """Optimized PSO workflow using vectorized operations."""

        # Pre-generate test states for evaluation
        test_states = generate_test_state_batch(1000)

        # Vectorized fitness function
        def fitness_function(gains_matrix: np.ndarray) -> np.ndarray:
            """Vectorized fitness evaluation."""
            if gains_matrix.ndim == 1:
                gains_matrix = gains_matrix.reshape(1, -1)

            return vectorized_fitness_evaluation(gains_matrix, test_states)

        # Use vectorized PSO
        from src.optimization.algorithms.vectorized_pso import VectorizedPSO

        optimizer = VectorizedPSO(
            fitness_function=fitness_function,
            n_particles=50,
            n_dimensions=6,
            bounds=get_gain_bounds_for_pso(SMCType.CLASSICAL),
            max_iterations=100
        )

        return optimizer.optimize()
```

---

## Scientific Validation

### Control Theory Validation

```python
# example-metadata:
# runnable: false

def validate_pso_optimized_controller(gains: np.ndarray, controller_type: SMCType) -> Dict[str, Any]:
    """Comprehensive validation of PSO-optimized controller."""

    validation_results = {}

    # Create optimized controller
    controller = create_smc_for_pso(controller_type, gains)

    # 1. Stability Analysis
    validation_results['stability'] = validate_lyapunov_stability(controller)

    # 2. Performance Metrics
    validation_results['performance'] = {
        'ise': compute_integral_squared_error(controller),
        'itae': compute_integral_time_absolute_error(controller),
        'settling_time': compute_settling_time(controller),
        'overshoot': compute_overshoot(controller)
    }

    # 3. Robustness Analysis
    validation_results['robustness'] = {
        'parameter_sensitivity': analyze_parameter_sensitivity(controller),
        'disturbance_rejection': test_disturbance_rejection(controller),
        'noise_tolerance': evaluate_noise_tolerance(controller)
    }

    # 4. Chattering Analysis
    validation_results['chattering'] = {
        'chattering_index': compute_chattering_index(controller),
        'high_frequency_content': analyze_frequency_content(controller),
        'actuator_stress': evaluate_actuator_stress(controller)
    }

    # 5. Control Theory Properties
    if controller_type == SMCType.CLASSICAL:
        validation_results['theory'] = validate_classical_smc_properties(gains)
    elif controller_type == SMCType.ADAPTIVE:
        validation_results['theory'] = validate_adaptive_smc_properties(gains)
    elif controller_type == SMCType.SUPER_TWISTING:
        validation_results['theory'] = validate_sta_smc_properties(gains)

    return validation_results

def validate_classical_smc_properties(gains: np.ndarray) -> Dict[str, bool]:
    """Validate classical SMC theoretical properties."""
    k1, k2, lam1, lam2, K, kd = gains

    return {
        'surface_stability': lam1 > 0 and lam2 > 0,  # Hurwitz stability
        'reaching_condition': K > 0,                  # Reaching condition
        'finite_time_convergence': True,              # Guaranteed by SMC theory
        'robustness_margin': K > 2 * max(k1, k2),    # Sufficient robustness
        'chattering_bound': K < 100,                  # Practical chattering limit
        'damping_sufficient': kd >= 0                 # Non-negative damping
    }

def validate_adaptive_smc_properties(gains: np.ndarray) -> Dict[str, bool]:
    """Validate adaptive SMC theoretical properties."""
    k1, k2, lam1, lam2, gamma = gains

    return {
        'surface_stability': lam1 > 0 and lam2 > 0,
        'adaptation_convergence': gamma > 0,
        'adaptation_rate_bound': 0.1 <= gamma <= 20,
        'finite_time_reaching': True,
        'parameter_convergence': gamma > 0.5  # Sufficient for convergence
    }
```

### Statistical Validation

```python
def statistical_validation_of_pso_results(controller_type: SMCType,
                                        optimized_gains: np.ndarray,
                                        n_trials: int = 50) -> Dict[str, Any]:
    """Statistical validation of PSO optimization results."""

    # Multiple independent evaluations
    performance_samples = []

    for trial in range(n_trials):
        # Add small random perturbations to test robustness
        perturbed_gains = optimized_gains * (1 + 0.01 * np.random.randn(len(optimized_gains)))

        # Create controller with perturbed gains
        controller = create_smc_for_pso(controller_type, perturbed_gains)

        # Evaluate performance
        metrics = evaluate_controller_performance(controller)
        performance_samples.append(metrics['total_cost'])

    # Statistical analysis
    performance_array = np.array(performance_samples)

    validation_stats = {
        'mean_performance': np.mean(performance_array),
        'std_performance': np.std(performance_array),
        'coefficient_variation': np.std(performance_array) / np.mean(performance_array),
        'confidence_interval_95': np.percentile(performance_array, [2.5, 97.5]),
        'worst_case_performance': np.max(performance_array),
        'best_case_performance': np.min(performance_array),
        'robustness_score': 1.0 / (1.0 + np.std(performance_array))
    }

    # Statistical significance tests
    from scipy import stats

    # Test for normality
    _, normality_p_value = stats.shapiro(performance_array)
    validation_stats['performance_distribution_normal'] = normality_p_value > 0.05

    # Compare with default gains
    default_gains = get_default_gains(controller_type.value)
    default_controller = create_smc_for_pso(controller_type, default_gains)
    default_performance = evaluate_controller_performance(default_controller)['total_cost']

    # Statistical improvement test
    improvement_ratio = default_performance / np.mean(performance_array)
    validation_stats['improvement_ratio'] = improvement_ratio
    validation_stats['significant_improvement'] = improvement_ratio > 1.1  # 10% improvement threshold

    return validation_stats
```

---

## Advanced PSO Patterns

### Multi-Objective PSO Integration

```python
def multi_objective_pso_optimization(controller_type: SMCType) -> Dict[str, Any]:
    """Multi-objective PSO optimization for SMC controllers."""

    # Define multiple objectives
    objectives = {
        'tracking_performance': lambda controller: evaluate_tracking_error(controller),
        'control_efficiency': lambda controller: evaluate_control_effort(controller),
        'robustness': lambda controller: evaluate_robustness_index(controller),
        'chattering_minimization': lambda controller: evaluate_chattering_index(controller)
    }

    # Create controller factory
    factory = create_pso_controller_factory(controller_type)

    # Multi-objective fitness function
    def multi_objective_fitness(gains: np.ndarray) -> List[float]:
        """Evaluate multiple objectives."""
        try:
            controller = factory(gains)
            return [objective_func(controller) for objective_func in objectives.values()]
        except:
            return [float('inf')] * len(objectives)

    # Pareto optimization using NSGA-II-style PSO
    from src.optimization.algorithms.multi_objective_pso import MultiObjectivePSO

    optimizer = MultiObjectivePSO(
        fitness_function=multi_objective_fitness,
        n_objectives=len(objectives),
        n_particles=100,
        n_dimensions=factory.n_gains,
        bounds=get_gain_bounds_for_pso(controller_type),
        max_iterations=200
    )

    pareto_solutions = optimizer.optimize()

    # Analyze Pareto front
    pareto_analysis = {
        'n_solutions': len(pareto_solutions),
        'objective_ranges': analyze_objective_ranges(pareto_solutions),
        'recommended_solution': select_best_tradeoff_solution(pareto_solutions),
        'diversity_metric': compute_pareto_diversity(pareto_solutions)
    }

    return {
        'pareto_solutions': pareto_solutions,
        'analysis': pareto_analysis,
        'objective_names': list(objectives.keys())
    }
```

### Adaptive PSO with Factory Integration

```python
# example-metadata:
# runnable: false

def adaptive_pso_optimization(controller_type: SMCType) -> Tuple[np.ndarray, float]:
    """Adaptive PSO with dynamic parameter adjustment."""

    factory = create_pso_controller_factory(controller_type)

    class AdaptivePSOController:
        """Adaptive PSO controller with factory integration."""

        def __init__(self):
            self.iteration = 0
            self.best_fitness_history = []
            self.stagnation_counter = 0
            self.current_bounds = get_gain_bounds_for_pso(controller_type)

        def adapt_parameters(self, current_best_fitness: float) -> Dict[str, float]:
            """Adapt PSO parameters based on progress."""

            # Check for stagnation
            if (len(self.best_fitness_history) > 0 and
                abs(current_best_fitness - self.best_fitness_history[-1]) < 1e-6):
                self.stagnation_counter += 1
            else:
                self.stagnation_counter = 0

            self.best_fitness_history.append(current_best_fitness)

            # Adaptive parameter adjustment
            if self.stagnation_counter > 10:
                # Increase exploration
                w = 0.9  # High inertia
                c1, c2 = 2.5, 1.5  # High cognitive, low social

                # Expand search bounds slightly
                lower, upper = self.current_bounds
                expansion = 0.1
                self.current_bounds = (
                    [l * (1 - expansion) for l in lower],
                    [u * (1 + expansion) for u in upper]
                )

            elif self.iteration < 50:
                # Early exploration phase
                w = 0.9
                c1, c2 = 2.0, 2.0
            else:
                # Late exploitation phase
                w = 0.4
                c1, c2 = 1.5, 2.5

            self.iteration += 1

            return {
                'w': w,
                'c1': c1,
                'c2': c2,
                'bounds': self.current_bounds
            }

        def fitness_function(self, gains: np.ndarray) -> float:
            """Adaptive fitness function with dynamic objectives."""

            try:
                controller = factory(gains)
                metrics = evaluate_controller_performance(controller)

                # Dynamic objective weighting based on iteration
                if self.iteration < 30:
                    # Early phase: focus on basic performance
                    return 0.7 * metrics['ise'] + 0.3 * metrics['control_effort']
                elif self.iteration < 80:
                    # Middle phase: balance performance and robustness
                    return (0.4 * metrics['ise'] +
                           0.3 * metrics['control_effort'] +
                           0.3 * metrics['robustness_penalty'])
                else:
                    # Late phase: focus on refinement
                    return (0.3 * metrics['ise'] +
                           0.2 * metrics['control_effort'] +
                           0.3 * metrics['robustness_penalty'] +
                           0.2 * metrics['chattering_penalty'])

            except:
                return float('inf')

    # Run adaptive PSO
    adaptive_controller = AdaptivePSOController()

    # Initial PSO configuration
    pso_params = adaptive_controller.adapt_parameters(float('inf'))

    optimizer = PSOTuner(
        controller_factory=adaptive_controller.fitness_function,
        config=config,
        adaptive_callback=adaptive_controller.adapt_parameters
    )

    return optimizer.optimize_adaptive()
```

---

## Best Practices

### 1. Factory Function Reuse

```python
# ✅ Good: Create factory once, use many times
factory = create_pso_controller_factory(SMCType.CLASSICAL)

def fitness_function(gains):
    controller = factory(gains)  # Fast operation
    return evaluate_performance(controller)

# ❌ Bad: Recreate factory every time
def fitness_function(gains):
    controller = create_smc_for_pso(SMCType.CLASSICAL, gains)  # Slow operation
    return evaluate_performance(controller)
```

### 2. Gain Validation

```python
# example-metadata:
# runnable: false

# ✅ Good: Validate gains before expensive simulation
def robust_fitness_function(gains):
    if not validate_smc_gains(controller_type, gains):
        return float('inf')  # Early exit for invalid gains

    controller = factory(gains)
    return evaluate_performance(controller)

# ❌ Bad: No validation, let controller creation fail
def fragile_fitness_function(gains):
    controller = factory(gains)  # May fail with cryptic error
    return evaluate_performance(controller)
```

### 3. Error Handling

```python
# example-metadata:
# runnable: false

# ✅ Good: Comprehensive error handling
def robust_fitness_function(gains):
    try:
        # Validate inputs
        if not validate_smc_gains(controller_type, gains):
            return float('inf')

        # Create controller
        controller = factory(gains)

        # Evaluate with timeout
        with timeout(30):  # 30-second timeout
            performance = evaluate_performance(controller)

        # Check for numerical issues
        if not np.isfinite(performance['total_cost']):
            return float('inf')

        return performance['total_cost']

    except TimeoutError:
        logger.warning(f"Evaluation timeout for gains: {gains}")
        return float('inf')
    except Exception as e:
        logger.warning(f"Evaluation failed for gains {gains}: {e}")
        return float('inf')
```

### 4. Performance Monitoring

```python
# example-metadata:
# runnable: false

# ✅ Good: Monitor PSO progress and performance
class PSO_Monitor:
    def __init__(self):
        self.iteration_times = []
        self.fitness_history = []
        self.evaluation_count = 0

    def log_iteration(self, iteration, best_fitness, elapsed_time):
        self.fitness_history.append(best_fitness)
        self.iteration_times.append(elapsed_time)

        if iteration % 10 == 0:
            avg_time = np.mean(self.iteration_times[-10:])
            logger.info(f"Iteration {iteration}: fitness={best_fitness:.6f}, "
                       f"avg_time={avg_time:.3f}s")

    def log_evaluation(self):
        self.evaluation_count += 1

        if self.evaluation_count % 100 == 0:
            logger.info(f"Completed {self.evaluation_count} evaluations")

monitor = PSO_Monitor()

def monitored_fitness_function(gains):
    monitor.log_evaluation()
    # ... fitness computation
    return fitness_value
```

### 5. Configuration Management

```python
# example-metadata:
# runnable: false

# ✅ Good: Centralized PSO configuration
PSO_CONFIGS = {
    SMCType.CLASSICAL: {
        'n_particles': 30,
        'max_iter': 100,
        'w': 0.9,
        'c1': 2.0,
        'c2': 2.0,
        'early_stopping': True
    },
    SMCType.ADAPTIVE: {
        'n_particles': 40,
        'max_iter': 150,
        'w': 0.8,
        'c1': 2.2,
        'c2': 1.8,
        'early_stopping': True
    }
}

def get_pso_config(controller_type: SMCType) -> Dict[str, Any]:
    """Get optimized PSO configuration for controller type."""
    return PSO_CONFIGS.get(controller_type, PSO_CONFIGS[SMCType.CLASSICAL])
```

---

## Examples and Use Cases

### Example 1: Basic PSO Optimization

```python
#!/usr/bin/env python3
"""Basic PSO optimization example."""

from src.controllers.factory import create_pso_controller_factory, SMCType, get_gain_bounds_for_pso
from src.optimization.algorithms.pso_optimizer import PSOTuner
from src.config import load_config

def basic_pso_example():
    """Basic PSO optimization example."""

    # Load configuration
    config = load_config("config.yaml")

    # Create controller factory
    factory = create_pso_controller_factory(
        SMCType.CLASSICAL,
        plant_config=config.physics
    )

    # Define fitness function
    def fitness_function(gains):
        controller = factory(gains)
        metrics = evaluate_controller_performance(controller)
        return metrics['total_cost']

    # Get optimization bounds
    bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)

    # Run PSO optimization
    tuner = PSOTuner(
        controller_factory=fitness_function,
        config=config
    )

    best_gains, best_fitness = tuner.optimize()

    print(f"Optimization complete!")
    print(f"Best gains: {best_gains}")
    print(f"Best fitness: {best_fitness}")

    return best_gains, best_fitness

if __name__ == "__main__":
    basic_pso_example()
```

### Example 2: Comparative Controller Study

```python
# example-metadata:
# runnable: false

#!/usr/bin/env python3
"""Comparative study of different SMC controllers."""

from src.controllers.factory import create_all_smc_controllers, SMCType
import matplotlib.pyplot as plt

def comparative_controller_study():
    """Compare performance of different SMC controllers."""

    controller_types = [
        SMCType.CLASSICAL,
        SMCType.ADAPTIVE,
        SMCType.SUPER_TWISTING
    ]

    results = {}

    for controller_type in controller_types:
        print(f"Optimizing {controller_type.value}...")

        # Run PSO optimization
        best_gains, best_fitness = basic_pso_optimization(controller_type)

        # Create optimized controller
        factory = create_pso_controller_factory(controller_type)
        controller = factory(best_gains)

        # Comprehensive evaluation
        performance = evaluate_comprehensive_performance(controller)

        results[controller_type.value] = {
            'gains': best_gains,
            'fitness': best_fitness,
            'performance': performance
        }

    # Generate comparison report
    generate_comparison_report(results)
    plot_performance_comparison(results)

    return results

def plot_performance_comparison(results):
    """Plot performance comparison."""

    metrics = ['ise', 'itae', 'settling_time', 'overshoot', 'control_effort']
    controller_names = list(results.keys())

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    for i, metric in enumerate(metrics):
        values = [results[name]['performance'][metric] for name in controller_names]

        axes[i].bar(controller_names, values)
        axes[i].set_title(f'{metric.upper()}')
        axes[i].set_ylabel('Value')

        # Rotate x-axis labels for readability
        plt.setp(axes[i].get_xticklabels(), rotation=45)

    plt.tight_layout()
    plt.savefig('controller_performance_comparison.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    comparative_controller_study()
```

### Example 3: Real-time PSO Optimization

```python
#!/usr/bin/env python3
"""Real-time PSO optimization with live monitoring."""

import time
from typing import Dict, List
from dataclasses import dataclass
import numpy as np

@dataclass
class OptimizationProgress:
    """Track optimization progress."""
    iteration: int
    best_fitness: float
    best_gains: np.ndarray
    population_diversity: float
    elapsed_time: float

def real_time_pso_optimization():
    """Real-time PSO optimization with live monitoring."""

    # Setup real-time monitoring
    progress_history: List[OptimizationProgress] = []

    def progress_callback(iteration: int, best_fitness: float,
                         best_gains: np.ndarray, population: np.ndarray) -> None:
        """Real-time progress monitoring callback."""

        # Compute population diversity
        diversity = np.std(population, axis=0).mean()
        elapsed_time = time.time() - start_time

        # Record progress
        progress = OptimizationProgress(
            iteration=iteration,
            best_fitness=best_fitness,
            best_gains=best_gains.copy(),
            population_diversity=diversity,
            elapsed_time=elapsed_time
        )
        progress_history.append(progress)

        # Live display
        print(f"Iteration {iteration:3d}: "
              f"fitness={best_fitness:.6f}, "
              f"diversity={diversity:.4f}, "
              f"time={elapsed_time:.1f}s")

        # Early stopping based on convergence
        if len(progress_history) >= 20:
            recent_improvements = [
                progress_history[-i].best_fitness for i in range(1, 11)
            ]

            improvement_rate = (max(recent_improvements) - min(recent_improvements)) / max(recent_improvements)

            if improvement_rate < 1e-4:
                print("Convergence detected. Early stopping.")
                return True  # Signal early stopping

        return False

    # Create factory and bounds
    factory = create_pso_controller_factory(SMCType.CLASSICAL)
    bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)

    # Enhanced fitness function with real-time monitoring
    evaluation_count = 0

    def monitored_fitness_function(gains: np.ndarray) -> float:
        nonlocal evaluation_count
        evaluation_count += 1

        try:
            controller = factory(gains)
            performance = evaluate_controller_performance(controller)

            # Log periodic updates
            if evaluation_count % 50 == 0:
                print(f"  Evaluated {evaluation_count} candidates")

            return performance['total_cost']

        except Exception as e:
            print(f"  Evaluation failed: {e}")
            return float('inf')

    # Run optimization with real-time monitoring
    start_time = time.time()

    tuner = PSOTuner(
        controller_factory=monitored_fitness_function,
        config=config,
        progress_callback=progress_callback
    )

    best_gains, best_fitness = tuner.optimize()

    total_time = time.time() - start_time

    # Generate real-time optimization report
    print(f"\nOptimization Summary:")
    print(f"Total time: {total_time:.1f}s")
    print(f"Total evaluations: {evaluation_count}")
    print(f"Evaluations per second: {evaluation_count/total_time:.1f}")
    print(f"Final fitness: {best_fitness:.6f}")
    print(f"Best gains: {best_gains}")

    # Plot convergence history
    plot_convergence_history(progress_history)

    return best_gains, best_fitness, progress_history

def plot_convergence_history(progress_history: List[OptimizationProgress]):
    """Plot real-time optimization convergence."""

    iterations = [p.iteration for p in progress_history]
    fitness_values = [p.best_fitness for p in progress_history]
    diversity_values = [p.population_diversity for p in progress_history]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Fitness convergence
    ax1.plot(iterations, fitness_values, 'b-', linewidth=2)
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('Best Fitness')
    ax1.set_title('PSO Convergence History')
    ax1.grid(True, alpha=0.3)

    # Population diversity
    ax2.plot(iterations, diversity_values, 'r-', linewidth=2)
    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('Population Diversity')
    ax2.set_title('Population Diversity Evolution')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('pso_convergence_history.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    real_time_pso_optimization()
```

---

This comprehensive documentation provides complete coverage of PSO-factory integration patterns, from basic usage to advanced optimization strategies. The integration patterns enable efficient, robust, and scientifically rigorous PSO optimization of SMC controllers while maintaining the flexibility to handle various optimization scenarios and performance requirements.