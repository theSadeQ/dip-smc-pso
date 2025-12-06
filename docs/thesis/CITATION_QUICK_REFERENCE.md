# LaTeX Citation Quick Reference

**Purpose**: Fast reference for common citation patterns in thesis writing

**Target**: Thesis authors using BibTeX/natbib/biblatex

---

## Basic Citation Commands

### Standard Citations

```latex
% Basic citation (Author, Year)
\cite{Levant2007}
→ Output: (Levant, 2007)

% Multiple citations
\cite{Levant2007,Khalil2002,Slotine1983}
→ Output: (Levant, 2007; Khalil, 2002; Slotine, 1983)

% Citation in text
As shown by \citet{Levant2007}, the algorithm...
→ Output: As shown by Levant (2007), the algorithm...

% Parenthetical citation
The super-twisting algorithm \citep{Levant2007} is...
→ Output: The super-twisting algorithm (Levant, 2007) is...
```

---

## Citations with Page Numbers

### Single Page

```latex
\cite[p.~42]{Levant2007}
→ Output: (Levant, 2007, p. 42)

% Note: Always use ~ (non-breaking space) between p. and number
% Correct: p.~42
% Wrong: p. 42
```

### Page Range

```latex
\cite[pp.~42--47]{Levant2007}
→ Output: (Levant, 2007, pp. 42-47)

% Note: Use -- (en-dash) for ranges, not - (hyphen)
% Correct: pp.~42--47
% Wrong: pp. 42-47 or pp.~42-47
```

### Multiple Discontinuous Pages

```latex
\cite[pp.~42, 57, 63]{Levant2007}
→ Output: (Levant, 2007, pp. 42, 57, 63)

\cite[pp.~42--47, 52, 63--65]{Levant2007}
→ Output: (Levant, 2007, pp. 42-47, 52, 63-65)
```

---

## Citations with Sections/Chapters

### Section

```latex
\cite[Sec.~3]{Levant2007}
→ Output: (Levant, 2007, Sec. 3)

\cite[Sec.~3.2]{Levant2007}
→ Output: (Levant, 2007, Sec. 3.2)

% With page numbers
\cite[Sec.~3, pp.~42--47]{Levant2007}
→ Output: (Levant, 2007, Sec. 3, pp. 42-47)
```

### Chapter

```latex
\cite[Ch.~2]{Khalil2002}
→ Output: (Khalil, 2002, Ch. 2)

\cite[Chs.~2--3]{Khalil2002}
→ Output: (Khalil, 2002, Chs. 2-3)
```

### Subsection

```latex
\cite[Subsec.~3.2.1]{Levant2007}
→ Output: (Levant, 2007, Subsec. 3.2.1)
```

---

## Citations with Equations

### Single Equation

```latex
\cite[Eq.~(7)]{Levant2007}
→ Output: (Levant, 2007, Eq. (7))

% Alternative (some journals)
\cite[Eq.~7]{Levant2007}
→ Output: (Levant, 2007, Eq. 7)
```

### Equation Range

```latex
\cite[Eqs.~(7)--(9)]{Levant2007}
→ Output: (Levant, 2007, Eqs. (7)-(9))
```

### Equation with Page

```latex
\cite[Eq.~(7), p.~42]{Levant2007}
→ Output: (Levant, 2007, Eq. (7), p. 42)
```

---

## Citations with Theorems/Lemmas

### Theorem

```latex
\cite[Theorem~1]{Levant2007}
→ Output: (Levant, 2007, Theorem 1)

\cite[Theorem~1, p.~42]{Levant2007}
→ Output: (Levant, 2007, Theorem 1, p. 42)
```

### Lemma

```latex
\cite[Lemma~2]{Khalil2002}
→ Output: (Khalil, 2002, Lemma 2)
```

### Corollary

```latex
\cite[Corollary~3]{Khalil2002}
→ Output: (Khalil, 2002, Corollary 3)
```

### Proposition

```latex
\cite[Proposition~4]{Khalil2002}
→ Output: (Khalil, 2002, Proposition 4)
```

---

## Citations with Figures/Tables

### Figure

```latex
\cite[Fig.~3]{Levant2007}
→ Output: (Levant, 2007, Fig. 3)

\cite[Fig.~3, p.~583]{Levant2007}
→ Output: (Levant, 2007, Fig. 3, p. 583)

% Multiple figures
\cite[Figs.~3--5]{Levant2007}
→ Output: (Levant, 2007, Figs. 3-5)
```

### Table

```latex
\cite[Table~2]{Quanser2020}
→ Output: (Quanser, 2020, Table 2)

\cite[Table~2, p.~34]{Quanser2020}
→ Output: (Quanser, 2020, Table 2, p. 34)
```

