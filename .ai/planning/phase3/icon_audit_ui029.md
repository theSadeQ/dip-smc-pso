# Icon Audit Report (UI-029)

**Date**: 2025-10-16
**Task**: Replace mixed iconography with consistent SVG icon set
**Estimated Effort**: 4-6 hours (focused scope)

---

## Executive Summary

**Total Files with Icons**: 750+ files across documentation
**Icon Categories Found**:
- ✓✗❌✅ Checkmarks/status indicators: 271 files
- ▶️⏸️⏹️ Media/control icons: 134 files
- →←↑↓ Directional arrows: 345 files

**Recommendation**: **Phased approach** - prioritize high-visibility user-facing docs (Guides, Quick Reference, Getting Started) rather than attempting to replace all 750+ files in 4-6 hours.

---

## Current Icon Usage Patterns

### Pattern 1: Status Indicators (Most Common)

**Files**: 271 files
**Usage**: Performance metrics tables, test results, validation checklists

**Example from `docs/guides/QUICK_REFERENCE.md` (line 108)**:
```markdown
| **ISE** | ∫‖x‖² dt | Tracking accuracy (quadratic) | ✓ |
| **ITAE** | ∫t·‖x‖ dt | Time-weighted error (convergence) | ✓ |
| **Settling Time** | t when ‖x‖ < 5% | Convergence speed | ✓ |
```

**Replacement Strategy**: Replace `✓` with inline SVG icon or CSS pseudo-element

---

### Pattern 2: Directional Indicators

**Files**: 345 files
**Usage**: Workflow diagrams, navigation, process flows

**Common Patterns**:
- `→` - Step progression ("config.yaml → controller → simulation")
- `←` - Backward reference
- `↑↓` - Hierarchy/ordering
- `⇒` - Implies/leads to

**Replacement Strategy**: Consider keeping as Unicode (semantic meaning) or use CSS arrow classes

---

### Pattern 3: Emoji Icons (Least Critical)

**Files**: Includes technical symbols (🔍, ⚙️, 📊)
**Usage**: Section headers, visual callouts

**Note**: CLAUDE.md section states:
> "This file uses ASCII text markers (e.g., [AI], [OK], [BLUE]) instead of Unicode emojis for Windows terminal compatibility."

**Recommendation**: Replace with ASCII markers or SVG icons consistently

---

## Scope Definition (4-6 Hour Plan)

### Phase 1: High-Priority Files (2 hours)

**Target**: User-facing guides with frequent access

1. **Quick Reference** (`docs/guides/QUICK_REFERENCE.md`)
   - Replace ✓ in performance metrics table (5 instances)
   - Add status icon legend at bottom

2. **Getting Started** (`docs/guides/getting-started.md`)
   - Audit icon usage (TBD - need to read file)
   - Replace with consistent set

3. **Index/Landing Pages**:
   - `docs/index.md`
   - `docs/guides/INDEX.md`
   - `docs/guides/README.md`

### Phase 2: Icon Library Setup (1.5 hours)

**Actions**:
1. Select icon library: **Heroicons** (recommended)
   - MIT licensed
   - SVG format
   - Excellent accessibility (built-in aria-labels)
   - Minimal footprint (~1 KB per icon)

2. Create `docs/_static/icons/` directory structure:
   ```
   docs/_static/icons/
   ├── status/
   │   ├── check.svg          (✓ replacement)
   │   ├── cross.svg          (✗ replacement)
   │   ├── warning.svg        (⚠️ replacement)
   │   └── info.svg           (ℹ️ replacement)
   ├── navigation/
   │   ├── arrow-right.svg    (→ replacement)
   │   ├── arrow-left.svg     (← replacement)
   │   └── arrow-down.svg     (↓ replacement)
   └── index.md               (Icon usage guide)
   ```

3. Add CSS classes to `docs/_static/custom.css`:
   ```css
   /* Icon system - UI-029 */
   .icon {
       display: inline-block;
       width: 1em;
       height: 1em;
       vertical-align: middle;
       fill: currentColor;
   }

   .icon-check { color: var(--color-success); }
   .icon-cross { color: var(--color-danger); }
   .icon-warning { color: var(--color-warning); }
   ```

### Phase 3: Template Creation (1 hour)

**Deliverables**:
1. **Markdown Icon Syntax**:
   ```markdown
   <!-- Old: ✓ -->
   <!-- New: -->
   <svg class="icon icon-check" aria-label="Success">
     <use href="/_static/icons/status/check.svg#icon"></use>
   </svg>
   ```

2. **Shortcode Alternative** (if MyST supports):
   ```markdown
   {icon}`check` - Success
   {icon}`cross` - Failed
   {icon}`warning` - Warning
   ```

3. **Icon Legend Template** (add to bottom of tables):
   ```markdown
   **Legend**: {icon}`check` - Lower is better
   ```

### Phase 4: Implementation (1.5 hours)

