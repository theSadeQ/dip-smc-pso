# Wave 1 Screen Reader Testing Guide (NVDA/JAWS)

**Purpose**: Manual accessibility validation of Wave 1 fixes (UI-002, UI-003, UI-004) using NVDA and JAWS screen readers.

**Date**: 2025-10-15
**Wave**: Wave 1 - Foundations & Accessibility
**Tester**: _______________
**Environment**: Windows 10/11 + NVDA 2024.x or JAWS 2024

---

## Prerequisites

### Required Software
- [ ] NVDA (Free): Download from https://www.nvaccess.org/download/
- [ ] JAWS (Commercial): https://www.freedomscientific.com/products/software/jaws/
- [ ] Chrome, Firefox, or Edge browser
- [ ] Documentation server running at http://localhost:9000

### Test Pages
1. Homepage: `http://localhost:9000/`
2. Getting Started: `http://localhost:9000/guides/getting-started.html`
3. Controller API Reference: `http://localhost:9000/reference/controllers/index.html`
4. Benchmarks: `http://localhost:9000/benchmarks/index.html`

---

## Test Suite 1: UI-004 - Code Block ARIA Accessibility

### Background
Wave 1 added ARIA live regions and controls to collapsible code blocks. Screen readers must announce:
- When code blocks collapse/expand
- What regions are controlled by toggle buttons
- Current state (expanded/collapsed)

### Test 1.1: Code Block Landmark Navigation

**Page**: Getting Started guide

**Steps**:
1. Open `http://localhost:9000/guides/getting-started.html` in browser
2. Start NVDA/JAWS
3. Press `R` key to navigate by regions (NVDA) or `R` key (JAWS)
4. Listen for "Code block [number] region" announcements

**Expected Behavior**:
- [ ] NVDA announces: "Code block 1 region" when focus lands on code container
- [ ] JAWS announces: "Code block 1 region landmark"
- [ ] Multiple code blocks have unique numbers (Code block 1, Code block 2, etc.)
- [ ] `aria-label` provides clear identification

**Actual Result**:
```
NVDA: ___________________________________________________
JAWS: ___________________________________________________
Status: [ ] PASS [ ] FAIL
```

---

### Test 1.2: Collapse/Expand Button Announcement

**Page**: Getting Started guide

**Steps**:
1. Tab to first code block's collapse button (top-right corner)
2. Listen to button announcement
3. Note current state (expanded/collapsed)

**Expected Behavior**:
- [ ] NVDA announces: "Toggle code block 1 visibility button, expanded"
- [ ] JAWS announces: "Toggle code block 1 visibility button expanded"
- [ ] `aria-expanded="true"` state is announced
- [ ] Button has clear label (not just "button")

**Actual Result**:
```
NVDA: ___________________________________________________
JAWS: ___________________________________________________
Status: [ ] PASS [ ] FAIL
```

---

### Test 1.3: ARIA Controls Relationship

**Page**: Getting Started guide

**Steps**:
1. Focus on code collapse button
2. Press NVDA+CTRL+F1 (NVDA) or INSERT+F1 (JAWS) for element info
3. Check for "Controls" property listing controlled regions

**Expected Behavior**:
- [ ] NVDA shows: "Controls: code-block-0 code-notice-0"
- [ ] JAWS announces controlled regions when querying element
- [ ] `aria-controls` attribute links button to both block and notice

**Actual Result**:
```
NVDA: ___________________________________________________
JAWS: ___________________________________________________
Status: [ ] PASS [ ] FAIL
```

---

### Test 1.4: Live Region Announcement (Collapse Action)

**Page**: Getting Started guide

**Steps**:
1. Focus on expanded code block's collapse button
2. Press SPACE or ENTER to collapse the code
3. Wait 1 second for live region announcement
4. Listen for collapse notice message

