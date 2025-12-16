# CA-02: Cross-Cutting Memory Management Audit

**Type**: Comprehensive Audit
**Duration**: 8 hours
**Scope**: Memory management across all controllers and core components

---

## Session Prompt

```
CROSS-CUTTING MEMORY MANAGEMENT AUDIT
WHAT: Verify memory management across all controllers and core components
WHY:  Ensure system is memory-safe for long-running simulations (research/production)
HOW:  Code review + leak detection + stress testing + cleanup verification
WIN:  Memory safety report + leak fixes + stress test validation
TIME: 8 hours

SCOPE: [INSERT SCOPE HERE - e.g., "all controllers" or "core simulation engine"]

INPUTS:
- Target files: src/controllers/*.py, src/core/*.py
- Test files: tests/test_integration/test_memory_management/
- Memory tools: tracemalloc, pytest-memray (if available)

ANALYSIS TASKS:
1. CODE REVIEW FOR MEMORY PATTERNS (2 hours)
   - Search for circular references
   - Verify weakref usage for callbacks
   - Check cleanup() methods exist
   - Review __del__ implementations (if any)
   - Identify potential leak sources
   - Document memory patterns (good/bad)

2. LEAK DETECTION (2 hours)
   - Run long simulation with tracemalloc
   - Monitor memory growth
   - Identify leaking objects
   - Trace leak sources to code
   - Document confirmed leaks

3. STRESS TESTING (2 hours)
   - Run 1000+ simulation cycles
   - Test all controllers
   - Monitor memory usage over time
   - Check for unbounded growth
   - Document stress test results

4. CLEANUP VERIFICATION (1.5 hours)
   - Test cleanup() methods
   - Verify object deletion
   - Check for orphaned objects
   - Test reset functionality
   - Document cleanup issues

5. FIX RECOMMENDATIONS (30 min)
   - Prioritize leaks by severity
   - Design fixes (weakref, cleanup, etc.)
   - Estimate effort per fix
   - Document fix plan

VALIDATION REQUIREMENTS:
1. Run stress test for ≥1000 cycles
2. Manually verify cleanup for 3+ components
3. Confirm leak fixes with before/after testing

DELIVERABLES:
1. Memory pattern report (good/bad patterns found)
2. Leak detection results (confirmed leaks with sources)
3. Stress test results (memory growth over time)
4. Cleanup verification results
5. Fix recommendations (prioritized, with effort)
6. Stress test validation script

SUCCESS CRITERIA:
- [ ] All target files reviewed for memory patterns
- [ ] Leak detection run for ≥1000 cycles
- [ ] All confirmed leaks documented with line numbers
- [ ] Cleanup methods tested
- [ ] Fix recommendations prioritized
- [ ] Stress test validation script committed
- [ ] Can answer: "Is the system memory-safe for long-running use?"
```

---

## Example Usage

```
CROSS-CUTTING MEMORY MANAGEMENT AUDIT
WHAT: Verify memory management across all controllers
WHY:  Ensure system is memory-safe for long-running simulations (research/production)
HOW:  Code review + leak detection + stress testing + cleanup verification
WIN:  Memory safety report + leak fixes + stress test validation
TIME: 8 hours

SCOPE: all controllers

INPUTS:
- Target files: src/controllers/*.py
- Test files: tests/test_integration/test_memory_management/
- Memory tools: tracemalloc

[Continue with analysis tasks...]
```

---

## Common Targets

- All controllers (cross-cutting)
- Core simulation engine
- Optimization subsystem
- UI/visualization components
- Full system (all components)
