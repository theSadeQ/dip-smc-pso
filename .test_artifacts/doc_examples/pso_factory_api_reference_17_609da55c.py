# Example from: docs\factory\pso_factory_api_reference.md
# Index: 17
# Runnable: True
# Hash: 609da55c

class PSOFactoryError(Exception):
    """Base exception for PSO factory integration errors."""
    pass

class ControllerCreationError(PSOFactoryError):
    """Raised when controller creation fails."""

    def __init__(self, smc_type: SMCType, gains: List[float], message: str):
        self.smc_type = smc_type
        self.gains = gains
        super().__init__(f"Failed to create {smc_type.value} controller: {message}")

class GainValidationError(PSOFactoryError):
    """Raised when gain validation fails."""

    def __init__(self, smc_type: SMCType, gains: List[float], violations: List[str]):
        self.smc_type = smc_type
        self.gains = gains
        self.violations = violations
        violation_text = "; ".join(violations)
        super().__init__(f"Gain validation failed for {smc_type.value}: {violation_text}")

class ConfigurationError(PSOFactoryError):
    """Raised when configuration is invalid."""
    pass

class SimulationError(PSOFactoryError):
    """Raised when simulation execution fails."""
    pass

# Error handling decorators
def handle_pso_errors(func):
    """Decorator for robust PSO error handling."""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except GainValidationError:
            # For PSO fitness functions, return penalty value
            return 1000.0
        except (ControllerCreationError, SimulationError) as e:
            # Log error and return penalty
            print(f"PSO evaluation error: {e}")
            return 1000.0
        except Exception as e:
            # Unexpected errors - log and return penalty
            print(f"Unexpected PSO error: {e}")
            return 1000.0

    return wrapper

# Robust PSO fitness function template
@handle_pso_errors
def robust_pso_fitness_function(gains: np.ndarray,
                              smc_type: SMCType,
                              simulation_config: Dict[str, Any]
                              ) -> float:
    """
    Template for robust PSO fitness functions with comprehensive error handling.

    Args:
        gains: Gain array from PSO
        smc_type: Controller type
        simulation_config: Simulation parameters

    Returns:
        Fitness value (lower is better)
    """
    # Create controller with automatic validation
    controller = create_smc_for_pso(smc_type, gains.tolist())

    # Run simulation with error handling
    result = run_simulation_with_error_handling(controller, simulation_config)

    # Compute fitness with validation
    fitness = compute_validated_fitness(result)

    return fitness

def run_simulation_with_error_handling(controller, config: Dict[str, Any]) -> Dict[str, Any]:
    """Run simulation with comprehensive error handling."""

    try:
        # Pre-validate simulation configuration
        validate_simulation_config(config)

        # Run simulation with timeout
        with timeout_context(config.get('timeout', 30.0)):
            result = run_simulation(controller, config)

        # Post-validate simulation results
        validate_simulation_results(result)

        return result

    except TimeoutError:
        raise SimulationError("Simulation timeout exceeded")
    except ValueError as e:
        raise SimulationError(f"Simulation parameter error: {e}")
    except Exception as e:
        raise SimulationError(f"Simulation execution failed: {e}")

@contextmanager
def timeout_context(seconds: float):
    """Context manager for simulation timeout."""
    import signal

    def timeout_handler(signum, frame):
        raise TimeoutError("Operation timed out")

    # Set timeout handler
    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(int(seconds))

    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)