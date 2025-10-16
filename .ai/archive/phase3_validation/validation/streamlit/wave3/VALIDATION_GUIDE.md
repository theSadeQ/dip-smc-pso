# Wave 3 Streamlit Theme Parity - Validation Execution Guide

**Purpose**: Complete validation workflow for verifying Streamlit theme implementation matches Sphinx documentation design system.

**Date**: 2025-10-16
**Wave**: Phase 3 Wave 3 - Streamlit Theme Parity

---

## Prerequisites

### 1. Environment Setup

**Required Python packages:**
```bash
pip install streamlit playwright pillow numpy pandas
python -m playwright install chromium
```

**Verify installations:**
```bash
python -c "import streamlit; print(f'Streamlit: {streamlit.__version__}')"
python -c "import playwright; print('Playwright: OK')"
python -c "from PIL import Image; print('Pillow: OK')"
python -c "import pandas; print(f'Pandas: {pandas.__version__}')"
```

### 2. Design Tokens

**Verify design tokens file exists:**
```bash
ls -lh .codex/phase2_audit/design_tokens_v2.json
```

**Expected location:** `.codex/phase2_audit/design_tokens_v2.json`

If missing, contact maintainer or check Phase 2 documentation.

### 3. Streamlit Configuration

**Verify config.yaml has streamlit section:**
```yaml
streamlit:
  enable_dip_theme: true  # For themed captures
  theme_version: "2.0.0"
```

---

## Validation Workflow

### Complete Pipeline (Estimated: 25-30 minutes)

```
1. Token Mapping (2 min)
   ↓
2. Baseline Screenshots (5 min)
   ↓
3. Themed Screenshots (5 min)
   ↓
4. Visual Regression Analysis (3 min)
   ↓
5. Accessibility Audit (5 min)
   ↓
6. Performance Measurement (2 min)
   ↓
7. Comparison Analysis (3 min)
   ↓
8. Review Reports
```

---

## Step-by-Step Execution

### Step 1: Token Mapping Generation (2 min)

**Purpose**: Generate CSV mapping of design tokens to CSS variables and Streamlit widgets.

**Command:**
```bash
cd .codex/phase3/validation/streamlit
python generate_token_mapping.py
```

**Expected Output:**
```
[OK] Token mapping generated: 18 tokens
[OK] Saved: wave3/token_mapping.csv
```

**Verify:**
```bash
cat wave3/token_mapping.csv | wc -l
# Expected: 19 lines (18 tokens + 1 header)
```

**Troubleshooting:**
- **Error: "Design tokens not found"**
  Solution: Verify `.codex/phase2_audit/design_tokens_v2.json` exists
- **Error: "pandas not installed"**
  Solution: `pip install pandas`

---

### Step 2: Baseline Screenshots (5 min)

**Purpose**: Capture screenshots with theme DISABLED for comparison baseline.

**1. Disable theme in config.yaml:**
```yaml
streamlit:
  enable_dip_theme: false  # CRITICAL: Must be false for baseline
```

**2. Start Streamlit:**
```bash
streamlit run streamlit_app.py
```

**3. Wait for app to load:**
- Open browser to http://localhost:8501
- Verify dashboard displays correctly
- Ensure no errors in terminal

**4. Run capture script:**
```bash
# In NEW terminal (keep Streamlit running)
cd .codex/phase3/validation/streamlit
python wave3_screenshot_capture.py baseline
```

**Expected Output:**
```
[1/7] Capturing homepage...
  [OK] Saved: 01_homepage.png
[2/7] Capturing sidebar...
  [OK] Saved: 02_sidebar.png
[3/7] Capturing button states...
  [OK] Saved: 03_button_normal.png
  [OK] Saved: 04_button_hover.png
  [OK] Saved: 05_button_focus.png
...
[SUCCESS] All screenshots captured successfully
```

**Verify:**
```bash
ls -lh wave3/baseline/*.png
# Expected: 9 PNG files (01-09)
```

