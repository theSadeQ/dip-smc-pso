# analysis.validation.statistical_tests

**Source:** `src\analysis\validation\statistical_tests.py`

## Module Overview

Statistical testing framework for analysis validation.

This module provides comprehensive statistical testing capabilities for
validating analysis results, comparing methods, and ensuring statistical
rigor in control engineering applications.

## Complete Source Code

```{literalinclude} ../../../src/analysis/validation/statistical_tests.py
:language: python
:linenos:
```

---

## Classes

### `TestType`

**Inherits from:** `Enum`

Types of statistical tests.

#### Source Code

```{literalinclude} ../../../src/analysis/validation/statistical_tests.py
:language: python
:pyobject: TestType
:linenos:
```

---

### `AlternativeHypothesis`

**Inherits from:** `Enum`

Alternative hypothesis types.

#### Source Code

```{literalinclude} ../../../src/analysis/validation/statistical_tests.py
:language: python
:pyobject: AlternativeHypothesis
:linenos:
```

---

### `StatisticalTestConfig`

Configuration for statistical tests.

#### Source Code

```{literalinclude} ../../../src/analysis/validation/statistical_tests.py
:language: python
:pyobject: StatisticalTestConfig
:linenos:
```

---

### `StatisticalTestSuite`

**Inherits from:** `StatisticalValidator`

Comprehensive statistical testing suite.

#### Source Code

```{literalinclude} ../../../src/analysis/validation/statistical_tests.py
:language: python
:pyobject: StatisticalTestSuite
:linenos:
```

#### Methods (27)

##### `__init__(self, config)`

Initialize statistical test suite.

[View full source →](#method-statisticaltestsuite-__init__)

##### `validation_methods(self)`

List of validation methods supported.

[View full source →](#method-statisticaltestsuite-validation_methods)

##### `validate(self, data)`

Perform comprehensive statistical validation.

[View full source →](#method-statisticaltestsuite-validate)

##### `_preprocess_data(self, data)`

Preprocess data for statistical testing.

[View full source →](#method-statisticaltestsuite-_preprocess_data)

##### `_perform_normality_tests(self, data)`

Perform normality tests.

[View full source →](#method-statisticaltestsuite-_perform_normality_tests)

##### `_perform_stationarity_tests(self, data)`

Perform stationarity tests.

[View full source →](#method-statisticaltestsuite-_perform_stationarity_tests)

##### `_perform_independence_tests(self, data)`

Perform independence tests.

[View full source →](#method-statisticaltestsuite-_perform_independence_tests)

##### `_perform_homoscedasticity_tests(self, data)`

Perform homoscedasticity tests.

[View full source →](#method-statisticaltestsuite-_perform_homoscedasticity_tests)

##### `_perform_hypothesis_tests(self, data, compare_groups)`

Perform hypothesis tests.

[View full source →](#method-statisticaltestsuite-_perform_hypothesis_tests)

##### `_perform_goodness_of_fit_tests(self, data, reference_distribution)`

Perform goodness of fit tests.

[View full source →](#method-statisticaltestsuite-_perform_goodness_of_fit_tests)

##### `_perform_power_analysis(self, data)`

Perform power analysis.

[View full source →](#method-statisticaltestsuite-_perform_power_analysis)

##### `_perform_effect_size_analysis(self, data, compare_groups)`

Perform effect size analysis.

[View full source →](#method-statisticaltestsuite-_perform_effect_size_analysis)

##### `_adf_test(self, data)`

Simplified Augmented Dickey-Fuller test.

[View full source →](#method-statisticaltestsuite-_adf_test)

##### `_kpss_test(self, data)`

Simplified KPSS test.

[View full source →](#method-statisticaltestsuite-_kpss_test)

##### `_variance_ratio_test(self, data)`

Variance ratio test for random walk.

[View full source →](#method-statisticaltestsuite-_variance_ratio_test)

##### `_ljung_box_test(self, data)`

Ljung-Box test for autocorrelation.

[View full source →](#method-statisticaltestsuite-_ljung_box_test)

##### `_durbin_watson_test(self, data)`

Durbin-Watson test for autocorrelation.

[View full source →](#method-statisticaltestsuite-_durbin_watson_test)

##### `_runs_test(self, data)`

Runs test for randomness.

[View full source →](#method-statisticaltestsuite-_runs_test)

##### `_one_sample_tests(self, data)`

One-sample statistical tests.

[View full source →](#method-statisticaltestsuite-_one_sample_tests)

##### `_two_sample_tests(self, data1, data2)`

Two-sample statistical tests.

[View full source →](#method-statisticaltestsuite-_two_sample_tests)

##### `_chi_square_goodness_of_fit(self, data, distribution)`

Chi-square goodness of fit test.

[View full source →](#method-statisticaltestsuite-_chi_square_goodness_of_fit)

##### `_ks_goodness_of_fit(self, data, distribution)`

Kolmogorov-Smirnov goodness of fit test.

[View full source →](#method-statisticaltestsuite-_ks_goodness_of_fit)

##### `_calculate_cohens_d(self, group1, group2)`

Calculate Cohen's d effect size.

[View full source →](#method-statisticaltestsuite-_calculate_cohens_d)

##### `_interpret_effect_size(self, effect_size)`

Interpret effect size magnitude.

[View full source →](#method-statisticaltestsuite-_interpret_effect_size)

##### `_interpret_durbin_watson(self, dw_stat)`

Interpret Durbin-Watson statistic.

[View full source →](#method-statisticaltestsuite-_interpret_durbin_watson)

##### `_calculate_required_sample_size(self, effect_size, power, alpha)`

Calculate required sample size for given power.

[View full source →](#method-statisticaltestsuite-_calculate_required_sample_size)

##### `_generate_validation_summary(self, results)`

Generate overall validation summary.

[View full source →](#method-statisticaltestsuite-_generate_validation_summary)

---

## Functions

### `create_statistical_test_suite(config)`

Factory function to create statistical test suite.

Parameters
----------
config : Dict[str, Any], optional
    Configuration parameters

Returns
-------
StatisticalTestSuite
    Configured statistical test suite

#### Source Code

```{literalinclude} ../../../src/analysis/validation/statistical_tests.py
:language: python
:pyobject: create_statistical_test_suite
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Dict, List, Optional, Tuple, Any, Union`
- `import numpy as np`
- `from scipy import stats`
- `import warnings`
- `from dataclasses import dataclass, field`
- `from enum import Enum`
- `from ..core.interfaces import StatisticalValidator, AnalysisResult, AnalysisStatus`
- `from ..core.data_structures import StatisticalTestResult, ConfidenceInterval`
