# Next Session Prompt Guide: Documentation Reorganization

**Project**: dip-smc-pso - Documentation Reorganization
**Purpose**: Copy-paste prompts for resuming work in next Claude Code session
**Created**: December 23, 2025
**Use Case**: Session recovery after token limit or multi-day gap

---

## Quick Reference: What to Say

### Scenario 1: Quick Wins (2 hours → 90/100 score)

**Copy-paste this prompt**:

```
I have a PROJECT COMPLETION REPORT for docs/ reorganization that needs improvements to reach 90/100 score (currently 85/100).

Context:
- Report: .ai_workspace/guides/DOCS_REORGANIZATION_PROJECT_COMPLETION_REPORT.md (1,912 lines)
- Audit: .ai_workspace/guides/DOCS_REORGANIZATION_REPORT_AUDIT.md (1,245 lines)
- Current score: 85/100 (PRODUCTION-READY but needs enhancements)

Goal: Execute Phase 1 improvements (2 hours) to reach 90/100:
1. Add ASCII directory tree diagrams (before/after comparison)
2. Add ROI calculation (time invested vs. time saved annually)
3. Create FAQ appendix (10-15 common questions)
4. Create Glossary appendix (20-30 technical terms)
5. Add "Quick Wins" section to recommendations

Instructions:
1. Read the audit file to understand gaps
2. Read the completion report to understand current state
3. Execute Phase 1 improvements from the audit (page 32, "Priority Roadmap")
4. Update the report in place (edit existing file)
5. Verify improvements raise score to 90/100 using scoring matrix (audit page 38)

Expected deliverable: Updated PROJECT_COMPLETION_REPORT.md with Phase 1 improvements (90/100 score).

Ready to start?
```

---

### Scenario 2: Near-Perfect Report (10 hours → 95/100 score)

**Copy-paste this prompt**:

```
I need to enhance my docs/ reorganization PROJECT COMPLETION REPORT from 85/100 to 95/100.

Context:
- Report: .ai_workspace/guides/DOCS_REORGANIZATION_PROJECT_COMPLETION_REPORT.md (1,912 lines)
- Audit: .ai_workspace/guides/DOCS_REORGANIZATION_REPORT_AUDIT.md (identifies gaps)
- Current score: 85/100 (PRODUCTION-READY)
- Target score: 95/100 (NEAR-PERFECT)

Goal: Execute Phases 1-2 improvements (10 hours total):

Phase 1 - Quick Wins (2 hours):
1. Add ASCII directory tree diagrams
2. Add ROI calculation
3. Create FAQ appendix
4. Create Glossary appendix
5. Add "Quick Wins" section

Phase 2 - Core Enhancements (8 hours):
1. Create validation scripts (check_old_references.sh, validate_structure.py, check_links.py)
2. Add timeline chart (ASCII or Mermaid)
3. Add metrics charts (directory reduction, warning elimination)
4. Create reusable template for future reorganizations

Instructions:
1. Read audit to understand complete gap analysis
2. Execute Phase 1 improvements first (verify 90/100 before proceeding)
3. Execute Phase 2 improvements (create scripts in scripts/docs/)
4. Update report with all enhancements
5. Self-assess using scoring matrix (audit page 38)

Expected deliverables:
- Updated PROJECT_COMPLETION_REPORT.md (95/100 score)
- 3 validation scripts in scripts/docs/
- 1 reusable template file

Time available: [tell me how much time you have]

Ready to start?
```

---

### Scenario 3: Just Review and Commit Current Work

**Copy-paste this prompt**:

```
I have a completed PROJECT COMPLETION REPORT for docs/ reorganization. Please review and help me commit it.

Files created:
- .ai_workspace/guides/DOCS_REORGANIZATION_PROJECT_COMPLETION_REPORT.md (1,912 lines)
- .ai_workspace/guides/DOCS_REORGANIZATION_REPORT_AUDIT.md (1,245 lines)

Current status:
- Report score: 85/100 (PRODUCTION-READY)
- All 5 phases documented (Phases 1-5)
- Complete timeline, metrics, lessons learned, recommendations
- Audit identifies path to 100/100 (optional improvements)

Tasks:
1. Read both files briefly to verify quality
2. Create git commit with appropriate message
3. Push to remote repository
4. Confirm completion

No improvements needed right now - just commit and push.

Ready?
```

