# Recovery from Token Limit or Multi-Month Gap

You are recovering from a token limit or returning after a gap.

**MANDATORY: Execute these steps in order:**

1. Run the recovery script:
   ```bash
   bash .dev_tools/recover_project.sh
   ```

2. Parse the output and extract:
   - Current phase and progress
   - Last 5 commits (to understand recent work)
   - Uncommitted changes (if any)
   - Recommended next actions

3. **CRITICAL: Read uncommitted work-in-progress files**

   If uncommitted files exist, intelligently read status documents to understand current situation:

   **Priority 1 - Active Work Status** (read FIRST):
   - `*_STATUS.md` (current work status)
   - `*_REPORT.md` (analysis reports)
   - `*_ANALYSIS.md` (findings/results)

   **Priority 2 - Recent Scripts** (if status files mention them):
   - New `.py` scripts in `scripts/` or root
   - Test files with relevant names

   **Priority 3 - Data Files** (only if needed for context):
   - `.csv`, `.json` summary files mentioned in status docs

   **Example patterns to detect:**
   ```
   benchmarks/MT6_AGENT_B_STATUS.md → Read immediately
   benchmarks/MT6_FIXED_BASELINE_REPORT.md → Read immediately
   scripts/mt6_fixed_baseline.py → Read if status references it
   ```

   **Extract from these files:**
   - What problem is being investigated?
   - What findings/discoveries were made?
   - What's the proposed next step or solution?
   - Are there any blockers or open questions?

4. Present to user with **full context**:
   ```
   ✅ Recovery Complete!

   Phase: [phase name]
   Progress: [X/Y tasks, Z% complete]

   Recent Work:
   - [last 3 commit messages]

   Status: [clean / uncommitted changes detected]

   Current Situation (from uncommitted work):
   - Problem: [what's being investigated]
   - Discovery: [key findings from status files]
   - Proposed Solution: [next steps identified]

   Recommended Next:
   - [top 3 recommended tasks based on actual work state]
   ```

5. Ask user: "Should I continue with [specific next step from status files]?"

**CRITICAL RULES:**
- Do NOT skip the recovery script - it provides critical context!
- Do NOT just list uncommitted files - READ them to understand the situation!
- Do NOT present generic recommendations - base them on actual work state!
- If you see `*_STATUS.md` or `*_REPORT.md` uncommitted, you MUST read them before presenting summary!
