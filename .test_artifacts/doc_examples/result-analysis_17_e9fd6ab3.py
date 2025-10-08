# Example from: docs\guides\how-to\result-analysis.md
# Index: 17
# Runnable: False
# Hash: e9fd6ab3

# Create metrics table for LaTeX
metrics_table = []
for ctrl, label in zip(controllers, labels):
    with open(f'results_{ctrl}.json') as f:
        metrics = json.load(f)['metrics']
        metrics_table.append([
            label,
            f"{metrics['ise']:.4f}",
            f"{metrics['itae']:.4f}",
            f"{metrics['settling_time']:.2f}",
            f"{metrics['overshoot']:.2f}"
        ])

# Generate LaTeX
latex = r"""\begin{table}[h]
\centering
\caption{Controller Performance Comparison}
\begin{tabular}{lcccc}
\hline
Controller & ISE & ITAE & Settling Time (s) & Overshoot (\%) \\
\hline
"""

for row in metrics_table:
    latex += " & ".join(row) + r" \\" + "\n"

latex += r"""\hline
\end{tabular}
\end{table}"""

print(latex)

# Save to file
with open('metrics_table.tex', 'w') as f:
    f.write(latex)