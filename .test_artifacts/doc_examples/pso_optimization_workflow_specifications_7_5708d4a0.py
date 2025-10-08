# Example from: docs\pso_optimization_workflow_specifications.md
# Index: 7
# Runnable: False
# Hash: 5708d4a0

class WorkflowErrorHandler:
    """
    Comprehensive error handling and recovery for PSO optimization workflow.
    """

    ERROR_CATEGORIES = {
        'CONFIGURATION_ERROR': {
            'severity': 'CRITICAL',
            'recovery_strategy': 'configuration_repair',
            'retry_enabled': True
        },
        'OPTIMIZATION_FAILURE': {
            'severity': 'HIGH',
            'recovery_strategy': 'parameter_adjustment',
            'retry_enabled': True
        },
        'CONSTRAINT_VIOLATION': {
            'severity': 'HIGH',
            'recovery_strategy': 'bounds_correction',
            'retry_enabled': True
        },
        'CONVERGENCE_FAILURE': {
            'severity': 'MEDIUM',
            'recovery_strategy': 'adaptive_tuning',
            'retry_enabled': True
        },
        'SAFETY_VIOLATION': {
            'severity': 'CRITICAL',
            'recovery_strategy': 'immediate_termination',
            'retry_enabled': False
        }
    }

    def handle_workflow_error(self, error: Exception, workflow_state: dict) -> ErrorHandlingResult:
        """
        Handle workflow errors with appropriate recovery strategies.
        """
        # Classify error
        error_category = self._classify_error(error, workflow_state)
        error_info = self.ERROR_CATEGORIES[error_category]

        result = ErrorHandlingResult()
        result.error_category = error_category
        result.severity = error_info['severity']

        # Apply recovery strategy
        if error_info['recovery_strategy'] == 'configuration_repair':
            recovery_result = self._attempt_configuration_repair(error, workflow_state)
        elif error_info['recovery_strategy'] == 'parameter_adjustment':
            recovery_result = self._attempt_parameter_adjustment(error, workflow_state)
        elif error_info['recovery_strategy'] == 'bounds_correction':
            recovery_result = self._attempt_bounds_correction(error, workflow_state)
        elif error_info['recovery_strategy'] == 'adaptive_tuning':
            recovery_result = self._attempt_adaptive_tuning(error, workflow_state)
        else:  # immediate_termination
            recovery_result = RecoveryResult(success=False, terminate=True)

        result.recovery_result = recovery_result
        result.retry_recommended = error_info['retry_enabled'] and recovery_result.success

        return result

    def _attempt_bounds_correction(self, error: Exception, workflow_state: dict) -> RecoveryResult:
        """
        Attempt to correct bounds-related errors, especially Issue #2 violations.
        """
        result = RecoveryResult()

        try:
            config = workflow_state.get('config', {})
            controller_type = workflow_state.get('controller_type', 'classical_smc')

            if controller_type == 'sta_smc':
                # Apply Issue #2 bounds corrections
                pso_bounds = config.get('pso', {}).get('bounds', {})
                sta_bounds = pso_bounds.get('sta_smc', pso_bounds)

                if 'max' in sta_bounds and len(sta_bounds['max']) >= 6:
                    # Apply Issue #2 corrections
                    original_lambda1_max = sta_bounds['max'][4]
                    original_lambda2_max = sta_bounds['max'][5]

                    # Reduce lambda bounds if they exceed Issue #2 limits
                    if original_lambda1_max > 10.0:
                        sta_bounds['max'][4] = 10.0
                        result.corrections.append(f'Reduced lambda1_max from {original_lambda1_max} to 10.0')

                    if original_lambda2_max > 10.0:
                        sta_bounds['max'][5] = 10.0
                        result.corrections.append(f'Reduced lambda2_max from {original_lambda2_max} to 10.0')

                    # Adjust corresponding min bounds if necessary
                    if sta_bounds['min'][4] > 5.0:
                        sta_bounds['min'][4] = 0.1
                        result.corrections.append('Adjusted lambda1_min for Issue #2 compliance')

                    if sta_bounds['min'][5] > 5.0:
                        sta_bounds['min'][5] = 0.1
                        result.corrections.append('Adjusted lambda2_min for Issue #2 compliance')

                    result.success = True
                    result.corrected_config = config

        except Exception as e:
            result.success = False
            result.error_message = str(e)

        return result