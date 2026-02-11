# 14-Day Full Immersion Schedule - Supporting Materials

This directory contains all supporting materials for the 14-Day Full Immersion Learning Plan for the DIP-SMC-PSO project.

---

## Overview

**Goal:** Compress 125-150 hours of learning into 14 days (8-10 hours/day)
**Target Outcome:** 70-85% project understanding + ability to contribute code
**Materials:** 30 podcast episodes, 30 cheatsheets, 6 controllers, full documentation

---

## Available Materials (4 Files)

### 1. Daily Checklist/Tracker (`daily_checklist.md`)

**Purpose:** Printable daily task checklist for all 14 days

**Contents:**
- Hour-by-hour breakdown for each day
- Morning/Afternoon/Evening blocks
- Checkboxes for all tasks
- Daily reflection prompts
- Notes sections
- Completion certificate

**How to Use:**
1. Print this document (47 pages)
2. Check off items as you complete them
3. Fill in reflection questions each evening
4. Track understanding ratings (1-10) daily
5. Sign completion certificate on Day 14

**Recommended:** Keep printed copy at your desk during entire immersion

---

### 2. Quick Reference Command Sheet (`quick_reference_commands.md`)

**Purpose:** One-page command reference for common operations

**Contents:**
- Essential simulation commands
- PSO optimization commands
- Testing commands (pytest, coverage)
- HIL simulation commands
- Documentation building (Sphinx)
- Git workflow commands
- Project recovery commands
- File navigation commands
- Troubleshooting tips
- Keyboard shortcuts

