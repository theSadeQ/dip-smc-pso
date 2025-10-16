"""
Generate token mapping table for Streamlit theme validation.

Maps design tokens → CSS variables → Streamlit widgets.
Output: wave3/token_mapping.csv
"""
import json
import pandas as pd
from pathlib import Path


def load_design_tokens() -> dict:
    """Load design tokens v2 from JSON file."""
    token_path = Path(__file__).parent.parent.parent.parent / "phase2_audit" / "design_tokens_v2.json"
    with open(token_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_token_mapping(tokens: dict) -> pd.DataFrame:
    """Generate token mapping table with all categories."""
    mapping_rows = []

    # ═══════════════════════════════════════════════════════════════════════
    # COLORS (8 tokens)
    # ═══════════════════════════════════════════════════════════════════════
    colors = tokens.get('colors', {})

    mapping_rows.append({
        'token_path': 'colors.primary.value',
        'css_variable': '--dip-primary',
        'streamlit_widget': '.stButton>button',
        'css_property': 'background-color',
        'expected_value': colors.get('primary', {}).get('value', 'N/A'),
        'category': 'colors',
        'priority': 'high'
    })

    mapping_rows.append({
        'token_path': 'colors.primary-hover.value',
        'css_variable': '--dip-primary-hover',
        'streamlit_widget': '.stButton>button:hover',
        'css_property': 'background-color',
        'expected_value': colors.get('primary-hover', {}).get('value', 'N/A'),
        'category': 'colors',
        'priority': 'high'
    })

    mapping_rows.append({
        'token_path': 'colors.text-primary.value',
        'css_variable': '--dip-text-primary',
        'streamlit_widget': 'div[data-testid="stMetric"] [data-testid="stMetricValue"]',
        'css_property': 'color',
        'expected_value': colors.get('text-primary', {}).get('value', 'N/A'),
        'category': 'colors',
        'priority': 'high'
    })

    mapping_rows.append({
        'token_path': 'colors.text-secondary.value',
        'css_variable': '--dip-text-secondary',
        'streamlit_widget': 'section[data-testid="stSidebar"] label',
        'css_property': 'color',
        'expected_value': colors.get('text-secondary', {}).get('value', 'N/A'),
        'category': 'colors',
        'priority': 'medium'
    })

    mapping_rows.append({
        'token_path': 'colors.text-muted.value',
        'css_variable': '--dip-text-muted',
        'streamlit_widget': 'div[data-testid="stMetric"] label',
        'css_property': 'color',
        'expected_value': colors.get('text-muted', {}).get('value', 'N/A'),
        'category': 'colors',
        'priority': 'medium'
    })

    mapping_rows.append({
        'token_path': 'colors.border.value',
        'css_variable': '--dip-border',
        'streamlit_widget': 'section[data-testid="stSidebar"]',
        'css_property': 'border-right',
        'expected_value': colors.get('border', {}).get('value', 'N/A'),
        'category': 'colors',
        'priority': 'low'
    })

    mapping_rows.append({
        'token_path': 'colors.bg-primary.value',
        'css_variable': '--dip-bg-primary',
        'streamlit_widget': 'div[data-testid="stMetric"]',
        'css_property': 'background-color',
        'expected_value': colors.get('bg-primary', {}).get('value', 'N/A'),
        'category': 'colors',
        'priority': 'medium'
    })

    mapping_rows.append({
        'token_path': 'colors.bg-secondary.value',
        'css_variable': '--dip-bg-secondary',
        'streamlit_widget': 'section[data-testid="stSidebar"]',
        'css_property': 'background-color',
        'expected_value': colors.get('bg-secondary', {}).get('value', 'N/A'),
        'category': 'colors',
        'priority': 'medium'
    })

    # ═══════════════════════════════════════════════════════════════════════
    # SPACING (4 tokens)
    # ═══════════════════════════════════════════════════════════════════════
    spacing = tokens.get('spacing', {})

    mapping_rows.append({
        'token_path': 'spacing.spacing-2.value',
        'css_variable': '--dip-space-2',
        'streamlit_widget': '.stButton>button',
        'css_property': 'padding',
        'expected_value': spacing.get('spacing-2', {}).get('value', 'N/A'),
        'category': 'spacing',
        'priority': 'high'
    })

    mapping_rows.append({
        'token_path': 'spacing.spacing-3.value',
        'css_variable': '--dip-space-3',
        'streamlit_widget': 'div[data-testid="stTabs"] button',
        'css_property': 'padding',
        'expected_value': spacing.get('spacing-3', {}).get('value', 'N/A'),
        'category': 'spacing',
        'priority': 'medium'
    })

    mapping_rows.append({
        'token_path': 'spacing.spacing-4.value',
        'css_variable': '--dip-space-4',
        'streamlit_widget': 'div[data-testid="stMetric"]',
        'css_property': 'padding',
        'expected_value': spacing.get('spacing-4', {}).get('value', 'N/A'),
        'category': 'spacing',
        'priority': 'medium'
    })

    mapping_rows.append({
        'token_path': 'spacing.spacing-5.value',
        'css_variable': '--dip-space-5',
        'streamlit_widget': 'section[data-testid="stSidebar"]',
        'css_property': 'padding',
        'expected_value': spacing.get('spacing-5', {}).get('value', 'N/A'),
        'category': 'spacing',
        'priority': 'low'
    })

    # ═══════════════════════════════════════════════════════════════════════
    # SHADOWS (2 tokens)
    # ═══════════════════════════════════════════════════════════════════════
    shadows = tokens.get('shadows', {})

    mapping_rows.append({
        'token_path': 'shadows.md.value',
        'css_variable': '--dip-shadow-md',
        'streamlit_widget': '.stButton>button',
        'css_property': 'box-shadow',
        'expected_value': shadows.get('md', {}).get('value', 'N/A'),
        'category': 'shadows',
        'priority': 'medium'
    })

    mapping_rows.append({
        'token_path': 'shadows.focus.value',
        'css_variable': '--dip-shadow-focus',
        'streamlit_widget': '.stButton>button:focus',
        'css_property': 'box-shadow',
        'expected_value': shadows.get('focus', {}).get('value', 'N/A'),
        'category': 'shadows',
        'priority': 'high'
    })

    # ═══════════════════════════════════════════════════════════════════════
    # BORDER RADIUS (2 tokens)
    # ═══════════════════════════════════════════════════════════════════════
    radius = tokens.get('border_radius', {})

    mapping_rows.append({
        'token_path': 'border_radius.sm.value',
        'css_variable': '--dip-radius-sm',
        'streamlit_widget': '.stButton>button',
        'css_property': 'border-radius',
        'expected_value': radius.get('sm', {}).get('value', 'N/A'),
        'category': 'border_radius',
        'priority': 'medium'
    })

    mapping_rows.append({
        'token_path': 'border_radius.md.value',
        'css_variable': '--dip-radius-md',
        'streamlit_widget': 'div[data-testid="stMetric"]',
        'css_property': 'border-radius',
        'expected_value': radius.get('md', {}).get('value', 'N/A'),
        'category': 'border_radius',
        'priority': 'medium'
    })

    # ═══════════════════════════════════════════════════════════════════════
    # TYPOGRAPHY (2 tokens)
    # ═══════════════════════════════════════════════════════════════════════
    typo = tokens.get('typography', {})

    mapping_rows.append({
        'token_path': 'typography.font-family-body.value',
        'css_variable': '--dip-font-body',
        'streamlit_widget': 'section[data-testid="stSidebar"]',
        'css_property': 'font-family',
        'expected_value': typo.get('font-family-body', {}).get('value', 'N/A'),
        'category': 'typography',
        'priority': 'low'
    })

    mapping_rows.append({
        'token_path': 'typography.font-family-mono.value',
        'css_variable': '--dip-font-mono',
        'streamlit_widget': 'div[data-testid="stCodeBlock"]',
        'css_property': 'font-family',
        'expected_value': typo.get('font-family-mono', {}).get('value', 'N/A'),
        'category': 'typography',
        'priority': 'low'
    })

    return pd.DataFrame(mapping_rows)


def main():
    """Main execution."""
    print("Loading design tokens...")
    tokens = load_design_tokens()

    print("Generating token mapping table...")
    df = generate_token_mapping(tokens)

    # Save to CSV
    output_dir = Path(__file__).parent / "wave3"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "token_mapping.csv"
    df.to_csv(output_path, index=False)

    # Print summary
    print(f"\n[OK] Token mapping table generated")
    print(f"  Total rows: {len(df)}")
    print(f"  Categories: {dict(df['category'].value_counts())}")
    print(f"  Output: {output_path}")

    # Print preview
    print(f"\nPreview (first 5 rows):")
    print(df.head().to_string())

    return df


if __name__ == "__main__":
    main()
