# Workspace Audit 2025-10 - Comprehensive Cleanup Plan

**Status:** Planning Complete | Execution Pending
**Created:** 2025-10-28
**Overall Health:** 4.5/10 → 8.5/10 (Target)
**Total Effort:** 38-44 hours across 3 phases

---

## PURPOSE

This directory contains comprehensive prompts for executing a full workspace organizational audit and cleanup. Each file is designed to be used as a **standalone prompt for a NEW Claude session**, providing complete context and step-by-step instructions.

**Use Case:** When you hit token limits or want to break up the 40+ hour cleanup into multiple sessions, simply open the relevant phase file in a new Claude session and start working.

---

## FILES IN THIS DIRECTORY

| File | Purpose | Effort | Use When |
|------|---------|--------|----------|
| **AUDIT_SUMMARY.md** | Executive summary, metrics, issue catalog | N/A | Review overall findings |
| **PHASE_1_IMMEDIATE.md** | CRITICAL fixes (nested dirs, gitignore) | 4h | Starting cleanup |
| **PHASE_2_THIS_WEEK.md** | Code organization (refactor, deprecate) | 6.5h | After Phase 1 |
| **PHASE_3_THIS_MONTH.md** | Comprehensive cleanup (flatten, test, docs) | 28-30h | After Phase 2 |
| **QUICK_REFERENCE.md** | Commands, troubleshooting, templates | N/A | During any phase |
| **README.md** | This file | N/A | Overview |

---

## QUICK START

### Option A: Execute All Phases (Recommended)

**Timeline:** 10 days of work

1. **Day 1:** Phase 1 (4 hours focused work)
2. **Days 2-3:** Phase 2 (6.5 hours, can split)
3. **Days 4-10:** Phase 3 (30 hours over 7 days, 4-5h/day)

**Commands:**
```bash
# Start Phase 1
cd D:/Projects/main
cat .project/ai/planning/workspace_audit_2025_10/PHASE_1_IMMEDIATE.md
# Follow instructions in file

# After Phase 1 complete
cat .project/ai/planning/workspace_audit_2025_10/PHASE_2_THIS_WEEK.md
# Follow instructions

# After Phase 2 complete
cat .project/ai/planning/workspace_audit_2025_10/PHASE_3_THIS_MONTH.md
# Follow instructions
```

### Option B: Quick Wins Only (2 hours)

**For:** Immediate impact with minimal time investment

```bash
cd D:/Projects/main

# Execute Quick Wins from PHASE_1_IMMEDIATE.md section "TASK 3"
# 10 commands, 2 hours, resolves 9 issues
```

### Option C: Cherry-Pick Issues

**For:** Addressing specific problems only

1. Read `AUDIT_SUMMARY.md` - Identify your issue
2. Find relevant section in phase files
3. Execute just that task

---

## USAGE GUIDELINES

### For Claude Code (AI Assistant)

**When User Says:**
- "Continue the audit cleanup" → Read `AUDIT_SUMMARY.md` first, then relevant phase
- "Start Phase 1" → Open `PHASE_1_IMMEDIATE.md`, follow instructions
- "What's the quick reference?" → Open `QUICK_REFERENCE.md`

**Each Phase File Contains:**
- ✅ Complete context (no prior session memory needed)
- ✅ Pre-flight checklist (verify prerequisites)
- ✅ Step-by-step instructions (copy-paste commands)
- ✅ Success criteria (validation)
- ✅ Rollback procedures (safety)
- ✅ Troubleshooting (common issues)

### For Human Users

**Best Practices:**
1. **Read AUDIT_SUMMARY.md first** - Understand the full scope
2. **Check QUICK_REFERENCE.md** - Familiarize with commands
3. **Follow phases in order** - Dependencies exist between phases
4. **Create backups** - Each phase starts with backup creation
5. **Run tests frequently** - Catch issues early
6. **Commit often** - Small, focused commits better than large ones

**Time Management:**
- Phase 1: Schedule 4 continuous hours (avoid interruptions)
- Phase 2: Can be split into 2 sessions (3h + 3.5h)
- Phase 3: Break into 6 sessions (5h each over 1 week)

---

## PHASE OVERVIEW

### Phase 1: IMMEDIATE (4 hours)
**Priority:** CRITICAL
**Risk:** LOW
**Focus:** Nested directories, gitignore, root cleanup

**What Gets Fixed:**
- Recursive `optimization_results/` nesting (520KB saved)
- Gitignore violations (8.5MB untracked)
- Root directory bloat (37 → ~25 items)
- 10 Quick Wins (easy high-impact fixes)

**Outcome:** Score 4.5 → 7.0

---

### Phase 2: THIS WEEK (6.5 hours)
**Priority:** HIGH
**Risk:** MEDIUM
**Focus:** Code organization improvements

**What Gets Fixed:**
- Duplicate optimizer module (deprecated)
- God object `factory.py` (1,435 → 200-400 line modules)
- Config policy clarifications

**Outcome:** Score 7.0 → 7.5

---

### Phase 3: THIS MONTH (28-30 hours)
**Priority:** MEDIUM
**Risk:** MEDIUM-HIGH
**Focus:** Comprehensive cleanup

**What Gets Fixed:**
- Deep directory structures (6 → 4 levels)
- Test coverage (78.9% → 100% ratio, 70% → 95% lines)
- Legacy documentation (10 → 0 files)

**Outcome:** Score 7.5 → 8.5

---