---

### Scenario 4: Start Fresh (No Context Provided)

**Copy-paste this prompt**:

```
I previously completed a documentation reorganization project (docs/ folder, 5 phases). I have comprehensive reports that need review and potential improvements.

Project files:
- Main report: .ai_workspace/guides/DOCS_REORGANIZATION_PROJECT_COMPLETION_REPORT.md
- Quality audit: .ai_workspace/guides/DOCS_REORGANIZATION_REPORT_AUDIT.md
- Phase 1-2 summary: .ai_workspace/guides/DOCS_ORGANIZATION_GUIDE.md
- Phase 3-5 summary: .ai_workspace/guides/DOCS_PHASES_3_4_5_SUMMARY.md

Context needed:
1. Read the audit file first (tells you current score: 85/100 and gaps)
2. Read the main report second (complete project documentation)
3. Tell me what improvements you recommend based on audit
4. Ask me how much time I have available

Then we can decide: quick wins (2h → 90/100), near-perfect (10h → 95/100), or perfection (25h → 100/100).

Start by reading the audit and telling me the current status.
```

---

### Scenario 5: Create Validation Scripts Only

**Copy-paste this prompt**:

```
I need to create validation scripts for documentation reorganization, referenced in my PROJECT COMPLETION REPORT but not yet implemented.

Context:
- Report: .ai_workspace/guides/DOCS_REORGANIZATION_PROJECT_COMPLETION_REPORT.md
- Audit: .ai_workspace/guides/DOCS_REORGANIZATION_REPORT_AUDIT.md (see "Category B: Automation Artifacts")

Scripts needed (create in scripts/docs/):
1. check_old_references.sh - Grep validation for old path references
2. validate_structure.py - Directory structure validator (check counts, depth, etc.)
3. check_links.py - Internal link checker for markdown files
4. rollback.sh - Automated rollback using git tags

Requirements:
- Follow existing script conventions in scripts/ directory
- Include usage documentation (--help flag)
- Test on current docs/ structure
- Add to report Appendix or create new section

Expected deliverable: 4 working scripts with usage docs.

Time available: 3 hours

Ready to start?
```

---

### Scenario 6: Create Reusable Template

**Copy-paste this prompt**:

```
Create a reusable template for future documentation reorganizations based on the completed docs/ project.

Context:
- Completed project: .ai_workspace/guides/DOCS_REORGANIZATION_PROJECT_COMPLETION_REPORT.md
- Audit recommendations: .ai_workspace/guides/DOCS_REORGANIZATION_REPORT_AUDIT.md (see "Category B: Automation Artifacts")

Template components needed:
1. Phase planning template (for planning reorganization phases)
2. Decision matrix template (5-criteria scoring for consolidations)
3. Validation checklist (pre/during/post session checklists)
4. Completion report skeleton (outline to fill in)

Requirements:
- Create as separate markdown files in .ai_workspace/templates/
- Include instructions for use
- Add examples from docs/ reorganization
- Link from main report

Expected deliverables:
- .ai_workspace/templates/reorganization_phase_plan_template.md
- .ai_workspace/templates/decision_matrix_template.md
- .ai_workspace/templates/validation_checklist_template.md
- .ai_workspace/templates/completion_report_template.md

Time available: 2 hours

Ready to start?
```

---

## Common Follow-Up Questions You Might Ask

### After I Start the Session

**Q: "What's the current score again?"**
A: "The current score is 85/100 (PRODUCTION-READY). The audit identifies gaps to reach 90, 95, or 100."