**Troubleshooting:**
- **Error: "Cannot connect to localhost:8501"**
  Solution: Ensure Streamlit is running in separate terminal
- **Error: "stAppViewContainer not found"**
  Solution: Wait longer for Streamlit to fully load (increase timeout)
- **[WARN] Button not found**
  Solution: Acceptable if dashboard has no buttons on homepage

**5. Stop Streamlit** (Ctrl+C in Streamlit terminal)

---

### Step 3: Themed Screenshots (5 min)

**Purpose**: Capture screenshots with theme ENABLED for comparison.

**1. Enable theme in config.yaml:**
```yaml
streamlit:
  enable_dip_theme: true  # CRITICAL: Must be true for themed
```

**2. Start Streamlit:**
```bash
streamlit run streamlit_app.py
```

**3. Verify theme applied:**
- Open browser to http://localhost:8501
- Check if buttons have custom styling (blue primary color)
- Check if sidebar has custom background
- Verify no console errors

**4. Run capture script:**
```bash
# In NEW terminal (keep Streamlit running)
cd .codex/phase3/validation/streamlit
python wave3_screenshot_capture.py themed
```

**Expected Output:**
```
[1/7] Capturing homepage...
  [OK] Saved: 01_homepage.png
...
[SUCCESS] All screenshots captured successfully
```

**Verify:**
```bash
ls -lh wave3/themed/*.png
# Expected: 9 PNG files (01-09)
diff <(ls wave3/baseline/) <(ls wave3/themed/)
# Expected: No differences (same filenames)
```

**Troubleshooting:**
- **Theme not visible**
  Solution: Hard refresh browser (Ctrl+Shift+R) to clear cached CSS
- **Error: "CSS variable not defined"**
  Solution: Check `src/utils/streamlit_theme.py` for syntax errors

**KEEP STREAMLIT RUNNING** for Steps 5 (Accessibility Audit)

---

### Step 4: Visual Regression Analysis (3 min)

**Purpose**: Compare baseline vs themed screenshots, calculate pixel differences.

**Command:**
```bash
cd .codex/phase3/validation/streamlit
python wave3_visual_regression.py
```

**Expected Output:**
```
Comparing: 01_homepage.png... [MODERATE] 12.34% difference
Comparing: 02_sidebar.png... [MODERATE] 15.67% difference
Comparing: 03_button_normal.png... [SIGNIFICANT] 28.90% difference
...
[SUCCESS] All comparisons completed
```

**Exit Criteria:**
- **PASS**: 0 extreme changes (>50%)
- **WARN**: 1-3 significant changes (20-50%) - acceptable for theme
- **FAIL**: Any extreme changes - layout may be broken

**Verify:**
```bash
cat wave3/visual_regression_report.json | grep extreme_changes
# Expected: "extreme_changes": 0

ls wave3/diffs/
# Expected: 9 diff_*.png files (visual diff images)
```

**Troubleshooting:**
- **Error: "Themed version not found"**
  Solution: Ensure Step 3 completed successfully
- **Error: "Image size mismatch"**
  Solution: Baseline and themed must be same viewport (1280x800)

**Review Detailed Report:**
```bash
cat wave3/visual_regression_summary.md
```

---

### Step 5: Accessibility Audit (5 min)

**Purpose**: Validate WCAG AA compliance using axe-core.

**Prerequisites:**
- Streamlit MUST be running on http://localhost:8501
- Theme MUST be enabled (from Step 3)

**Command:**
```bash
cd .codex/phase3/validation/streamlit
python wave3_axe_audit.py
```

**Expected Output:**
```
Running accessibility scan...
[OK] Scan complete

Violations by severity:
  Critical: 0
  Serious:  0
  Moderate: 2
  Minor:    1
  Total:    3

[PASS] Validation PASSED: WCAG AA compliance met
```

**Exit Criteria:**
- **PASS**: 0 critical AND 0 serious violations
- **FAIL**: Any critical or serious violations

