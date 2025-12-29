# WORKSPACE AUDIT - QUICK REFERENCE GUIDE

**Purpose:** Fast lookup for commands, file locations, and common operations during audit cleanup

---

## FILE LOCATIONS

```
.ai_workspace/planning/workspace_audit_2025_10/
├── AUDIT_SUMMARY.md           # Executive summary, metrics, catalog
├── PHASE_1_IMMEDIATE.md       # 4 hours, CRITICAL fixes
├── PHASE_2_THIS_WEEK.md       # 6.5 hours, HIGH fixes
├── PHASE_3_THIS_MONTH.md      # 28-30 hours, MEDIUM fixes
└── QUICK_REFERENCE.md         # This file

academic/audit_cleanup/      # Generated during cleanup
├── optimization_results_analysis/
├── factory_analysis/
├── depth_analysis/
├── test_coverage/
├── phase1_validation.txt
├── phase2_validation.txt
└── phase3_validation.txt
```

---

## PHASE QUICK START

### Start Phase 1
```bash
cd D:/Projects/main
git branch audit-cleanup-backup-$(date +%Y%m%d)
git tag audit-start-$(date +%Y%m%d_%H%M%S)
# Follow: PHASE_1_IMMEDIATE.md
```

### Start Phase 2
```bash
# Verify Phase 1 complete
[ -f academic/audit_cleanup/phase1_validation.txt ] && echo "OK" || echo "ERROR"
python -m pytest tests/ -v  # Must pass
git branch phase2-backup-$(date +%Y%m%d)
# Follow: PHASE_2_THIS_WEEK.md
```

### Start Phase 3
```bash
# Verify Phases 1-2 complete
[ -f academic/audit_cleanup/phase2_validation.txt ] && echo "OK" || echo "ERROR"
python -m pytest tests/ --cov=src --cov-report=term
git branch phase3-backup-$(date +%Y%m%d)
# Follow: PHASE_3_THIS_MONTH.md
```

---

## COMMON COMMANDS

### Git Operations

```bash
# Create backup before starting
git branch audit-backup-$(date +%Y%m%d)
git tag audit-start-$(date +%Y%m%d_%H%M%S)

# Untrack gitignored files (keeps local)
git rm -r --cached logs/
git rm -r --cached academic/

# Verify files still exist locally
ls logs/ academic/

# Commit with AI footer
git commit -m "fix: Message here

Detailed description...

Related: Workspace Audit 2025-10-28, Issue C2
Refs: .ai_workspace/planning/workspace_audit_2025_10/PHASE_1_IMMEDIATE.md

[AI]"

# Push to remote (MANDATORY per CLAUDE.md §2)
git push origin main
```

### Test Operations

```bash
# Run full test suite
python -m pytest tests/ -v

# Run specific test directory
python -m pytest tests/test_controllers/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=term-missing

# Generate HTML coverage report
python -m pytest tests/ --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

### Directory Analysis

```bash
# Count root directory items
ls | wc -l  # Target: ≤19

# Find deepest directories
find src -type d | awk -F/ '{print NF-1, $0}' | sort -nr | head -10

# Find large files
find . -type f -size +1M | grep -v ".git" | grep -v "node_modules"

# List hidden directories at root
ls -d .*/ | wc -l  # Target: ≤7
```

### Documentation

```bash
# Rebuild Sphinx docs
sphinx-build -M html docs docs/_build -W --keep-going

# Check for broken links (if linkchecker installed)
linkchecker docs/_build/html/index.html

# Find legacy documentation
find docs -name "*legacy*" -o -name "*backup*"
```

---

## QUICK WINS (Copy-Paste)

### QW1: Delete Empty .benchmarks/
```bash
[ -d .benchmarks ] && [ -z "$(ls -A .benchmarks)" ] && rmdir .benchmarks && echo "OK"
```

### QW2: Remove delete_ansi.bat
```bash
git rm delete_ansi.bat
git commit -m "chore: Remove temporary ANSI fix script from root

Related: Workspace Audit 2025-10-28, Issue L3
Refs: .ai_workspace/planning/workspace_audit_2025_10/PHASE_1_IMMEDIATE.md

[AI]"
```

### QW3: Delete data/data/ Duplication
```bash
# Compare first
diff -r data/ data/data/
# If identical
rm -rf data/data/
git add data/
git commit -m "fix(data): Remove nested data/data/ duplication

Related: Workspace Audit 2025-10-28, Issue C5
Refs: .ai_workspace/planning/workspace_audit_2025_10/PHASE_1_IMMEDIATE.md

[AI]"
```

### QW4: Delete .ai_workspace/dev_tools/.ai_workspace/dev_tools/
```bash
rm -rf .ai_workspace/dev_tools/.ai_workspace/dev_tools/
echo "[OK] Deleted nested .dev_tools (gitignored, no commit needed)"
```

### QW5: Fix Root __pycache__
```bash
echo "/__pycache__/" >> .gitignore
git rm -r --cached __pycache__/ 2>/dev/null
rm -rf __pycache__/
git add .gitignore
git commit -m "fix(git): Gitignore root __pycache__ directory