**Q: "What are the quick wins?"**
A: "Phase 1 quick wins (2 hours): ASCII directory trees, ROI calculation, FAQ appendix, Glossary appendix, Quick Wins section. These raise the score from 85 → 90."

**Q: "Should I do Phase 1 or go straight to Phase 2?"**
A: "Always do Phase 1 first. It's only 2 hours and gets you to 90/100. Then decide if you want to continue to Phase 2 (95/100) or stop."

**Q: "Where is the audit roadmap?"**
A: "Audit file, page 32: 'Priority Roadmap to Perfect Status' section. It lists Phases 1-4 with time estimates and expected scores."

**Q: "Can I just commit the current report?"**
A: "Yes, the report is already PRODUCTION-READY (85/100). See Scenario 3 above for commit-only prompt."

---

## Tips for Effective Session Recovery

### 1. Always Provide File Paths

**Good**:
```
Report: .ai_workspace/guides/DOCS_REORGANIZATION_PROJECT_COMPLETION_REPORT.md
Audit: .ai_workspace/guides/DOCS_REORGANIZATION_REPORT_AUDIT.md
```

**Bad**:
```
"The report we created last time"
```

---

### 2. State Your Goal Clearly

**Good**:
```
Goal: Execute Phase 1 improvements (2 hours) to reach 90/100 score
```

**Bad**:
```
"Make the report better"
```

---

### 3. Specify Time Available

**Good**:
```
Time available: 2 hours
```

**Bad**:
```
"I have some time"
```

---

### 4. Reference Specific Sections

**Good**:
```
See audit page 32: "Priority Roadmap to Perfect Status"
```

**Bad**:
```
"Check the audit for next steps"
```

---

### 5. Clarify What You DON'T Want

**Good**:
```
No improvements needed - just commit and push current work
```

**Bad**:
```
"Help me with the report"
```

---

## Troubleshooting: If Session Doesn't Go Smoothly

### Problem 1: Claude Doesn't Remember Context

**Symptom**: "I don't see the files you mentioned"

**Solution**: Provide full file paths and ask Claude to read them:
```
Please read these files first:
1. .ai_workspace/guides/DOCS_REORGANIZATION_REPORT_AUDIT.md
2. .ai_workspace/guides/DOCS_REORGANIZATION_PROJECT_COMPLETION_REPORT.md

Then tell me the current score and recommended improvements.
```

---

### Problem 2: Claude Asks Too Many Questions

**Symptom**: Claude asks 5+ questions before starting work

**Solution**: Be very specific in your initial prompt:
```
Don't ask me questions. Execute Phase 1 improvements directly:
1. Add ASCII directory trees (before/after)
2. Add ROI calculation
3. Create FAQ appendix (10-15 questions)
4. Create Glossary appendix (20-30 terms)
5. Add "Quick Wins" section

Use the audit as your guide. Start with #1 (directory trees).
```

---

### Problem 3: Claude Wants to Rewrite Everything

**Symptom**: "I'll create a new report from scratch"

**Solution**: Emphasize editing, not rewriting:
```
DO NOT create a new report. Edit the existing file in place:
- File: .ai_workspace/guides/DOCS_REORGANIZATION_PROJECT_COMPLETION_REPORT.md
- Use Edit tool to add sections
- Preserve all existing content
- Only add Phase 1 improvements (directory trees, ROI, FAQ, Glossary, Quick Wins)
```

---

### Problem 4: Claude Goes Off-Track

**Symptom**: Claude starts analyzing the docs/ folder instead of improving the report

**Solution**: Redirect firmly:
```
STOP. You're analyzing docs/ but that's already done.

Your task: Improve the REPORT ABOUT the reorganization.
- Report file: .ai_workspace/guides/DOCS_REORGANIZATION_PROJECT_COMPLETION_REPORT.md
- Audit file: .ai_workspace/guides/DOCS_REORGANIZATION_REPORT_AUDIT.md

Read the audit, identify Phase 1 improvements, apply them to the report. Don't analyze docs/ folder.
```

---

## Advanced: Custom Prompts for Specific Improvements

