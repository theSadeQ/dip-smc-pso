# controllers.smc.algorithms.adaptive.parameter_estimation

**Source:** `src\controllers\smc\algorithms\adaptive\parameter_estimation.py`

## Module Overview

Parameter and Uncertainty Estimation for Adaptive SMC.

Implements online estimation of system uncertainties and disturbance bounds
to improve adaptive gain selection and overall controller performance.

Mathematical Background:
- Uncertainty bound estimation: η̂ = max{|disturbance|, model_error}
- Sliding mode observer: estimate unknown dynamics components
- Recursive least squares: parameter identification

## Complete Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/adaptive/parameter_estimation.py
:language: python
:linenos:
```

---

## Classes

### `UncertaintyEstimator`

Online uncertainty estimation for adaptive SMC.

Estimates bounds on system uncertainties and disturbances
to improve adaptive gain selection.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/adaptive/parameter_estimation.py
:language: python
:pyobject: UncertaintyEstimator
:linenos:
```

#### Methods (8)

##### `__init__(self, window_size, forgetting_factor, initial_estimate, estimation_gain)`

Initialize uncertainty estimator.

[View full source →](#method-uncertaintyestimator-__init__)

##### `update_estimate(self, surface_value, surface_derivative, control_input, dt)`

Update uncertainty estimate based on sliding surface behavior.

[View full source →](#method-uncertaintyestimator-update_estimate)

##### `_compute_uncertainty_indicator(self, s, s_dot, u)`

Compute uncertainty indicator from surface behavior.

[View full source →](#method-uncertaintyestimator-_compute_uncertainty_indicator)

##### `get_uncertainty_bound(self)`

Get current uncertainty bound estimate.

[View full source →](#method-uncertaintyestimator-get_uncertainty_bound)

##### `get_confidence_interval(self, confidence)`

Get confidence interval for uncertainty estimate.

[View full source →](#method-uncertaintyestimator-get_confidence_interval)

##### `analyze_estimation_quality(self)`

Analyze quality of uncertainty estimation.

[View full source →](#method-uncertaintyestimator-analyze_estimation_quality)

##### `update_estimates(self, surface_value, adaptation_rate, dt)`

Compatibility method for tests - maps to update_estimate with surface derivative.

[View full source →](#method-uncertaintyestimator-update_estimates)

##### `current_estimates(self)`

Current uncertainty estimates for test compatibility.

[View full source →](#method-uncertaintyestimator-current_estimates)

---

### `ParameterIdentifier`

Online parameter identification using recursive least squares.

Identifies unknown system parameters to improve model accuracy
and reduce uncertainty bounds.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/adaptive/parameter_estimation.py
:language: python
:pyobject: ParameterIdentifier
:linenos:
```

#### Methods (6)

##### `__init__(self, n_parameters, forgetting_factor, initial_covariance)`

Initialize parameter identifier.

[View full source →](#method-parameteridentifier-__init__)

##### `update_parameters(self, regressor, measurement)`

Update parameter estimates using RLS algorithm.

[View full source →](#method-parameteridentifier-update_parameters)

##### `get_parameter_estimates(self)`

Get current parameter estimates.

[View full source →](#method-parameteridentifier-get_parameter_estimates)

##### `get_parameter_covariance(self)`

Get parameter covariance matrix.

[View full source →](#method-parameteridentifier-get_parameter_covariance)

##### `get_parameter_confidence(self, confidence)`

Get confidence intervals for parameters.

[View full source →](#method-parameteridentifier-get_parameter_confidence)

##### `reset_identifier(self, initial_covariance)`

Reset parameter identifier state.

[View full source →](#method-parameteridentifier-reset_identifier)

---

### `CombinedEstimator`

Combined uncertainty estimation and parameter identification.

Integrates uncertainty estimation with parameter identification
for improved adaptive SMC performance.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/adaptive/parameter_estimation.py
:language: python
:pyobject: CombinedEstimator
:linenos:
```

#### Methods (4)

##### `__init__(self, n_parameters)`

Initialize combined estimator.

[View full source →](#method-combinedestimator-__init__)

##### `update_estimates(self, surface_value, surface_derivative, control_input, regressor, measurement, dt)`

Update both uncertainty and parameter estimates.

[View full source →](#method-combinedestimator-update_estimates)

##### `set_estimation_active(self, active)`

Enable/disable online estimation.

[View full source →](#method-combinedestimator-set_estimation_active)

##### `get_combined_analysis(self)`

Get comprehensive analysis of estimation performance.

[View full source →](#method-combinedestimator-get_combined_analysis)

---

## Dependencies

This module imports:

- `from typing import List, Optional, Union, Dict, Any`
- `import numpy as np`
- `from collections import deque`
