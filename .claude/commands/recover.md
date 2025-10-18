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

3. Present to user:
   ```
   ✅ Recovery Complete!

   Phase: [phase name]
   Progress: [X/Y tasks, Z% complete]

   Recent Work:
   - [last 3 commit messages]

   Status: [clean / uncommitted changes detected]

   Recommended Next:
   - [top 3 recommended tasks]
   ```

4. Ask user: "What would you like to continue with?"

**Do NOT skip the recovery script - it provides critical context!**