### Just Add Directory Tree Diagrams

```
Add ASCII directory tree diagrams to DOCS_REORGANIZATION_PROJECT_COMPLETION_REPORT.md.

Location to add: Section 10 "Before/After Comparison"

Content needed:
1. Before tree (39 directories, show structure with issues highlighted)
2. After tree (34 directories, show clean structure)
3. Use ASCII art (├──, └──, │ symbols)

Example format:
```
docs/
├── reference/ (7 files at root) [PROBLEM]
│   ├── controllers/ (61 files)
│   └── plant/ (30 files)
├── references/ (duplicate) [PROBLEM]
└── ...
```

Don't modify anything else. Just add directory trees to Section 10.

Time: 30 minutes
```

---

### Just Add ROI Calculation

```
Add ROI calculation to DOCS_REORGANIZATION_PROJECT_COMPLETION_REPORT.md.

Location: Section 5 "Quantitative Results" (after "Impact Summary")

Calculation:
- Time invested: 2.5 hours (analysis + execution + docs)
- Time saved annually: Estimate based on:
  - Faster navigation: 5 min/week saved × 10 users × 52 weeks = 43.3 hours/year
  - Reduced maintenance: 2 hours/year
  - Improved onboarding: 30 min/new user × 10 new users/year = 5 hours/year
  - Total saved: ~50 hours/year
- ROI: 50 hours saved / 2.5 hours invested = 20x return

Format as table with assumptions documented.

Time: 30 minutes
```

---

### Just Add FAQ Appendix

```
Create FAQ appendix for DOCS_REORGANIZATION_PROJECT_COMPLETION_REPORT.md.

Location: New "Appendix G: Frequently Asked Questions" (after Appendix F)

Questions to answer (10-15):
1. Can I rollback individual phases?
2. Why not consolidate all small directories?
3. How long does reorganization take?
4. What if Sphinx build fails after rollback?
5. How do I prevent broken links in future?
6. Why use git mv instead of regular mv?
7. What's the difference between checkpoints and commits?
8. Can I skip phases or do them out of order?
9. How often should I reorganize docs/?
10. What if I find more duplicate directories later?
... (add 5 more based on audit recommendations)

Format: **Q:** bold questions, A: regular answers with code examples where applicable.

Time: 30 minutes
```

---

### Just Add Glossary Appendix

```
Create Glossary appendix for DOCS_REORGANIZATION_PROJECT_COMPLETION_REPORT.md.

Location: New "Appendix H: Glossary" (after FAQ appendix)

Terms to define (20-30):
- Checkpoint
- Consolidation
- Decision matrix
- Git mv
- Grep validation
- Minimal disruption
- MyST Markdown
- Phase
- Rename detection
- Rollback
- Sphinx
- Tag
... (add 15-20 more technical terms from the report)

Format:
**Term**: Definition in 1-2 sentences. Example if applicable.

Alphabetical order.

Time: 15 minutes
```

---

## Emergency Recovery: If Everything Goes Wrong

### Last Resort Prompt

```
EMERGENCY RECOVERY - Previous session work needs salvage.

Files that exist:
- .ai_workspace/guides/DOCS_REORGANIZATION_PROJECT_COMPLETION_REPORT.md (main report, 1,912 lines)
- .ai_workspace/guides/DOCS_REORGANIZATION_REPORT_AUDIT.md (quality audit, 1,245 lines)
- .ai_workspace/guides/DOCS_ORGANIZATION_GUIDE.md (Phases 1-2 details, 639 lines)
- .ai_workspace/guides/DOCS_PHASES_3_4_5_SUMMARY.md (Phases 3-5 details, 391 lines)
- .ai_workspace/guides/DOCS_FOLDER_COMPLETE_REPORT.md (current state, 440 lines)

What I need:
1. Verify all files exist and are readable (use Read tool)
2. Tell me the current state of the main report (score, completeness)
3. Tell me what the audit recommends
4. Ask me what I want to do next

Don't make any changes yet. Just assess and report back.
```

