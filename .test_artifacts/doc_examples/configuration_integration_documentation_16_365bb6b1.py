# Example from: docs\configuration_integration_documentation.md
# Index: 16
# Runnable: True
# Hash: 365bb6b1

from jinja2 import Template
import yaml
from typing import Dict, Any

class ConfigurationTemplateManager:
    """Manage configuration templates with parameter substitution."""

    def __init__(self):
        self.templates = self._load_templates()
        self.parameter_sets = self._load_parameter_sets()

    def _load_templates(self) -> Dict[str, Template]:
        """Load configuration templates."""

        templates = {}

        # Base controller template
        templates['controller_template'] = Template("""
controllers:
  {{ controller_type }}:
    gains: {{ gains }}
    max_force: {{ max_force | default(150.0) }}
    dt: {{ dt | default(0.001) }}
    {% if controller_type == 'classical_smc' %}
    boundary_layer: {{ boundary_layer | default(0.02) }}
    switch_method: "{{ switch_method | default('tanh') }}"
    {% elif controller_type == 'adaptive_smc' %}
    leak_rate: {{ leak_rate | default(0.01) }}
    dead_zone: {{ dead_zone | default(0.05) }}
    K_min: {{ K_min | default(0.1) }}
    K_max: {{ K_max | default(100.0) }}
    {% elif controller_type == 'sta_smc' %}
    power_exponent: {{ power_exponent | default(0.5) }}
    regularization: {{ regularization | default(1e-6) }}
    {% endif %}
        """)

        # PSO template
        templates['pso_template'] = Template("""
pso:
  n_particles: {{ n_particles | default(30) }}
  max_iter: {{ max_iter | default(100) }}
  w: {{ inertia_weight | default(0.9) }}
  c1: {{ cognitive_coeff | default(2.0) }}
  c2: {{ social_coeff | default(2.0) }}
  bounds:
    {{ controller_type }}:
      lower: {{ lower_bounds }}
      upper: {{ upper_bounds }}
        """)

        # Complete system template
        templates['system_template'] = Template("""
# Generated configuration for {{ system_name }}
global_seed: {{ seed | default(42) }}

physics:
  m1: {{ physics.m1 | default(0.5) }}
  m2: {{ physics.m2 | default(0.5) }}
  M: {{ physics.M | default(2.0) }}
  l1: {{ physics.l1 | default(0.5) }}
  l2: {{ physics.l2 | default(0.5) }}
  b1: {{ physics.b1 | default(0.1) }}
  b2: {{ physics.b2 | default(0.1) }}
  I1: {{ physics.I1 | default(0.1) }}
  I2: {{ physics.I2 | default(0.1) }}

simulation:
  duration: {{ simulation.duration | default(5.0) }}
  dt: {{ simulation.dt | default(0.001) }}
  initial_state: {{ simulation.initial_state | default([0.1, 0.05, 0.0, 0.0, 0.0, 0.0]) }}
  use_full_dynamics: {{ simulation.use_full_dynamics | default(false) }}

{{ controller_config }}

{{ pso_config }}

cost_function:
  weights:
    ise: {{ cost_weights.ise | default(0.4) }}
    control_effort: {{ cost_weights.control_effort | default(0.3) }}
    settling_time: {{ cost_weights.settling_time | default(0.2) }}
    overshoot: {{ cost_weights.overshoot | default(0.1) }}
        """)

        return templates

    def _load_parameter_sets(self) -> Dict[str, Dict[str, Any]]:
        """Load predefined parameter sets."""

        return {
            'conservative': {
                'gains': {
                    'classical_smc': [15, 10, 8, 5, 25, 3],
                    'adaptive_smc': [18, 12, 10, 6, 2.5],
                    'sta_smc': [20, 12, 15, 8, 6, 4]
                },
                'max_force': 100.0,
                'boundary_layer': 0.03,
                'pso': {'n_particles': 20, 'max_iter': 50}
            },
            'aggressive': {
                'gains': {
                    'classical_smc': [30, 25, 20, 15, 60, 8],
                    'adaptive_smc': [35, 28, 22, 18, 8.0],
                    'sta_smc': [40, 25, 30, 20, 15, 10]
                },
                'max_force': 200.0,
                'boundary_layer': 0.01,
                'pso': {'n_particles': 50, 'max_iter': 150}
            },
            'research': {
                'gains': {
                    'classical_smc': [20, 15, 12, 8, 35, 5],
                    'adaptive_smc': [25, 18, 15, 10, 4],
                    'sta_smc': [25, 15, 20, 12, 8, 6]
                },
                'max_force': 150.0,
                'boundary_layer': 0.02,
                'pso': {'n_particles': 40, 'max_iter': 100}
            }
        }

    def generate_configuration(self,
                             controller_type: str,
                             parameter_set: str = 'research',
                             custom_params: Optional[Dict[str, Any]] = None,
                             output_file: Optional[str] = None) -> str:
        """Generate configuration from template."""

        # Get base parameters
        base_params = self.parameter_sets.get(parameter_set, self.parameter_sets['research'])

        # Merge with custom parameters
        if custom_params:
            params = self._deep_merge(base_params, custom_params)
        else:
            params = base_params

        # Get controller-specific gains
        controller_gains = params['gains'].get(controller_type, [20, 15, 12, 8, 35, 5])

        # Generate controller configuration
        controller_template_params = {
            'controller_type': controller_type,
            'gains': controller_gains,
            'max_force': params.get('max_force', 150.0),
            'boundary_layer': params.get('boundary_layer', 0.02)
        }

        controller_config = self.templates['controller_template'].render(**controller_template_params)

        # Generate PSO configuration
        from src.controllers.factory import get_gain_bounds_for_pso, SMCType

        try:
            smc_type = getattr(SMCType, controller_type.upper().replace('_SMC', ''))
            lower_bounds, upper_bounds = get_gain_bounds_for_pso(smc_type)
        except:
            lower_bounds = [1.0] * len(controller_gains)
            upper_bounds = [50.0] * len(controller_gains)

        pso_template_params = {
            'controller_type': controller_type,
            'n_particles': params.get('pso', {}).get('n_particles', 30),
            'max_iter': params.get('pso', {}).get('max_iter', 100),
            'lower_bounds': lower_bounds,
            'upper_bounds': upper_bounds
        }

        pso_config = self.templates['pso_template'].render(**pso_template_params)

        # Generate complete system configuration
        system_template_params = {
            'system_name': f"{controller_type.upper()} Control System",
            'controller_config': controller_config,
            'pso_config': pso_config,
            'physics': params.get('physics', {}),
            'simulation': params.get('simulation', {}),
            'cost_weights': params.get('cost_weights', {})
        }

        system_config = self.templates['system_template'].render(**system_template_params)

        # Save to file if requested
        if output_file:
            with open(output_file, 'w') as f:
                f.write(system_config)

        return system_config

    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge dictionaries."""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

# Usage
template_manager = ConfigurationTemplateManager()

# Generate conservative classical SMC configuration
config_yaml = template_manager.generate_configuration(
    controller_type='classical_smc',
    parameter_set='conservative',
    custom_params={
        'physics': {'m1': 0.6, 'm2': 0.4},
        'simulation': {'duration': 3.0}
    },
    output_file='conservative_classical_config.yaml'
)

print("Generated configuration:")
print(config_yaml)