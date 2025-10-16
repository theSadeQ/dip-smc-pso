# Browser Compatibility Matrix

Key CSS/HTML features introduced or relied upon by Phase 2 material specifications. Support data based on MDN as of Oct 2025.

| Feature | Usage in Specs | Chrome | Firefox | Safari | Edge | IE11 | Notes |
|---------|----------------|--------|---------|--------|------|------|-------|
| CSS Custom Properties (`var()`) | Token system for colors, spacing, typography | 49+ ✅ | 31+ ✅ | 9.1+ ✅ | 79+ ✅ | ❌ | IE11 unsupported; fallback tokens documented but Phase 2 targets evergreen browsers only. |
| `prefers-reduced-motion` media query | Disable animations for UI-001/013 | 74+ ✅ | 63+ ✅ | 10.1+ ✅ | 79+ ✅ | ❌ | Provide JS fallback note if analytics show legacy usage (currently <0.4%). |
| `prefers-contrast` media query | Enhance contrast for code controls | 96+ ✅ | 106+ ✅ | 16+ ✅ | 96+ ✅ | ❌ | Optional enhancement; gracefully ignored elsewhere. |
| `:focus-visible` pseudo-class | Accessible focus outlines without visual noise | 86+ ✅ | 85+ ✅ | 15.4+ ✅ | 86+ ✅ | ❌ | Polyfill available but not required; fallback to `:focus`. |
| `@media (max-width: 375px)` | Mobile typography + layout adjustments (UI-020–023) | 29+ ✅ | 29+ ✅ | 9+ ✅ | 12+ ✅ | 9+ ✅ | Supported broadly; ensure combined with `overflow-wrap`. |
| `overflow-wrap: break-word` | Mobile H1 fix (UI-020) | 58+ ✅ | 49+ ✅ | 14.1+ ✅ | 79+ ✅ | ❌ | IE11 fallback: `word-break: break-word` (non-standard) documented but not required. |
| `hyphens: auto` (+ vendor prefixes) | Controlled hyphenation for mobile titles | 55+ ✅ | 43+ ✅ | 5.1+ ✅ | 79+ ✅ | ❌ | Requires correct `lang` attribute; fallback uses `overflow-wrap`. |
| `contain: layout` | Prevent layout shifts in code blocks | 52+ ✅ | 69+ ✅ | 15.4+ ✅ | 79+ ✅ | ❌ | Optional optimisation; safe to ignore where unsupported. |
| `scroll-behavior: smooth` | Smooth anchor navigation | 61+ ✅ | 36+ ✅ | 15.4+ ✅ | 79+ ✅ | ❌ | For non-supporting browsers, behaviour defaults to instant scroll. |
| `backdrop-filter` | Code control master bar aesthetics | 76+ ✅ | 103+ ✅ | 13+ ✅ | 79+ ✅ | ❌ | Provide fallback solid color to maintain readability. |
| `position: sticky` | Coverage matrix header (UI-033) | 56+ ✅ | 32+ ✅ | 13+ ✅ | 16+ ✅ | ❌ | Graceful degradation: table remains functional without sticky header. |
| `aria-live="polite"` | Announce collapsed notices | ✅ | ✅ | ✅ | ✅ | ✅ | Screen reader support requires markup change; works cross-browser. |
| `<button type="button">` semantics inside Sphinx templates | Improved keyboard + ARIA semantics | ✅ | ✅ | ✅ | ✅ | ✅ | Works across browsers; ensure no reliance on `<a>` for button roles. |

✅ = fully supported; ❌ = not supported.

Evergreen browser support meets project requirement (>98% user base). For IE11 (deprecated), Phase 2 documents fallbacks or explicitly states non-support.

