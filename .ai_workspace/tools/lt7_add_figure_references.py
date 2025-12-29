"""
LT-7 Figure Reference Integration Script

Systematically adds narrative figure references throughout the research paper
to meet academic publication standards.

Author: Claude Code
Date: December 21, 2025
"""

import re
from pathlib import Path

# Define figure reference insertion rules
REFERENCE_RULES = [
    # Section 7.2 - Transient Response
    {
        "search": "**Key Finding:** STA SMC achieves fastest settling (1.82s, 16% faster than Classical) and lowest overshoot (2.3%, 60% better than Classical), validating theoretical finite-time convergence advantage.",
        "replace": "**Key Finding:** STA SMC achieves fastest settling (1.82s, 16% faster than Classical) and lowest overshoot (2.3%, 60% better than Classical), as shown in Figure 7.2, validating theoretical finite-time convergence advantage."
    },
    {
        "search": "**Performance Ranking (Settling Time):**",
        "replace": "**Performance Ranking (Settling Time, see Figure 7.2 left panel):**"
    },
    {
        "search": "**Statistical Validation:** Bootstrap 95% CIs confirm STA significantly outperforms others (non-overlapping intervals).",
        "replace": "**Statistical Validation:** Bootstrap 95% CIs confirm STA significantly outperforms others (non-overlapping intervals, illustrated in Figure 7.2 error bars)."
    },

    # Section 7.3 - Chattering Analysis
    {
        "search": "**Key Finding:** STA SMC achieves 74% chattering reduction vs Classical SMC (index 2.1 vs 8.2), validating continuous control law advantage.",
        "replace": "**Key Finding:** STA SMC achieves 74% chattering reduction vs Classical SMC (index 2.1 vs 8.2), as shown in Figure 7.3 (left panel), validating continuous control law advantage."
    },
    {
        "search": "**FFT Analysis:** STA shows dominant low-frequency content (<10 Hz), while Classical and Adaptive exhibit significant high-frequency components (30-40 Hz) characteristic of boundary layer switching.",
        "replace": "**FFT Analysis:** STA shows dominant low-frequency content (<10 Hz), while Classical and Adaptive exhibit significant high-frequency components (30-40 Hz) characteristic of boundary layer switching (illustrated in Figure 7.3 right panel)."
    },
    {
        "search": "**Practical Implications:**\n- STA: Minimal actuator wear, quieter operation, suitable for precision applications\n- Classical: Moderate chattering acceptable for industrial use\n- Adaptive: Higher wear requires robust actuators",
        "replace": "**Practical Implications (based on Figure 7.3 chattering index analysis):**\n- STA: Minimal actuator wear, quieter operation, suitable for precision applications\n- Classical: Moderate chattering acceptable for industrial use\n- Adaptive: Higher wear requires robust actuators"
    },

    # Section 7.4 - Energy Efficiency
    {
        "search": "**Key Finding:** STA SMC most energy-efficient (11.8J baseline for 10s simulation), with continuous control law minimizing wasted effort.",
        "replace": "**Key Finding:** STA SMC most energy-efficient (11.8J baseline for 10s simulation), as shown in Figure 7.4 (left panel), with continuous control law minimizing wasted effort."
    },
    {
        "search": "**Hardware Implications:** All controllers <15J typical for 10s stabilization, safe for 250W actuators.",
        "replace": "**Hardware Implications:** All controllers <15J typical for 10s stabilization, safe for 250W actuators (see Figure 7.4 for total energy and peak power comparison)."
    },

    # Section 8 integrations will continue...
]

def add_figure_references(file_path: Path, output_path: Path = None):
    """Add figure references to research paper."""

    if output_path is None:
        output_path = file_path

    # Read file
    content = file_path.read_text(encoding='utf-8')

    # Track changes
    changes_made = 0

    # Apply each reference rule
    for rule in REFERENCE_RULES:
        if rule["search"] in content:
            content = content.replace(rule["search"], rule["replace"])
            changes_made += 1
            print(f"[OK] Added reference: {rule['replace'][:80]}...")
        else:
            print(f"[SKIP] Pattern not found: {rule['search'][:80]}...")

    # Write updated content
    output_path.write_text(content, encoding='utf-8')

    print(f"\n[INFO] Total changes: {changes_made}")
    print(f"[INFO] Output written to: {output_path}")

    return changes_made

if __name__ == "__main__":
    paper_path = Path("D:/Projects/main/.artifacts/research/papers/LT7_journal_paper/LT7_RESEARCH_PAPER.md")

    if paper_path.exists():
        changes = add_figure_references(paper_path)
        print(f"\n[DONE] Figure reference integration complete ({changes} references added)")
    else:
        print(f"[ERROR] File not found: {paper_path}")