Related: Workspace Audit 2025-10-28, Issue H2
Refs: .ai_workspace/planning/workspace_audit_2025_10/PHASE_1_IMMEDIATE.md

[AI]"
```

### QW6-7: Untrack Gitignored Directories
```bash
# Verify patterns exist in .gitignore
grep "^logs/$" .gitignore
grep "^\academic/$" .gitignore

# Untrack (keeps local files)
git rm -r --cached logs/ academic/

# Commit
git commit -m "fix(git): Untrack runtime-only directories (logs, artifacts)

Problem: 8.5MB tracked despite gitignore rules
Solution: Untrack using git rm --cached (local files preserved)

Related: Workspace Audit 2025-10-28, Issue C2
Refs: .ai_workspace/planning/workspace_audit_2025_10/PHASE_1_IMMEDIATE.md

[AI]"
```

---

## VALIDATION COMMANDS

### Phase 1 Validation
```bash
# All-in-one validation
cat > /tmp/validate_phase1.sh <<'EOF'
#!/bin/bash
echo "=== Phase 1 Validation ==="

echo -n "Root items: "
ls | wc -l
echo "Target: ≤19"

echo -n "Nested optimization_results: "
find optimization_results -name "optimization_results" -type d | wc -l
echo "Target: 0"

echo -n "logs/ tracked: "
git ls-files logs/ | wc -l
echo "Target: 0"

echo -n "academic/ tracked: "
git ls-files academic/ | wc -l
echo "Target: 0"

echo -n "data/data/ exists: "
[ -d data/data ] && echo "YES (BAD)" || echo "NO (GOOD)"

echo "=== Git Status ==="
git status --porcelain
EOF

bash /tmp/validate_phase1.sh
```

### Phase 2 Validation
```bash
# Check deprecation warnings
python -c "from src.optimizer import PSOTuner" 2>&1 | grep -i deprecation

# Check factory imports still work
python -c "from src.controllers.factory import create_controller; print('OK')"

# Check factory module sizes
find src/controllers/factory -name "*.py" -exec wc -l {} \;

# Run full test suite
python -m pytest tests/ -v --tb=short
```

### Phase 3 Validation
```bash
# Directory depth check
echo "Max src depth: $(find src -type d | awk -F/ '{print NF-1}' | sort -nr | head -1) (target: ≤4)"
echo "Max docs depth: $(find docs -type d | awk -F/ '{print NF-1}' | sort -nr | head -1) (target: ≤3)"

# Test coverage
python -m pytest tests/ --cov=src --cov-report=term | grep "TOTAL"

# Legacy files in docs/
find docs -name "*legacy*" -o -name "*backup*" | wc -l
echo "Target: 0"

# Full test suite
python -m pytest tests/ -v

# Documentation build
sphinx-build -M html docs docs/_build -W --keep-going
```

---

## TROUBLESHOOTING

### "git rm --cached" doesn't work
```bash
# Check if file is actually tracked
git ls-files | grep <filename>

# If not listed, already untracked
# If listed, try force:
git rm -rf --cached <path>
```

### Tests fail after refactoring
```bash
# Find import errors
python -m pytest tests/ -v 2>&1 | grep -i "importerror\|modulenotfounderror"

# Check specific import
python -c "from src.module import Class"

# Find all imports of old path
grep -rn "old.path" src/ tests/
```

### Sphinx build fails
```bash
# Check for missing files in toctree
sphinx-build -M html docs docs/_build 2>&1 | grep "toctree"

# Verify file paths
ls docs/path/to/file.md

# Update docs/index.rst with correct paths
```

### Permission denied (Windows)
```bash
# Use PowerShell with force
powershell -Command "Remove-Item -Recurse -Force directory_name"

# Or close apps with files open
# Check Task Manager for processes with locks
```

### Pre-commit hooks block commit
```bash
# Temporarily disable
git commit --no-verify -m "message"

# Or fix the issue hooks are complaining about
```

---

## COMMIT MESSAGE TEMPLATES

### Fix Commit
```
fix(scope): Brief description

Detailed explanation of what was fixed and why.

Problem:
- Description of issue

Solution:
- What was done

Impact:
- Effect of the fix

Related: Workspace Audit 2025-10-28, Issue C1 (CRITICAL)
Refs: .ai_workspace/planning/workspace_audit_2025_10/PHASE_1_IMMEDIATE.md

[AI]
```

### Refactor Commit
```
refactor(scope): Brief description

HIGH PRIORITY: One-line summary of refactor

Problem:
- What anti-pattern existed

Solution:
- How it was refactored

Testing:
- Verification that tests pass

Impact:
- Improved maintainability/performance/clarity

Related: Workspace Audit 2025-10-28, Issue H5 (HIGH)
Refs: .ai_workspace/planning/workspace_audit_2025_10/PHASE_2_THIS_WEEK.md

[AI]
```

### Docs Commit
```
docs: Brief description

Cleanup: More specific description

Changes:
- List of changes

Rationale:
- Why these changes

Related: Workspace Audit 2025-10-28, Issue M2 (MEDIUM)
Refs: .ai_workspace/planning/workspace_audit_2025_10/PHASE_3_THIS_MONTH.md

