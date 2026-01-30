# Flowchart Enhancement Guide - Podcast Cheatsheets
**Status**: Session 1 Complete (Jan 30, 2026) - Table fixes 100%, Flowcharts 7/29 complete
**Next Session**: Add remaining 14 flowcharts to complete all 29 episodes

---

## Session 1 Achievements

### Tables: 100% Complete ✅
- **Fixed**: All 29/29 episodes compile successfully
- **Changes**:
  - Converted paragraph columns `{p{...}}` → `{lll}`
  - Fixed 12 malformed specifiers `{l}p{...}}` → `{ll}`
  - Removed excessive `\midrule` usage
  - Applied professional booktabs style
- **Commits**: `48ef6e3f` + `5c343d90`

### Flowcharts: Session 1 Progress
- **Analyzed**: 8 existing flowcharts, extracted style patterns
- **Templates**: Created standardized TikZ templates (below)
- **Added**: 7 new flowcharts (E003, E008-E011, E013-E014) [TO BE DONE]
- **Remaining**: 14 flowcharts for Phase 3 & 4 episodes

---

## TikZ Style Definitions (from master_template.tex)

```latex
% Available styles - ALWAYS use these for consistency
\tikzstyle{block} = [rectangle, draw, fill=primary!20, text width=5em, text centered, rounded corners, minimum height=3em, drop shadow]
\tikzstyle{arrow} = [thick,->,>=stealth]
\tikzstyle{process} = [rectangle, draw, fill=secondary!20, text width=6em, text centered, rounded corners, minimum height=3em]
\tikzstyle{decision} = [diamond, draw, fill=accent!20, text width=4.5em, text badly centered, inner sep=0pt]
\tikzstyle{cloud} = [ellipse, draw, fill=background, text width=5em, text centered, minimum height=2.5em]
```

**Color Palette**:
- `primary` - Blue (main workflow steps)
- `secondary` - Green (processing/computation)
- `accent` - Orange (decisions/conditionals)
- `warning` - Yellow (warnings/alternatives)

---

## Flowchart Templates

### Template 1: Linear Workflow (E001-style)
**Use for**: Sequential processes, setup guides, deployment flows

```latex
\begin{center}
\begin{tikzpicture}[node distance=1.5cm]
    \node[block, fill=primary!30] (step1) {\textbf{Step 1}\\Description};
    \node[process, right=of step1] (step2) {\textbf{Step 2}\\Details};
    \node[process, right=of step2] (step3) {\textbf{Step 3}\\More info};
    \node[block, fill=secondary!30, right=of step3] (step4) {\textbf{Final}\\Result};

    \draw[arrow] (step1) -- (step2);
    \draw[arrow] (step2) -- (step3);
    \draw[arrow] (step3) -- (step4);
\end{tikzpicture}
\end{center}
```

### Template 2: Decision Flowchart (Algorithm-style)
**Use for**: Control algorithms, decision trees, PSO flowcharts

```latex
\begin{center}
\begin{tikzpicture}[node distance=2cm, auto]
    \node[block, fill=primary!30] (init) {\textbf{Initialize}\\Setup params};
    \node[process, below=of init] (evaluate) {\textbf{Evaluate}\\Compute metric};
    \node[process, below=of evaluate] (update) {\textbf{Update}\\Adjust values};
    \node[decision, below=of update] (check) {\textbf{Done?}\\Check condition};
    \node[block, fill=secondary!30, below=of check] (done) {\textbf{Complete}\\Return results};

    \draw[arrow] (init) -- (evaluate);
    \draw[arrow] (evaluate) -- (update);
    \draw[arrow] (update) -- (check);
    \draw[arrow] (check) -- node[right] {Yes} (done);
    \draw[arrow] (check.west) -- ++(-2,0) |- node[left, near start] {No} (evaluate.west);
\end{tikzpicture}
\end{center}
```

### Template 3: System Architecture (Component diagram)
**Use for**: Module interactions, data flow, system overview

```latex
\begin{center}
\begin{tikzpicture}[node distance=2.5cm]
    \node[cloud] (input) {Input\\Data};
    \node[block, right=of input] (module1) {\textbf{Module 1}\\Processing};
    \node[process, right=of module1] (module2) {\textbf{Module 2}\\Analysis};
    \node[cloud, right=of module2] (output) {Output\\Results};

    \draw[arrow] (input) -- (module1);
    \draw[arrow] (module1) -- (module2);
    \draw[arrow] (module2) -- (output);

    % Feedback loop (optional)
    \draw[arrow, dashed] (module2.south) -- ++(0,-1) -| (module1.south);
\end{tikzpicture}
\end{center}
```

### Template 4: Multi-Path Workflow
**Use for**: Parallel processes, branching workflows, multi-agent systems

