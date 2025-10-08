# Example from: docs\configuration_integration_documentation.md
# Index: 14
# Runnable: False
# Hash: de2354ac

class ConfigurationValidator:
    """Comprehensive configuration validation system."""

    def __init__(self):
        self.validation_rules = self._initialize_validation_rules()
        self.validation_errors = []
        self.validation_warnings = []

    def _initialize_validation_rules(self):
        """Initialize controller-specific validation rules."""
        return {
            'classical_smc': self._validate_classical_smc,
            'adaptive_smc': self._validate_adaptive_smc,
            'sta_smc': self._validate_sta_smc,
            'hybrid_adaptive_sta_smc': self._validate_hybrid_smc,
            'mpc_controller': self._validate_mpc
        }

    def validate_configuration(self, controller_type: str, config: Dict[str, Any]) -> bool:
        """Validate configuration for specific controller type."""

        self.validation_errors.clear()
        self.validation_warnings.clear()

        try:
            # Basic validation
            self._validate_basic_structure(config)

            # Controller-specific validation
            if controller_type in self.validation_rules:
                self.validation_rules[controller_type](config)
            else:
                self.validation_warnings.append(f"No specific validation rules for {controller_type}")

            # Cross-parameter validation
            self._validate_cross_parameters(config)

            return len(self.validation_errors) == 0

        except Exception as e:
            self.validation_errors.append(f"Validation failed: {e}")
            return False

    def _validate_basic_structure(self, config: Dict[str, Any]):
        """Validate basic configuration structure."""

        required_fields = ['gains', 'max_force', 'dt']
        for field in required_fields:
            if field not in config:
                self.validation_errors.append(f"Missing required field: {field}")

    def _validate_classical_smc(self, config: Dict[str, Any]):
        """Validate Classical SMC configuration."""

        gains = config.get('gains', [])

        # Gain count validation
        if len(gains) != 6:
            self.validation_errors.append("Classical SMC requires 6 gains")
            return

        k1, k2, lam1, lam2, K, kd = gains

        # Positivity constraints
        if not all(g > 0 for g in gains):
            self.validation_errors.append("All gains must be positive")

        # Stability constraints
        if lam1 <= 0 or lam2 <= 0:
            self.validation_errors.append("Surface coefficients λ1, λ2 must be positive")

        # Practical constraints
        if K > 200:
            self.validation_warnings.append("High switching gain K may cause chattering")

        if lam1/k1 > 50 or lam2/k2 > 50:
            self.validation_warnings.append("High surface coefficient ratios")

        # Boundary layer validation
        boundary_layer = config.get('boundary_layer', 0)
        if boundary_layer <= 0:
            self.validation_errors.append("Boundary layer must be positive")

        if boundary_layer > 0.1:
            self.validation_warnings.append("Large boundary layer may reduce tracking accuracy")

    def _validate_adaptive_smc(self, config: Dict[str, Any]):
        """Validate Adaptive SMC configuration."""

        gains = config.get('gains', [])

        # Gain count validation
        if len(gains) != 5:
            self.validation_errors.append("Adaptive SMC requires 5 gains")
            return

        k1, k2, lam1, lam2, gamma = gains

        # Adaptation rate validation
        if gamma <= 0:
            self.validation_errors.append("Adaptation rate γ must be positive")

        if gamma > 50:
            self.validation_warnings.append("High adaptation rate may cause instability")

        # Leak rate validation
        leak_rate = config.get('leak_rate', 0.01)
        if not 0 < leak_rate < 1:
            self.validation_errors.append("Leak rate must be in (0, 1)")

        # Dead zone validation
        dead_zone = config.get('dead_zone', 0.05)
        if dead_zone <= 0:
            self.validation_errors.append("Dead zone must be positive")

        # Adaptive gain bounds
        K_min = config.get('K_min', 0.1)
        K_max = config.get('K_max', 100.0)
        K_init = config.get('K_init', 10.0)

        if not 0 < K_min < K_max:
            self.validation_errors.append("Must have 0 < K_min < K_max")

        if not K_min <= K_init <= K_max:
            self.validation_errors.append("K_init must be in [K_min, K_max]")

    def _validate_sta_smc(self, config: Dict[str, Any]):
        """Validate Super-Twisting SMC configuration."""

        gains = config.get('gains', [])

        if len(gains) != 6:
            self.validation_errors.append("Super-twisting SMC requires 6 gains")
            return

        K1, K2, k1, k2, lam1, lam2 = gains

        # Algorithmic gains
        if K1 <= 0 or K2 <= 0:
            self.validation_errors.append("Algorithmic gains K1, K2 must be positive")

        # Convergence conditions
        if K2 > 2 * K1:
            self.validation_warnings.append("K2 > 2*K1 may cause oscillations")

        if K1 < max(k1, k2):
            self.validation_warnings.append("K1 < max(k1,k2) may not achieve finite-time convergence")

        # Power exponent
        power_exponent = config.get('power_exponent', 0.5)
        if not 0 < power_exponent < 1:
            self.validation_errors.append("Power exponent must be in (0, 1)")

    def _validate_hybrid_smc(self, config: Dict[str, Any]):
        """Validate Hybrid SMC configuration."""

        gains = config.get('gains', [])

        if len(gains) != 4:
            self.validation_errors.append("Hybrid SMC requires 4 gains")

        # Check sub-configurations
        classical_config = config.get('classical_config')
        adaptive_config = config.get('adaptive_config')

        if classical_config is None:
            self.validation_errors.append("Missing classical_config for hybrid controller")
        else:
            self._validate_classical_smc(classical_config)

        if adaptive_config is None:
            self.validation_errors.append("Missing adaptive_config for hybrid controller")
        else:
            self._validate_adaptive_smc(adaptive_config)

        # Hybrid mode validation
        hybrid_mode = config.get('hybrid_mode', 'classical_adaptive')
        valid_modes = ['classical_adaptive', 'sta_adaptive', 'dynamic_switching']

        if hybrid_mode not in valid_modes:
            self.validation_errors.append(f"Invalid hybrid_mode: {hybrid_mode}")

    def _validate_mpc(self, config: Dict[str, Any]):
        """Validate MPC configuration."""

        # Horizon validation
        horizon = config.get('horizon', 10)
        if not isinstance(horizon, int) or horizon < 1:
            self.validation_errors.append("Horizon must be positive integer")

        if horizon > 50:
            self.validation_warnings.append("Large horizon may cause computational issues")

        # Weight validation
        weights = ['q_x', 'q_theta', 'r_u']
        for weight in weights:
            value = config.get(weight, 1.0)
            if not isinstance(value, (int, float)) or value < 0:
                self.validation_errors.append(f"{weight} must be non-negative number")

    def _validate_cross_parameters(self, config: Dict[str, Any]):
        """Validate relationships between parameters."""

        max_force = config.get('max_force', 150.0)
        dt = config.get('dt', 0.001)

        # Timestep validation
        if dt > 0.01:
            self.validation_warnings.append("Large timestep (>0.01s) may cause numerical issues")

        if dt < 1e-5:
            self.validation_warnings.append("Very small timestep may be computationally expensive")

        # Force limits
        if max_force > 500:
            self.validation_warnings.append("Very high force limit may be unrealistic")

        if max_force < 10:
            self.validation_warnings.append("Low force limit may prevent effective control")

    def get_validation_report(self) -> Dict[str, Any]:
        """Get comprehensive validation report."""
        return {
            'valid': len(self.validation_errors) == 0,
            'errors': self.validation_errors.copy(),
            'warnings': self.validation_warnings.copy(),
            'error_count': len(self.validation_errors),
            'warning_count': len(self.validation_warnings)
        }

# Usage
validator = ConfigurationValidator()

# Validate configuration
config = {
    'gains': [20, 15, 12, 8, 35, 5],
    'max_force': 150.0,
    'boundary_layer': 0.02,
    'dt': 0.001
}

is_valid = validator.validate_configuration('classical_smc', config)
report = validator.get_validation_report()

if not is_valid:
    print("Configuration validation failed:")
    for error in report['errors']:
        print(f"  ❌ {error}")

if report['warnings']:
    print("Configuration warnings:")
    for warning in report['warnings']:
        print(f"  ⚠️  {warning}")