---

## Post-Session: What to Tell Future Claude

### After Completing Phase 1 (90/100)

**For next session, say**:
```
I previously completed Phase 1 improvements on DOCS_REORGANIZATION_PROJECT_COMPLETION_REPORT.md.

Current status:
- Score: 90/100 (EXCELLENT)
- Phase 1 complete: Directory trees, ROI, FAQ, Glossary, Quick Wins added
- Audit: .ai_workspace/guides/DOCS_REORGANIZATION_REPORT_AUDIT.md

Next steps (optional):
- Phase 2 (8 hours → 95/100): Validation scripts, charts, template
- Phase 3 (4.5 hours → 98/100): Stakeholder feedback, benchmarks
- Phase 4 (11 hours → 100/100): Peer review, web version, video

Options:
A. Execute Phase 2 (I have 8 hours available)
B. Execute specific improvements only (tell me what you recommend)
C. Commit and finish (90/100 is good enough)

What do you recommend based on the audit?
```

---

### After Completing Phase 2 (95/100)

**For next session, say**:
```
DOCS_REORGANIZATION_PROJECT_COMPLETION_REPORT.md is now at 95/100 (NEAR-PERFECT).

Completed:
- Phase 1: Directory trees, ROI, FAQ, Glossary, Quick Wins
- Phase 2: Validation scripts, charts, template

Remaining (optional for 100/100):
- Phase 3 (4.5 hours → 98/100): Stakeholder feedback, industry benchmarks, anti-patterns
- Phase 4 (11 hours → 100/100): Peer review, interactive web version, video walkthrough

Options:
A. Execute Phase 3 (I have 4.5 hours)
B. Skip to Phase 4 (I have 11 hours)
C. Commit as-is (95/100 is excellent)

Recommendation: Commit as-is. 95/100 exceeds expectations for documentation reports.

Should I commit and push?
```

---

## Summary: The One Prompt to Rule Them All

**If you only remember one prompt, use this**:

```
I have a PROJECT COMPLETION REPORT for docs/ reorganization that needs improvements.

Files:
- Report: .ai_workspace/guides/DOCS_REORGANIZATION_PROJECT_COMPLETION_REPORT.md
- Audit: .ai_workspace/guides/DOCS_REORGANIZATION_REPORT_AUDIT.md

Current score: 85/100
Target score: [tell me: 90, 95, or 100]
Time available: [tell me: 2h, 10h, or 25h]

Instructions:
1. Read the audit to understand gaps
2. Read the report to understand current state
3. Recommend appropriate phase (Phase 1/2/3/4) based on my time
4. Execute improvements
5. Verify final score using scoring matrix

Start by reading the audit and telling me which phase I should do.
```

**This prompt works for ALL scenarios** because it:
- Provides file paths
- States current status
- Asks Claude to recommend next steps
- Gives Claude flexibility to guide you

---

## Final Checklist: Before Starting Next Session

**Preparation** (1 minute):
- [ ] Decide your goal (90/100, 95/100, or 100/100)
- [ ] Check time available (2h, 10h, or 25h)
- [ ] Copy appropriate prompt from this guide
- [ ] Paste into Claude Code
- [ ] Start working

**During Session**:
- [ ] Reference specific sections from audit (e.g., "audit page 32")
- [ ] Ask Claude to verify score after each phase
- [ ] Use Edit tool (not Write tool) to modify existing report
- [ ] Check scoring matrix before declaring "done"

**After Session**:
- [ ] Verify improvements were added (Read tool to check)
- [ ] Update this guide with new status (for future you)
- [ ] Commit changes (if satisfied with quality)
- [ ] Note final score for next session

---

**Document Status**: FINAL
**Created**: December 23, 2025
**Purpose**: Copy-paste prompts for next session recovery
**Use Case**: Resume documentation reorganization improvements
**Recommended**: Use Scenario 1 (Quick Wins, 2 hours → 90/100) for best ROI