---

## Citations with Algorithms

```latex
\cite[Algorithm~1]{Kennedy1995}
→ Output: (Kennedy, 1995, Algorithm 1)

\cite[Algorithm~1, pp.~12--13]{Kennedy1995}
→ Output: (Kennedy, 1995, Algorithm 1, pp. 12-13)
```

---

## Advanced Citation Patterns

### Multiple Different Citations

```latex
% Different sources with different page numbers
\cite[p.~42]{Levant2007}, \cite[Ch.~3]{Khalil2002}
→ Output: (Levant, 2007, p. 42), (Khalil, 2002, Ch. 3)
```

### Citation with Custom Text

```latex
% See also
\cite[see also][pp.~42--47]{Levant2007}
→ Output: (see also Levant, 2007, pp. 42-47)

% e.g.
\cite[e.g.,][]{Levant2007,Khalil2002}
→ Output: (e.g., Levant, 2007; Khalil, 2002)

% cf. (compare)
\cite[cf.][]{Levant2007}
→ Output: (cf. Levant, 2007)
```

### Citing Appendix

```latex
\cite[Appendix~A]{Levant2007}
→ Output: (Levant, 2007, Appendix A)

\cite[Appendix~A, pp.~92--95]{Levant2007}
→ Output: (Levant, 2007, Appendix A, pp. 92-95)
```

---

## Common Use Cases in Thesis

### Background/Literature Review

```latex
% General background
Sliding mode control has been widely studied
\citep{Utkin1977,Slotine1983,Levant2007}.

% Specific concept introduction
The super-twisting algorithm \citep[pp.~579--582]{Levant2007} is
a second-order sliding mode controller.

% Comparison
While \citet{Utkin1977} introduced classical SMC,
\citet{Levant2007} extended it to higher-order variants.
```

### Theoretical Development

```latex
% Theorem citation
Finite-time convergence is guaranteed by homogeneity
\citep[Theorem~1, p.~578]{Levant2007}.

% Equation reference
The controller is defined as \citep[Eq.~(15), p.~581]{Levant2007}:
\begin{equation}
  u = -\alpha \frac{\dot{\sigma} + \beta|\sigma|^{1/2}\text{sign}\,\sigma}
               {|\dot{\sigma}| + \beta|\sigma|^{1/2}}
\end{equation}
```

### Implementation/Methods

```latex
% Algorithm reference
The PSO algorithm \citep[Algorithm~1]{Kennedy1995} was implemented
with the following parameters...

% Parameters from literature
System parameters were taken from the hardware manual
\citep[Table~2, p.~34]{Quanser2020}.
```

### Results/Validation

```latex
% Figure comparison
Our simulation results (Fig.~\ref{fig:phase}) show similar
behavior to \citet[Fig.~3, p.~583]{Levant2007}.

% Quantitative comparison
The settling time of 2.3 seconds matches the theoretical
prediction \citep[p.~584]{Levant2007}.
```

---

## Typography Rules

### Non-Breaking Spaces (~)

**Always use ~ before:**
- Numbers: `p.~42`, `Fig.~3`, `Eq.~(7)`
- Abbreviations: `Sec.~3`, `Ch.~2`, `Theorem~1`

**Why**: Prevents line breaks between abbreviation and number.

```latex
% Correct
\cite[p.~42]{Author}
\cite[Fig.~3]{Author}
\cite[Theorem~1, p.~42]{Author}

% Wrong (may break across lines)
\cite[p. 42]{Author}
\cite[Fig. 3]{Author}
```

### En-Dashes (--)

**Use for ranges:**

```latex
% Correct
pp.~42--47
Eqs.~(7)--(9)
Figs.~3--5

% Wrong
pp.~42-47  (hyphen, too short)
pp.~42—47  (em-dash, too long)
```

### Parentheses

**Equation numbers always in parentheses:**

```latex
% Correct
Eq.~(7)
Eqs.~(7)--(9)

% Sometimes acceptable (depends on journal)
Eq.~7
```

---

## BibTeX Entry Verification

### Essential Fields

```bibtex
@article{Levant2007,
  author  = {Arie Levant},              % Required
  title   = {Title of Paper},           % Required
  journal = {Journal Name},             % Required
  year    = {2007},                     % Required
  volume  = {53},                       % Highly recommended
  number  = {9},                        % Recommended
  pages   = {1--10},                    % Recommended
  doi     = {10.1109/TAC.2007.xxxxxx}  % Highly recommended
}

@book{Khalil2002,
  author    = {Hassan K. Khalil},       % Required
  title     = {Nonlinear Systems},      % Required
  publisher = {Prentice Hall},          % Required
  year      = {2002},                   % Required
  edition   = {3rd},                    % Recommended
  isbn      = {xxx-x-xxx-xxxxx-x}      % Optional
}
```

