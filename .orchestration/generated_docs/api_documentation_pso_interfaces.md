# PSO Integration API Documentation

## Core Functions

### create_smc_for_pso
```python
def create_smc_for_pso(
    smc_type: SMCType,
    gains: List[float],
    plant_config: Any,
    max_force: float = 100.0,
    dt: float = 0.01
) -> PSOControllerWrapper
```

**Purpose**: Create SMC controller optimized for PSO integration

**Parameters**:
- `smc_type`: Type of SMC controller (SMCType enum)
- `gains`: List of gain parameters specific to controller type
- `plant_config`: Plant configuration object
- `max_force`: Maximum control force (optional)
- `dt`: Control time step (optional)

**Returns**: PSOControllerWrapper with simplified interface

**Example**:
```python
controller = create_smc_for_pso(
    SMCType.CLASSICAL,
    [10.0, 5.0, 8.0, 3.0, 15.0, 2.0],
    plant_config
)
```

### get_gain_bounds_for_pso
```python
def get_gain_bounds_for_pso(smc_type: SMCType) -> Tuple[List[float], List[float]]
```

**Purpose**: Get optimization bounds for SMC controller gains

**Parameters**:
- `smc_type`: Type of SMC controller

**Returns**: Tuple of (lower_bounds, upper_bounds)

**Example**:
```python
bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)
lower, upper = bounds
```

### validate_smc_gains
```python
def validate_smc_gains(smc_type: SMCType, gains: List[float]) -> bool
```

**Purpose**: Validate if gains are within acceptable bounds

**Parameters**:
- `smc_type`: Type of SMC controller
- `gains`: List of gain values to validate

**Returns**: True if gains are valid, False otherwise

**Example**:
```python
valid = validate_smc_gains(SMCType.CLASSICAL, [10.0, 5.0, 8.0, 3.0, 15.0, 2.0])
```

## PSOControllerWrapper Methods

### compute_control
```python
def compute_control(self, state: np.ndarray) -> np.ndarray
```

**Purpose**: Compute control output for given state

**Parameters**:
- `state`: System state vector (6 elements for DIP)

**Returns**: Control force as 1D numpy array

**Example**:
```python
state = np.array([0.1, 0.2, 0.3, 0.0, 0.0, 0.0])
control = controller.compute_control(state)
```

## Error Handling
- Invalid gains return high fitness penalty in PSO
- Invalid SMC type raises ValueError
- Malformed state inputs raise appropriate exceptions
