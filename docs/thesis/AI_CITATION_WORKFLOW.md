# AI-Assisted PDF Citation Workflow

**Purpose**: Systematic workflow for using Claude AI to extract, track, and cite content from research PDFs

**Status**: [OK] Operational (December 2025)

**Target Users**: Thesis authors needing precise section/page/equation citations

---

## Quick Start

### Method 1: Find Specific Content
```
You: "Find the super-twisting algorithm in Levant2007"

Claude will:
1. Read thesis/sources_archive/manuelly downloaded/levant2007.pdf
2. Search for super-twisting algorithm
3. Return: Section number, page number, equation numbers
4. Provide LaTeX citation: \cite[Sec.~4, pp.~579--582]{Levant2007}
```

### Method 2: Extract All Key Sections
```
You: "Extract all theorems from Levant2007 with page numbers"

Claude will:
1. Read the PDF
2. Find all theorems
3. Create a table with locations
4. Generate citation templates
```

### Method 3: Create Tracking Document
```
You: "Create usage tracking for Levant2007"

Claude will:
1. Generate citation_tracking/Levant2007_tracking.md
2. List all sections, theorems, equations
3. Add placeholders for "Used in thesis section X"
4. Include ready-to-use LaTeX citations
```

---

## Complete Workflow

### Step 1: Identify Citation Need

**During thesis writing, when you need to cite:**
- Specific theorem → "Find Lyapunov theorem in Khalil2002"
- Algorithm pseudocode → "Extract PSO algorithm from Kennedy1995"
- System parameters → "Find DIP parameters in Quanser2020"
- Equation → "Where is the super-twisting formula in Levant2007?"
- Figure/table → "Find phase portrait in Shtessel2014"

### Step 2: Request Extraction

**Ask Claude with natural language:**
```
"Find [topic] in [PDF_name]"
"Extract [content_type] from [PDF_name]"
"Where does [PDF_name] discuss [topic]?"
"Create citations for [topic] from [PDF_name]"
"Compare [topic] in [PDF1] vs [PDF2]"
```

### Step 3: Receive Structured Response

**Claude provides:**
1. **Exact location**: Section, page, line, equation number
2. **LaTeX citation**: Ready-to-paste format
3. **Content summary**: Key points from that section
4. **Citation template**: With proper formatting

**Example response:**
```
The super-twisting algorithm is in:
- Section 4, pages 579-582
- Equation (15), page 581

LaTeX citation:
\cite[Eq.~(15), p.~581]{Levant2007}

Content:
The quasi-continuous controller is defined as...
```

### Step 4: Track Usage

**Claude creates tracking file:**
```markdown
# Levant2007 Usage Tracking

## Section 4: Controller Design (pp. 579-582)
**Used in:** Thesis Section 3.4 (STA Controller Implementation)
**Citation:** `\cite[Sec.~4]{Levant2007}`
**Content:** Super-twisting algorithm, finite-time convergence

## Equation (15) (p. 581)
**Used in:** Thesis Section 3.4, Equation (3.12)
**Citation:** `\cite[Eq.~(15), p.~581]{Levant2007}`
**Content:** u = -α[σ̇ + β|σ|^(1/2)sign(σ)] / [|σ̇| + β|σ|^(1/2)]
```

### Step 5: Integrate into Thesis

**Copy-paste LaTeX citation:**
```latex
% In your thesis
The super-twisting controller \cite[Eq.~(15), p.~581]{Levant2007}
is continuous everywhere except the origin.
```

---

## Supported Citation Formats

### Page Numbers
```latex
\cite[p.~42]{Author2020}           % Single page
\cite[pp.~42--47]{Author2020}      % Page range
```

### Sections
```latex
\cite[Sec.~3]{Author2020}          % Single section
\cite[Sec.~3, pp.~42--47]{Author2020}  % Section + pages
\cite[Ch.~2]{Author2020}           % Chapter
```

### Equations
```latex
\cite[Eq.~(7)]{Author2020}         % Single equation
\cite[Eqs.~(7)--(9)]{Author2020}   % Equation range
\cite[Eq.~(7), p.~42]{Author2020}  % Equation + page
```

### Theorems/Lemmas
```latex
\cite[Theorem~1]{Author2020}
\cite[Lemma~2, p.~56]{Author2020}
\cite[Corollary~3]{Author2020}
```

### Figures/Tables
```latex
\cite[Fig.~3]{Author2020}
\cite[Table~2, p.~34]{Author2020}
\cite[Figs.~3--5]{Author2020}
```

### Algorithms
```latex
\cite[Algorithm~1]{Author2020}
\cite[Algorithm~1, pp.~12--13]{Author2020}
```

---

## Common Use Cases

### Use Case 1: Background Literature Review