[AI]
```

---

## ROLLBACK COMMANDS

### Rollback Last Commit
```bash
git reset --soft HEAD~1  # Keep changes staged
git reset HEAD~1         # Keep changes unstaged
git reset --hard HEAD~1  # Discard changes (DANGEROUS)
```

### Rollback to Phase Start
```bash
# Phase 1
git reset --hard audit-start-*

# Phase 2
git reset --hard phase2-backup-$(date +%Y%m%d)

# Phase 3
git reset --hard phase3-backup-$(date +%Y%m%d)
```

### Restore Specific File
```bash
# From last commit
git checkout HEAD -- path/to/file

# From specific commit
git checkout <commit-hash> -- path/to/file
```

### Restore from Tar Backup
```bash
cd ..
tar -xzf main_backup_*.tar.gz -C main_restored/
cd main_restored
# Compare and cherry-pick needed files
```

---

## MEASUREMENT COMMANDS

### Count Issues Resolved
```bash
# CRITICAL issues (5 total)
echo "C1: optimization_results nesting"
[ $(find optimization_results -name "optimization_results" -type d | wc -l) -eq 0 ] && echo "✅" || echo "❌"

echo "C2: gitignore violations"
[ $(git ls-files logs/ academic/ | wc -l) -eq 0 ] && echo "✅" || echo "❌"

echo "C3: root bloat"
[ $(ls | wc -l) -le 19 ] && echo "✅" || echo "❌"

echo "C4: .dev_tools nesting"
[ ! -d .ai_workspace/dev_tools/.dev_tools ] && echo "✅" || echo "❌"

echo "C5: data/data duplication"
[ ! -d data/data ] && echo "✅" || echo "❌"
```

### Calculate Overall Score
```bash
# Scoring rubric (manual assessment)
echo "Directory Structure: X/10"
echo "Configuration: X/10"
echo "Documentation: X/10"
echo "Code Organization: X/10"
echo "Testing: X/10"
echo "Hidden Complexity: X/10"
echo "Git Hygiene: X/10"
echo "Average: X/10"
```

### Generate Metrics Report
```bash
cat > academic/audit_cleanup/metrics_report.txt <<EOF
=== Workspace Audit Metrics ===
Date: $(date +%Y-%m-%d)

Root Items: $(ls | wc -l) (target: ≤19)
Hidden Dirs: $(ls -d .*/ 2>/dev/null | wc -l) (target: ≤7)
Max Src Depth: $(find src -type d | awk -F/ '{print NF-1}' | sort -nr | head -1) (target: ≤4)
Max Docs Depth: $(find docs -type d | awk -F/ '{print NF-1}' | sort -nr | head -1) (target: ≤3)
Test/Source Ratio: $(echo "scale=1; $(find tests -name "test_*.py" | wc -l) * 100 / $(find src -name "*.py" ! -name "__init__.py" | wc -l)" | bc)% (target: 100%)
Legacy Files: $(find docs -name "*legacy*" -o -name "*backup*" | wc -l) (target: 0)

Git Status: $(git status --porcelain | wc -l) changes
Last Commit: $(git log -1 --oneline)
EOF

cat academic/audit_cleanup/metrics_report.txt
```

---

## USEFUL SHORTCUTS

### Find All Python Files
```bash
find src tests -name "*.py" ! -name "__init__.py"
```

### Find Imports of Specific Module
```bash
grep -rn "from src.optimizer" src/ tests/
```

### Count Lines in Module
```bash
wc -l src/controllers/factory.py
```

### Find Large Files
```bash
find . -type f -size +500k | grep -v ".git" | xargs ls -lh
```

### List Directory Sizes
```bash
du -sh */ | sort -h
```

### Check Gitignore Rules
```bash
git check-ignore -v path/to/file
```

---

## PHASE COMPLETION CHECKLIST

### Phase 1
- [ ] Nested directories fixed
- [ ] Gitignore violations resolved
- [ ] Quick Wins 1-7 executed
- [ ] Root items ≤25
- [ ] Validation report generated
- [ ] Committed and pushed

### Phase 2
- [ ] src/optimizer deprecated
- [ ] factory.py refactored
- [ ] CLAUDE.md updated
- [ ] All tests pass
- [ ] Migration guides created
- [ ] Committed and pushed

### Phase 3
- [ ] Directories flattened (≤4 src, ≤3 docs)
- [ ] Test coverage 100% ratio, 95%+ lines
- [ ] Legacy docs cleaned
- [ ] All tests pass
- [ ] Docs build clean
- [ ] Committed and pushed

---

## EMERGENCY CONTACTS

**Stuck?** Re-read the relevant phase prompt:
- Phase 1: `PHASE_1_IMMEDIATE.md`
- Phase 2: `PHASE_2_THIS_WEEK.md`
- Phase 3: `PHASE_3_THIS_MONTH.md`

**Need Context?** Read: `AUDIT_SUMMARY.md`

**Can't Find Something?** This file: `QUICK_REFERENCE.md`

---

**Last Updated:** 2025-10-28
**Audit Version:** 1.0
**Total Commands:** 50+