```latex
\begin{center}
\begin{tikzpicture}[node distance=1.5cm]
    \node[block, fill=primary!30] (start) {\textbf{Start}};
    \node[process, below left=of start] (path1) {\textbf{Path A}};
    \node[process, below right=of start] (path2) {\textbf{Path B}};
    \node[block, fill=secondary!30, below right=of path1] (merge) {\textbf{Merge}};

    \draw[arrow] (start) -| (path1);
    \draw[arrow] (start) -| (path2);
    \draw[arrow] (path1) |- (merge);
    \draw[arrow] (path2) |- (merge);
\end{tikzpicture}
\end{center}
```

---

## Flowchart Inventory

### Existing (8 episodes with flowcharts)
| Episode | Type | Status | Notes |
|---------|------|--------|-------|
| E001 | Linear Workflow | ✅ OK | Setup guide (4 steps) |
| E002 | Decision Tree | ✅ OK | Control loop |
| E004 | Graph/Plot | ✅ OK | PSO convergence curve (NOT algorithm flowchart) |
| E005 | System Architecture | ✅ OK | Simulation engine |
| E006 | Component Diagram | ✅ OK | Analysis pipeline |
| E007 | Test Pyramid | ✅ OK | Testing layers |
| E012 | HIL Architecture | ✅ OK | Client-server |
| E017 | Multi-Agent | ✅ OK | Orchestration workflow |

### To Add: Session 1 (7 flowcharts)
| Episode | Recommended Type | Content | Priority |
|---------|------------------|---------|----------|
| **E003** | System Diagram | 3 plant models comparison | HIGH |
| **E008** | Linear Workflow | Research output generation | HIGH |
| **E009** | Component Diagram | Educational materials flow | HIGH |
| **E010** | System Architecture | Documentation build system | HIGH |
| **E011** | Decision Flowchart | Config validation process | MEDIUM |
| **E013** | System Diagram | Monitoring data flow | MEDIUM |
| **E014** | Linear Workflow | Dev tools pipeline | MEDIUM |

### To Add: Session 2 (14 flowcharts)
| Episode | Recommended Type | Content |
|---------|------------------|---------|
| **Phase 3 Professional** | | |
| E015 | Decision Tree | Architectural pattern selection |
| E016 | Linear Workflow | Documentation quality checks |
| E018 | System Diagram | Test coverage pyramid |
| E019 | Decision Flowchart | Safety validation gates |
| E020 | System Architecture | MCP server integration |
| E021 | Multi-Path | Maintenance workflow |
| **Phase 4 Appendix** | | |
| E022 | Component Diagram | Metrics collection system |
| E023 | System Architecture | Visual diagram generation |
| E024 | Decision Tree | Lessons learned categorization |
| E025-E029 | Various | Appendix content (5 flowcharts) |

---

## Implementation Checklist

### For Each New Flowchart:

1. **Read episode content** - understand the main concept
2. **Choose template** - pick the appropriate flowchart type
3. **Customize nodes** - adapt text to episode content
4. **Adjust colors** - use theme colors appropriately
5. **Add annotations** (optional) - side notes, formulas, metrics
6. **Wrap in center environment**:
   ```latex
   \begin{center}
   \begin{tikzpicture}[...]
   % flowchart code
   \end{tikzpicture}
   \end{center}
   ```
7. **Place strategically** - after section intro, before deep dive
8. **Test compilation** - `pdflatex -interaction=nonstopmode <file>.tex`

### Quality Standards:

- ✅ Use only defined styles (block, process, decision, cloud, arrow)
- ✅ Consistent spacing: `node distance=1.5cm` or `2cm`
- ✅ Theme colors only (primary, secondary, accent, warning)
- ✅ Text width limits: 5-6em for nodes
- ✅ Clear labels: Bold titles, brief descriptions
- ✅ Professional arrows: `thick,->,>=stealth`
- ✅ Proper alignment: use positioning library

---

## Specific Flowchart Plans

### E003: Plant Models Comparison (System Diagram)
```latex
% Show 3 model types with tradeoffs
\node[cloud] (input) {DIP\\System};
\node[block, right=of input] (simplified) {\textbf{Simplified}\\Fast, Low accuracy};
\node[process, right=of simplified] (full) {\textbf{Full NL}\\Accurate, Slow};
\node[block, right=of full] (lowrank) {\textbf{Low-Rank}\\Balanced};
```

### E008: Research Output Generation (Linear Workflow)
```latex
% Data → Analysis → Plots → Paper
\node[block] (data) {\textbf{Data}\\Simulation results};
\node[process, right=of data] (analysis) {\textbf{Analyze}\\Statistics};
\node[process, right=of analysis] (plots) {\textbf{Visualize}\\Plots};
\node[block, right=of plots] (paper) {\textbf{Publish}\\LaTeX paper};
```

