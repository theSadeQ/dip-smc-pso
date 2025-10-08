# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 28
# Runnable: False
# Hash: 5e8228e5

# example-metadata:
# runnable: false

#!/usr/bin/env python3
"""Comprehensive factory debugging suite."""

import logging
import traceback
import time
import json
from pathlib import Path

class FactoryDebugger:
    """Comprehensive debugging tools for factory integration."""

    def __init__(self, log_file='factory_debug.log'):
        self.log_file = log_file
        self._setup_logging()
        self.debug_data = {}

    def _setup_logging(self):
        """Setup detailed logging."""
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('FactoryDebugger')

    def debug_controller_creation(self, controller_type, **kwargs):
        """Debug controller creation step by step."""

        debug_info = {
            'timestamp': time.time(),
            'controller_type': controller_type,
            'kwargs': kwargs,
            'steps': [],
            'errors': [],
            'success': False
        }

        try:
            # Step 1: Check controller availability
            step1 = self._debug_step_availability(controller_type)
            debug_info['steps'].append(step1)

            if not step1['success']:
                return debug_info

            # Step 2: Parameter resolution
            step2 = self._debug_step_parameters(controller_type, kwargs)
            debug_info['steps'].append(step2)

            # Step 3: Configuration creation
            step3 = self._debug_step_configuration(controller_type, step2['resolved_params'])
            debug_info['steps'].append(step3)

            # Step 4: Controller instantiation
            step4 = self._debug_step_instantiation(controller_type, step3['config'])
            debug_info['steps'].append(step4)

            if step4['success']:
                debug_info['success'] = True
                debug_info['controller'] = step4['controller']

        except Exception as e:
            debug_info['errors'].append({
                'type': type(e).__name__,
                'message': str(e),
                'traceback': traceback.format_exc()
            })

        # Store debug data
        self.debug_data[f"{controller_type}_{time.time()}"] = debug_info

        return debug_info

    def _debug_step_availability(self, controller_type):
        """Debug controller availability."""
        step = {'name': 'availability_check', 'success': False}

        try:
            from src.controllers.factory import list_available_controllers, CONTROLLER_REGISTRY

            available = list_available_controllers()
            step['available_controllers'] = available
            step['controller_in_registry'] = controller_type in CONTROLLER_REGISTRY
            step['controller_available'] = controller_type in available

            if controller_type in available:
                controller_info = CONTROLLER_REGISTRY[controller_type]
                step['controller_info'] = {
                    'class_available': controller_info['class'] is not None,
                    'description': controller_info['description'],
                    'gain_count': controller_info['gain_count']
                }
                step['success'] = True
            else:
                step['error'] = f"Controller {controller_type} not available"

        except Exception as e:
            step['error'] = str(e)

        return step

    def _debug_step_parameters(self, controller_type, kwargs):
        """Debug parameter resolution."""
        step = {'name': 'parameter_resolution', 'success': False}

        try:
            # Analyze provided parameters
            step['provided_params'] = list(kwargs.keys())
            step['gains_provided'] = 'gains' in kwargs
            step['config_provided'] = 'config' in kwargs

            # Check gains if provided
            if 'gains' in kwargs:
                gains = kwargs['gains']
                step['gains_analysis'] = {
                    'type': type(gains).__name__,
                    'length': len(gains) if hasattr(gains, '__len__') else 'N/A',
                    'all_numeric': all(isinstance(g, (int, float)) for g in gains) if hasattr(gains, '__iter__') else False
                }

            # Resolve final parameters
            from src.controllers.factory import get_default_gains

            if 'gains' not in kwargs:
                default_gains = get_default_gains(controller_type)
                step['using_default_gains'] = True
                step['default_gains'] = default_gains
                resolved_gains = default_gains
            else:
                resolved_gains = kwargs['gains']

            step['resolved_params'] = kwargs.copy()
            step['resolved_params']['gains'] = resolved_gains
            step['success'] = True

        except Exception as e:
            step['error'] = str(e)

        return step

    def _debug_step_configuration(self, controller_type, params):
        """Debug configuration creation."""
        step = {'name': 'configuration_creation', 'success': False}

        try:
            from src.controllers.factory import CONTROLLER_REGISTRY

            controller_info = CONTROLLER_REGISTRY[controller_type]
            config_class = controller_info['config_class']

            step['config_class'] = config_class.__name__
            step['required_params'] = controller_info['required_params']

            # Try to create configuration
            if controller_type == 'classical_smc':
                config = config_class(
                    gains=params['gains'],
                    max_force=params.get('max_force', 150.0),
                    boundary_layer=params.get('boundary_layer', 0.02),
                    dt=params.get('dt', 0.001)
                )
            elif controller_type == 'adaptive_smc':
                config = config_class(
                    gains=params['gains'],
                    max_force=params.get('max_force', 150.0),
                    dt=params.get('dt', 0.001)
                )
            # ... other controller types
            else:
                # Generic creation
                config = config_class(**params)

            step['config'] = config
            step['success'] = True

        except Exception as e:
            step['error'] = str(e)
            step['traceback'] = traceback.format_exc()

        return step

    def _debug_step_instantiation(self, controller_type, config):
        """Debug controller instantiation."""
        step = {'name': 'controller_instantiation', 'success': False}

        try:
            from src.controllers.factory import CONTROLLER_REGISTRY

            controller_info = CONTROLLER_REGISTRY[controller_type]
            controller_class = controller_info['class']

            step['controller_class'] = controller_class.__name__

            # Create controller
            controller = controller_class(config)

            # Verify controller interface
            step['has_compute_control'] = hasattr(controller, 'compute_control')
            step['has_reset'] = hasattr(controller, 'reset')
            step['has_gains'] = hasattr(controller, 'gains')

            if hasattr(controller, 'gains'):
                step['controller_gains'] = controller.gains

            step['controller'] = controller
            step['success'] = True

        except Exception as e:
            step['error'] = str(e)
            step['traceback'] = traceback.format_exc()

        return step

    def generate_debug_report(self, output_file='debug_report.json'):
        """Generate comprehensive debug report."""

        report = {
            'timestamp': time.time(),
            'total_debug_sessions': len(self.debug_data),
            'sessions': self.debug_data
        }

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        print(f"Debug report saved to: {output_file}")
        return report

# Usage
debugger = FactoryDebugger()

# Debug controller creation
debug_info = debugger.debug_controller_creation(
    'classical_smc',
    gains=[20, 15, 12, 8, 35, 5]
)

if debug_info['success']:
    print("✅ Controller creation successful")
else:
    print("❌ Controller creation failed")
    for error in debug_info['errors']:
        print(f"Error: {error['message']}")

# Generate report
debugger.generate_debug_report()