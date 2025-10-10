# Bug Report: [Short Description]

**Date:** YYYY-MM-DD
**Reporter:** [Name/Role]
**Severity:** [Critical/High/Medium/Low]
**Status:** [New/In Progress/Fixed/Wontfix]
**Component:** [Module/File]

## Bug Summary

**Title:** [Concise, specific title]
**Description:** [1-2 sentence overview]
**First Observed:** YYYY-MM-DD
**Affected Versions:** [Version range]

## Environment

**Operating System:** [e.g., Windows 11, Ubuntu 22.04]
**Python Version:** [e.g., 3.12.6]
**Dependencies:**
```
numpy==1.26.4
pytest==8.3.5
streamlit==1.37.1
[Other relevant packages]
```

**Hardware:**
- CPU: [e.g., Intel i7-10700K]
- RAM: [e.g., 32GB]
- GPU: [if relevant]

## Steps to Reproduce

1. [First step]
2. [Second step]
3. [Third step]
4. [Final step that triggers bug]

**Minimal Reproducible Example:**
```python
# Minimal code that reproduces the issue
import numpy as np
from src.controllers import ClassicalSMC

# Steps to reproduce
controller = ClassicalSMC(gains=[...])
result = controller.compute_control(state, last_control)
# Bug occurs here
```

## Expected Behavior

[Describe what should happen]

**Expected Output:**
```
[Show expected result]
```

## Actual Behavior

[Describe what actually happens]

**Actual Output:**
```
[Show actual result / error message]
```

**Error Traceback:**
```python
Traceback (most recent call last):
  File "...", line X, in <module>
    ...
  File "...", line Y, in function_name
    ...
TypeError: ...
```

## Analysis

### Root Cause (If Known)

[Explain the underlying cause of the bug]

**Problematic Code:**
```python
# Location: file.py:line
def problematic_function():
    # Issue: [description]
    ...
```

### Impact Assessment

**User Impact:**
- Who is affected: [Users/Developers/Deployment]
- Frequency: [Always/Sometimes/Rarely]
- Workaround available: [Yes/No]

**System Impact:**
- Performance degradation: [Yes/No]
- Data corruption risk: [Yes/No]
- Security implications: [Yes/No]

### Related Issues

- #XXX - Similar issue in different module
- #YYY - Possible duplicate
- #ZZZ - Related enhancement

## Investigation Steps Taken

1. **[Investigation 1]**
   - Approach: [What was tried]
   - Result: [What was found]

2. **[Investigation 2]**
   - Approach: [What was tried]
   - Result: [What was found]

## Proposed Solution

### Option 1: [Solution Name]

**Description:** [How to fix]

**Pros:**
- [Advantage 1]
- [Advantage 2]

**Cons:**
- [Disadvantage 1]
- [Disadvantage 2]

**Implementation:**
```python
# Proposed fix
def fixed_function():
    # Changes
    ...
```

**Effort:** [Hours/Days]

### Option 2: [Alternative Solution]

[Same structure as Option 1]

### Recommended Solution

**Choice:** Option X
**Rationale:** [Why this option is best]

## Testing Plan

### Unit Tests
```python
def test_bug_fix():
    """Verify bug is fixed."""
    # Test case
    assert expected == actual
```

### Integration Tests
- [ ] Test with controller integration
- [ ] Test with simulation runner
- [ ] Test edge cases

### Regression Tests
- [ ] Verify no existing functionality broken
- [ ] Run full test suite
- [ ] Check performance impact

## Temporary Workaround

**For Users:**
```python
# Workaround code
# Use this until fix is deployed
```

**Instructions:**
1. [Step 1]
2. [Step 2]

## Fix Implementation

**Branch:** `fix/issue-XXX-description`
**Pull Request:** #XXX
**Commits:**
- `abc123` - Fix core issue
- `def456` - Add regression tests
- `ghi789` - Update documentation

## Verification

### Pre-Fix Behavior
```bash
# Command that fails before fix
python -m pytest tests/test_bug.py
# FAILED (1 failed in 0.5s)
```

### Post-Fix Behavior
```bash
# Command that passes after fix
python -m pytest tests/test_bug.py
# PASSED (1 passed in 0.3s)
```

## Documentation Updates

- [ ] Update API documentation
- [ ] Update user guide
- [ ] Add to CHANGELOG.md
- [ ] Update migration guide (if breaking change)

## Deployment Notes

**Risk Level:** [Low/Medium/High]
**Deployment Window:** [Anytime/Scheduled maintenance]
**Rollback Plan:** [Steps to revert if needed]

**Pre-deployment Checklist:**
- [ ] All tests passing
- [ ] Code review completed
- [ ] Documentation updated
- [ ] Staging environment validated

**Post-deployment Verification:**
- [ ] Verify fix in production
- [ ] Monitor for related errors
- [ ] Notify affected users

## Lessons Learned

**Prevention:**
- [How to prevent similar bugs in future]
- [Process improvements]
- [Tool/automation suggestions]

**Detection:**
- [How to catch earlier in development]
- [Additional tests to add]
- [Monitoring improvements]

## References

- **Documentation:** [Links]
- **Related Code:** [File paths]
- **External Issues:** [GitHub/Stack Overflow links]
- **Discussions:** [Slack/Email threads]

---

**Last Updated:** YYYY-MM-DD
**Assignee:** [Name]
**Reviewer:** [Name]
**Status:** ✅ Fixed / ⚠️ In Progress / ❌ Open
