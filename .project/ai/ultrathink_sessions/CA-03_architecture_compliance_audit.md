# CA-03: Architecture Compliance Audit

**Type**: Comprehensive Audit
**Duration**: 8 hours
**Scope**: Codebase architectural integrity

---

## Session Prompt

```
ARCHITECTURE COMPLIANCE AUDIT
WHAT: Verify codebase adheres to documented architecture in docs/architecture/
WHY:  Ensure architectural integrity before major refactor or publication
HOW:  Compare code with architecture docs + check dependencies + verify patterns
WIN:  Compliance report + architectural drift analysis + alignment recommendations
TIME: 8 hours

SCOPE: [INSERT SCOPE HERE - e.g., "full codebase" or "controllers + core"]

INPUTS:
- Architecture docs: docs/architecture/*.md
- Source code: src/
- Expected patterns: [list or "discover from docs"]

ANALYSIS TASKS:
1. DOCUMENT ARCHITECTURE EXPECTATIONS (1 hour)
   - Read all architecture docs
   - Extract expected patterns (factories, interfaces, etc.)
   - List expected module structure
   - Document expected dependencies
   - Create architecture checklist

2. MODULE STRUCTURE VERIFICATION (1.5 hours)
   - Compare src/ structure with architecture docs
   - Check for missing/unexpected modules
   - Verify file organization
   - Document structure deviations

3. PATTERN COMPLIANCE CHECK (2 hours)
   - Factory pattern: used correctly?
   - Interface pattern: base classes followed?
   - Dependency injection: used where expected?
   - Separation of concerns: violated anywhere?
   - Document pattern violations

4. DEPENDENCY ANALYSIS (2 hours)
   - Map actual dependencies (imports)
   - Compare with expected dependencies
   - Identify circular dependencies
   - Check for inappropriate coupling
   - Visualize dependency graph
   - Document dependency issues

5. DRIFT ANALYSIS (1 hour)
   - What has diverged from architecture?
   - Why did it diverge? (intentional or accidental?)
   - What is impact of drift?
   - Document architectural drift

6. ALIGNMENT RECOMMENDATIONS (30 min)
   - How to bring code into compliance?
   - Or update architecture docs?
   - Prioritize by impact
   - Estimate effort
   - Document recommendations

VALIDATION REQUIREMENTS:
1. Manually verify dependency map for 3+ modules
2. Cross-check pattern usage with code review
3. Confirm architectural expectations with docs (not assumptions)

DELIVERABLES:
1. Architecture expectations checklist (from docs)
2. Module structure compliance report
3. Pattern compliance report (violations with examples)
4. Dependency graph (actual vs expected)
5. Architectural drift analysis
6. Alignment recommendations (prioritized, with effort)

SUCCESS CRITERIA:
- [ ] All architecture docs read and expectations extracted
- [ ] Module structure compared with expectations
- [ ] Patterns verified across codebase
- [ ] Dependency graph generated and analyzed
- [ ] Drift documented with root causes
- [ ] Recommendations prioritized
- [ ] Can answer: "Does the code match the architecture?"
```

---

## Example Usage

```
ARCHITECTURE COMPLIANCE AUDIT
WHAT: Verify codebase adheres to documented architecture in docs/architecture/
WHY:  Ensure architectural integrity before major refactor or publication
HOW:  Compare code with architecture docs + check dependencies + verify patterns
WIN:  Compliance report + architectural drift analysis + alignment recommendations
TIME: 8 hours

SCOPE: full codebase

INPUTS:
- Architecture docs: docs/architecture/*.md
- Source code: src/
- Expected patterns: discover from docs

[Continue with analysis tasks...]
```

---

## Common Targets

- Full codebase (comprehensive)
- Controllers module
- Core simulation engine
- Optimization subsystem
- UI/HIL components