**Expected Behavior**:
- [ ] NVDA announces: "Code hidden (click ▲ to expand)" (polite announcement)
- [ ] JAWS announces the same message after collapse completes
- [ ] `aria-live="polite"` notice element is announced automatically
- [ ] Announcement happens AFTER animation completes (not during)
- [ ] Button state changes to "collapsed" or "expanded false"

**Actual Result**:
```
NVDA: ___________________________________________________
JAWS: ___________________________________________________
Timing: [ ] Immediate [ ] After animation [ ] Never
Status: [ ] PASS [ ] FAIL
```

---

### Test 1.5: Live Region Announcement (Expand Action)

**Page**: Getting Started guide

**Steps**:
1. Focus on collapsed code block's expand button
2. Press SPACE or ENTER to expand the code
3. Wait for expansion animation
4. Verify notice message disappears (no false announcement)

**Expected Behavior**:
- [ ] NVDA does NOT announce "Code hidden" message when expanding
- [ ] JAWS does NOT announce stale message
- [ ] Live region is hidden (display: none) when code is expanded
- [ ] Button state updates to "expanded true"
- [ ] No phantom announcements of hidden content

**Actual Result**:
```
NVDA: ___________________________________________________
JAWS: ___________________________________________________
Status: [ ] PASS [ ] FAIL
```

---

### Test 1.6: Multiple Code Blocks Navigation

**Page**: API reference with multiple code examples

**Steps**:
1. Open page with 3+ code blocks
2. Tab through all collapse buttons
3. Verify each has unique ID and announcement

**Expected Behavior**:
- [ ] Each button announces different code block number: "block 1", "block 2", etc.
- [ ] No duplicate IDs (all unique)
- [ ] Each button controls correct code block (no cross-wiring)
- [ ] Focus order is logical (top to bottom)

**Actual Result**:
```
Code Block 1: ___________________________________________
Code Block 2: ___________________________________________
Code Block 3: ___________________________________________
Status: [ ] PASS [ ] FAIL
```

---

## Test Suite 2: UI-002/UI-003 - Text Contrast & Readability

### Background
Wave 1 improved muted text contrast from 3.7:1 (FAIL) to 4.52:1 (PASS WCAG AA) and collapsed notice contrast to 12.4:1 (PASS WCAG AAA).

### Test 2.1: Caption/Metadata Text Readability

**Page**: All pages

**Steps**:
1. Navigate to page footer
2. Find copyright text, "last updated" timestamp, and figure captions
3. Use screen reader reading mode (NVDA: NVDA+SPACE, JAWS: JAWS+Z)
4. Verify text is announced clearly (not skipped or garbled)

**Expected Behavior**:
- [ ] NVDA reads all caption text without errors
- [ ] JAWS reads all metadata text without errors
- [ ] Text is not announced as "empty" or skipped
- [ ] Color contrast is visually acceptable (gray on white, but readable)

**Actual Result**:
```
Copyright text: __________________________________________
Last updated: ____________________________________________
Figure captions: _________________________________________
Status: [ ] PASS [ ] FAIL
```

---

### Test 2.2: Collapsed Notice Visual Contrast

**Page**: Getting Started guide