**Execution**:
1. Replace icons in Quick Reference performance table
2. Replace icons in Getting Started guide
3. Update 3-5 index pages
4. Test Sphinx rebuild
5. Visual verification in browser

**Out of Scope for Phase 1**:
- ❌ ALL 750+ files (too large for 4-6 hours)
- ❌ Internal reports/analysis docs (low user visibility)
- ❌ Auto-generated reference docs
- ✅ ONLY user-facing guides + high-traffic pages

---

## Icon Library Selection

### Recommended: Heroicons

**Why Heroicons?**
- ✅ MIT license (free for commercial use)
- ✅ SVG format (scalable, accessible)
- ✅ Outline + Solid variants (visual hierarchy)
- ✅ Small file size (~800 bytes per icon)
- ✅ Built-in accessibility (proper viewBox, aria support)
- ✅ Active maintenance (Tailwind Labs)

**Icons Needed** (minimal set):
1. **Status**: check, x-mark, exclamation-triangle, information-circle
2. **Navigation**: arrow-right, arrow-left, arrow-up, arrow-down
3. **Actions**: magnifying-glass, cog-6-tooth, document-text
4. **Indicators**: check-circle, x-circle, clock

**Total**: ~12 icons × 800 bytes = ~10 KB (negligible)

**Alternatives Considered**:
- **Feather**: Similar to Heroicons, slightly larger files
- **Lucide**: Fork of Feather with more icons (overkill for our needs)

---

## Implementation Steps (Detailed)

### Step 1: Download Heroicons (15 min)

```bash
# Option A: Manual download
# Download from https://heroicons.com
# Extract only needed icons to docs/_static/icons/

# Option B: NPM (if Node.js available)
npm install heroicons
cp node_modules/heroicons/24/outline/{check,x-mark,arrow-right}.svg docs/_static/icons/status/
```

### Step 2: Create Icon CSS (30 min)

Add to `docs/_static/custom.css`:

```css
/* =============================================================================
   ICON SYSTEM - UI-029
   ============================================================================= */

/* Base icon styling */
.icon {
    display: inline-block;
    width: 1em;
    height: 1em;
    vertical-align: -0.125em; /* Align with text baseline */
    fill: none;
    stroke: currentColor;
    stroke-width: 2;
    stroke-linecap: round;
    stroke-linejoin: round;
}

/* Icon sizes */
.icon-sm { width: 0.875em; height: 0.875em; }
.icon-lg { width: 1.25em; height: 1.25em; }
.icon-xl { width: 1.5em; height: 1.5em; }

/* Icon colors */
.icon-success { color: var(--color-success); }
.icon-danger { color: var(--color-danger); }
.icon-warning { color: var(--color-warning); }
.icon-info { color: var(--color-info); }
.icon-primary { color: var(--color-primary); }

/* Specific icon contexts */
table .icon {
    width: 1.125em;
    height: 1.125em;
    vertical-align: middle;
}

/* Dark mode adjustments */
@media (prefers-color-scheme: dark) {
    .icon {
        stroke-width: 1.75; /* Slightly thinner in dark mode */
    }
}
```

### Step 3: Replace QUICK_REFERENCE.md Icons (45 min)

**Before**:
```markdown
| **ISE** | ∫‖x‖² dt | Tracking accuracy (quadratic) | ✓ |
```

**After**:
```markdown
| **ISE** | ∫‖x‖² dt | Tracking accuracy (quadratic) | <svg class="icon icon-success" aria-label="Lower is better"><use href="/_static/icons/status/check.svg#icon"></use></svg> |
```

**Or** (if MyST shortcode supported):
```markdown
| **ISE** | ∫‖x‖² dt | Tracking accuracy (quadratic) | {icon}`check|success` |
```

### Step 4: Create Icon Usage Guide (30 min)

Create `docs/_static/icons/README.md`:

```markdown
# Icon System (UI-029)

## Available Icons

### Status Icons

| Icon | Usage | Markdown |
|------|-------|----------|
| ✅ | Success, passed, confirmed | `{icon}`check\|success`` |
| ❌ | Failed, error, blocked | `{icon}`cross\|danger`` |
| ⚠️ | Warning, caution | `{icon}`warning\|warning`` |
| ℹ️ | Information, note | `{icon}`info\|info`` |

### Navigation Icons

| Icon | Usage | Markdown |
|------|-------|----------|
| → | Next step, forward | `{icon}`arrow-right`` |
| ← | Previous step, back | `{icon}`arrow-left`` |
| ↓ | Expand, more details | `{icon}`arrow-down`` |

## Usage Guidelines

1. **Accessibility**: All icons MUST have `aria-label` or be decorative (`aria-hidden="true"`)
2. **Color**: Use semantic colors (success, danger, warning) for status icons
3. **Size**: Default 1em matches text size; use `.icon-lg` for emphasis
4. **Inline**: Icons inline with text should use `vertical-align: middle`

## Migration from Unicode

| Old (Unicode) | New (SVG) | Notes |
|---------------|-----------|-------|
| ✓ | `{icon}`check\|success`` | Green checkmark |
| ✗ | `{icon}`cross\|danger`` | Red X |
| → | `{icon}`arrow-right`` | Directional arrow |
```

