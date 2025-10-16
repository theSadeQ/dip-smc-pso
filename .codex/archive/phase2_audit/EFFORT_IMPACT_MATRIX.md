# Effort vs. Impact Matrix

Effort estimates represent combined UX + FED time (analysis, design, documentation). Impact scores sourced from `PHASE1_DEEP_DIVE_ANALYSIS.md`. ROI = Impact ÷ Effort to help prioritise sequencing.

| Issue | Severity | Effort (hrs) | Impact Score | ROI (Impact/Effort) | Planned Wave | Notes |
|-------|----------|--------------|--------------|---------------------|--------------|-------|
| UI-001 | Medium | 4 | 24 | 6.0 | Wave 3 | Default opacity is set to 0.3, making the caret nearly invisible until hover and leading users to miss the collapse affordance. |
| UI-002 | Critical | 2 | 50 | 25.0 | Wave 1 | Muted text color #9ca3af reaches only 2.54:1 contrast on white, failing WCAG AA for normal copy used across overview paragraphs. |
| UI-003 | High | 6 | 24 | 4.0 | Wave 1 | Collapsed message text (#94a3b8 on white) renders at 0.85rem with 3:1 contrast, below the 4.5:1 requirement for status text. |
| UI-004 | High | 12 | 18 | 1.5 | Wave 1 | Status copy is injected with a ::after pseudo-element, so screen readers never announce that content is hidden or how to reveal it. |
| UI-005 | Medium | 8 | 18 | 2.25 | Wave 1 | Two identical "4 code blocks" control bars render consecutively, creating 48px of dead space and duplicate actions at the top of the page. |
| UI-006 | Medium | 6 | 15 | 2.5 | Wave 2 | Text is forced uppercase at 0.75rem with 0.8px letter-spacing, which drops legibility for short status labels on smaller viewports. |
| UI-007 | Medium | 6 | 24 | 4.0 | Wave 1 | Audience sections sit on 4px vertical rhythm so links blur together, making it hard to scan the three personas called out. |
| UI-008 | Low | 4 | 12 | 3.0 | Wave 1 | Card grid sits 12px from the Quick Start section, so the two modules visually merge and the navigation block reads like a caption. |
| UI-009 | Medium | 10 | 21 | 2.1 | Wave 2 | Controller quick navigation renders 60+ links with almost no grouping or column gutter, overwhelming the right half of the page. |
| UI-010 | Medium | 5 | 15 | 3.0 | Wave 1 | Links use brand red (#ef4444) for emphasis even though they are neutral destinations, conflicting with the danger palette used elsewhere. |
| UI-011 | Medium | 8 | 12 | 1.5 | Wave 2 | Dense data table uses ~11px body text, forcing readers to zoom to interpret 120+ rows of metrics. |
| UI-012 | Low | 3 | 8 | 2.67 | Wave 1 | Header row background and zebra striping are only 4% apart in luminance, so column boundaries disappear in the long report. |
| UI-013 | Low | 6 | 15 | 2.5 | Wave 1 | Animated badge pulses indefinitely but there is no prefers-reduced-motion override, so reduced-motion users still see flicker. |
| UI-014 | Low | 4 | 12 | 3.0 | Wave 1 | Icon sits 42px inside the left padding, pushing body copy off alignment and stealing 60px of horizontal content space. |
| UI-015 | Medium | 5 | 18 | 3.6 | Wave 1 | Warning emphasis uses pure red text with no accompanying icon or weight change, which fails color-blind safe guidance. |
| UI-016 | Low | 4 | 12 | 3.0 | Wave 2 | Step numbers are plain paragraphs; without distinct typography or spacing, the ordered workflow is hard to follow. |
| UI-017 | Medium | 5 | 15 | 3.0 | Wave 2 | Bullets wrap flush under the bullet glyph instead of aligning with the text, creating a ragged left edge through the mega list. |
| UI-018 | Medium | 8 | 21 | 2.62 | Wave 2 | Columns run the full viewport width and blow past 120 characters, forcing horizontal eye travel and hurting scan speed. |
| UI-019 | Low | 3 | 12 | 4.0 | Wave 1 | Overview paragraph lands immediately under an H1 with no leading, so the first sentence visually collides with the heading. |
| UI-020 | High | 8 | 32 | 4.0 | Wave 2 | H1 on 320px splits "Documentation" mid-word due to aggressive word-break behaviour, harming brand readability. |
| UI-021 | Medium | 5 | 24 | 4.8 | Wave 1 | Collapse/Expand buttons stack with 0px vertical gap on mobile, so the controls read as a single malformed button. |
| UI-022 | High | 9 | 32 | 3.56 | Wave 2 | Card grid still renders two columns at 320px, squeezing labels like "Interactive Graph" onto four lines. |
| UI-023 | Medium | 5 | 24 | 4.8 | Wave 1 | Last updated text wraps into a three-line block with almost zero leading, reducing legibility on handhelds. |
| UI-024 | Medium | 6 | 18 | 3.0 | Wave 2 | At 768px the icon grid still uses three columns, causing icons and copy to collide with the right margin. |
| UI-025 | Low | 4 | 8 | 2.0 | Wave 2 | On tablet the anchor list drops below content but keeps desktop font size, so the secondary TOC dominates mid-page. |
| UI-026 | Medium | 6 | 18 | 3.0 | Wave 3 | Current section in the right rail only changes weight, no color or bullet indicator, so readers can’t quickly locate position. |
| UI-027 | Low | 3 | 12 | 4.0 | Wave 1 | Circular FAB blends with page background on light theme because the drop shadow is only 0 2px 10px rgba(0,0,0,0.3). |
| UI-028 | Low | 4 | 12 | 3.0 | Wave 2 | Cards rely on underlines alone to separate headings from content, so category titles disappear in long scrolls. |
| UI-029 | Low | 4 | 6 | 1.5 | Wave 3 | Iconography mixes emojis and solid icons, which feels unbranded compared to the primary documentation set. |
| UI-030 | Low | 3 | 12 | 4.0 | Wave 1 | Pager arrows sit 8px from link text, so the previous/next affordance looks misaligned and unclear. |
| UI-031 | Medium | 6 | 18 | 3.0 | Wave 1 | Gradient callouts use white text over pastel backgrounds, which drops to ~3.3:1 contrast in the info variant. |
| UI-032 | Low | 4 | 6 | 1.5 | Wave 3 | Previous/next links include full sentence titles so breadcrumbs wrap to three lines, pushing the footer further down. |
| UI-033 | Medium | 9 | 14 | 1.56 | Wave 3 | Table exposes no sticky header or filter affordance, leaving readers to scroll hundreds of rows without context. |
| UI-034 | Low | 4 | 12 | 3.0 | Wave 2 | Bulleted lists mix bold labels and body copy on the same line, leading to awkward sentence breaks and scan fatigue. |

**Insights**
- ROI ≥4.0 candidates (UI-002, UI-021, UI-023, UI-027, UI-030) form the quick-win backlog.
- Low ROI items (UI-004, UI-011, UI-029, UI-033) require careful sequencing and potentially additional justification before implementation.

