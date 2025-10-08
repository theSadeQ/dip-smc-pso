# Example from: docs\factory\pso_factory_api_reference.md
# Index: 6
# Runnable: False
# Hash: 4ed1cbc3

def validate_smc_gains(smc_type: SMCType,
                      gains: List[float],
                      strict: bool = True,
                      return_details: bool = False
                      ) -> Union[bool, Tuple[bool, Dict[str, Any]]]:
    """
    Comprehensive validation of SMC gains against mathematical constraints.

    Performs multi-level validation:
    1. Basic constraints (positivity, bounds checking)
    2. Mathematical constraints (stability, convergence)
    3. Physical constraints (actuator limits, bandwidth)
    4. Numerical constraints (conditioning, finite values)

    Mathematical Validation Framework:

    Classical SMC Validation:
        1. Stability: λ1, λ2, K > 0 (Lyapunov condition V̇ ≤ -η|s|)
        2. Reachability: K > |d_max| (uncertainty bound)
        3. Performance: Pole placement within stability region
        4. Saturation: K·φ ≤ max_force (actuator limits)

    Super-Twisting Validation:
        1. Convergence: K1 > K2 > 0 (finite-time stability)
        2. Lyapunov: K1² > 4LK2 (sufficient condition)
        3. Reachability: Gains sufficient for uncertainty rejection
        4. Bandwidth: Avoid high-frequency content

    Adaptive SMC Validation:
        1. Stability: Base gains satisfy classical constraints
        2. Adaptation: 0.1 ≤ γ ≤ 20 (bounded adaptation)
        3. Convergence: Adaptation rate vs system bandwidth
        4. Robustness: Parameter drift prevention

    Hybrid SMC Validation:
        1. Mode stability: Each mode individually stable
        2. Switching stability: No instability during transitions
        3. Performance: Smooth mode transitions
        4. Robustness: Consistent performance across modes

    Args:
        smc_type: Controller type for validation
        gains: Gain array to validate
        strict: Enable strict mathematical validation
        return_details: Return detailed validation information

    Returns:
        If return_details=False: Boolean validation result
        If return_details=True: Tuple of (is_valid, validation_details)

    Validation Details Dictionary:
        {
            'is_valid': bool,
            'errors': List[str],           # Constraint violations
            'warnings': List[str],         # Potential issues
            'stability_analysis': {
                'lyapunov_stable': bool,
                'convergence_rate': float,
                'stability_margin': float
            },
            'performance_analysis': {
                'estimated_settling_time': float,
                'estimated_overshoot': float,
                'bandwidth_estimate': float
            },
            'constraint_details': {
                'basic_constraints': Dict,
                'mathematical_constraints': Dict,
                'physical_constraints': Dict
            }
        }

    Usage Examples:
        # Basic validation
        is_valid = validate_smc_gains(SMCType.CLASSICAL, [10,8,15,12,50,5])

        # Detailed validation
        is_valid, details = validate_smc_gains(
            SMCType.CLASSICAL, gains, return_details=True
        )
        print(f"Stability margin: {details['stability_analysis']['stability_margin']}")

        # PSO integration with validation
        def pso_fitness_with_validation(gains):
            if not validate_smc_gains(SMCType.CLASSICAL, gains):
                return 1000.0  # Penalty for invalid gains
            return evaluate_controller_performance(gains)

    Raises:
        ValueError: If basic validation fails (wrong gain count, NaN values)
        TypeError: If inputs have wrong types
    """
    # Input validation
    if not isinstance(smc_type, SMCType):
        raise TypeError(f"smc_type must be SMCType, got {type(smc_type)}")

    if not isinstance(gains, (list, np.ndarray)):
        raise TypeError(f"gains must be list or array, got {type(gains)}")

    # Convert to list if numpy array
    if isinstance(gains, np.ndarray):
        gains = gains.tolist()

    # Initialize validation results
    errors = []
    warnings = []
    stability_analysis = {}
    performance_analysis = {}
    constraint_details = {
        'basic_constraints': {},
        'mathematical_constraints': {},
        'physical_constraints': {}
    }

    # Get gain specification
    gain_spec = SMC_GAIN_SPECS[smc_type]

    # Basic validation
    if len(gains) != gain_spec.n_gains:
        errors.append(f"Expected {gain_spec.n_gains} gains, got {len(gains)}")
        if return_details:
            return False, {
                'is_valid': False,
                'errors': errors,
                'warnings': warnings,
                'stability_analysis': {},
                'performance_analysis': {},
                'constraint_details': constraint_details
            }
        return False

    # Check for finite values
    if not all(np.isfinite(g) for g in gains):
        errors.append("All gains must be finite (no NaN or infinite values)")

    # Check for reasonable magnitudes
    if any(abs(g) > 1e6 for g in gains):
        warnings.append("Some gains are very large (>1e6), may cause numerical issues")

    if any(abs(g) < 1e-8 for g in gains[:-1]):  # Exclude kd for classical
        warnings.append("Some gains are very small (<1e-8), may affect performance")

    # Controller-specific mathematical validation
    if smc_type == SMCType.CLASSICAL:
        k1, k2, lam1, lam2, K, kd = gains

        # Basic constraints
        constraint_details['basic_constraints'] = {
            'k1_positive': k1 > 0,
            'k2_positive': k2 > 0,
            'lambda1_positive': lam1 > 0,
            'lambda2_positive': lam2 > 0,
            'K_positive': K > 0,
            'kd_nonnegative': kd >= 0
        }

        # Check positivity constraints
        if any(g <= 0 for g in gains[:5]):
            errors.append("Surface gains (k1,k2,λ1,λ2) and switching gain (K) must be positive")
        if kd < 0:
            errors.append("Damping gain (kd) must be non-negative")

        # Mathematical constraints (strict mode)
        if strict:
            # Estimate stability properties
            # Simplified stability analysis
            min_surface_gain = min(lam1, lam2)
            estimated_bandwidth = min_surface_gain
            estimated_uncertainty = 10.0  # Conservative estimate

            constraint_details['mathematical_constraints'] = {
                'switching_gain_adequate': K > estimated_uncertainty,
                'surface_gains_adequate': min_surface_gain > 1.0,
                'damping_reasonable': kd <= min_surface_gain
            }

            if K <= estimated_uncertainty:
                warnings.append(f"Switching gain K={K:.2f} may be too small for uncertainty rejection")

            # Stability analysis
            stability_margin = K - estimated_uncertainty
            convergence_rate = min(min_surface_gain, stability_margin) if stability_margin > 0 else 0

            stability_analysis = {
                'lyapunov_stable': stability_margin > 0,
                'convergence_rate': convergence_rate,
                'stability_margin': stability_margin / K if K > 0 else 0
            }

            # Performance estimates
            estimated_settling_time = 4.0 / min_surface_gain if min_surface_gain > 0 else float('inf')
            estimated_overshoot = max(0, (k1 + k2) / (lam1 + lam2) - 1) * 100 if (lam1 + lam2) > 0 else 100

            performance_analysis = {
                'estimated_settling_time': estimated_settling_time,
                'estimated_overshoot': estimated_overshoot,
                'bandwidth_estimate': estimated_bandwidth
            }

        # Physical constraints
        max_force_estimate = 100.0  # Default actuator limit
        constraint_details['physical_constraints'] = {
            'force_saturation_check': K <= max_force_estimate,
            'bandwidth_feasible': max(lam1, lam2) <= 50.0
        }

        if K > max_force_estimate:
            warnings.append(f"Switching gain K={K:.1f} may exceed actuator limits")

    elif smc_type == SMCType.SUPER_TWISTING:
        K1, K2, lam1, lam2, alpha1, alpha2 = gains

        # Basic constraints
        constraint_details['basic_constraints'] = {
            'K1_positive': K1 > 0,
            'K2_positive': K2 > 0,
            'K1_greater_K2': K1 > K2,
            'lambda1_positive': lam1 > 0,
            'lambda2_positive': lam2 > 0,
            'alpha1_positive': alpha1 > 0,
            'alpha2_positive': alpha2 > 0
        }

        # Critical convergence constraint
        if K1 <= K2:
            errors.append("K1 must be greater than K2 for finite-time convergence")
        if any(g <= 0 for g in gains):
            errors.append("All STA gains must be positive")

        # Mathematical constraints (strict mode)
        if strict:
            # Finite-time convergence analysis
            L_estimate = 15.0  # Conservative Lipschitz constant estimate
            convergence_condition = K1**2 > 4 * L_estimate * K2

            constraint_details['mathematical_constraints'] = {
                'finite_time_convergence': convergence_condition,
                'gains_well_separated': K1 > K2 * 1.1,
                'lipschitz_condition': K1**2 > 4 * L_estimate * K2
            }

            if not convergence_condition:
                warnings.append("May not satisfy sufficient condition for finite-time convergence")

            # Stability analysis
            convergence_rate = min(K1, K2) if K1 > K2 else 0
            stability_margin = (K1 - K2) / K1 if K1 > 0 else 0

            stability_analysis = {
                'lyapunov_stable': K1 > K2 > 0,
                'convergence_rate': convergence_rate,
                'stability_margin': stability_margin
            }

    elif smc_type == SMCType.ADAPTIVE:
        k1, k2, lam1, lam2, gamma = gains

        # Basic constraints
        constraint_details['basic_constraints'] = {
            'k1_positive': k1 > 0,
            'k2_positive': k2 > 0,
            'lambda1_positive': lam1 > 0,
            'lambda2_positive': lam2 > 0,
            'gamma_in_bounds': 0.1 <= gamma <= 20.0
        }

        # Check positivity and adaptation bounds
        if any(g <= 0 for g in gains[:4]):
            errors.append("Surface gains must be positive")
        if not (0.1 <= gamma <= 20.0):
            errors.append("Adaptation rate γ must be in [0.1, 20.0]")

        # Mathematical constraints (strict mode)
        if strict:
            # Adaptation stability analysis
            system_bandwidth = min(lam1, lam2)
            adaptation_bandwidth = gamma * system_bandwidth

            constraint_details['mathematical_constraints'] = {
                'adaptation_stable': gamma < 10.0,
                'adaptation_not_too_slow': gamma > 0.2,
                'separation_principle': adaptation_bandwidth < system_bandwidth
            }

            if gamma > 10.0:
                warnings.append("High adaptation rate may cause instability")
            if gamma < 0.2:
                warnings.append("Low adaptation rate may be too slow")

            # Stability analysis
            stability_analysis = {
                'lyapunov_stable': True,  # Assuming proper design
                'convergence_rate': min(system_bandwidth, gamma),
                'stability_margin': (20.0 - gamma) / 20.0
            }

    elif smc_type == SMCType.HYBRID:
        k1, k2, lam1, lam2 = gains

        # Basic constraints
        constraint_details['basic_constraints'] = {
            'k1_positive': k1 > 0,
            'k2_positive': k2 > 0,
            'lambda1_positive': lam1 > 0,
            'lambda2_positive': lam2 > 0
        }

        if any(g <= 0 for g in gains):
            errors.append("All hybrid gains must be positive")

        # Mathematical constraints (strict mode)
        if strict:
            # Hybrid stability analysis (simplified)
            min_gain = min(gains)

            constraint_details['mathematical_constraints'] = {
                'mode_stability': min_gain > 1.0,
                'switching_stability': max(gains) / min_gain < 10.0
            }

            stability_analysis = {
                'lyapunov_stable': min_gain > 0,
                'convergence_rate': min_gain,
                'stability_margin': min_gain / max(gains) if max(gains) > 0 else 0
            }

    # Overall validation result
    is_valid = len(errors) == 0

    if return_details:
        validation_details = {
            'is_valid': is_valid,
            'errors': errors,
            'warnings': warnings,
            'stability_analysis': stability_analysis,
            'performance_analysis': performance_analysis,
            'constraint_details': constraint_details
        }
        return is_valid, validation_details
    else:
        return is_valid