# Figure 1: DIP System Schematic - Manual Creation Requirements

**Status**: ⏸️ Manual creation required (TikZ, Inkscape, or PowerPoint)

**Estimated Time**: 1-2 hours

---

## Required Content

### System Diagram Elements:

1. **Cart**:
   - Rectangular body on wheels
   - Mass label: `M` (cart mass)
   - Position: `x` (horizontal displacement)
   - Force input: `F` (control force, horizontal arrow)

2. **First Pendulum (Link 1)**:
   - Hinged to cart
   - Length: `l₁`
   - Mass: `m₁` (at center of mass)
   - Angle: `θ₁` (measured from vertical up)
   - Moment of inertia: `I₁`

3. **Second Pendulum (Link 2)**:
   - Hinged to end of first pendulum
   - Length: `l₂`
   - Mass: `m₂` (at center of mass)
   - Angle: `θ₂` (measured from vertical up)
   - Moment of inertia: `I₂`

4. **Coordinate Frame**:
   - Ground reference line (horizontal dashed)
   - Vertical axis (dotted, labeled "Vertical")
   - x-axis (horizontal, cart motion)
   - Angular measurements (curved arrows showing θ₁, θ₂)

5. **Annotations**:
   - Gravity vector: `g` (downward arrow)
   - All masses, lengths, and angles clearly labeled
   - Control input `F` with arrow showing direction

---

## Physical Parameters (from config.yaml)

**To be extracted and added to figure caption:**

```python
# From config.yaml (lines ~248-260)
M = ? kg          # Cart mass
m₁ = ? kg         # Pendulum 1 mass
m₂ = ? kg         # Pendulum 2 mass
l₁ = ? m          # Pendulum 1 length
l₂ = ? m          # Pendulum 2 length
I₁ = ? kg·m²      # Pendulum 1 inertia
I₂ = ? kg·m²      # Pendulum 2 inertia
g = 9.81 m/s²     # Gravity
```

**Action Required**: Extract exact values from `config.yaml` for figure caption.

---

## Style Guidelines

### IEEE Format Requirements:

