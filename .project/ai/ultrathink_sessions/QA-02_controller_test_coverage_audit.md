# QA-02: Controller Test Coverage Audit

**Type**: Quick Audit
**Duration**: 3 hours
**Scope**: Single controller and its tests

---

## Session Prompt

```
CONTROLLER TEST COVERAGE AUDIT
WHAT: Analyze test coverage for [controller_name] controller
WHY:  Ensure controller meets 95% coverage standard before research deployment
HOW:  Run pytest-cov, analyze coverage report, identify untested code paths
WIN:  Coverage report + specific tests needed to reach 95%
TIME: 3 hours

TARGET CONTROLLER: [INSERT CONTROLLER NAME HERE]

INPUTS:
- Controller file: src/controllers/[controller_name].py
- Test file: tests/test_controllers/test_[controller_name].py
- Coverage threshold: 95%

ANALYSIS TASKS:
1. RUN COVERAGE (30 min)
   - Execute: python -m pytest tests/test_controllers/test_[controller_name].py --cov=src/controllers/[controller_name] --cov-report=html
   - Document current coverage %
   - Identify uncovered lines
   - Save HTML report

2. ANALYZE GAPS (1 hour)
   - What code paths are untested?
   - Are edge cases covered?
   - Are error conditions tested?
   - Is cleanup/reset tested?
   - Document specific missing tests

3. DESIGN TESTS (1 hour)
   - Write test plan for each gap
   - Specify inputs, expected outputs
   - Estimate effort per test
   - Prioritize by risk/complexity

4. VALIDATE EXISTING TESTS (30 min)
   - Do tests actually verify behavior?
   - Are assertions meaningful?
   - Is test data realistic?
   - Are tests isolated/independent?

VALIDATION REQUIREMENTS:
1. Manually review all uncovered lines (not just count)
2. Verify coverage report matches manual inspection
3. Ensure test plan covers ALL uncovered code paths

DELIVERABLES:
1. Coverage report (current % + gaps)
2. Test plan (specific tests needed)
3. Effort estimate to reach 95%
4. Risk assessment (what breaks if gaps not fixed)

SUCCESS CRITERIA:
- [ ] Coverage % documented
- [ ] All uncovered lines listed with line numbers
- [ ] Test plan covers 100% of gaps
- [ ] Each test has input/output specification
- [ ] Effort estimated (hours)
- [ ] Can answer: "What tests are needed for 95%?"
```

---

## Example Usage

```
CONTROLLER TEST COVERAGE AUDIT
WHAT: Analyze test coverage for adaptive_smc controller
WHY:  Ensure controller meets 95% coverage standard before research deployment
HOW:  Run pytest-cov, analyze coverage report, identify untested code paths
WIN:  Coverage report + specific tests needed to reach 95%
TIME: 3 hours

TARGET CONTROLLER: adaptive_smc

INPUTS:
- Controller file: src/controllers/adaptive_smc.py
- Test file: tests/test_controllers/test_adaptive_smc.py
- Coverage threshold: 95%

[Continue with analysis tasks...]
```

---

## Common Targets

- classical_smc
- sta_smc
- adaptive_smc
- hybrid_adaptive_sta_smc
- swing_up_smc
- mpc_controller