**Scenario**: Writing Section 2.2 (Higher-Order Sliding Modes)

**Request**:
```
"Extract key concepts from Levant2007 Introduction for background section"
```

**Claude Response**:
```
Section 1 (pp. 576-577) covers:
1. 2-SMC for constraints with relative degree 2
2. Chattering avoidance
3. Homogeneity-based analysis

Citations:
- General background: \cite[pp.~576--577]{Levant2007}
- 2-SMC definition: \cite[Sec.~1]{Levant2007}
- Chattering: \cite[p.~576]{Levant2007}
```

### Use Case 2: Theoretical Proof

**Scenario**: Proving finite-time stability in Section 3.1

**Request**:
```
"Find the finite-time stability theorem in Levant2007"
```

**Claude Response**:
```
Theorem 1 (p. 578):
"Contractivity, finite-time stability, and asymptotic stability
are equivalent for homogeneous systems."

Citation:
\cite[Theorem~1, p.~578]{Levant2007}

Usage in thesis:
Finite-time convergence is guaranteed by homogeneity
\cite[Theorem~1, p.~578]{Levant2007}, which proves...
```

### Use Case 3: Algorithm Implementation

**Scenario**: Implementing STA controller in Section 3.4

**Request**:
```
"Extract the quasi-continuous STA controller equation from Levant2007"
```

**Claude Response**:
```
Equation (15), page 581:
u = -α[σ̇ + β|σ|^(1/2)sign(σ)] / [|σ̇| + β|σ|^(1/2)]

Citation:
\cite[Eq.~(15), p.~581]{Levant2007}

Latex for thesis:
The quasi-continuous controller \cite[Eq.~(15), p.~581]{Levant2007}
\begin{equation}
  u = -\alpha \frac{\dot{\sigma} + \beta|\sigma|^{1/2}\text{sign}\,\sigma}
               {|\dot{\sigma}| + \beta|\sigma|^{1/2}}
\end{equation}
```

### Use Case 4: Simulation Validation

**Scenario**: Comparing your results to literature in Section 5.2

**Request**:
```
"Find simulation results in Levant2007 for comparison"
```

**Claude Response**:
```
Section 5 (pp. 583-585), Figure 3 (p. 583):
- Phase trajectories showing finite-time convergence
- Accuracy: |σ| ~ τ²

Citations:
- General results: \cite[Sec.~5]{Levant2007}
- Specific figure: \cite[Fig.~3, p.~583]{Levant2007}

Usage:
Our simulation results (Fig. 5.2) match the phase trajectories
reported in \cite[Fig.~3, p.~583]{Levant2007}.
```

### Use Case 5: Multi-PDF Comparison

**Scenario**: Comparing STA variants across sources

**Request**:
```
"Compare super-twisting algorithm in Levant2007 vs Shtessel2014"
```

**Claude Response**:
```
Levant2007:
- Eq. (15), p. 581: Quasi-continuous form
- Section 4: Homogeneity-based analysis
- Citation: \cite[Eq.~(15)]{Levant2007}

Shtessel2014:
- Chapter 5: STA with adaptive gains
- Section 5.3: Disturbance rejection
- Citation: \cite[Ch.~5]{Shtessel2014}

Difference:
Levant focuses on homogeneity theory, Shtessel on practical adaptation.

Thesis usage:
While \cite{Levant2007} analyzes STA via homogeneity,
\cite[Ch.~5]{Shtessel2014} extends it with adaptive gains.
```

---

## features

### Feature 1: Batch Extraction

**Request**:
```
"Create tracking files for all PDFs in sources_archive"
```

**Claude will**:
1. Read all PDFs in `thesis/sources_archive/manuelly downloaded/`
2. Generate `citation_tracking/[Author][Year]_tracking.md` for each
3. Extract all sections, theorems, equations
4. Create master index

### Feature 2: Topic-Based Search

**Request**:
```
"Find all references to 'chattering' across all PDFs"
```

**Claude will**:
1. Search all PDFs
2. List occurrences with page numbers
3. Generate multi-source citations

### Feature 3: Citation Consistency Check

**Request**:
```
"Check citation consistency in thesis/main.tex"
```

**Claude will**:
1. Read your thesis LaTeX file
2. Verify all \cite{} references exist in thesis/references.bib
3. Check citation format consistency
4. Suggest missing page numbers

### Feature 4: BibTeX Integration

**Request**:
```
"Extract BibTeX entry from Levant2007 PDF"
```

**Claude will**:
1. Read PDF metadata
2. Extract: title, author, journal, year, pages, DOI
3. Generate BibTeX entry
4. Add to thesis/references.bib

---

## Directory Structure