- **Size**: Single column (3.5" wide) or as needed for clarity
- **Resolution**: 300 DPI minimum
- **Format**: PDF or EPS (vector preferred)
- **Font**: Times New Roman or similar serif, 10pt
- **Line Width**: 0.8-1.0 pt for main elements
- **Colors**: Black and white preferred (grayscale acceptable)

### Visual Clarity:

- Clear distinction between cart, pendulum 1, and pendulum 2
- Angles measured consistently from vertical
- All labels non-overlapping and readable
- Professional engineering diagram style (not cartoonish)

---

## Recommended Tools

### Option A: TikZ (LaTeX) - Best for IEEE Papers

**Advantages**: Vector graphics, consistent fonts, easy LaTeX integration

**Example starter code**:
```latex
\begin{tikzpicture}
  % Cart
  \draw[fill=lightgray] (0,0) rectangle (1,0.5);
  \draw (0,0) circle (0.1);  % Wheel
  \draw (1,0) circle (0.1);  % Wheel
  \node at (0.5,0.25) {$M$};

  % Force arrow
  \draw[->,thick,red] (-0.5,0.25) -- (-0.1,0.25) node[midway,above] {$F$};

  % Pendulum 1
  \draw[thick] (0.5,0.5) -- ++(60:2) node[midway,right] {$l_1$};
  \filldraw (0.5,0.5) ++(60:1) circle (0.1) node[right] {$m_1$};

  % Pendulum 2
  \draw[thick] (0.5,0.5) ++(60:2) -- ++(30:1.5) node[midway,right] {$l_2$};
  \filldraw (0.5,0.5) ++(60:2) ++(30:0.75) circle (0.1) node[right] {$m_2$};

  % Angles
  \draw[->] (0.5,0.5) ++(0:0.3) arc (0:60:0.3) node[midway,right] {$\theta_1$};

  % Coordinate system
  \draw[->] (0.5,0.5) -- (2,0.5) node[right] {$x$};
  \draw[dotted] (0.5,0.5) -- (0.5,3) node[above] {Vertical};
\end{tikzpicture}
```

### Option B: Inkscape (Free Vector Graphics)

**Advantages**: GUI-based, easy to learn, exports to PDF/EPS

**Steps**:
1. Download Inkscape (https://inkscape.org/)
2. Create new document, set size to 3.5" × 3.0"
3. Use basic shapes: rectangles (cart), circles (wheels, masses), lines (pendulums)
4. Add text labels using Times New Roman font
5. Export as PDF (File → Save As → PDF)

### Option C: PowerPoint (Quick & Dirty)

**Advantages**: Familiar interface, fast creation

**Steps**:
1. Set slide size to 3.5" × 3.0" (Design → Slide Size → Custom)
2. Insert shapes (rectangles, lines, circles)
3. Add text labels
4. Export as PDF (File → Export → PDF)
5. **Downside**: May not be vector-quality

---

## Caption Template

```latex
\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{fig1_dip_schematic.pdf}
\caption{Double inverted pendulum system on a cart. The cart (mass $M$) is
actuated by horizontal force $F$. Two pendulums (masses $m_1$, $m_2$; lengths
$l_1$, $l_2$) are connected in series. Angular positions $\theta_1$ and
$\theta_2$ are measured from the vertical. System parameters: $M = ? kg$,
$m_1 = ? kg$, $m_2 = ? kg$, $l_1 = ? m$, $l_2 = ? m$, $g = 9.81 m/s^2$.}
\label{fig:dip_schematic}
\end{figure}
```

---

## Similar Examples in Literature

**Search for**:
- IEEE CDC/ACC papers on inverted pendulum control
- "Double inverted pendulum schematic"
- TikZ examples: `\usepackage{tikz}` galleries

**Good reference papers**:
1. Wiley (2023): "Stabilization of Double Inverted Pendulum via Hierarchical SMC"
   - DOI: 10.1155/2023/3916279
   - Likely has clear DIP schematic

2. Any recent IEEE paper on cart-pole systems
   - Standard conventions for angle measurement
   - Professional diagram style

---

## Action Items

### Before Creating Figure:

- [ ] Extract physical parameters from `config.yaml`
- [ ] Decide on tool (TikZ recommended for IEEE)
- [ ] Review similar figures in literature for conventions

### During Creation:

- [ ] Ensure angles measured from vertical (standard convention)
- [ ] Label all masses, lengths, angles clearly
- [ ] Show control force `F` as arrow
- [ ] Include coordinate frame
- [ ] Use professional engineering style

### After Creation:

- [ ] Export as PDF at 300 DPI
- [ ] Verify file size < 1 MB
- [ ] Test inclusion in LaTeX document
- [ ] Write complete caption with parameter values

---

## Fallback Option

**If manual creation is too time-consuming**:

Use a **placeholder** for now and note in the paper:
> "Figure 1: [DIP system schematic - to be created with TikZ]"

Then continue with writing the paper. The schematic can be added during final polishing.

**Priority**: Writing Sections VII, IV, and III are more critical than Figure 1. The figure can be added at the end.

---

## Estimated Effort Breakdown

| Task | Time | Tool |
|------|------|------|
| Extract parameters from config | 15 min | Text editor |
| Create basic schematic | 30-60 min | TikZ/Inkscape |
| Polish and add labels | 15-30 min | Same |
| Test in LaTeX document | 10 min | LaTeX |
| **Total** | **1-2 hours** | - |

---

## Current Status

- **6/7 figures complete** (automated generation)
- **1/7 figures pending** (manual creation)
- **Recommendation**: Proceed with writing Section VII, defer Figure 1 to final polishing

**Next Step**: Start writing Section VII (Results) while Figure 1 is in progress or deferred.