### Step 5: Asset Pack v3 Documentation (45 min)

Create `.codex/phase3/asset_pack_v3.md`:

```markdown
# Asset Pack v3 - Icon System (UI-029)

## Overview

Standardized SVG icon system replacing mixed Unicode/emoji usage.

## Contents

### Icon Library
- **Source**: Heroicons v2.1.1 (MIT License)
- **Format**: SVG (inline or `<use>` reference)
- **Total Icons**: 12 core icons (~10 KB total)
- **Location**: `docs/_static/icons/`

### Directory Structure
```
docs/_static/icons/
├── status/          # Checkmarks, warnings, errors
├── navigation/      # Arrows, directional indicators
├── actions/         # Search, settings, etc.
└── README.md        # Usage guide
```

## Design Tokens Integration

Icons use existing design tokens from v2.0.0:

```css
.icon-success { color: var(--color-success); }   /* #059669 */
.icon-danger { color: var(--color-danger); }     /* #dc2626 */
.icon-warning { color: var(--color-warning); }   /* #d97706 */
.icon-info { color: var(--color-info); }         /* #2563eb */
```

## Accessibility

All icons follow WCAG 2.1 Level AA:
- Minimum 3:1 contrast ratio (verified with design tokens)
- `aria-label` for semantic icons
- `aria-hidden="true"` for decorative icons
- Keyboard-accessible when interactive

## Browser Support

- Chrome 90+ ✅
- Firefox 88+ ✅
- Safari 14+ ✅
- Edge 90+ ✅

## File Size Impact

- **Individual icon**: ~800 bytes (SVG)
- **12 core icons**: ~10 KB uncompressed
- **Gzipped**: ~3 KB (minimal overhead)

## Migration Path

**Phase 1** (This release):
- Quick Reference Guide
- Getting Started Guide
- Index/landing pages

**Phase 2** (Future):
- Tutorial series
- API reference docs

**Phase 3** (Optional):
- Internal reports
- Generated documentation

## Maintenance

**Icon Updates**: Download new icons from https://heroicons.com
**Adding Icons**: Place in appropriate subdirectory, update README.md
**Deprecation**: Keep old Unicode in comments for 1 release cycle

## License

Heroicons: MIT License (Copyright 2020 Refactoring UI Inc.)
Project usage: Academic/Research (check project LICENSE file)
```

---

## Success Metrics

**Phase 1 Complete When**:
1. ✅ 3-5 high-priority files updated with new icon system
2. ✅ Icon library installed in `docs/_static/icons/`
3. ✅ CSS classes added to `custom.css`
4. ✅ Usage guide created (`docs/_static/icons/README.md`)
5. ✅ Asset pack v3 documented

**Quality Checks**:
- Sphinx rebuild successful (no errors)
- Visual verification in browser (icons render correctly)
- Accessibility check (icons have aria-labels)
- File size check (<15 KB total added assets)

---

## Out of Scope (Deferred to Future)

The following are **NOT** included in the 4-6 hour Phase 1:

1. ❌ Replacing icons in all 750+ files (unrealistic for time budget)
2. ❌ Custom icon design (using pre-built Heroicons)
3. ❌ JavaScript-based icon loading (pure CSS/HTML)
4. ❌ Animated icons (static SVG only)
5. ❌ Internal documentation/reports (low user visibility)
6. ❌ Auto-generated API reference docs (separate process)

---

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| MyST markdown doesn't support `<svg>` tags | High | Fall back to image syntax `![check](/_static/icons/status/check.svg)` |
| Icon file size adds to page load | Low | Use SVG sprites or inline critical icons |
| Accessibility issues | Medium | Test with screen reader (NVDA/JAWS) |
| Browser compatibility | Low | SVG supported in all modern browsers |

---

## Timeline

**Total Estimated**: 5.5 hours (within 4-6 hour budget)

| Phase | Time | Status |
|-------|------|--------|
| Audit & Planning | 1 hour | ✅ Complete (this document) |
| Icon Library Setup | 1.5 hours | ⏳ Pending |
| Template Creation | 1 hour | ⏳ Pending |
| Implementation | 1.5 hours | ⏳ Pending |
| Testing & Validation | 0.5 hours | ⏳ Pending |

---

## Next Steps

1. **Download Heroicons**: Get 12 core icons from https://heroicons.com
2. **Create directory**: `mkdir -p docs/_static/icons/{status,navigation,actions}`
3. **Add CSS**: Append icon system CSS to `docs/_static/custom.css`
4. **Update QUICK_REFERENCE.md**: Replace ✓ with SVG icons (5 instances)
5. **Test Sphinx rebuild**: Verify icons render correctly
6. **Create usage guide**: Document icon syntax for future use

---

**Audit Created**: 2025-10-16
**Next Action**: Download Heroicons and create icon directory structure
