# LT-7 Conference Paper LaTeX Conversion Guide

**Status:** 20% Complete (Infrastructure + Abstract + Introduction)
**Remaining Work:** 12-15 hours
**Target:** IEEE Journal format submission-ready LaTeX

---

## Completion Status

### ✓ Complete (20%)
- [x] LaTeX infrastructure (main.tex with IEEE template)
- [x] Abstract converted (1,621 characters)
- [x] Introduction converted (6,654 characters, 68 lines)
- [x] Bibliography started (25 citations formatted, 43 remaining)
- [x] Section placeholders created (9 sections)
- [x] Conversion automation script (`convert_markdown_to_latex.py`)

### ⏸ Pending (80%)
- [ ] Section 2: System Model (~400 lines, 2-3 hours)
- [ ] Section 3: Controller Design (~600 lines, 3-4 hours)
- [ ] Section 4: Stability Analysis (~500 lines, 2-3 hours)
- [ ] Section 5: PSO Optimization (~300 lines, 1-2 hours)
- [ ] Section 6: Experimental Setup (~200 lines, 1 hour)
- [ ] Section 7: Performance Results (~400 lines, 2 hours)
- [ ] Section 8: Robustness Analysis (~300 lines, 1-2 hours)
- [ ] Section 9: Discussion (~200 lines, 1 hour)
- [ ] Section 10: Conclusion (~100 lines, 30 minutes)
- [ ] Complete bibliography (43 citations, 1 hour)
- [ ] Extract and format 14 figures (2 hours)
- [ ] Convert 13 tables to LaTeX booktabs format (3 hours)

---

## Quick Start

### 1. Run Automated Conversion (Partial)
```bash
cd research/conference_paper
python convert_markdown_to_latex.py
```

**What it does:**
- Extracts sections 2-10 from `LT7_RESEARCH_PAPER.md`
- Converts markdown formatting to LaTeX
- Handles citations [1,2,3] -> \cite{ref1,ref2,ref3}
- Converts headers, lists, bold/italic
- Outputs to `sections/*.tex`

**Limitations:**
- Tables require manual conversion
- Figures need extraction and placement
- Math equations need review
- Citations need proper BibTeX keys

### 2. Manual Refinement Required
After running the script, manually refine each section:

**For each section file:**
1. Review LaTeX formatting (ensure proper escaping)
2. Fix table conversions (use `booktabs` package)
3. Add figure references with correct labels
4. Verify math equations compile
5. Update citation keys to match `references.bib`

### 3. Complete Bibliography
**Current:** 25/68 citations (37%)
**Remaining:** 43 citations

**Process:**
1. Extract all `[1]` through `[68]` references from markdown
2. Search CrossRef/Google Scholar for BibTeX entries
3. Add to `references.bib` with proper keys
4. Update in-text citations to use new keys

**Automation available:**
```bash
# Extract all citation numbers from markdown
grep -oP '\[\d+\]' ../../analysis_reports/long_term/LT7_RESEARCH_PAPER.md | sort -u

# Use LT7_CROSSREF_REPORT.md for DOIs
# See: research/analysis_reports/long_term/LT7_CROSSREF_REPORT.md
```

### 4. Extract Figures
**Source:** `benchmarks/*.png` (14 figures at 300 DPI)
**Target:** `research/conference_paper/figures/*.pdf`

**Figures to extract:**
- Figure 5.1: PSO convergence curves
- Figure 5.2: MT-6 PSO comparison
- Figure 7.1: Computational efficiency
- Figure 7.2: Transient response (a) settling (b) overshoot
- Figure 7.3: Chattering (a) index (b) frequency
- Figure 7.4: Energy (a) total (b) peak
- Figure 7.5: Overall performance radar
- Figure 8.1: Model uncertainty tolerance
- Figure 8.2: Disturbance rejection
- Figure 8.3: PSO generalization failure
- Figure 8.4: Controller selection matrix
- Figure 9.1: Tradeoff scatter plots
- Figure 9.2: Design guidelines flowchart
- Figure 9.3: Computational overhead vs performance

**Conversion:**
```bash
# Convert PNG to PDF (300 DPI)
for fig in benchmarks/*.png; do
  convert -density 300 "$fig" "research/conference_paper/figures/$(basename $fig .png).pdf"
done
```

### 5. Convert Tables
**Tables:** 13 total (in markdown format)