**Verify:**
```bash
cat wave3/axe_audit_report.json | grep -A5 summary
# Expected: "critical_violations": 0, "serious_violations": 0
```

**Troubleshooting:**
- **Error: "Cannot connect to localhost:8501"**
  Solution: Ensure Streamlit is still running from Step 3
- **[FAIL] Critical violations found**
  Solution: Review `wave3/axe_audit_report.json` for specific issues
  - Common: color-contrast issues
  - Fix: Adjust colors in `.codex/phase2_audit/design_tokens_v2.json`

**Review Detailed Report:**
```bash
cat wave3/axe_audit_summary.md
```

**Stop Streamlit** (Ctrl+C) after this step.

---

### Step 6: Performance Measurement (2 min)

**Purpose**: Measure CSS size and verify <3KB gzipped budget.

**Command:**
```bash
cd .codex/phase3/validation/streamlit
python wave3_performance.py
```

**Expected Output:**
```
[1/1] Measuring CSS size...
[OK] CSS Size Measured:
  Uncompressed: 4521 bytes (4.41 KB)
  Gzipped:      1834 bytes (1.79 KB)
  Compression:  2.46x
  Target:       3072 bytes (3 KB)
  Status:       PASS ✓

[PASS] CSS size validation PASSED
```

**Exit Criteria:**
- **PASS**: Gzipped size <3072 bytes (3 KB)
- **FAIL**: Gzipped size ≥3072 bytes

**Verify:**
```bash
cat wave3/performance_metrics.json | grep gzipped_kb
# Expected: "gzipped_kb": <3.0
```

**Troubleshooting:**
- **Error: "Design tokens not found"**
  Solution: Verify `.codex/phase2_audit/design_tokens_v2.json` exists
- **[FAIL] CSS exceeds 3KB**
  Solution: Optimize CSS in `src/utils/streamlit_theme.py`
  - Remove unused selectors
  - Combine duplicate rules
  - Use CSS minification

**Review Detailed Report:**
```bash
cat wave3/performance_summary.md
```

---

### Step 7: Comparison Analysis (3 min)

**Purpose**: Aggregate all validation results into comprehensive pass/fail report.

**Command:**
```bash
cd .codex/phase3/validation/streamlit
python wave3_comparison_analysis.py
```

**Expected Output:**
```
[1/4] Loading token mapping results...
  Status: success
  Total tokens: 18
  Result: PASS ✓

[2/4] Loading visual regression results...
  Status: success
  Extreme changes: 0
  Result: PASS ✓

[3/4] Loading accessibility audit results...
  Status: success
  Critical: 0
  Serious: 0
  Result: PASS ✓

[4/4] Loading performance metrics...
  Status: success
  CSS size: 1.79 KB gzipped
  Result: PASS ✓

[SUCCESS] All validation checks passed!
Overall Status: PASSED ✓
Tests Passed: 4/4
```

**Exit Criteria:**
- **PASS**: All 4 validation categories pass
- **FAIL**: Any category fails

**Verify:**
```bash
cat wave3/validation_results.json | grep overall_pass
# Expected: "overall_pass": true
```

**Review Comprehensive Summary:**
```bash
cat wave3/VALIDATION_SUMMARY.md
```

**Troubleshooting:**
- **Error: "File not found"**
  Solution: Ensure all previous steps completed successfully
- **[FAIL] Some tests failed**
  Solution: Review `VALIDATION_SUMMARY.md` for specific failures and remediation steps

---

## Output Directory Structure

After complete execution:

