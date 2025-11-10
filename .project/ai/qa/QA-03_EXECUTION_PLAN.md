# QA-03 Execution Plan: Dynamics Model Configuration Audit

**Date**: November 10, 2025
**Target Component**: Dynamics Models (DIPDynamics vs SimplifiedDIPDynamics)
**Auditor**: Claude Code
**Duration**: 2.5 hours
**Priority**: CRITICAL (Recent PSO failure due to model mismatch)

---

## Rationale

**Why Dynamics Configuration?**

Recent Phase 4.1 PSO investigation revealed:
- MT-8 gains optimized for `DIPDynamics` (full model)
- Phase 4.1 PSO used `SimplifiedDIPDynamics`
- Result: 750/750 simulations diverged (100% failure rate)
- **Root cause**: Configuration did not enforce/validate dynamics model consistency

**Audit Objective:**

Ensure config.yaml explicitly specifies which dynamics model to use and validates consistency across all optimization/simulation workflows.

---

## Customized QA-03 Prompt

```
CONFIGURATION VALIDATION AUDIT
WHAT: Verify config.yaml dynamics model specification and validation
WHY:  Prevent dynamics model mismatches (MT-8 used DIPDynamics, Phase4.1 used SimplifiedDIPDynamics)
HOW:  Parse config.yaml, search all code for dynamics instantiation, test validation
WIN:  Validated dynamics config + model consistency checker + usage report
TIME: 2.5 hours

TARGET COMPONENT: Dynamics Models (DIPDynamics, SimplifiedDIPDynamics)

CONTEXT:
- Recent failure: MT-8 ROBUST_GAINS [10.149, 12.839, 6.815, 2.75] optimized for DIPDynamics
- Phase 4.1 PSO applied these gains to SimplifiedDIPDynamics
- Result: 750/750 simulations diverged at t≈3.9s
- Lesson: Configuration must prevent model/gains mismatches

INPUTS:
- Configuration file: config.yaml
- Full dynamics: src/core/dynamics.py (DIPDynamics)
- Simplified dynamics: src/plant/models/simplified/dynamics.py (SimplifiedDIPDynamics)
- Optimization scripts: scripts/mt8_*.py, scripts/research/phase4_1_*.py
- Expected parameters: dynamics_model, physics parameters

ANALYSIS TASKS:

1. DISCOVER DYNAMICS USAGE (45 min)
   - Search all Python files for DIPDynamics imports
   - Search all Python files for SimplifiedDIPDynamics imports
   - Identify which scripts use which models
   - Document model switching patterns
   - Key files to check:
     * simulate.py
     * scripts/mt8_robust_pso.py (uses DIPDynamics)
     * scripts/research/phase4_1_optimize_s_based_thresholds.py (uses SimplifiedDIPDynamics)
     * src/core/simulation_runner.py
     * streamlit_app.py

2. VERIFY config.yaml COMPLETENESS (45 min)
   - Check if dynamics_model is specified in config.yaml
   - Verify physics parameters (m1, m2, M, L1, L2, g) completeness
   - Check if model choice is validated on load
   - Document missing dynamics model specification
   - Verify gain-to-model linkage (are optimized gains tagged with model?)

3. TEST LOADING & VALIDATION (30 min)
   - Load config.yaml with load_config()
   - Check if dynamics model can be auto-detected
   - Test with missing dynamics_model field
   - Test with invalid model name
   - Document error handling (does it fail gracefully?)

4. CHECK DOCUMENTATION & CONSISTENCY (30 min)
   - Is dynamics model documented in config.yaml comments?
   - Are model differences explained anywhere?
   - Is there a model selection guide?
   - Check optimization_results/*.json for model metadata
   - Verify MT-8 gains JSON files include model tag

CRITICAL QUESTIONS TO ANSWER:
1. Does config.yaml specify which dynamics model to use?
2. Can users accidentally mix models and gains?
3. Do optimized gain files (.json) include model provenance?
4. Is there validation that prevents model mismatches?
5. Are model differences documented for users?

VALIDATION REQUIREMENTS:
1. Grep all scripts for dynamics model instantiation
2. Check if config.yaml has dynamics_model field
3. Test loading config with/without model specification
4. Verify MT-8 gain files include model metadata
5. Manual test: Can you load SimplifiedDIPDynamics with DIPDynamics config?

DELIVERABLES:
1. **Dynamics Usage Report**
   - List of all files using DIPDynamics
   - List of all files using SimplifiedDIPDynamics
   - Model usage patterns by script type

2. **Configuration Gap Analysis**
   - Does config.yaml have dynamics_model field? (Expected: NO)
   - Are physics params complete? (Expected: YES)
   - Is model validated on load? (Expected: NO)

3. **Model Metadata Audit**
   - Do optimization_results/*.json files tag model used? (Check MT-8 files)
   - Can gains be traced back to their optimization model?

4. **Validation Script** (if gaps found)
   - Script to check model/gains consistency
   - Add to pre-PSO checklist

5. **Recommendation Report**
   - Add dynamics_model to config.yaml (values: "full", "simplified")
   - Add model validation in load_config()
   - Tag all optimized gain files with model provenance
   - Add model consistency checker script

SUCCESS CRITERIA:
- [x] All dynamics instantiations mapped
- [x] config.yaml dynamics model field assessed
- [x] Model metadata in gain files checked
- [x] Validation gaps documented
- [ ] Recommendation report written
- [ ] Can answer: "How do we prevent future model mismatches?"

EXPECTED FINDINGS:
Based on recent investigation:
- Config.yaml likely DOES NOT specify dynamics model
- MT-8 gain files likely DO NOT include model metadata
- No validation prevents mixing SimplifiedDIPDynamics with DIPDynamics gains
- Documentation does NOT explain model differences

IMPACT:
This audit addresses the root cause of 750 PSO simulation failures.
Implementing recommendations will prevent similar incidents.
```

