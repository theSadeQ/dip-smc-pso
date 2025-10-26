# Baseline Screenshots for Visual Regression Testing

**Created:** 2025-10-12
**Purpose:** Reference screenshots for automated visual regression testing

---

## Overview

These baseline screenshots serve as the "golden master" for visual regression testing. Future test runs will compare new screenshots against these baselines to detect unintended visual changes.

---

## Baseline Images

| Screenshot | Purpose | Date | Browser | Notes |
|------------|---------|------|---------|-------|
| `test_1_1_buttons.png` | Verify all collapse buttons are present | 2025-10-12 | Chromium | Shows initial page state with all buttons visible |
| `test_1_3_all_collapsed.png` | All code blocks collapsed | 2025-10-12 | Chromium | Verifies "Collapse All" functionality |
| `test_1_3_all_expanded.png` | All code blocks expanded | 2025-10-12 | Chromium | Verifies "Expand All" functionality |
| `test_6_1_mobile_320px.png` | Mobile responsive layout (320px) | 2025-10-12 | Chromium | iPhone SE viewport |
| `test_6_1_tablet_768px.png` | Tablet responsive layout (768px) | 2025-10-12 | Chromium | iPad viewport |
| `test_6_1_desktop_1024px.png` | Desktop responsive layout (1024px) | 2025-10-12 | Chromium | Desktop viewport |

---

## How to Use

### Automated Comparison

The `ScreenshotManager` utility provides pixel-diff comparison:

```python
from utils.screenshot_manager import ScreenshotManager

manager = ScreenshotManager()
result = manager.compare_with_baseline(
    test_screenshot_path="test_1_1_buttons_20251012_142413.png",
    baseline_name="test_1_1_buttons",
    tolerance=0.05  # 5% difference allowed
)

if result["match"]:
    print("Screenshot matches baseline!")
else:
    print(f"Difference: {result['diff_percent']:.2f}%")
```

### Visual Regression Tests

Tests can be added to the test suite:

```python
def test_visual_regression_buttons(helper, screenshot_manager):
    """Compare button screenshot with baseline."""
    helper.goto_docs()
    test_path = helper.take_screenshot("buttons_regression")

    result = screenshot_manager.compare_with_baseline(
        test_path, "test_1_1_buttons", tolerance=0.05
    )

    assert result["match"], result["message"]
```

---

## Updating Baselines

Baselines should be updated when:
1. **Intentional visual changes** are made to the documentation
2. **CSS updates** affect button appearance
3. **Layout changes** are approved

### Update Process

1. **Run tests and verify new screenshots are correct:**
   ```bash
   python tests/browser_automation/run_tests.py
   ```

2. **Visually inspect the new screenshots:**
   ```bash
   # Open screenshots in image viewer
   # Verify changes are intentional and correct
   ```

3. **Copy new screenshots to baseline directory:**
   ```bash
   cp tests/browser_automation/artifacts/screenshots/YYYYMMDD/test_*.png \
      tests/browser_automation/artifacts/screenshots/baseline/
   ```

4. **Commit updated baselines with clear explanation:**
   ```bash
   git add tests/browser_automation/artifacts/screenshots/baseline/
   git commit -m "test: Update visual regression baselines

   - Update button appearance after CSS changes
   - New baseline reflects approved design updates

   [AI] Generated with Claude Code"
   ```

---

## Known Differences

### Minor Variations Expected

- **Anti-aliasing differences** (< 1% variance) across operating systems
- **Font rendering** may differ slightly between Windows/Mac/Linux
- **Color accuracy** (< 2% variance) due to display calibration

### Tolerance Settings

- **Strict mode:** tolerance=0.01 (1% difference allowed)
- **Standard mode:** tolerance=0.05 (5% difference allowed)
- **Relaxed mode:** tolerance=0.10 (10% difference allowed)

**Recommended:** Use tolerance=0.05 for most tests

---

## Validation Report

### Baseline Creation

- **Date:** 2025-10-12
- **Test Run:** All 17 tests passed
- **Browser:** Chromium 1187
- **Platform:** Windows 11
- **Resolution:** 1920x1080

### Screenshot Quality

- **Format:** PNG
- **Color Depth:** 24-bit RGB
- **Compression:** Lossless
- **Average File Size:** 350-520 KB

### Coverage

- ✅ Functional validation (buttons, collapse/expand)
- ✅ Responsive layouts (mobile, tablet, desktop)
- ✅ Master controls (Collapse All, Expand All)

---

## Troubleshooting

### False Positives

If tests fail with small differences (< 5%):

1. **Check pixel difference report**
2. **Visually compare screenshots**
3. **Increase tolerance** if differences are acceptable
4. **Update baselines** if intentional changes confirmed

### Missing Baselines

If baseline images are missing:

```bash
# Generate new baselines
python tests/browser_automation/run_tests.py
python tests/browser_automation/create_baselines.py
```

---

## Maintenance

- **Review baselines:** Monthly
- **Update after major changes:** As needed
- **Archive old baselines:** Keep in `baseline/archive/YYYY-MM-DD/`

---

## Contact

For questions about baseline management, see:
- `tests/browser_automation/README.md` - Testing guide
- `tests/browser_automation/utils/screenshot_manager.py` - Implementation