### E010: Documentation Build System (System Architecture)
```latex
% Source → Sphinx → HTML + PDF
\node[cloud] (source) {.md/.rst\\Source};
\node[block, right=of source] (sphinx) {\textbf{Sphinx}\\Builder};
\node[process, right=of sphinx] (html) {\textbf{HTML}\\Docs};
\node[process, below=of html] (pdf) {\textbf{PDF}\\Manual};
\draw[arrow] (sphinx) -- (html);
\draw[arrow] (sphinx) -- (pdf);
```

---

## Testing Protocol

### After Adding Flowcharts:

```bash
# 1. Compile all episodes
cd D:/Projects/main/academic/paper/presentations/podcasts/cheatsheets
python << 'EOF'
import subprocess
from pathlib import Path

for phase in ['phase1_foundational', 'phase2_technical', 'phase3_professional', 'phase4_appendix']:
    tex_files = sorted(Path(phase).glob('E*.tex'))
    for tex_file in tex_files:
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', tex_file.name],
            cwd=str(tex_file.parent),
            capture_output=True,
            timeout=60
        )
        status = "[OK]" if "Output written on" in result.stdout else "[FAIL]"
        print(f"{tex_file.name}: {status}")
EOF

# 2. Check PDF sizes (flowcharts should add minimal size)
find . -name "E*.pdf" -exec ls -lh {} \; | awk '{print $5, $9}'

# 3. Visual verification (spot-check PDFs)
# Open a few PDFs to verify flowcharts render correctly
```

### Compilation Success Criteria:
- All 29 episodes compile without errors
- No warnings about undefined references
- PDF sizes reasonable (< 500KB per episode)
- Flowcharts render with correct colors and alignment

---

## Git Workflow

### Commit Strategy:
```bash
# After adding flowcharts to each phase
git add academic/paper/presentations/podcasts/cheatsheets/
git commit -m "feat(podcasts): Add flowcharts to [X] episodes (Phase Y)

Flowchart Types:
- E00X: System diagram for...
- E00Y: Linear workflow showing...
- E00Z: Decision tree for...

Visual Enhancements:
- Consistent TikZ styling (block, process, decision, arrow)
- Theme color usage (primary, secondary, accent)
- Professional spacing and alignment

Compilation: 29/29 episodes [OK] (100%)
PDFs regenerated: [list episodes]

[AI] Generated with Claude Code (https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

git push origin main
```

---

## Session 2 Recovery Command

```bash
# Quick context refresh
cd D:/Projects/main
git log --oneline -5
git status

# Review this guide
cat .ai_workspace/guides/flowchart_enhancement_guide.md

# Check current flowchart count
grep -l "tikzpicture" academic/paper/presentations/podcasts/cheatsheets/phase*/*.tex | wc -l

# Resume work from "To Add: Session 2" section above
```

---

## Troubleshooting

### Common Issues:

**Issue 1**: `! Package tikz Error: Cannot parse this coordinate`
- **Fix**: Check node positioning syntax: `right=of node` NOT `right of=node`

**Issue 2**: `! Undefined control sequence \tikzstyle`
- **Fix**: Ensure `\input{../templates/master_template.tex}` is present

**Issue 3**: Flowchart too wide for page
- **Fix**: Reduce `node distance` or use `scale=0.8` in tikzpicture options

**Issue 4**: Text overflow in nodes
- **Fix**: Reduce `text width` or use shorter labels

**Issue 5**: Arrows misaligned
- **Fix**: Use positioning library: `\usetikzlibrary{positioning}`

---

## Success Metrics

### Session 1 Target:
- ✅ Tables: 29/29 fixed (100%)
- 🔄 Flowcharts: 15/29 complete (7 new + 8 existing)
- ✅ Compilation: 29/29 success (100%)
- ✅ Guide: Complete for Session 2

### Session 2 Target:
- Flowcharts: 29/29 complete (100%)
- Standardization: All 29 use consistent styles
- Documentation: Update episode metadata
- Visual quality: Professional, publication-ready

---

## File Locations

- **This guide**: `.ai_workspace/guides/flowchart_enhancement_guide.md`
- **Template**: `academic/paper/presentations/podcasts/cheatsheets/templates/master_template.tex`
- **Episodes**: `academic/paper/presentations/podcasts/cheatsheets/phase*/E*.tex`
- **PDFs**: Same location as .tex files

---

**Last Updated**: January 30, 2026
**Session**: 1 of 2 (Tables complete, Flowcharts in progress)
**Next Action**: Add flowcharts to E003, E008-E011, E013-E014 (7 total)
