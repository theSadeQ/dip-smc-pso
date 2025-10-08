# Example from: docs\pso_troubleshooting_maintenance_manual.md
# Index: 17
# Runnable: True
# Hash: a02dabd9

import yaml
import jsonschema
from pathlib import Path

class ConfigurationValidator:
    """Validate PSO configuration files."""

    def __init__(self):
        self.schema = self._load_config_schema()

    def _load_config_schema(self):
        """Load configuration validation schema."""
        return {
            "type": "object",
            "required": ["pso", "cost_function", "simulation", "controllers"],
            "properties": {
                "pso": {
                    "type": "object",
                    "required": ["n_particles", "n_iterations"],
                    "properties": {
                        "n_particles": {"type": "integer", "minimum": 5, "maximum": 500},
                        "n_iterations": {"type": "integer", "minimum": 10, "maximum": 2000},
                        "cognitive_weight": {"type": "number", "minimum": 0.1, "maximum": 5.0},
                        "social_weight": {"type": "number", "minimum": 0.1, "maximum": 5.0},
                        "inertia_weight": {"type": "number", "minimum": 0.1, "maximum": 1.0}
                    }
                },
                "cost_function": {
                    "type": "object",
                    "required": ["weights"],
                    "properties": {
                        "weights": {
                            "type": "object",
                            "required": ["state_error", "control_effort", "control_rate", "stability"],
                            "properties": {
                                "state_error": {"type": "number", "minimum": 0},
                                "control_effort": {"type": "number", "minimum": 0},
                                "control_rate": {"type": "number", "minimum": 0},
                                "stability": {"type": "number", "minimum": 0}
                            }
                        }
                    }
                }
            }
        }

    def validate_config(self, config_path):
        """Validate configuration file."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)

            # JSON Schema validation
            jsonschema.validate(config, self.schema)

            # Custom validations
            validation_results = {
                'syntax_valid': True,
                'schema_valid': True,
                'warnings': [],
                'errors': []
            }

            # Check parameter ranges
            pso_config = config.get('pso', {})
            if pso_config.get('n_particles', 0) * pso_config.get('n_iterations', 0) > 50000:
                validation_results['warnings'].append(
                    "High computational load: particles × iterations > 50,000"
                )

            # Check cost function weights
            weights = config.get('cost_function', {}).get('weights', {})
            total_weight = sum(weights.values()) if weights else 0
            if total_weight < 0.1:
                validation_results['warnings'].append(
                    "Very low total cost function weights - optimization may be ineffective"
                )

            return validation_results

        except yaml.YAMLError as e:
            return {
                'syntax_valid': False,
                'schema_valid': False,
                'errors': [f"YAML syntax error: {e}"],
                'warnings': []
            }

        except jsonschema.ValidationError as e:
            return {
                'syntax_valid': True,
                'schema_valid': False,
                'errors': [f"Schema validation error: {e.message}"],
                'warnings': []
            }

    def backup_config(self, config_path):
        """Create timestamped backup of configuration."""
        config_file = Path(config_path)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = config_file.parent / f"{config_file.stem}_backup_{timestamp}{config_file.suffix}"

        shutil.copy2(config_path, backup_path)
        print(f"✅ Configuration backed up to: {backup_path}")
        return backup_path

# Usage
validator = ConfigurationValidator()
validation_result = validator.validate_config('config.yaml')

if validation_result['schema_valid']:
    print("✅ Configuration is valid")
    if validation_result['warnings']:
        print("⚠️  Warnings:")
        for warning in validation_result['warnings']:
            print(f"  - {warning}")
else:
    print("❌ Configuration validation failed:")
    for error in validation_result['errors']:
        print(f"  - {error}")