# Example from: docs\pso_configuration_schema_documentation.md
# Index: 8
# Runnable: False
# Hash: ac88892e

# example-metadata:
# runnable: false

class ConfigurationErrorHandler:
    """
    Comprehensive error handling and diagnostic system for PSO configuration.
    """

    ERROR_CATEGORIES = {
        'SYNTAX': {
            'severity': 'CRITICAL',
            'auto_fixable': False,
            'description': 'YAML syntax or structure errors'
        },
        'TYPE': {
            'severity': 'CRITICAL',
            'auto_fixable': True,
            'description': 'Data type mismatches'
        },
        'BOUNDS': {
            'severity': 'HIGH',
            'auto_fixable': True,
            'description': 'Parameter bounds violations'
        },
        'MATHEMATICAL': {
            'severity': 'HIGH',
            'auto_fixable': False,
            'description': 'Mathematical consistency violations'
        },
        'PERFORMANCE': {
            'severity': 'MEDIUM',
            'auto_fixable': True,
            'description': 'Suboptimal performance configuration'
        },
        'COMPATIBILITY': {
            'severity': 'MEDIUM',
            'auto_fixable': True,
            'description': 'Controller compatibility issues'
        }
    }

    def diagnose_configuration_errors(self, config: dict,
                                    controller_type: str = None) -> dict:
        """
        Comprehensive configuration error diagnosis with auto-fix suggestions.
        """
        diagnosis = {
            'errors': [],
            'warnings': [],
            'auto_fixes': [],
            'manual_actions': [],
            'overall_status': 'UNKNOWN'
        }

        # Run diagnostic checks
        for category, info in self.ERROR_CATEGORIES.items():
            category_errors = self._check_category(category, config, controller_type)

            for error in category_errors:
                error['category'] = category
                error['severity'] = info['severity']
                error['auto_fixable'] = info['auto_fixable']

                if error['severity'] == 'CRITICAL':
                    diagnosis['errors'].append(error)
                else:
                    diagnosis['warnings'].append(error)

                # Generate fix suggestions
                if error['auto_fixable']:
                    fix = self._generate_auto_fix(error, config)
                    if fix:
                        diagnosis['auto_fixes'].append(fix)
                else:
                    manual_action = self._generate_manual_action(error)
                    if manual_action:
                        diagnosis['manual_actions'].append(manual_action)

        # Determine overall status
        if diagnosis['errors']:
            diagnosis['overall_status'] = 'CRITICAL'
        elif len(diagnosis['warnings']) > 5:
            diagnosis['overall_status'] = 'NEEDS_ATTENTION'
        elif diagnosis['warnings']:
            diagnosis['overall_status'] = 'MINOR_ISSUES'
        else:
            diagnosis['overall_status'] = 'HEALTHY'

        return diagnosis

    def _check_category(self, category: str, config: dict, controller_type: str) -> list:
        """
        Check specific error category and return found issues.
        """
        errors = []

        if category == 'MATHEMATICAL':
            # PSO convergence check
            if 'algorithm_params' in config:
                params = config['algorithm_params']
                if 'c1' in params and 'c2' in params:
                    phi = params['c1'] + params['c2']
                    if phi <= 4.0:
                        errors.append({
                            'code': 'PSO_CONVERGENCE_RISK',
                            'message': f'PSO may not converge: φ = c₁ + c₂ = {phi:.3f} ≤ 4.0',
                            'location': 'algorithm_params.c1, algorithm_params.c2',
                            'impact': 'Optimization may fail to converge'
                        })

        elif category == 'BOUNDS' and controller_type:
            # Issue #2 specific checks for STA-SMC
            if controller_type == 'sta_smc' and 'bounds' in config:
                bounds = config['bounds']
                if 'sta_smc' in bounds and 'max' in bounds['sta_smc']:
                    max_bounds = bounds['sta_smc']['max']
                    if len(max_bounds) >= 6:
                        lambda1_max, lambda2_max = max_bounds[4], max_bounds[5]
                        if lambda1_max > 10.0 or lambda2_max > 10.0:
                            errors.append({
                                'code': 'ISSUE2_BOUNDS_VIOLATION',
                                'message': f'STA-SMC lambda bounds may cause overshoot: λ₁_max={lambda1_max}, λ₂_max={lambda2_max}',
                                'location': 'bounds.sta_smc.max[4:6]',
                                'impact': 'May cause >5% overshoot (Issue #2 regression)'
                            })

        elif category == 'PERFORMANCE':
            # Suboptimal parameter detection
            if 'algorithm_params' in config:
                params = config['algorithm_params']
                if 'n_particles' in params:
                    n_particles = params['n_particles']
                    if n_particles < 10 or n_particles > 50:
                        errors.append({
                            'code': 'SUBOPTIMAL_SWARM_SIZE',
                            'message': f'Swarm size {n_particles} outside optimal range [10, 50]',
                            'location': 'algorithm_params.n_particles',
                            'impact': 'Suboptimal convergence speed or quality'
                        })

        return errors

    def _generate_auto_fix(self, error: dict, config: dict) -> dict:
        """
        Generate automatic fix for fixable errors.
        """
        if error['code'] == 'PSO_CONVERGENCE_RISK':
            return {
                'error_code': error['code'],
                'fix_type': 'parameter_adjustment',
                'action': 'Increase c₁ and c₂ to ensure φ > 4',
                'changes': {
                    'algorithm_params.c1': 2.1,
                    'algorithm_params.c2': 2.1
                },
                'justification': 'Ensures PSO convergence with φ = 4.2 > 4'
            }

        elif error['code'] == 'ISSUE2_BOUNDS_VIOLATION':
            return {
                'error_code': error['code'],
                'fix_type': 'bounds_correction',
                'action': 'Apply Issue #2 lambda bounds corrections',
                'changes': {
                    'bounds.sta_smc.max[4]': 10.0,  # lambda1
                    'bounds.sta_smc.max[5]': 10.0   # lambda2
                },
                'justification': 'Prevents overshoot regression from Issue #2'
            }

        elif error['code'] == 'SUBOPTIMAL_SWARM_SIZE':
            current_size = config['algorithm_params']['n_particles']
            optimal_size = np.clip(current_size, 15, 25)  # Clamp to optimal range
            return {
                'error_code': error['code'],
                'fix_type': 'parameter_optimization',
                'action': f'Adjust swarm size to optimal range',
                'changes': {
                    'algorithm_params.n_particles': optimal_size
                },
                'justification': f'Optimizes convergence for {optimal_size} particles'
            }

        return None

    def apply_auto_fixes(self, config: dict, fixes: list) -> tuple:
        """
        Apply automatic fixes to configuration.

        Returns:
        tuple: (fixed_config, applied_fixes, failed_fixes)
        """
        fixed_config = config.copy()
        applied_fixes = []
        failed_fixes = []

        for fix in fixes:
            try:
                for path, new_value in fix['changes'].items():
                    self._set_nested_value(fixed_config, path, new_value)
                applied_fixes.append(fix)
            except Exception as e:
                fix['error'] = str(e)
                failed_fixes.append(fix)

        return fixed_config, applied_fixes, failed_fixes

    def _set_nested_value(self, config: dict, path: str, value: any) -> None:
        """
        Set nested configuration value using dot notation path.
        """
        keys = path.split('.')
        current = config

        for key in keys[:-1]:
            if '[' in key and ']' in key:
                # Handle array indexing
                array_key, index_str = key.split('[')
                index = int(index_str.rstrip(']'))
                if array_key not in current:
                    current[array_key] = []
                current = current[array_key]

                # Extend array if necessary
                while len(current) <= index:
                    current.append(None)
                current = current[index]
            else:
                if key not in current:
                    current[key] = {}
                current = current[key]

        # Set the final value
        final_key = keys[-1]
        if '[' in final_key and ']' in final_key:
            array_key, index_str = final_key.split('[')
            index = int(index_str.rstrip(']'))
            if array_key not in current:
                current[array_key] = []
            while len(current[array_key]) <= index:
                current[array_key].append(None)
            current[array_key][index] = value
        else:
            current[final_key] = value