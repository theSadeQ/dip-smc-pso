# Git Hooks for Documentation Quality

This directory contains Git hooks that enforce **CLAUDE.md Section 15: Documentation Quality Standards**.

---

## Overview

The pre-commit hook automatically scans staged markdown files in `docs/` for AI-ish language patterns before allowing commits. This ensures all documentation meets professional writing standards.

**Enforcement Policy:**
- **Threshold:** ≤5 AI-ish patterns per file
- **Action:** Commits blocked if threshold exceeded
- **Bypass:** `git commit --no-verify` (emergency only)

---

## Installation

### Option 1: Bash Script (Linux/macOS/Git Bash on Windows)

```bash
bash .dev_tools/git-hooks/install-hooks.sh
```

### Option 2: PowerShell Script (Windows)

```powershell
.\.dev_tools\git-hooks\Install-Hooks.ps1
```

### Option 3: Manual Installation

**Bash version (Git Bash/WSL):**
```bash
cp .dev_tools/git-hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

**PowerShell version (Native Windows):**
```powershell
Copy-Item .dev_tools\git-hooks\pre-commit.ps1 .git\hooks\pre-commit.ps1
```

---

## How It Works

1. **Trigger:** Runs automatically before each commit
2. **Scan:** Checks all staged markdown files in `docs/`
3. **Detection:** Uses `scripts/docs/detect_ai_patterns.py` to identify:
   - Greeting language ("Let's explore...", "Welcome!")
   - Marketing buzzwords ("comprehensive", "powerful", "seamless")
   - Hedge words ("leverage", "utilize", "delve into")
   - Unnecessary transitions ("As we can see...", "It's worth noting...")
4. **Decision:**
   - ✅ **≤5 patterns per file:** Commit approved
   - ❌ **>5 patterns per file:** Commit blocked with detailed report

---

## Example Output

### Passing Commit

```
[PRE-COMMIT] Running documentation quality checks...
[PRE-COMMIT] Checking 3 staged documentation files...
[PRE-COMMIT] Scanning: docs/user-guide/getting-started.md
[PASS] docs/user-guide/getting-started.md: No AI-ish patterns detected
[PRE-COMMIT] Scanning: docs/api/controllers.md
[WARN] docs/api/controllers.md: 2 patterns detected (acceptable: ≤5)
[PRE-COMMIT] Scanning: docs/theory/smc-foundations.md
[PASS] docs/theory/smc-foundations.md: No AI-ish patterns detected

========================================
Documentation Quality Check Summary
========================================
Files scanned: 3
Total AI-ish patterns: 2
Files exceeding threshold: 0

========================================
COMMIT APPROVED: Documentation Quality Passed
========================================
```

### Failing Commit

```
[PRE-COMMIT] Running documentation quality checks...
[PRE-COMMIT] Checking 1 staged documentation files...
[PRE-COMMIT] Scanning: docs/reports/analysis.md
[FAIL] docs/reports/analysis.md: 12 patterns detected (threshold: 5)

========================================
Documentation Quality Check Summary
========================================
Files scanned: 1
Total AI-ish patterns: 12
Files exceeding threshold: 1

========================================
COMMIT BLOCKED: Documentation Quality Failure
========================================

1 file(s) exceed the AI-ish pattern threshold (>5 patterns per file).

Please review and fix the following issues:

File: docs/reports/analysis.md
  Line 23: "Let's explore the comprehensive framework..." → "The framework provides..."
  Line 45: "You'll love how seamlessly it integrates..." → "The integration includes..."
  Line 67: "Our powerful optimizer leverages cutting-edge algorithms..." → "The optimizer uses PSO (Kennedy & Eberhart, 1995)..."

Guidance:
  1. Review CLAUDE.md Section 15: Documentation Quality Standards
  2. Consult docs/DOCUMENTATION_STYLE_GUIDE.md for professional writing guidelines
  3. Run: python scripts/docs/suggest_fixes.py --file <filename> for automated suggestions

To bypass this check (emergency only):
  git commit --no-verify
