# CA-01: System Integration Audit

**Type**: Comprehensive Audit
**Duration**: 7 hours
**Scope**: Integration between two major components

---

## Session Prompt

```
SYSTEM INTEGRATION AUDIT
WHAT: Verify integration between [component A] and [component B]
WHY:  Ensure components work together correctly before production deployment
HOW:  Interface analysis + data flow tracing + integration testing + error handling
WIN:  Integration quality report + interface contract + comprehensive integration tests
TIME: 7 hours

TARGET COMPONENTS:
- Component A: [INSERT COMPONENT A HERE]
- Component B: [INSERT COMPONENT B HERE]

INPUTS:
- Component A code: src/[path_a]/
- Component B code: src/[path_b]/
- Integration tests: tests/test_integration/
- Expected data flow: [describe or "discover"]

ANALYSIS TASKS:
1. INTERFACE DISCOVERY (1 hour)
   - Identify all interaction points (function calls, data sharing)
   - Document function signatures
   - Extract expected input/output types
   - Map data flow (A → B, B → A)
   - Document interface contract

2. DATA FLOW ANALYSIS (1.5 hours)
   - Trace data through both components
   - Verify type consistency (A's output = B's input?)
   - Check data transformations
   - Identify potential data corruption points
   - Document data flow diagram

3. ERROR HANDLING VERIFICATION (1.5 hours)
   - What happens if A fails? Does B handle it?
   - What happens if B fails? Does A handle it?
   - Are errors propagated correctly?
   - Is cleanup performed on error?
   - Document error handling gaps

4. INTEGRATION TESTING (2 hours)
   - Review existing integration tests
   - Identify missing test scenarios
   - Write test plan for gaps
   - Execute existing tests
   - Document test coverage

5. PERFORMANCE VALIDATION (1 hour)
   - Measure integration overhead
   - Check for data bottlenecks
   - Verify no memory leaks across boundary
   - Test with realistic data volumes
   - Document performance issues

VALIDATION REQUIREMENTS:
1. Execute integration end-to-end with realistic data
2. Inject errors and verify handling (A fails, B fails)
3. Manually trace data flow for 2+ scenarios

DELIVERABLES:
1. Interface contract document (signatures, types, data flow)
2. Data flow diagram (visual representation)
3. Error handling report (gaps, recommendations)
4. Integration test plan (missing scenarios)
5. Performance validation results
6. Integration quality scorecard

SUCCESS CRITERIA:
- [ ] All interaction points documented
- [ ] Data flow traced for all scenarios
- [ ] Error handling verified (both directions)
- [ ] Integration tests executed
- [ ] Performance validated
- [ ] Test plan covers all gaps
- [ ] Can answer: "Do these components integrate correctly?"
```

---

## Example Usage

```
SYSTEM INTEGRATION AUDIT
WHAT: Verify integration between PSO optimizer and simulation runner
WHY:  Ensure components work together correctly before production deployment
HOW:  Interface analysis + data flow tracing + integration testing + error handling
WIN:  Integration quality report + interface contract + comprehensive integration tests
TIME: 7 hours

TARGET COMPONENTS:
- Component A: PSO optimizer
- Component B: Simulation runner

INPUTS:
- Component A code: src/optimizer/pso_optimizer.py
- Component B code: src/core/simulation_runner.py
- Integration tests: tests/test_integration/test_pso_simulation.py
- Expected data flow: PSO → simulation → cost → PSO

[Continue with analysis tasks...]
```

---

## Common Targets

- PSO optimizer ↔ Simulation runner
- Controller ↔ Dynamics model
- HIL plant server ↔ Controller client
- UI ↔ Simulation engine
- Monitoring ↔ Control loop