```
thesis/
 sources_archive/
    manuelly downloaded/
        levant2007.pdf
        Khalil2002.pdf
        Kennedy1995.pdf
        ... (22 PDFs total)
 citation_tracking/
    INDEX.md                    # Master index of all PDFs
    Levant2007_tracking.md      # Per-PDF tracking
    Khalil2002_tracking.md
    ...
 references.bib                  # BibTeX database
 main.tex                        # Thesis LaTeX
```

---

## Example Workflows

### Workflow A: Starting a New Thesis Section

1. **Identify needed citations**: "I'm writing Section 2.2 on Higher-Order SMC"
2. **Request**: "Extract HOSMC overview from Levant2007 and Shtessel2014"
3. **Receive**: Structured comparison with page numbers
4. **Write thesis**: Copy-paste LaTeX citations
5. **Track**: Claude auto-updates tracking files

### Workflow B: Proving a Theorem

1. **Identify theorem**: "Need Lyapunov stability proof"
2. **Request**: "Find Lyapunov theorem for SMC in Khalil2002"
3. **Receive**: Theorem statement, page, section
4. **Cite in proof**: `\cite[Theorem~4.1, p.~128]{Khalil2002}`
5. **Cross-reference**: Claude suggests related theorems

### Workflow C: Implementing Algorithm

1. **Identify algorithm**: "Need PSO pseudocode"
2. **Request**: "Extract PSO algorithm from Kennedy1995"
3. **Receive**: Algorithm steps, parameters, page number
4. **Implement**: Code based on algorithm
5. **Cite code**: `% Based on \cite[Algorithm~1]{Kennedy1995}`

---

## Quality Assurance

### Accuracy Checklist
- [ ] Page numbers verified against PDF page count
- [ ] Section numbers match PDF table of contents
- [ ] Equation numbers match PDF numbering
- [ ] Theorem names match PDF exactly
- [ ] Citations follow consistent format

### Citation Best Practices
1. **Always include page numbers** for specific content
2. **Use section numbers** for broader concepts
3. **Cite equations** with both equation and page numbers
4. **Reference figures** with figure number and page
5. **Multiple sources** when making general claims

---

## Troubleshooting

### Problem: Can't find specific content

**Solution**:
```
You: "Search Levant2007 for all occurrences of 'homogeneity'"
Claude: Lists all pages containing "homogeneity"
```

### Problem: PDF has different page numbering

**Solution**: Claude reports both:
- PDF page number (for Read tool)
- Document page number (for citation)

Example: "Page 5 of PDF, document page 579"

### Problem: Need to cite multiple pages

**Solution**:
```
\cite[pp.~576--577, 582]{Levant2007}  % Multiple ranges
```

### Problem: Can't remember BibTeX key

**Solution**:
```
You: "What's the BibTeX key for the Levant super-twisting paper?"
Claude: "Levant2007" (checks references.bib)
```

---

## Integration with Thesis Writing

### During Literature Review
```
You: "I'm writing Section 2.1 on SMC history. Find key papers."
Claude:
1. Searches your PDFs
2. Extracts historical timeline
3. Generates citations for each milestone
4. Creates bibliography entries
```

### During Theoretical Development
```
You: "I need to prove stability. Find relevant theorems."
Claude:
1. Searches for Lyapunov theorems
2. Lists all applicable theorems with locations
3. Suggests citation strategy
4. Creates tracking entry
```

### During Implementation
```
You: "I'm coding the STA controller. Find the algorithm."
Claude:
1. Extracts algorithm pseudocode
2. Provides equation numbers
3. Lists parameter definitions
4. Suggests citation for code comments
```

### During Results Validation
```
You: "Compare my Fig 5.2 to literature."
Claude:
1. Finds similar figures in PDFs
2. Lists comparison papers
3. Generates citation for validation
4. Notes differences/similarities
```

---

## Time Savings

**Traditional approach**: 5-10 minutes per citation (open PDF, search, find page, format)

**AI-assisted approach**: 30 seconds per citation (ask Claude, copy-paste)

**For 100 citations**: 8 hours → 1 hour saved

---

## Next Steps

1. **Try it now**: "Find the super-twisting algorithm in Levant2007"
2. **Create tracking**: "Generate tracking file for Levant2007"
3. **Extract content**: "Extract all theorems from Khalil2002"
4. **Compare sources**: "Compare PSO algorithms in Kennedy1995 vs Eberhart1995"

---

## See Also

- `citation_tracking/INDEX.md` - Master index of all tracked PDFs
- `thesis/references.bib` - BibTeX database
- `docs/thesis/CITATION_TEMPLATE.md` - Citation format examples

---

**Status**: [OK] Ready for immediate use

**Last Updated**: 2025-12-06

**Author**: Claude AI (Sonnet 4.5) + Human collaboration