```
wave3/
├── token_mapping.csv              # Step 1: Token-to-widget mapping
├── baseline/                      # Step 2: Theme disabled screenshots
│   ├── 01_homepage.png
│   ├── 02_sidebar.png
│   └── ... (9 total)
├── themed/                        # Step 3: Theme enabled screenshots
│   ├── 01_homepage.png
│   ├── 02_sidebar.png
│   └── ... (9 total)
├── diffs/                         # Step 4: Visual diff images
│   ├── diff_01_homepage.png
│   └── ... (9 total)
├── visual_regression_report.json  # Step 4: Pixel difference data
├── visual_regression_summary.md   # Step 4: Human-readable report
├── axe_audit_report.json          # Step 5: Accessibility violations
├── axe_audit_summary.md           # Step 5: Human-readable report
├── performance_metrics.json       # Step 6: CSS size data
├── performance_summary.md         # Step 6: Human-readable report
├── validation_results.json        # Step 7: Aggregated results
├── VALIDATION_SUMMARY.md          # Step 7: Comprehensive report
└── VALIDATION_GUIDE.md            # This file
```

---

## Interpreting Results

### Visual Regression Assessment Levels

| Level | Diff % | Meaning | Action |
|-------|--------|---------|--------|
| **MINIMAL** | <5% | Negligible changes | OK - Expected for minor styling |
| **MODERATE** | 5-20% | Expected theme changes | OK - Verify visually correct |
| **SIGNIFICANT** | 20-50% | Large style changes | WARN - Review diff images |
| **EXTREME** | >50% | Possibly broken | FAIL - Fix layout issues |

### Accessibility Violation Severity

| Severity | Impact | Action Required |
|----------|--------|----------------|
| **Critical** | Blocks users with disabilities | MUST FIX before deployment |
| **Serious** | Significant barrier | MUST FIX before deployment |
| **Moderate** | Some users affected | SHOULD FIX soon |
| **Minor** | Low impact | MAY FIX eventually |

### Performance Budget

| Metric | Threshold | Meaning |
|--------|-----------|---------|
| **Gzipped CSS** | <3 KB | Production-ready |
| **Uncompressed** | <10 KB | Reasonable size |
| **Compression Ratio** | >2.0x | Good compression |

---

## Common Issues and Solutions

### Issue 1: Screenshots are blank/white

**Symptoms:**
- All screenshots in baseline/ or themed/ are white/empty
- No errors during capture

**Diagnosis:**
```bash
identify wave3/baseline/01_homepage.png
# If all pixels are white, screenshot failed to capture content
```

**Solution:**
1. Increase wait timeout in `wave3_screenshot_capture.py`:
   ```python
   await asyncio.sleep(5)  # Increase from 2 to 5 seconds
   ```
2. Verify Streamlit is fully loaded before capture:
   ```bash
   curl http://localhost:8501  # Should return HTML
   ```

---

### Issue 2: Theme not visible in screenshots

**Symptoms:**
- Baseline and themed screenshots look identical
- Visual regression shows MINIMAL changes everywhere

**Diagnosis:**
```bash
# Check if CSS is actually injected
curl http://localhost:8501 | grep "data-theme=\"dip-docs\""
# Should find the wrapper div
```

**Solution:**
1. Verify `config.yaml` has `enable_dip_theme: true`
2. Hard refresh browser (Ctrl+Shift+R)
3. Check `streamlit_app.py` calls `inject_theme()`
4. Review browser console for CSS errors

---

### Issue 3: Accessibility audit finds critical contrast issues

**Symptoms:**
```
Critical violations: 3
- color-contrast: Element has insufficient color contrast
```

**Solution:**
1. Review specific violations:
   ```bash
   cat wave3/axe_audit_report.json | grep -A10 color-contrast
   ```
2. Check contrast ratio using browser DevTools:
   - Right-click element → Inspect
   - Look for contrast ratio in Styles panel
3. Fix in design tokens:
   ```json
   "colors": {
     "text-primary": {"value": "#111827"},  // Increase darkness
     "bg-primary": {"value": "#ffffff"}     // Ensure sufficient contrast
   }
   ```
4. Re-run validation pipeline

---

### Issue 4: CSS exceeds 3KB budget

**Symptoms:**
```
[FAIL] CSS size validation FAILED
Gzipped: 3245 bytes (3.17 KB)
Over budget by: 173 bytes
```

