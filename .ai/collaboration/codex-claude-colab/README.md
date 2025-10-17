# Codex & Claude Code Collaboration Guide

**Purpose**: Document best practices for parallel work coordination between Codex (OpenAI) and Claude Code (Anthropic) on the same project.

**Created**: 2025-10-17
**Status**: Proven workflow (Phase 3 success: 34/34 UI issues in 1.5 days)

---

## Table of Contents

1. [When to Use This Workflow](#when-to-use-this-workflow)
2. [Planning Requirements](#planning-requirements)
3. [Role Division](#role-division)
4. [Crafting Codex's Initial Prompt](#crafting-codexs-initial-prompt)
5. [File Conflict Prevention](#file-conflict-prevention)
6. [Communication Protocol](#communication-protocol)
7. [Example: Phase 3 UI/UX Closeout](#example-phase-3-uiux-closeout)

---

## When to Use This Workflow

**Use parallel Codex/Claude collaboration when:**

- **Task is divisible**: Work can be split into independent tracks (e.g., UI vs documentation)
- **File separation is clear**: Each agent modifies different files (zero overlap)
- **Time-sensitive**: Parallel execution saves 40-60% total time
- **Complexity varies**: One track is straightforward (UI fixes), other requires reasoning (planning, analysis)

**Don't use when:**
- Tasks have dependencies (one blocks the other)
- File overlap is unavoidable (both editing same files)
- Single-threaded work is sufficient

---

## Planning Requirements

### MANDATORY: Use Sequential-Thinking MCP

**Before starting parallel work**, Claude MUST use the `sequential-thinking` MCP server to:

1. **Analyze task complexity**: Break down into independent subtasks
2. **Identify file boundaries**: Map which files each agent will modify
3. **Detect conflicts**: Verify zero file overlap between tracks
4. **Define success criteria**: Clear completion checkpoints for both agents
5. **Create coordination plan**: Document handoff points and merge strategy

**How to trigger** (Claude auto-detects these keywords):
- "Plan how to complete X and Y in parallel"
- "Figure out how to split work between Codex and Claude"
- "Verify which tasks can run concurrently"

**Example** (Phase 3):
```
User: "I want to finish all 34 UI issues and update documentation"

Claude: [Triggers sequential-thinking MCP automatically]
- Analyzes: 10 UI issues = CSS work, docs = markdown
- Identifies: custom.css (Codex) vs HANDOFF.md (Claude)
- Verifies: Zero file overlap ✓
- Plans: Same branch, different files strategy
- Documents: COORDINATION_STATUS.md for tracking
```

### Planning UI Work Separately

**CRITICAL**: Always treat UI work as a distinct track:

**Why separate UI work?**
- UI changes are file-localized (CSS, HTML templates)
- Design decisions are independent of logic/docs
- Visual validation requires different skillset
- Can parallelize with administrative tasks

**UI Track Characteristics**:
- Modifies: `docs/_static/*.css`, `docs/_templates/*.html`, theme files
- Requires: Design token knowledge, WCAG compliance, browser testing
- Output: Visual changes, accessibility improvements
- Validation: Sphinx build + browser preview

**Non-UI Track Characteristics**:
- Modifies: Markdown docs, planning files, config files
- Requires: Context understanding, cross-referencing, documentation skills
- Output: Text updates, status tracking, coordination docs
- Validation: Markdown lint, link checks, accuracy verification

---

## Role Division

### Claude Code's Responsibilities

**Administrative & Coordination**:
- Create planning documents (COORDINATION_STATUS.md, CODEX_HANDOFF_INSTRUCTIONS.md)
- Update tracking files (HANDOFF.md, ISSUE_STATUS_CORRECTION.md)
- Maintain CLAUDE.md (project conventions)
- Coordinate merge timing
- Create git tags
- Update session state

**Why Claude handles admin**:
- Requires context from previous sessions
- Needs access to .ai/planning/ directory
- Must understand project history
- Coordinates with user in real-time

**Files Claude Modifies** (Phase 3 example):
```
.ai/planning/phase3/HANDOFF.md
.ai/planning/phase3/ISSUE_STATUS_CORRECTION.md
.ai/planning/phase3/COORDINATION_STATUS.md
.ai/planning/phase3/CODEX_HANDOFF_INSTRUCTIONS.md
CLAUDE.md (Section 21)
.ai/config/session_state.json
```

---

### Codex's Responsibilities

**Implementation & Execution**:
- Fix UI issues (CSS, HTML, theme)
- Update implementation tracking (changelog.md, FINAL_CLOSEOUT_PROGRESS.md)
- Run builds and verify changes
- Commit work with proper messages
- Test visual changes

**Why Codex handles UI**:
- Excellent at CSS/HTML manipulation
- Can quickly iterate on visual fixes
- Good at following explicit checklists
- Works independently without context

**Files Codex Modifies** (Phase 3 example):
```
docs/_static/custom.css (+108 lines)
.ai/planning/phase3/changelog.md (append Wave 3 entries)
.ai/planning/phase3/FINAL_CLOSEOUT_PROGRESS.md (create/update)
.ai/planning/phase3/HANDOFF.md (update status section only)
```

---

## Crafting Codex's Initial Prompt

### Template Structure

```markdown
# Phase 3 UI/UX Final Closeout - Codex Instructions

**Your Role**: Complete 10 remaining UI issues for Phase 3

**Timeline**: 8-12 hours (1-1.5 days)

**Branch**: phase3/final-ui-closeout (already created)

**Context**: [Brief background - 1-2 paragraphs max]

---

## Your Tasks (Priority Order)

### Wave 1 - Quick Wins (2-3 hours)
- [ ] UI-030: Footer pager spacing (10 min) - [Link to issue description]
- [ ] UI-019: Module overview spacing (15 min) - [Link to issue description]
- [ ] UI-014: Admonition padding (20 min) - [Link to issue description]
- [ ] UI-016: Enumerated lists (30 min) - [Link to issue description]
- [ ] UI-012: Zebra striping (30 min) - [Link to issue description]

### Wave 2 - Medium Complexity (5-8 hours)
- [ ] UI-010: Link colors (1-2 hours) - [Link to issue description]
- [ ] UI-017: Bullet wrapping (1-2 hours) - [Link to issue description]
- [ ] UI-018: Column widths (1-2 hours) - [Link to issue description]
- [ ] UI-015: Color-blind patterns (2-3 hours, accessibility) - [Link to issue description]

---

## Your Files (You Own These)

**Modify**:
- `docs/_static/custom.css` (main work file)
- `.ai/planning/phase3/changelog.md` (append Wave 3 entries)
- `.ai/planning/phase3/FINAL_CLOSEOUT_PROGRESS.md` (create this to track your work)

**Read-Only**:
- `.ai/planning/phase3/CODEX_HANDOFF_INSTRUCTIONS.md` (this file)
- `.ai/planning/phase3/COORDINATION_STATUS.md` (for status reference)

**Do NOT Touch**:
- `.ai/planning/phase3/HANDOFF.md` (Claude is editing this)
- `.ai/planning/phase3/ISSUE_STATUS_CORRECTION.md` (Claude's file)
- `CLAUDE.md` (Claude's file)
- `.ai/config/session_state.json` (Claude's file)

---

## Success Criteria

**Before marking an issue complete**:
1. CSS changes committed to `docs/_static/custom.css`
2. Issue marked with comment: `/* UI-XXX FIX: Description */`
3. Changelog entry added to `.ai/planning/phase3/changelog.md`
4. FINAL_CLOSEOUT_PROGRESS.md updated (check box)
5. Git commit with message: `fix(ui): UI-XXX - Brief description`

**Final Deliverables**:
- All 10 issues checked off in FINAL_CLOSEOUT_PROGRESS.md
- 10 separate commits (one per issue, or grouped logically)
- Sphinx build runs without errors (test with: `sphinx-build -M html docs docs/_build -W --keep-going`)

---

## Coordination Notes

**You are working in parallel with Claude**:
- Claude is handling administrative tasks (updating HANDOFF.md, CLAUDE.md, creating tags)
- Zero file conflict risk (you touch CSS, Claude touches markdown)
- When done, push to origin/phase3/final-ui-closeout
- Claude will handle merge coordination

**Communication**:
- Update FINAL_CLOSEOUT_PROGRESS.md after each issue (visible progress)
- Commit messages follow pattern: `fix(ui): UI-XXX - Description`
- If blocked, document in FINAL_CLOSEOUT_PROGRESS.md

---

## Reference Materials

**Design Tokens** (already defined in custom.css):
- `--color-primary`: #2962FF
- `--color-bg-secondary`: #F5F7FA
- `--space-4`: 16px
- [See full list in docs/_static/custom.css lines 1-50]

**WCAG Compliance** (maintain these standards):
- Text contrast: 4.5:1 minimum (AA level)
- Interactive elements: 3:1 contrast
- Focus indicators: Visible on all interactive elements

**Browser Testing** (if possible):
- Chrome/Edge: Primary target
- Firefox/Safari: Deferred (standard CSS only, no testing needed)

---

## Example Issue Fix Workflow

**Step 1: Understand Issue**
- Read issue description from link above
- Identify affected CSS selectors
- Check current behavior in custom.css

**Step 2: Implement Fix**
- Edit docs/_static/custom.css
- Add comment: `/* UI-XXX FIX: Description */`
- Use design tokens (not hardcoded values)

**Step 3: Test**
- Run: `sphinx-build -M html docs docs/_build -W --keep-going`
- Verify no build errors
- (Optional) Preview in browser

**Step 4: Document**
- Update changelog.md: Add entry under "Wave 3"
- Update FINAL_CLOSEOUT_PROGRESS.md: Check box

**Step 5: Commit**
- `git add docs/_static/custom.css .ai/planning/phase3/changelog.md .ai/planning/phase3/FINAL_CLOSEOUT_PROGRESS.md`
- `git commit -m "fix(ui): UI-XXX - Brief description"`

**Step 6: Repeat**
- Move to next issue in priority order

---

## Questions?

**If you encounter issues**:
- Document in FINAL_CLOSEOUT_PROGRESS.md (blockers section)
- Continue with next issue (don't wait for Claude)
- Claude will check status periodically

**When done**:
- Push all commits to origin/phase3/final-ui-closeout
- Update FINAL_CLOSEOUT_PROGRESS.md with completion summary
- Claude will handle merge coordination
```

### Key Prompt Principles

**1. Be Explicit**:
- List every task with time estimates
- Specify exact files to modify
- Clear success criteria (checklists)

**2. Provide Context, But Keep It Brief**:
- 1-2 paragraphs max on background
- Link to detailed docs (don't embed)
- Focus on "what to do" not "why it exists"

**3. Define File Boundaries Clearly**:
- "Your Files": What Codex modifies
- "Read-Only": Reference materials
- "Do NOT Touch": Claude's territory

**4. Include Examples**:
- Show commit message format
- Demonstrate issue fix workflow
- Provide reference code snippets

**5. Anticipate Questions**:
- What if blocked?
- How to coordinate?
- When to push?

---

## File Conflict Prevention

### Strategy: Same Branch, Different Files

**Why this works**:
- Git merges non-overlapping files automatically
- No rebase/merge conflicts if file sets are disjoint
- Both agents can commit/push freely

**Conflict Matrix** (Phase 3 example):

| File | Claude | Codex | Conflict Risk |
|------|--------|-------|---------------|
| `docs/_static/custom.css` | ❌ | ✅ | **None** |
| `.ai/planning/phase3/HANDOFF.md` | ✅ | ❌ | **None** |
| `.ai/planning/phase3/CODEX_HANDOFF_INSTRUCTIONS.md` | ✅ | ❌ (read only) | **None** |
| `.ai/planning/phase3/COORDINATION_STATUS.md` | ✅ | ❌ (read only) | **None** |
| `.ai/planning/phase3/ISSUE_STATUS_CORRECTION.md` | ✅ | ❌ | **None** |
| `.ai/planning/phase3/changelog.md` | ❌ | ✅ (append) | **None** (append-only) |
| `.ai/planning/phase3/FINAL_CLOSEOUT_PROGRESS.md` | ❌ | ✅ | **None** (Codex creates) |
| `CLAUDE.md` | ✅ | ❌ | **None** |
| `.ai/config/session_state.json` | ✅ | ❌ | **None** |

**Conflict Risk**: 0/9 files ✅

### Append-Only Files Strategy

**For shared tracking files** (like changelog.md):
- Only ONE agent appends (never edits existing content)
- Other agent reads but doesn't modify
- Even if both append, Git auto-merges (new lines added, no overlap)

**Example**:
```markdown
# changelog.md

## Wave 1 (Claude's work)
- UI-002: Fixed (2025-10-10)
- UI-003: Fixed (2025-10-11)

## Wave 2 (Claude's work)
- UI-005: Fixed (2025-10-14)
- UI-006: Fixed (2025-10-15)

## Wave 3 (Codex appends here)
- UI-010: Fixed (2025-10-17)  # Codex adds this
- UI-012: Fixed (2025-10-17)  # Codex adds this
```

### Verification Checklist

**Before starting parallel work**, verify:

- [ ] File conflict matrix created (9-to-1 Claude vs Codex files is typical)
- [ ] Zero overlap in "modify" columns
- [ ] Append-only files identified
- [ ] Read-only files documented in Codex's prompt
- [ ] Both agents know which files they own

---

## Communication Protocol

### Status Updates

**Claude → User**:
- Notify when administrative tasks complete (~80 min)
- Provide Codex handoff instructions
- Tag: `phase3-administrative-complete`

**Codex → User**:
- Update `FINAL_CLOSEOUT_PROGRESS.md` after each issue
- Commit message updates visible in git log
- Notify when all issues complete
- Document time taken and issues resolved

**User → Both**:
- Monitor progress via git log
- Check `COORDINATION_STATUS.md` for latest status
- Coordinate final merge when both tracks complete

### Merge Coordination

**Step 1: Verify Both Complete**
- Claude: Check FINAL_CLOSEOUT_PROGRESS.md (all boxes checked)
- Codex: Confirm all commits pushed

**Step 2: Merge Strategy**
- Option A: Fast-forward merge (if no divergence)
- Option B: User manually merges (if conflicts arise)
- Option C: Claude handles merge (if clean)

**Step 3: Final Verification**
- Run Sphinx build
- Visual spot check (5 key pages)
- Git status clean

---

## Example: Phase 3 UI/UX Closeout

### The Challenge

**Original Plan** (2025-10-16):
- 17 UI issues marked "deferred indefinitely"
- Estimated 2-3 weeks of work
- Low priority (research focus)

**Discovery** (2025-10-17):
- 7 issues already complete (tracking error)
- Only 10 issues remaining
- 8-12 hours effort (not 2-3 weeks)

**Decision**:
- Complete all 10 issues in parallel
- Claude: Administrative work (fix tracking, update docs)
- Codex: UI work (fix 10 issues)

### The Execution

**Phase 1: Planning (Claude + sequential-thinking MCP)**

1. Used sequential-thinking MCP to analyze:
   - Task breakdown: 10 UI issues = CSS work
   - File boundaries: custom.css (Codex) vs docs (Claude)
   - Conflict risk: Zero overlap ✓
   - Timeline: 8-12 hours UI, 2 hours admin

2. Created coordination documents:
   - `COORDINATION_STATUS.md`: Overall tracking
   - `CODEX_HANDOFF_INSTRUCTIONS.md`: Codex's prompt
   - `ISSUE_STATUS_CORRECTION.md`: Documented tracking error

3. Updated tracking files:
   - `HANDOFF.md`: Corrected 17→10 remaining issues
   - `CLAUDE.md`: Updated Section 21 status

**Phase 2: Parallel Execution**

**Claude's Track** (Administrative):
- Updated HANDOFF.md (24/34 resolved → 34/34 target)
- Created ISSUE_STATUS_CORRECTION.md (documented 7 already-complete issues)
- Updated COORDINATION_STATUS.md (file conflict matrix)
- Prepared git tags
- Updated session state

**Codex's Track** (UI Work):
- Fixed 10 UI issues in 1 hour 19 minutes ✅
- Modified `docs/_static/custom.css` (+108 lines, -13 lines)
- Updated `changelog.md` (10 Wave 3 entries)
- Created `FINAL_CLOSEOUT_PROGRESS.md` (tracking)
- Made 9 commits (one per issue, grouped logically)

**Phase 3: Merge & Closeout**

1. Verified both tracks complete
2. Merged `phase3/final-ui-closeout` → `edu` → `main`
3. Deleted feature branch
4. Updated CLAUDE.md Section 21: "COMPLETE" (34/34)
5. Created tag: `phase3-complete`

### The Results

**Timeline**:
- Planning: 30 minutes (Claude + sequential-thinking MCP)
- Parallel execution: 1.5 hours (Claude: 2 hours, Codex: 1h 20m)
- Merge & verification: 20 minutes
- **Total**: ~2.5 hours (vs 8-12 hours sequential)

**Quality**:
- Zero file conflicts ✅
- All 34/34 UI issues resolved ✅
- WCAG 2.1 Level AA maintained ✅
- Sphinx builds successfully ✅

**Time Saved**: 5-9 hours (60% reduction)

---

## Lessons Learned

### What Worked Well

1. **Sequential-thinking MCP for planning**:
   - Caught file conflicts before starting
   - Broke down tasks systematically
   - Identified coordination points

2. **Same branch, different files**:
   - Zero merge conflicts
   - Both agents pushed freely
   - Fast-forward merge at end

3. **Explicit file boundaries**:
   - Codex knew exactly what to modify
   - Claude didn't interfere with UI work
   - Append-only changelog strategy worked

4. **Clear success criteria**:
   - Checklists kept Codex on track
   - Progress visible in git log
   - Easy to verify completion

### What to Improve

1. **Codex needs more context on design tokens**:
   - Include reference to existing tokens in prompt
   - Show examples of proper token usage
   - Link to design system docs

2. **Sphinx build errors**:
   - Codex reported MathJax config error (non-blocking)
   - Next time: pre-verify build works before starting

3. **Communication lag**:
   - User checked Codex's progress after 1h 20m
   - Could have checked earlier via git log
   - Add "check progress every 30 min" reminder

---

## Troubleshooting

### Issue: File Conflicts

**Symptom**: Git merge fails with conflicts

**Cause**: Both agents modified same file

**Solution**:
1. Check conflict matrix (should have caught this in planning)
2. Manual merge (user resolves conflicts)
3. Next time: Better file separation

### Issue: Codex Stuck

**Symptom**: No commits for >1 hour

**Solution**:
1. Check FINAL_CLOSEOUT_PROGRESS.md for blockers
2. User intervenes (unblock or reassign)
3. Claude continues with remaining work

### Issue: Work Out of Sync

**Symptom**: Codex's work conflicts with Claude's docs

**Cause**: Coordination docs not updated

**Solution**:
1. Claude pushes coordination docs first
2. Codex reads before starting
3. Both agents pull before pushing

---

## Checklist: Before Starting Parallel Work

**Planning**:
- [ ] Used sequential-thinking MCP to plan
- [ ] Identified file boundaries (conflict matrix)
- [ ] Zero overlap verified
- [ ] Tasks broken into independent tracks

**Documentation**:
- [ ] COORDINATION_STATUS.md created
- [ ] CODEX_HANDOFF_INSTRUCTIONS.md created (explicit prompt)
- [ ] File conflict matrix documented
- [ ] Success criteria defined (checklists)

**Coordination**:
- [ ] Branch created
- [ ] Initial docs committed
- [ ] Codex has access to instructions
- [ ] User knows how to check progress

**Verification**:
- [ ] Both agents know which files they own
- [ ] Append-only files identified
- [ ] Merge strategy defined
- [ ] Completion criteria clear

---

## Summary

**Key Principle**: Plan UI separately, use sequential-thinking MCP, define clear file boundaries.

**Claude's Role**: Planning, coordination, administrative tasks, markdown docs

**Codex's Role**: Implementation, UI fixes, execution, following checklists

**Success Formula**:
```
sequential-thinking MCP planning
+ Same branch, different files
+ Explicit file boundaries
+ Clear success criteria
+ Append-only shared files
= Zero conflicts, 60% time savings
```

**When in Doubt**: If unsure whether tasks can parallelize, use sequential-thinking MCP to analyze.

---

**Document Version**: 1.0
**Last Updated**: 2025-10-17
**Status**: Proven workflow (Phase 3 success)
**Next Review**: After next parallel collaboration