---

## Common Mistakes to Avoid

### 1. Missing Non-Breaking Spaces

```latex
% Wrong
\cite[p. 42]{Author}  % May break: "...(Author, 2007, p.\n42)"

% Correct
\cite[p.~42]{Author}  % Keeps together: "...(Author, 2007, p. 42)"
```

### 2. Using Hyphen Instead of En-Dash

```latex
% Wrong
\cite[pp.~42-47]{Author}  % Hyphen

% Correct
\cite[pp.~42--47]{Author}  % En-dash
```

### 3. Inconsistent Abbreviations

```latex
% Pick ONE style and stick to it:

% Style 1 (with periods)
Sec.~3, Fig.~5, Eq.~(7), Ch.~2

% Style 2 (without periods, some journals)
Sec 3, Fig 5, Eq (7), Ch 2

% NEVER mix within same thesis
```

### 4. Missing Page Numbers for Specific Claims

```latex
% Weak
The algorithm converges in finite time \cite{Levant2007}.

% Better (proves you read it)
The algorithm converges in finite time \cite[Theorem~1, p.~578]{Levant2007}.
```

### 5. Over-Citing

```latex
% Too much
The super-twisting algorithm \cite{Levant2007} is a second-order
sliding mode controller \cite{Levant2007} that provides finite-time
convergence \cite{Levant2007}.

% Better
The super-twisting algorithm \cite{Levant2007} is a second-order
sliding mode controller that provides finite-time convergence.
```

---

## Package Requirements

### natbib (recommended)

```latex
\usepackage{natbib}
\bibliographystyle{plainnat}  % or abbrvnat, unsrtnat

% Provides: \citep{}, \citet{}, \citeauthor{}, \citeyear{}
```

### biblatex (alternative)

```latex
\usepackage[style=authoryear,backend=biber]{biblatex}
\addbibresource{references.bib}

% Provides: \parencite{}, \textcite{}, \autocite{}
```

---

## Quick Command Reference Table

| Citation Type | Command | Example Output |
|---------------|---------|----------------|
| Basic | `\cite{Author2020}` | (Author, 2020) |
| In-text | `\citet{Author2020}` | Author (2020) |
| Parenthetical | `\citep{Author2020}` | (Author, 2020) |
| Page | `\cite[p.~42]{Author2020}` | (Author, 2020, p. 42) |
| Pages | `\cite[pp.~42--47]{Author2020}` | (Author, 2020, pp. 42-47) |
| Section | `\cite[Sec.~3]{Author2020}` | (Author, 2020, Sec. 3) |
| Chapter | `\cite[Ch.~2]{Author2020}` | (Author, 2020, Ch. 2) |
| Equation | `\cite[Eq.~(7)]{Author2020}` | (Author, 2020, Eq. (7)) |
| Theorem | `\cite[Theorem~1]{Author2020}` | (Author, 2020, Theorem 1) |
| Figure | `\cite[Fig.~3]{Author2020}` | (Author, 2020, Fig. 3) |
| Table | `\cite[Table~2]{Author2020}` | (Author, 2020, Table 2) |
| Algorithm | `\cite[Algorithm~1]{Author2020}` | (Author, 2020, Algorithm 1) |

---

## AI-Assisted Citation Workflow

### Get Ready-to-Use Citations from AI

```
You: "Find the super-twisting algorithm in Levant2007"

Claude: "Equation (15), page 581

LaTeX citation:
\cite[Eq.~(15), p.~581]{Levant2007}

Usage:
The quasi-continuous controller \cite[Eq.~(15), p.~581]{Levant2007}
is defined as..."
```

**Benefit**: No manual PDF navigation, instant LaTeX-formatted citations

---

## Checklist for Citation Quality

### Before Submitting Thesis

- [ ] All citations have page numbers for specific claims
- [ ] Non-breaking spaces used consistently (`~`)
- [ ] En-dashes used for ranges (`--`)
- [ ] Abbreviation style consistent throughout
- [ ] All BibTeX entries complete (author, title, year, journal/publisher)
- [ ] No over-citing (multiple cites for same point)
- [ ] Citations match claims (don't cite if you didn't read it)
- [ ] All cited works listed in references.bib
- [ ] No LaTeX errors in citations (check log file)

---

## See Also

- [AI Citation Workflow](AI_CITATION_WORKFLOW.md) - How to use AI for citations
- `thesis/citation_tracking/INDEX.md` - All tracked PDFs
- `thesis/references.bib` - BibTeX database

---

**Last Updated**: 2025-12-06

**Quick Start**: Copy-paste citation commands directly into your thesis LaTeX file!