## SUCCESS METRICS

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Overall Score** | **4.5/10** | **8.5/10** | **+89%** |
| CRITICAL Issues | 5 | 0 | -100% |
| HIGH Issues | 12 | 0 | -100% |
| MEDIUM Issues | 8 | 0 | -100% |
| Root Items | 37 | ≤19 | -48% |
| Test Coverage | 70% | 95%+ | +36% |
| Max Depth (src) | 6 | 4 | -33% |

---

## DEPENDENCIES

### Phase Dependencies
```
Phase 1 (CRITICAL)
    ↓
Phase 2 (HIGH) - Requires Phase 1 complete
    ↓
Phase 3 (MEDIUM) - Requires Phases 1+2 complete
```

### Technical Dependencies
- **Git:** Clean working tree before each phase
- **Tests:** Full suite must pass before starting phases 2-3
- **Python:** 3.9+ environment with all dependencies installed
- **Tools:** pytest, sphinx-build, tar (for backups)

---

## RISK MITIGATION

### Backup Strategy
Every phase starts with:
```bash
git branch phase-backup-$(date +%Y%m%d)
git tag phase-start-$(date +%Y%m%d_%H%M%S)
tar -czf ../main_backup_$(date +%Y%m%d_%H%M%S).tar.gz .
```

### Rollback Procedures
- **Single Task:** `git reset HEAD~1`
- **Entire Phase:** `git reset --hard phase-backup-*`
- **Complete Rollback:** `git reset --hard audit-start-*`
- **File Restore:** Extract from tar backup

### Testing Strategy
- Run full test suite between major tasks
- Commit frequently (small, focused commits)
- Validate after each phase completion

---

## ANTI-PATTERN CATALOG

**Total Issues:** 41

**By Severity:**
- 5 CRITICAL (Phase 1)
- 12 HIGH (Phase 2)
- 8 MEDIUM (Phase 3)
- 6 LOW (Phase 3)

**By Category:**
- Directory structure: 12 issues
- Code organization: 7 issues
- Documentation: 8 issues
- Configuration: 5 issues
- Testing: 4 issues
- Git hygiene: 5 issues

**See AUDIT_SUMMARY.md for complete catalog**

---

## FREQUENTLY ASKED QUESTIONS

### Q: Can I skip phases?
**A:** Not recommended. Phases have dependencies:
- Phase 2 assumes Phase 1 cleanup (clean root, fixed gitignore)
- Phase 3 assumes Phase 2 refactoring (factory split, flattened imports)

### Q: What if I only have 2 hours?
**A:** Execute Quick Wins from Phase 1 (section "TASK 3"). Resolves 9 issues in 2 hours.

### Q: Can I do Phase 3 tasks out of order?
**A:** Yes! Phase 3 tasks are mostly independent:
- Task 1 (flatten dirs) - 6-8h
- Task 2 (test coverage) - 20h (can split into 4x5h sessions)
- Task 3 (docs cleanup) - 2h

### Q: What if tests fail during cleanup?
**A:** Stop immediately. Rollback last change:
```bash
git reset --hard HEAD~1
```
Review phase instructions and troubleshooting section.

### Q: How do I verify phases are complete?
**A:** Each phase ends with "POST-PHASE VALIDATION" section. Run those commands.

### Q: Can I use these prompts in future audits?
**A:** Yes! Update dates/issue numbers, but structure is reusable.

---

## TROUBLESHOOTING

### "I'm stuck on a task"
1. Check phase's Troubleshooting section
2. Consult `QUICK_REFERENCE.md`
3. Rollback and try alternative approach

### "Tests are failing"
1. Read error messages carefully
2. Check for import path changes
3. Verify test files weren't accidentally deleted
4. Run single test file to isolate issue: `pytest tests/test_foo.py -v`

### "Git won't let me commit"
1. Check pre-commit hooks: `cat .git/hooks/pre-commit`
2. Temporarily bypass: `git commit --no-verify -m "message"`
3. Fix underlying issue hooks detected

### "I need to pause mid-phase"
1. Commit current work (even if task incomplete)
2. Note where you stopped in commit message
3. Push to remote to save state
4. Resume later from that commit

---

## POST-AUDIT MAINTENANCE

### Quarterly Health Check (15 min)
```bash
# Run workspace health check
python scripts/check_workspace_health.py  # If exists

# Or manual checks
ls | wc -l  # ≤19
find src -type d | awk -F/ '{print NF-1}' | sort -nr | head -1  # ≤4
pytest --cov=src | grep TOTAL  # ≥95%
```

### Prevention (CI/CD)
Consider adding workspace health checks to CI:
- Root item count enforcement
- Directory depth limits
- Test coverage requirements

See `AUDIT_SUMMARY.md` section "POST-AUDIT MAINTENANCE" for CI example.

---

## RELATED DOCUMENTATION

- **CLAUDE.md §14:** Workspace organization rules
- **Testing Standards:** `.project/ai/config/testing_standards.md`
- **Repository Management:** `.project/ai/config/repository_management.md`
- **Agent Orchestration:** `.project/ai/config/agent_orchestration.md`

---

## VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-28 | Initial audit and planning documentation |

---

## FEEDBACK & IMPROVEMENTS

**Found Issues?** Update the relevant phase file and commit changes.

**Suggestions?** Add to lessons learned after audit completion:
- `.project/ai/lessons_learned/workspace_audit_2025_10.md`

**Reusable Insights?** Extract to:
- `.project/ai/config/workspace_organization.md`

---

**Remember:** These are comprehensive guides designed for NEW Claude sessions with no prior context. Each phase file is complete and self-contained.

**Good luck with the cleanup!** 🚀