**How to Use:**
1. Print this document (single page or poster size)
2. Keep visible near keyboard
3. Copy-paste commands (don't type from scratch)
4. Refer to it 20+ times per day
5. Use as terminal cheat sheet

**Recommended:** Laminate for durability or pin to wall

---

### 3. VS Code Workspace Settings (`vscode_learning_settings.json`)

**Purpose:** Optimized VS Code configuration for learning the codebase

**Contents:**
- Python configuration (interpreter, linting, type checking)
- Testing integration (pytest, coverage)
- File explorer settings (show important hidden files)
- Search configuration (exclude caches)
- Editor settings (readable code, breadcrumbs, sticky scroll)
- Git integration (inline diffs, decorations)
- Terminal configuration
- Learning-specific features (auto-save, peek editor)
- Documentation preview settings
- YAML/JSON config support
- Performance optimizations
- Keyboard shortcut hints
- Recommended extensions list

**How to Use:**
1. Copy this file to `.vscode/settings.json` in project root
2. Restart VS Code
3. Install recommended extensions (listed in comments)
4. Customize as you discover preferences during 14 days

**Key Features:**
- Auto-save every 5 seconds (lose less work)
- Breadcrumbs for code navigation (F12 to definition)
- Sticky scroll keeps context visible
- Git changes inline
- Test explorer integration
- Markdown preview optimized

---

### 4. Progress Tracking Template (`progress_tracker.md`)

**Purpose:** Comprehensive daily progress journal for entire immersion

**Contents:**
- Immersion overview section
- 14 daily tracking pages with:
  - Materials consumed checklist
  - Hands-on activities checklist
  - Understanding ratings (1-10)
  - Key insights (3-5 sentences)
  - Challenges faced
  - Experiment results tables
  - Performance metrics
- Week 1 reflection
- Week 2 detailed capstone project tracking:
  - Phase 1: Design
  - Phase 2: Configuration
  - Phase 3: Optimization (PSO results)
  - Phase 4: Benchmark (statistical comparison)
  - Phase 5: Analysis (significance testing)
  - Phase 6: Documentation (report + git)
- Final 14-day reflection:
  - Self-assessment (0-100)
  - Achievements checklist
  - Top 5 learnings
  - Knowledge gaps
  - Next steps plan
- Post-immersion continued learning tracker
- Resources created during immersion
- Contact for help

**How to Use:**
1. Update this document at end of each day (15-20 minutes)
2. Fill in all tables, ratings, and reflection prompts
3. Track actual hours vs. planned hours
4. Document all experiments and results
5. Use for capstone project detailed tracking on Day 14
6. Complete final reflection after Day 14
7. Use continued learning tracker for Weeks 3-12

**Recommended:** Review weekly to track progress trends

---

## Quick Start

**Day 1 Morning Setup (30 minutes):**
```bash
# 1. Copy VS Code settings
cp .ai_workspace/edu/immersion_schedule/vscode_learning_settings.json .vscode/settings.json

# 2. Print daily checklist
start .ai_workspace/edu/immersion_schedule/daily_checklist.md  # Open and print

# 3. Print quick reference
start .ai_workspace/edu/immersion_schedule/quick_reference_commands.md  # Open and print

# 4. Open progress tracker in VS Code
code .ai_workspace/edu/immersion_schedule/progress_tracker.md  # Keep open in tab
```

**Daily Workflow:**
1. **Morning:** Check daily checklist, start Streamlit
2. **Afternoon:** Follow checklist tasks, run experiments
3. **Evening:** Update progress tracker, reflect on learnings

---

## Printing Recommendations

### Daily Checklist
- **Pages:** 47
- **Format:** Single-sided, stapled
- **Paper:** Standard 8.5x11"
- **Keep:** At desk throughout 14 days

### Quick Reference
- **Pages:** 1 (multi-page, but focus on first page)
- **Format:** Poster size (optional) or standard
- **Paper:** Cardstock for durability
- **Location:** Pin to wall or keep near keyboard

### Progress Tracker
- **Pages:** Digital only (update in VS Code)
- **Backup:** Daily git commits recommended

---

## Integration with Main Schedule

These materials complement the main 14-day schedule:
- **Schedule:** `.ai_workspace/edu/immersion_schedule/14_day_schedule.md` (if exists)
- **Podcasts:** `academic/paper/presentations/podcasts/episodes/`
- **Cheatsheets:** `academic/paper/presentations/podcasts/cheatsheets/`
- **Code:** `src/` directory
- **Documentation:** `docs/` and `.ai_workspace/guides/`

---

## Customization

All materials are markdown or JSON - easy to customize:

1. **Add/Remove Tasks:** Edit `daily_checklist.md` checkboxes
2. **Change Commands:** Modify `quick_reference_commands.md`
3. **Adjust VS Code:** Edit `vscode_learning_settings.json`
4. **Extend Tracking:** Add sections to `progress_tracker.md`

---

## Success Metrics

By using these materials consistently for 14 days:

**Expected Outcomes:**
- [OK] 70-85% project understanding
- [OK] Ability to run all 6 controllers
- [OK] Complete PSO optimization independently
- [OK] Write tests for new features
- [OK] Generate publication-quality plots
- [OK] Contribute code to project

**Time Investment:**
- Daily checklist: 8-10 hours/day of focused learning
- Progress tracker: 15-20 minutes/day of reflection
- Quick reference: Used 20+ times/day
- VS Code settings: One-time setup (30 minutes)

**Total Hours:** 112-140 hours over 14 days

---

## Troubleshooting

### Can't Print Checklist?
- Open in browser: `start daily_checklist.md`
- Use browser print (Ctrl+P)
- Export to PDF first if needed

### VS Code Settings Not Working?
- Ensure file is at `.vscode/settings.json` in project root
- Restart VS Code
- Check syntax (valid JSON)

### Progress Tracker Too Detailed?
- Skip tables/metrics if not relevant
- Focus on reflections and understanding ratings
- Customize sections as needed

### Commands Not Working?
- Verify you're on Windows (use `python` not `python3`)
- Check you're in project root: `D:\Projects\main\`
- Ensure dependencies installed: `pip install -r requirements.txt`

---

## Next Steps After Day 14

1. Archive your filled-out materials:
   ```bash
   mkdir academic/logs/immersion_2026/
   cp progress_tracker.md academic/logs/immersion_2026/
   cp daily_checklist.md academic/logs/immersion_2026/
   ```

2. Begin Tutorial 01: `docs/guides/getting-started.md`

3. Continue 1-2 hours/day for 2-3 months (mastery path)

4. Use podcasts during commute for reinforcement

5. Join research tasks: `.ai_workspace/planning/research/`

---

## Contact & Support

**If you get stuck:**
- Check `.ai_workspace/guides/` for operational guides
- Review `docs/NAVIGATION.md` for documentation
- Use `/recover` command if you hit token limits
- Consult `CLAUDE.md` for project conventions

**For questions:**
- Open GitHub issue: https://github.com/theSadeQ/dip-smc-pso/issues
- Review FAQ: `docs/guides/faq.md`

---

## File Manifest

| File | Size | Purpose | Usage Frequency |
|------|------|---------|-----------------|
| `daily_checklist.md` | ~16 KB | Task checklist | Daily (print once) |
| `quick_reference_commands.md` | ~12 KB | Command reference | 20+ times/day |
| `vscode_learning_settings.json` | ~14 KB | IDE configuration | One-time setup |
| `progress_tracker.md` | ~18 KB | Progress journal | Daily (15-20 min) |
| `README.md` (this file) | ~8 KB | Guide to materials | Reference |

**Total Size:** ~68 KB (all text files)

---

## Version History

- **v1.0** (2026-02-11): Initial release with all 4 supporting materials
  - Created by Claude Code during immersion schedule planning
  - Covers 14 days, 112-140 hours, 30 episodes, 6 controllers

---

## License & Attribution

These materials are part of the DIP-SMC-PSO project.
See project root `LICENSE` for details.

Generated with [AI] assistance on 2026-02-11.

---

**Ready to start your immersion? Begin with Day 1 setup, print your materials, and dive in!**