---

## Execution Steps

### Phase 1: Discovery (45 min)

1. **Search for dynamics imports:**
   ```bash
   grep -r "from src.core.dynamics import" --include="*.py"
   grep -r "from src.plant.models.simplified.dynamics import" --include="*.py"
   ```

2. **Identify model usage patterns:**
   - MT-8 scripts → DIPDynamics
   - Phase 4.1 scripts → SimplifiedDIPDynamics
   - Main simulate.py → Which model?
   - Streamlit app → Which model?

### Phase 2: Config Analysis (45 min)

1. **Check config.yaml structure:**
   - Search for "dynamics" or "model" fields
   - Verify physics section completeness
   - Check for model selection mechanism

2. **Analyze load_config():**
   - Does it validate dynamics model?
   - Does it provide defaults?
   - Does it enforce consistency?

### Phase 3: Testing (30 min)

1. **Load config and test:**
   ```python
   from src.config import load_config
   config = load_config()
   # Does config.dynamics_model exist?
   # Can we load wrong model?
   ```

2. **Check gain file metadata:**
   ```bash
   cat optimization_results/mt8_robust_hybrid_adaptive_sta_smc.json
   # Does it specify DIPDynamics?
   ```

### Phase 4: Recommendations (30 min)

1. **Write recommendation report**
2. **Draft config.yaml additions**
3. **Outline validation script**

---

## Expected Deliverables

1. **D:\Projects\main\.project\ai\qa\QA-03_DYNAMICS_CONFIG_AUDIT_REPORT.md**
   - Dynamics usage inventory
   - Configuration gap analysis
   - Model metadata audit results
   - Specific recommendations

2. **D:\Projects\main\.project\ai\qa\proposed_config_additions.yaml**
   - Proposed dynamics_model field
   - Model selection documentation

3. **D:\Projects\main\scripts\validate_model_consistency.py** (if needed)
   - Script to verify model/gains compatibility
   - Check before running PSO

---

## Timeline

- **Total:** 2.5 hours
- **Discovery:** 45 min (dynamics usage mapping)
- **Config Analysis:** 45 min (config.yaml + load_config review)
- **Testing:** 30 min (load testing + metadata check)
- **Recommendations:** 30 min (report writing)

---

## Success Definition

**PASS Criteria:**
- All dynamics instantiations documented
- Configuration gaps identified
- Specific, actionable recommendations provided
- Can answer: "How do we prevent model mismatches?"

**Bonus:**
- Validation script created
- Config.yaml updated with model field
- Gain files updated with model metadata

---

## Why This Matters

This audit addresses the **exact failure mode** that caused 750 PSO simulations to diverge:
- Gains optimized for Model A
- Applied to Model B
- 100% failure rate

Preventing this in the future is CRITICAL for:
- Research reproducibility
- User trust in optimization results
- Avoiding wasted compute time
- Publication credibility

---

**Ready to execute:** Awaiting user approval to begin QA-03 audit.
