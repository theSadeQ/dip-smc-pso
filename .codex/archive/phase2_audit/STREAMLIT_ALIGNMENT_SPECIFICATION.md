# Streamlit Alignment Specification (Theme 7)

Technical plan for bringing the Streamlit dashboard into parity with the updated design system while staying resilient to future Streamlit updates.

---

## Scope & Objectives

1. Apply Phase 2 token system (colors, spacing, typography) to Streamlit.
2. Harmonize interactive components (`st.button`, `st.metric`, `st.download_button`, sidebar nav).
3. Introduce accessibility improvements (contrast, focus, reduced motion) consistent with docs.
4. Ensure alignment survives Streamlit upgrades (1.31 → 2.0) via isolated overrides.

---

## Integration Architecture

| Layer | Strategy | Implementation Detail |
|-------|----------|-----------------------|
| Token Source | Reuse `design_tokens_v2.json`. | Load JSON in Streamlit via `pathlib.Path('.codex/phase2_audit/design_tokens_v2.json')`. |
| CSS Variables Injection | Inject `<style>` block with `:root` variables + scoped classes. | Use `st.markdown(style_block, unsafe_allow_html=True)` after `set_page_config`. |
| Component Mapping | Map Streamlit widget classes to design tokens. | Define class selectors (e.g., `.stButton > button`) referencing tokens. |
| Dark Mode Handling | Provide optional toggle for future; currently light-mode parity only. | Namespace dark-mode variables but keep disabled until Phase 4. |
| Version Guard | Encapsulate overrides in attribute `[data-theme="dip-docs"]`. | Wrap page body via `st.markdown('<div data-theme=\"dip-docs\">', ...)` to avoid collisions with upstream changes. |

---

## Token Loading (Python)

```python
from pathlib import Path
import json

def load_tokens():
    token_path = Path(".codex/phase2_audit/design_tokens_v2.json")
    tokens = json.loads(token_path.read_text())
    color = tokens["colors"]
    spacing = tokens["spacing"]
    type_scale = tokens["typography"]
    return color, spacing, type_scale

COLORS, SPACING, TYPO = load_tokens()
```

---

## CSS Injection Snippet

```python
css = f"""
<style id="dip-streamlit-theme">
:root[data-theme="dip-docs"] {{
  --color-primary: {COLORS["primary"]["value"]};
  --color-primary-hover: {COLORS["primary-hover"]["value"]};
  --color-text-primary: {COLORS["text-primary"]["value"]};
  --color-text-secondary: {COLORS["text-secondary"]["value"]};
  --color-text-muted: {COLORS["text-muted"]["value"]};
  --spacing-2: {SPACING["spacing-sm"]["value"]};
  --spacing-3: {SPACING["spacing-md"]["value"]};
  --spacing-4: {SPACING["spacing-lg"]["value"]};
}}

.block-container[data-theme="dip-docs"] {{
  max-width: 1120px;
  padding: var(--spacing-4) var(--spacing-3);
  font-family: {TYPO["font-family-body"]["value"]};
  color: var(--color-text-primary);
}}

.stButton[data-baseweb="button"] > button {{
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-hover));
  color: #fff;
  border-radius: 8px;
  padding: calc(var(--spacing-2) + 2px) var(--spacing-4);
  font-weight: 600;
  box-shadow: 0 6px 18px rgba(11, 39, 99, 0.25);
  transition: transform 150ms ease, box-shadow 150ms ease;
}}

.stButton[data-baseweb="button"] > button:hover {{
  transform: translateY(-1px);
  box-shadow: 0 10px 24px rgba(11, 39, 99, 0.28);
}}

.stButton[data-baseweb="button"] > button:focus-visible {{
  outline: 3px solid var(--color-primary);
  outline-offset: 2px;
}}

.stMetric > div {{
  border-radius: 12px;
  background: linear-gradient(160deg, rgba(11, 39, 99, 0.08), rgba(59, 130, 246, 0.05));
  padding: var(--spacing-4);
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.15);
}}

.stDownloadButton button {{
  background: var(--color-primary);
  color: #fff;
  border-radius: 999px;
  padding: calc(var(--spacing-2) + 1px) var(--spacing-4);
}}

.stDownloadButton button::before {{
  content: "⇩";
  margin-right: var(--spacing-2);
}}

.sidebar .stButton > button {{
  width: 100%;
  justify-content: flex-start;
}}
</style>
"""

st.markdown("<div data-theme='dip-docs'>", unsafe_allow_html=True)
st.markdown(css, unsafe_allow_html=True)
```

Ensure closing `</div>` appended at end of layout.

---

## Widget Mapping Matrix

| Streamlit Element | Current Issue | Target Treatment | Implementation Detail |
|-------------------|---------------|------------------|-----------------------|
| Primary buttons (`st.button`, `st.download_button`) | Default gray, square corners. | Gradient primary with focus state + iconography. | CSS above; add `aria-label` updates via Streamlit kwargs. |
| Sidebar navigation | Sparse spacing, flat hover. | 8px vertical rhythm, bold active item, hover color. | Add `.sidebar .css-1d391kg` selectors to apply `padding: var(--spacing-2) 0; border-left`. |
| `st.metric` cards | Flat white backgrounds. | Gradient header, bold numeric, token spacing. | Use CSS `.stMetric` overrides; map deltas to semantic colors. |
| Code snippets (`st.code`) | Default theme mismatch. | Apply docs Pygments theme via `st.markdown` style block. | Import CSS from docs once tokens stabilized. |
| Tabs/expanders | Default spacing. | Align with docs spacing & typography. | Override `.stTabs [data-baseweb="tab"]` with tokenized padding + focus ring. |

---

## Testing & Validation

1. **Visual Regression**: Percy snapshots for home, simulation, analytics tabs (desktop + 375px).
2. **Accessibility**: axe scan for contrast; keyboard traversal focusing on button hover/active states.
3. **Performance**: Ensure CSS injection adds <3KB (gzip). Use `streamlit run` with Chrome DevTools coverage.
4. **Compatibility**: Verify on Streamlit 1.31 (current) and preview release (2.0-beta if available). Maintain feature flag to disable custom skin if runtime mismatch detected.

---

## Future Proofing

- Document override wrapper in `DECISION_LOG.md` with rationale.
- Provide toggle in configuration: `ENABLE_DIP_THEME = True`. When false, revert to vanilla Streamlit for troubleshooting.
- Track Streamlit release notes; if DOM structure changes, adjust selectors in one central stylesheet (`streamlit_theme.css`).
- Consider packaging as internal Streamlit theme module for reuse across teams in Phase 3.