**Solution:**
1. Remove unused CSS rules in `src/utils/streamlit_theme.py`
2. Combine duplicate selectors
3. Use CSS shorthand properties:
   ```css
   /* Before: 4 rules */
   padding-top: 8px;
   padding-right: 12px;
   padding-bottom: 8px;
   padding-left: 12px;

   /* After: 1 rule */
   padding: 8px 12px;
   ```
4. Re-run performance measurement

---

## Manual Verification Checklist

After automated validation passes, manually verify:

- [ ] Homepage loads with themed colors
- [ ] Sidebar has custom background color
- [ ] Primary buttons have blue background (#2563eb)
- [ ] Hover states show darker blue (#0b2763)
- [ ] Focus rings are visible (3px blue outline)
- [ ] Metrics cards have rounded corners
- [ ] Text is readable (sufficient contrast)
- [ ] Code blocks use monospace font
- [ ] Tabs have custom styling
- [ ] Mobile viewport (resize browser) looks correct

---

## Next Steps After Validation

### If All Tests Pass:

1. **Update CHANGELOG.md:**
   ```markdown
   ## [Unreleased] - Wave 3 Complete
   ### Added
   - Streamlit theme parity with Sphinx documentation
   - Design token-driven theming system
   - Comprehensive validation pipeline
   ```

2. **Mark Wave 3 Complete:**
   ```bash
   git add .
   git commit -m "feat(phase3): Complete Wave 3 Streamlit theme parity validation"
   ```

3. **Document Integration:**
   - Write `docs/guides/workflows/streamlit-theme-integration.md`
   - Include customization guide
   - Add troubleshooting section

4. **Create Completion Summary:**
   - Document: `.codex/phase3/WAVE3_STREAMLIT_COMPLETION.md`
   - Include before/after screenshots
   - List metrics and achievements

### If Any Tests Fail:

1. **Review Detailed Reports:**
   - `wave3/VALIDATION_SUMMARY.md` - Overall status
   - Category-specific reports (visual_regression, axe_audit, etc.)

2. **Fix Issues:**
   - Address failures in order of severity (Critical → Serious → Moderate)
   - Re-run specific validation step after each fix
   - Use `python wave3_comparison_analysis.py` to check overall status

3. **Re-validate:**
   - Re-run entire pipeline after fixes
   - Ensure all categories pass

---

## Quick Reference

### Essential Commands

```bash
# Full validation pipeline (one-liner)
cd .codex/phase3/validation/streamlit && \
python generate_token_mapping.py && \
echo "Set enable_dip_theme: false in config.yaml, then start Streamlit" && \
read -p "Press Enter when ready..." && \
python wave3_screenshot_capture.py baseline && \
echo "Set enable_dip_theme: true in config.yaml, then restart Streamlit" && \
read -p "Press Enter when ready..." && \
python wave3_screenshot_capture.py themed && \
python wave3_visual_regression.py && \
python wave3_axe_audit.py && \
python wave3_performance.py && \
python wave3_comparison_analysis.py
```

### Check Overall Status

```bash
cat .codex/phase3/validation/streamlit/wave3/VALIDATION_SUMMARY.md | head -20
```

### View Individual Reports

```bash
# Token mapping
cat wave3/token_mapping.csv

# Visual regression
cat wave3/visual_regression_summary.md

# Accessibility
cat wave3/axe_audit_summary.md

# Performance
cat wave3/performance_summary.md

# Aggregated
cat wave3/VALIDATION_SUMMARY.md
```

---

## Support

**Documentation:**
- Phase 3 Plan: `.codex/phase3/WAVE3_STREAMLIT_PLAN.md`
- Token System: `.codex/phase2_audit/design_tokens_v2.json`
- Theme Module: `src/utils/streamlit_theme.py`

**GitHub Issues:**
- Report validation failures: https://github.com/theSadeQ/dip-smc-pso/issues
- Tag with: `phase3`, `streamlit`, `validation`

**Contact:**
- Maintainer: See CONTRIBUTING.md
