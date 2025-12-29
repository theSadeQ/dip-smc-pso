# QA-03: Configuration Validation Audit

**Type**: Quick Audit
**Duration**: 2.5 hours
**Scope**: Single component's configuration

---

## Session Prompt

```
CONFIGURATION VALIDATION AUDIT
WHAT: Verify config.yaml completeness and correctness for [component]
WHY:  Ensure configuration has all required parameters before deployment
HOW:  Parse YAML, compare with code, test loading, check defaults
WIN:  Validated config + missing parameter list + loading test results
TIME: 2.5 hours

TARGET COMPONENT: [INSERT COMPONENT NAME HERE]

INPUTS:
- Configuration file: config.yaml
- Component code: src/[component_path]/[component_name].py
- Expected parameters: [list or "discover from code"]

ANALYSIS TASKS:
1. DISCOVER REQUIRED PARAMETERS (45 min)
   - Search code for config access (config['key'])
   - Build list of ALL parameters used
   - Identify required vs optional
   - Document default values in code

2. VERIFY config.yaml COMPLETENESS (45 min)
   - Check each required parameter exists
   - Verify data types match expectations
   - Check value ranges (min/max)
   - Document missing or incorrect params

3. TEST LOADING (30 min)
   - Load config with component
   - Test with missing optional params
   - Test with invalid values
   - Document error handling

4. CHECK DOCUMENTATION (30 min)
   - Is each parameter documented?
   - Are valid ranges specified?
   - Are defaults documented?
   - Are examples provided?

VALIDATION REQUIREMENTS:
1. Execute component with loaded config (does it work?)
2. Test with intentionally invalid config (does it fail gracefully?)
3. Cross-reference config keys with code (manual grep)

DELIVERABLES:
1. Parameter inventory (required, optional, defaults)
2. Missing parameter list (what's used in code but not in config.yaml)
3. Invalid parameter list (wrong type/range)
4. Documentation gaps list
5. Loading test results

SUCCESS CRITERIA:
- [ ] All code-accessed parameters identified
- [ ] Each parameter classified (required/optional)
- [ ] Missing parameters listed
- [ ] Loading test executed successfully
- [ ] Error handling verified
- [ ] Can answer: "Is config.yaml complete and correct?"
```

---

## Example Usage

```
CONFIGURATION VALIDATION AUDIT
WHAT: Verify config.yaml completeness and correctness for PSO optimizer
WHY:  Ensure configuration has all required parameters before deployment
HOW:  Parse YAML, compare with code, test loading, check defaults
WIN:  Validated config + missing parameter list + loading test results
TIME: 2.5 hours

TARGET COMPONENT: PSO optimizer

INPUTS:
- Configuration file: config.yaml
- Component code: src/optimizer/pso_optimizer.py
- Expected parameters: discover from code

[Continue with analysis tasks...]
```

---

## Common Targets

- PSO optimizer
- Controllers (classical_smc, sta_smc, etc.)
- Simulation runner
- HIL system
- Visualization tools
