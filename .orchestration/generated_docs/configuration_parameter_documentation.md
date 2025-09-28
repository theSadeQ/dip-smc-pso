# Configuration Parameter Documentation

## SMC Gain Specifications

### Classical SMC (SMCType.CLASSICAL)
- **Parameters**: 6 gains [k1, k2, lam1, lam2, K, kd]
- **Bounds**: Typically [0.1, 50.0] for most gains
- **Description**:
  - k1, k2: Sliding surface gains for pendulum 1 and 2
  - lam1, lam2: Sliding surface velocity gains
  - K: Switching gain magnitude
  - kd: Derivative gain for smoothing

### Adaptive SMC (SMCType.ADAPTIVE)
- **Parameters**: 5 gains [k1, k2, lam1, lam2, gamma]
- **Bounds**: [0.1, 50.0] for k gains, [1.0, 200.0] for gamma
- **Description**:
  - k1, k2, lam1, lam2: Same as classical SMC
  - gamma: Adaptation rate parameter

## Parameter Tuning Guidelines

### Sliding Surface Gains (k1, k2)
- **Range**: [1.0, 50.0]
- **Effect**: Higher values provide faster response but may cause chattering
- **Tuning**: Start with moderate values (5-15), increase for better tracking

### Velocity Gains (lam1, lam2)
- **Range**: [0.1, 20.0]
- **Effect**: Damping in sliding surface
- **Tuning**: Increase to reduce overshoot, decrease for faster response

### Switching Gain (K)
- **Range**: [1.0, 200.0]
- **Effect**: Robustness to uncertainties
- **Tuning**: Increase to handle disturbances, minimize to reduce chattering

## Configuration Best Practices
1. Start with default values from literature
2. Use PSO optimization for fine-tuning
3. Validate stability after parameter changes
4. Consider physical system limitations