**Steps**:
1. Collapse a code block
2. Visually inspect the notice message: "Code hidden (click ▲ to expand)"
3. Verify dark background (#1b2433) with light text (#f8fbff)
4. Check if text is easily readable

**Expected Behavior**:
- [ ] Notice has dark blue/gray background
- [ ] Text is white or very light color
- [ ] High contrast is visually obvious (12.4:1 ratio)
- [ ] Text is not washed out or hard to read

**Visual Assessment**:
```
Background color (approx): ___________________________
Text color (approx): ___________________________________
Readability: [ ] Excellent [ ] Good [ ] Fair [ ] Poor
Status: [ ] PASS [ ] FAIL
```

---

## Test Suite 3: Keyboard Navigation & Focus

### Test 3.1: Tab Order Logical

**Page**: Homepage

**Steps**:
1. Start at top of page
2. Press TAB repeatedly to navigate through all interactive elements
3. Note if focus jumps unexpectedly or skips elements

**Expected Behavior**:
- [ ] Tab order follows visual layout (top to bottom, left to right)
- [ ] All interactive elements are reachable via TAB
- [ ] No keyboard traps (can escape from any element with TAB/SHIFT+TAB)
- [ ] Focus indicator is clearly visible

**Actual Result**:
```
Tab order issues: ________________________________________
Keyboard traps: __________________________________________
Status: [ ] PASS [ ] FAIL
```

---

### Test 3.2: Focus Indicator Visibility

**Page**: All pages

**Steps**:
1. Tab to code collapse button
2. Observe focus indicator (outline or highlight)
3. Verify it's visible against all background colors

**Expected Behavior**:
- [ ] Focus outline is clearly visible (2-3px solid line)
- [ ] Contrasts well with button background
- [ ] Blue or high-contrast color (#3b82f6 expected)
- [ ] Does not disappear on hover

**Actual Result**:
```
Focus indicator style: ___________________________________
Visibility rating: [ ] Excellent [ ] Good [ ] Fair [ ] Poor
Status: [ ] PASS [ ] FAIL
```

---

## Test Suite 4: Browser Compatibility

### Test 4.1: Multi-Browser ARIA Consistency

**Browsers to Test**: Chrome, Firefox, Edge

**Steps**:
1. Open Getting Started guide in each browser
2. Test code block collapse/expand with NVDA
3. Verify announcements are consistent across browsers

**Expected Behavior**:
- [ ] Chrome: ARIA announcements work identically
- [ ] Firefox: ARIA announcements work identically
- [ ] Edge: ARIA announcements work identically
- [ ] No browser-specific failures

**Actual Result**:
```
Chrome: [ ] PASS [ ] FAIL - Notes: _____________________
Firefox: [ ] PASS [ ] FAIL - Notes: _____________________
Edge: [ ] PASS [ ] FAIL - Notes: _____________________
```

---

## Summary & Sign-Off

### Overall Test Results

| Test Suite | Tests Run | Passed | Failed | Notes |
|------------|-----------|--------|--------|-------|
| UI-004 Code Blocks | 6 | ___ | ___ | |
| UI-002/003 Contrast | 2 | ___ | ___ | |
| Keyboard Navigation | 2 | ___ | ___ | |
| Browser Compatibility | 1 | ___ | ___ | |
| **TOTAL** | **11** | **___** | **___** | |

### Critical Issues Found
```
Issue 1: _____________________________________________________
Issue 2: _____________________________________________________
Issue 3: _____________________________________________________
```

### Wave 1 Exit Criteria: NVDA/JAWS Validation

**Status**: [ ] PASS (0 critical issues) [ ] FAIL (1+ critical issues)

**Tester Signature**: ___________________________
**Date**: ___________________________
**NVDA Version**: ___________________________
**JAWS Version**: ___________________________

---

## Appendix: NVDA Keyboard Shortcuts

- **Toggle reading mode**: NVDA+SPACE
- **Navigate by headings**: H (next), SHIFT+H (previous)
- **Navigate by regions**: R (next), SHIFT+R (previous)
- **Navigate by buttons**: B (next), SHIFT+B (previous)
- **Element information**: NVDA+CTRL+F1
- **Focus mode**: NVDA+SPACE (toggle between browse/focus)
- **Say current line**: NVDA+UP ARROW
- **Read from cursor**: NVDA+DOWN ARROW

## Appendix: JAWS Keyboard Shortcuts

- **Toggle virtual cursor**: JAWS+Z
- **Navigate by headings**: H (next), SHIFT+H (previous)
- **Navigate by regions**: R (next), SHIFT+R (previous)
- **Navigate by buttons**: B (next), SHIFT+B (previous)
- **Element information**: INSERT+F1
- **Say current line**: INSERT+UP ARROW
- **Read from cursor**: INSERT+DOWN ARROW
- **Forms mode**: ENTER on form field (auto-enters)