```

---

## Testing the Hook

1. **Stage a documentation file:**
   ```bash
   git add docs/user-guide/tutorial.md
   ```

2. **Attempt commit:**
   ```bash
   git commit -m "Update tutorial documentation"
   ```

3. **Review results:**
   - If patterns detected, fix issues and re-commit
   - Use `python scripts/docs/suggest_fixes.py --file docs/user-guide/tutorial.md` for suggestions

---

## Bypassing the Hook (Emergency Only)

If you must commit without quality checks (strongly discouraged):

```bash
git commit --no-verify -m "Emergency commit"
```

**Warning:** Bypassing the hook creates technical debt. Create a follow-up issue to fix documentation quality.

---

## Fixing Documentation Issues

### Quick Fixes

Use the automated fix suggestion tool:

```bash
python scripts/docs/suggest_fixes.py --file docs/path/to/file.md
```

### Manual Review

1. **Read the style guide:**
   ```bash
   cat docs/DOCUMENTATION_STYLE_GUIDE.md
   ```

2. **Review CLAUDE.md Section 15:**
   - Core writing principles
   - Anti-patterns to avoid
   - Professional writing examples

3. **Apply fixes:**
   - Remove greeting language
   - Replace marketing buzzwords with specific technical claims
   - Use direct statements instead of hedge words
   - Eliminate unnecessary transitions

---

## Troubleshooting

### Hook Not Running

**Check hook is executable:**
```bash
ls -la .git/hooks/pre-commit
# Should show: -rwxr-xr-x (executable)
```

**Make executable if needed:**
```bash
chmod +x .git/hooks/pre-commit
```

### Pattern Detection Script Not Found

**Verify script exists:**
```bash
ls scripts/docs/detect_ai_patterns.py
```

**If missing, restore from repository:**
```bash
git checkout scripts/docs/detect_ai_patterns.py
```

### Hook Runs But Doesn't Block Commits

**Check exit code:**
```bash
bash .git/hooks/pre-commit
echo $?  # Should be 1 (error) when patterns exceed threshold
```

**Verify Python script works:**
```bash
python scripts/docs/detect_ai_patterns.py --file docs/README.md
```

---

## Maintenance

### Updating the Hook

1. **Modify source:**
   Edit `.dev_tools/git-hooks/pre-commit`

2. **Reinstall:**
   ```bash
   bash .dev_tools/git-hooks/install-hooks.sh
   ```

3. **Commit changes:**
   ```bash
   git add .dev_tools/git-hooks/
   git commit -m "Update pre-commit hook"
   ```

### Disabling the Hook Temporarily

**Option 1: Rename the hook:**
```bash
mv .git/hooks/pre-commit .git/hooks/pre-commit.disabled
```

**Option 2: Use `--no-verify` flag:**
```bash
git commit --no-verify -m "Message"
```

**Re-enable:**
```bash
mv .git/hooks/pre-commit.disabled .git/hooks/pre-commit
```

---

## Integration with CLAUDE.md Section 15

This pre-commit hook enforces the documentation quality standards documented in **CLAUDE.md Section 15: Documentation Quality Standards**.

**Key Standards Enforced:**
1. **Direct, not conversational** - No "Let's", "Welcome", etc.
2. **Specific, not generic** - Metrics over buzzwords
3. **Technical, not marketing** - Facts over enthusiasm
4. **Show, don't tell** - Examples over claims
5. **Cite, don't hype** - References over superlatives

**Success Metrics:**
- AI-ish phrase frequency: <10% of October 2025 baseline
- Tone consistency: 95%+ professional
- Technical accuracy: Zero regressions
- Per-file threshold: ≤5 patterns

---

## References

- **CLAUDE.md Section 15:** Documentation Quality Standards
- **Style Guide:** `docs/DOCUMENTATION_STYLE_GUIDE.md`
- **Audit Report:** `academic/docs_audit/AI_PATTERN_AUDIT_REPORT.md`
- **Detection Tool:** `scripts/docs/detect_ai_patterns.py`
- **Fix Suggestions:** `scripts/docs/suggest_fixes.py`

---

**Maintained By:** Documentation Quality Team
**Questions:** See CLAUDE.md Section 15: Documentation Quality Standards
