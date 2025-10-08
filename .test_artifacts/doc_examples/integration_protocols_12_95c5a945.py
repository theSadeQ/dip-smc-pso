# Example from: docs\technical\integration_protocols.md
# Index: 12
# Runnable: False
# Hash: 95c5a945

class InterfaceContract:
    """Interface contract specification and validation."""

    def __init__(self, interface_name: str, requirements: Dict[str, Any]):
        self.interface_name = interface_name
        self.requirements = requirements

    def validate_implementation(self, implementation: Any) -> bool:
        """Validate that implementation satisfies contract."""
        try:
            for requirement, spec in self.requirements.items():
                if requirement == 'methods':
                    self._validate_methods(implementation, spec)
                elif requirement == 'properties':
                    self._validate_properties(implementation, spec)
                elif requirement == 'types':
                    self._validate_types(implementation, spec)

            return True

        except Exception as e:
            logger.error(f"Contract validation failed for {self.interface_name}: {e}")
            return False

    def _validate_methods(self, implementation: Any, method_specs: Dict[str, Dict]):
        """Validate required methods."""
        for method_name, spec in method_specs.items():
            if not hasattr(implementation, method_name):
                raise AttributeError(f"Missing required method: {method_name}")

            method = getattr(implementation, method_name)
            if not callable(method):
                raise TypeError(f"Attribute {method_name} is not callable")

            # Validate method signature if specified
            if 'signature' in spec:
                self._validate_method_signature(method, spec['signature'])

# Define standard contracts
CONTROLLER_CONTRACT = InterfaceContract(
    'ControllerInterface',
    {
        'methods': {
            'compute_control': {
                'signature': {
                    'args': ['state', 'last_control', 'history'],
                    'return_type': 'ControlResult'
                }
            }
        },
        'properties': {
            'max_force': 'float',
            'controller_type': 'str'
        }
    }
)

PLANT_MODEL_CONTRACT = InterfaceContract(
    'PlantModelInterface',
    {
        'methods': {
            'compute_dynamics': {
                'signature': {
                    'args': ['state', 'control', 'disturbances'],
                    'return_type': 'np.ndarray'
                }
            },
            'get_linearization': {
                'signature': {
                    'args': ['state', 'control'],
                    'return_type': 'Tuple[np.ndarray, np.ndarray]'
                }
            }
        },
        'properties': {
            'state_dimension': 'int',
            'control_dimension': 'int'
        }
    }
)