**LaTeX booktabs template:**
```latex
\begin{table}[t]
\centering
\caption{Your caption here}
\label{tab:yourlabel}
\begin{tabular}{lrrr}
\toprule
Header1 & Header2 & Header3 & Header4 \\
\midrule
Row1 & 1.23 & 4.56 & 7.89 \\
Row2 & 2.34 & 5.67 & 8.90 \\
\bottomrule
\end{tabular}
\end{table}
```

**Tables to convert:**
- Table 1: Controller comparison matrix
- Table 2: Computational complexity
- Table 3: Performance metrics summary
- Table 4: PSO optimization results
- Table 5: Robustness analysis
- ... (8 more tables)

### 6. Build and Test
```bash
# Install LaTeX (if needed)
# Windows: MiKTeX or TeX Live
# Linux: sudo apt-get install texlive-full
# Mac: brew install --cask mactex

# Build paper
cd research/conference_paper
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

# View output
open main.pdf  # Mac
xdg-open main.pdf  # Linux
start main.pdf  # Windows
```

---

## Conversion Checklist

### Infrastructure ✓
- [x] main.tex created with IEEE template
- [x] sections/ directory with 11 files
- [x] references.bib started
- [x] figures/ directory created
- [x] tables/ directory created

### Content Conversion
- [x] Abstract (100%)
- [x] Introduction (100%)
- [ ] Section 2: System Model (0%)
- [ ] Section 3: Controller Design (0%)
- [ ] Section 4: Stability Analysis (0%)
- [ ] Section 5: PSO Optimization (0%)
- [ ] Section 6: Experimental Setup (0%)
- [ ] Section 7: Performance Results (0%)
- [ ] Section 8: Robustness Analysis (0%)
- [ ] Section 9: Discussion (0%)
- [ ] Section 10: Conclusion (0%)

### Bibliography
- [x] Infrastructure setup (100%)
- [x] First 25 citations (37%)
- [ ] Remaining 43 citations (0%)
- [ ] Citation key consistency check (0%)

### Figures
- [ ] Extract 14 PNG files (0%)
- [ ] Convert to PDF (0%)
- [ ] Add to LaTeX with captions (0%)
- [ ] Verify resolution (300 DPI) (0%)

### Tables
- [ ] Convert 13 tables to LaTeX (0%)
- [ ] Format with booktabs (0%)
- [ ] Add captions and labels (0%)

### Final Quality Checks
- [ ] Full compilation without errors
- [ ] All references cited
- [ ] All figures referenced
- [ ] All tables referenced
- [ ] Spell check
- [ ] Grammar check
- [ ] IEEE format compliance

---

## Time Estimates

| Task | Hours | Priority |
|------|-------|----------|
| Run conversion script | 0.5 | High |
| Manual section refinement (2-10) | 8-10 | High |
| Complete bibliography | 1 | High |
| Extract and convert figures | 2 | Medium |
| Convert tables | 3 | Medium |
| Build and debug LaTeX | 1 | High |
| Final proofreading | 2 | Low |
| **Total** | **17-19 hours** | |

---

## Known Issues and Workarounds

### Issue 1: Math Equation Formatting
**Problem:** Markdown inline math `$x^2$` may not convert properly
**Solution:** Manually review all equations in sections 4 (stability) and 5 (PSO)

### Issue 2: Citation Key Mismatches
**Problem:** Script uses `ref1`, `ref2`, but BibTeX has semantic keys
**Solution:** Run find-replace to update keys after completing bibliography

### Issue 3: Figure Placement
**Problem:** LaTeX float placement may differ from markdown
**Solution:** Use `[t]` (top), `[h]` (here), or `[!t]` (force top) as needed

### Issue 4: Table Alignment
**Problem:** Markdown tables use simple syntax, LaTeX needs column specs
**Solution:** Use online converter (tablesgenerator.com) then add booktabs

---

## Next Steps

1. **Immediate (30 min):** Run `convert_markdown_to_latex.py` to generate initial LaTeX
2. **Short-term (4-6 hours):** Manually refine sections 2-5 (critical technical content)
3. **Medium-term (3-4 hours):** Complete sections 6-10 and bibliography
4. **Final (2-3 hours):** Figures, tables, and compilation testing

---

**Document Version:** 1.0
**Last Updated:** 2025-12-16
**Status:** Infrastructure complete, content conversion 20%
**Estimated Completion:** 12-15 hours of focused work
