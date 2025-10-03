# interfaces.hil.test_automation

**Source:** `src\interfaces\hil\test_automation.py`

## Module Overview

Automated testing framework for HIL systems.
This module provides comprehensive test automation capabilities including
test case management, assertion validation, performance testing, and
automated report generation for control system validation.

## Complete Source Code

```{literalinclude} ../../../src/interfaces/hil/test_automation.py
:language: python
:linenos:
```

---

## Classes

### `TestStatus`

**Inherits from:** `Enum`

Test execution status enumeration.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/test_automation.py
:language: python
:pyobject: TestStatus
:linenos:
```

---

### `AssertionType`

**Inherits from:** `Enum`

Test assertion type enumeration.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/test_automation.py
:language: python
:pyobject: AssertionType
:linenos:
```

---

### `TestAssertion`

Test assertion configuration.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/test_automation.py
:language: python
:pyobject: TestAssertion
:linenos:
```

---

### `TestCase`

Individual test case configuration.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/test_automation.py
:language: python
:pyobject: TestCase
:linenos:
```

---

### `TestSuite`

Test suite containing multiple test cases.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/test_automation.py
:language: python
:pyobject: TestSuite
:linenos:
```

---

### `TestResult`

Test execution result.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/test_automation.py
:language: python
:pyobject: TestResult
:linenos:
```

---

### `HILTestFramework`

Comprehensive test automation framework for HIL systems.

Provides automated test execution, assertion validation,
performance testing, and report generation capabilities.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/test_automation.py
:language: python
:pyobject: HILTestFramework
:linenos:
```

#### Methods (19)

##### `__init__(self, hil_system, test_scenarios)`

Initialize HIL test framework.

[View full source →](#method-hiltestframework-__init__)

##### `add_test_suite(self, suite)`

Add test suite to framework.

[View full source →](#method-hiltestframework-add_test_suite)

##### `add_test_case(self, suite_name, test_case)`

Add test case to existing suite.

[View full source →](#method-hiltestframework-add_test_case)

##### `run_test_suite(self, suite_name)`

Run complete test suite.

[View full source →](#method-hiltestframework-run_test_suite)

##### `run_test_case(self, test_case)`

Run individual test case.

[View full source →](#method-hiltestframework-run_test_case)

##### `run_all_suites(self)`

Run all configured test suites.

[View full source →](#method-hiltestframework-run_all_suites)

##### `_run_sequential_tests(self, suite)`

Run test cases sequentially.

[View full source →](#method-hiltestframework-_run_sequential_tests)

##### `_run_parallel_tests(self, suite)`

Run test cases in parallel.

[View full source →](#method-hiltestframework-_run_parallel_tests)

##### `_execute_test_case(self, test_case)`

Execute individual test case logic.

[View full source →](#method-hiltestframework-_execute_test_case)

##### `_run_test_assertions(self, test_case, result)`

Run test assertions and collect results.

[View full source →](#method-hiltestframework-_run_test_assertions)

##### `_monitor_assertion(self, assertion, start_time, duration)`

Monitor and validate test assertion.

[View full source →](#method-hiltestframework-_monitor_assertion)

##### `_validate_assertion(self, assertion, actual_value)`

Validate individual assertion.

[View full source →](#method-hiltestframework-_validate_assertion)

##### `_get_signal_value(self, signal_name)`

Get current value of specified signal.

[View full source →](#method-hiltestframework-_get_signal_value)

##### `_execute_setup_commands(self, commands)`

Execute setup commands.

[View full source →](#method-hiltestframework-_execute_setup_commands)

##### `_execute_teardown_commands(self, commands)`

Execute teardown commands.

[View full source →](#method-hiltestframework-_execute_teardown_commands)

##### `_execute_command(self, command)`

Execute individual command.

[View full source →](#method-hiltestframework-_execute_command)

##### `_set_signal_value(self, signal_name, value)`

Set signal value in HIL system.

[View full source →](#method-hiltestframework-_set_signal_value)

##### `_apply_initial_conditions(self, conditions)`

Apply initial conditions for test.

[View full source →](#method-hiltestframework-_apply_initial_conditions)

##### `_apply_test_inputs(self, inputs)`

Apply test inputs.

[View full source →](#method-hiltestframework-_apply_test_inputs)

---

### `TestReportGenerator`

Generate comprehensive test reports.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/test_automation.py
:language: python
:pyobject: TestReportGenerator
:linenos:
```

#### Methods (6)

##### `__init__(self)`

[View full source →](#method-testreportgenerator-__init__)

##### `generate_comprehensive_report(self, suite_results, test_results)`

Generate comprehensive test report.

[View full source →](#method-testreportgenerator-generate_comprehensive_report)

##### `_generate_summary(self, suite_results, test_results)`

Generate test summary.

[View full source →](#method-testreportgenerator-_generate_summary)

##### `_generate_statistics(self, test_results)`

Generate test statistics.

[View full source →](#method-testreportgenerator-_generate_statistics)

##### `_generate_recommendations(self, test_results)`

Generate test recommendations.

[View full source →](#method-testreportgenerator-_generate_recommendations)

##### `_result_to_dict(self, result)`

Convert test result to dictionary.

[View full source →](#method-testreportgenerator-_result_to_dict)

---

## Dependencies

This module imports:

- `import asyncio`
- `import time`
- `import json`
- `from dataclasses import dataclass, field`
- `from typing import Dict, Any, Optional, List, Callable, Union`
- `from enum import Enum`
- `import logging`
