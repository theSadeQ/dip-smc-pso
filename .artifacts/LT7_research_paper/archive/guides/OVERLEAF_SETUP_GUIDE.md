# Overleaf Setup Guide - LT-7 Conference Paper

**File Ready**: `D:\Projects\main\.artifacts\LT7_research_paper\LT7_conference_overleaf.zip` (1.1 MB)

---

## STEP 1: Go to Overleaf (2 minutes)

1. Open your web browser
2. Go to: **https://www.overleaf.com**
3. Click **"Register"** (top right) if you don't have an account
   - OR click **"Log In"** if you already have one
4. **Free account** is sufficient for this paper

---

## STEP 2: Upload Your Paper (30 seconds)

1. Once logged in, click the big green **"New Project"** button
2. Select **"Upload Project"**
3. Click **"Select a .zip file"**
4. Navigate to: `D:\Projects\main\.artifacts\LT7_research_paper\`
5. Select **`LT7_conference_overleaf.zip`**
6. Click **"Open"** or **"Upload"**
7. Wait ~10 seconds for upload
8. Overleaf will automatically extract and open your project

---

## STEP 3: Compile the PDF (10 seconds)

**Overleaf compiles automatically!** You should see:

- **Left pane**: Your LaTeX code (main.tex)
- **Right pane**: PDF preview (auto-generates)

If the PDF doesn't appear:
1. Click **"Recompile"** button (top of right pane)
2. Wait ~15-20 seconds for first compilation

---

## STEP 4: Check for Errors

Look at the **logs/output** (click "Logs and output files" button near Recompile):

### Expected Issues:

1. **Missing Figure 1** - This is NORMAL! We haven't created it yet.
   - Error: `File fig1_dip_schematic.pdf not found`
   - **Action**: We'll add it later (Phase 2 of plan)

2. **Possible package warnings** - Usually harmless
   - LaTeX packages may show warnings about formatting
   - **If PDF generated**: Ignore minor warnings

### Success Criteria:
- ✅ PDF appears on right side
- ✅ Most of the paper visible (9 sections)
- ✅ Figures 2-7 appear correctly
- ✅ Only Figure 1 is missing (expected)

---

## STEP 5: Quick Quality Check (5 minutes)

Scroll through the PDF and verify:

1. **Title & Abstract**: Appears correctly
2. **Sections I-IX**: All 9 sections visible
3. **Figures**: Figures 2, 3, 4, 5, 6, 7 render correctly (colorful plots)
4. **Tables**: Tables I-V formatted properly
5. **References**: Bibliography at end (34 citations)
6. **Page Count**: How many pages? (probably 8-10 pages currently)

**Write down the page count** - we'll need this for condensing!

---

## STEP 6: Download PDF (optional)

If you want a local copy:

1. Click **"Download"** menu (top bar)
2. Select **"PDF"**
3. Save to your computer

---

## What's in the ZIP File?

```
overleaf_upload/
├── main.tex              # Your paper (612 lines)
├── references.bib        # Bibliography (34 citations)
└── figures/              # All figure files (24 files)
    ├── fig2_adaptive_boundary.pdf/.png
    ├── fig3_baseline_radar.pdf/.png
    ├── fig4_pso_convergence.pdf/.png
    ├── fig5_chattering_boxplot.pdf/.png
    ├── fig6_robustness_degradation.pdf/.png
    ├── fig7_disturbance_rejection.pdf/.png
    └── (+ 18 other supplementary figures)
```

---

## Troubleshooting

### Problem: "Project won't upload"
- **Solution**: Check file size < 50 MB (ours is 1.1 MB, well under limit)
- **Alternative**: Upload main.tex and references.bib manually, then upload figures folder

### Problem: "Compilation timeout"
- **Solution**: Free Overleaf has 1-minute timeout. Our paper should compile in ~20 seconds.
- **Alternative**: Remove some high-resolution figures temporarily

### Problem: "Can't see PDF"
- **Solution 1**: Click "Recompile" button
- **Solution 2**: Clear browser cache (Ctrl+Shift+R)
- **Solution 3**: Try different browser (Chrome/Edge recommended)

---

## Next Steps After Overleaf Compilation

Once your PDF compiles successfully:

1. **Report the page count** → Tell Claude how many pages (e.g., "9 pages")
2. **Phase 2: Create Figure 1** → DIP schematic diagram (TikZ or PowerPoint)
3. **Phase 3: Condense to 6 pages** → Strategic editing to meet IEEE limit
4. **Phase 4: Final validation** → Proofread and package for submission

---

## Tips for Using Overleaf

- **Auto-save**: Overleaf saves every few seconds (no Ctrl+S needed!)
- **Collaboration**: Share project link if you want co-authors to edit
- **Version History**: Click "History" to see all changes (like Git)
- **Keyboard shortcuts**: Ctrl+Enter = Recompile

---

**YOU ARE NOW READY TO COMPILE YOUR PAPER! 🚀**

**Estimated time**: 3-5 minutes from opening browser to seeing your PDF

**Let Claude know once you've compiled and what the page count is!**
