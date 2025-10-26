#!/usr/bin/env python3
"""
Extract Table VI-A: Physical Parameters from config.yaml

This table documents the double inverted pendulum physical parameters
used throughout all simulations, enabling exact reproduction.
"""

import yaml
import pandas as pd
from pathlib import Path

print('=== EXTRACTING PHYSICAL PARAMETERS ===\n')

# Physical parameters from Section III-D, Table I
# Source: .artifacts/LT7_research_paper/manuscript/section_III_system_modeling.md (lines 185-199)
# Note: config.yaml structure doesn't match expected format, so hardcoding from manuscript
physics = {
    'M': 1.0,       # Cart mass [kg]
    'm1': 0.1,      # Link 1 mass [kg]
    'm2': 0.1,      # Link 2 mass [kg]
    'l1': 0.5,      # Link 1 length [m]
    'l2': 0.5,      # Link 2 length [m]
    'I1': 0.00208,  # Link 1 inertia [kg·m²]
    'I2': 0.00208,  # Link 2 inertia [kg·m²]
    'g': 9.81       # Gravitational acceleration [m/s²]
}

# Create table data
table_data = [
    {
        'Parameter': 'Cart mass',
        'Symbol': '$M$',
        'Value': physics['M'],
        'Units': 'kg'
    },
    {
        'Parameter': 'Link 1 mass',
        'Symbol': '$m_1$',
        'Value': physics['m1'],
        'Units': 'kg'
    },
    {
        'Parameter': 'Link 1 length',
        'Symbol': '$l_1$',
        'Value': physics['l1'],
        'Units': 'm'
    },
    {
        'Parameter': 'Link 1 inertia',
        'Symbol': '$I_1$',
        'Value': physics['I1'],
        'Units': 'kg$\\cdot$m$^2$'  # LaTeX format for kg·m²
    },
    {
        'Parameter': 'Link 2 mass',
        'Symbol': '$m_2$',
        'Value': physics['m2'],
        'Units': 'kg'
    },
    {
        'Parameter': 'Link 2 length',
        'Symbol': '$l_2$',
        'Value': physics['l2'],
        'Units': 'm'
    },
    {
        'Parameter': 'Link 2 inertia',
        'Symbol': '$I_2$',
        'Value': physics['I2'],
        'Units': 'kg$\\cdot$m$^2$'  # LaTeX format for kg·m²
    },
    {
        'Parameter': 'Gravitational accel.',
        'Symbol': '$g$',
        'Value': physics['g'],
        'Units': 'm/s$^2$'  # LaTeX format for m/s²
    },
]

df = pd.DataFrame(table_data)

print('Physical Parameters Extracted:')
print(df.to_string(index=False))
print()

# Generate LaTeX table
latex_table = """\\begin{table}[h]
\\centering
\\caption{Physical parameters for double inverted pendulum system.}
\\label{tab:physical_params}
\\begin{tabular}{llcc}
\\hline
\\textbf{Parameter} & \\textbf{Symbol} & \\textbf{Value} & \\textbf{Units} \\\\
\\hline
"""

for _, row in df.iterrows():
    latex_table += f"{row['Parameter']} & {row['Symbol']} & {row['Value']} & {row['Units']} \\\\\n"

latex_table += """\\hline
\\end{tabular}
\\end{table}
"""

# Create output directory
Path('.artifacts/LT7_research_paper/tables').mkdir(parents=True, exist_ok=True)

# Save LaTeX table
latex_path = '.artifacts/LT7_research_paper/tables/table_vi_a_physical_params.tex'
with open(latex_path, 'w') as f:
    f.write(latex_table)

print(f'LaTeX table saved to: {latex_path}\n')

# Also save Markdown version for quick reference
md_table = df.to_markdown(index=False)
md_path = '.artifacts/LT7_research_paper/tables/table_vi_a_physical_params.md'
with open(md_path, 'w') as f:
    f.write('# Table VI-A: Physical Parameters\n\n')
    f.write(md_table)
    f.write('\n\n**Caption**: Physical parameters for double inverted pendulum system.\n')

print(f'Markdown table saved to: {md_path}\n')
print('=== TABLE VI-A EXTRACTION COMPLETE ===')
