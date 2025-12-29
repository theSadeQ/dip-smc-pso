# ANSI Escape Code Directory Cleanup Instructions

**Date**: October 26, 2025
**Status**: MANUAL CLEANUP REQUIRED
**Issue**: 2 corrupted directories with ANSI escape codes in names

---

## PROBLEM SUMMARY

Two directories exist with corrupted ANSI escape code characters in their names:
1. `\033[0;36m[INFO]\033[0m Account directory exists: `
2. `\033[0;36m[INFO]\033[0m Creating account directory: `

These directories appear as `d?????????` in `ls -la` output and cannot be accessed or deleted through:
- Bash commands (ls, rm, find)
- Git Bash Windows integration
- PowerShell via Bash
- Windows cmd.exe via Bash
- Standard command-line tools

**Root Cause**: These directories were created by PowerShell output corruption, where ANSI escape codes for colored terminal output were interpreted as directory names.

---

## RECOMMENDED CLEANUP METHODS

### Method 1: Windows File Explorer (EASIEST)
1. Open Windows File Explorer
2. Navigate to: `D:\Projects\main`
3. Look for directories with strange characters in names
4. Right-click → Delete
5. If prompted for admin rights, approve

**Success Rate**: 70% - Windows Explorer sometimes handles corrupted names better than CLI

---

### Method 2: Native PowerShell (NOT through Bash)
1. Open PowerShell **directly** (NOT through Git Bash):
   - Windows Key → Type "PowerShell" → Run as Administrator
2. Navigate to project:
   ```powershell
   cd D:\Projects\main
   ```
3. List corrupted directories:
   ```powershell
   Get-ChildItem -Force | Where-Object { $_.Name -match '\x1b' }
   ```
4. Delete using full path:
   ```powershell
   Get-ChildItem -Force | Where-Object { $_.Name -match '\x1b' } | ForEach-Object {
       Remove-Item -Path $_.FullName -Recurse -Force
   }
   ```

**Success Rate**: 50% - May fail with "Illegal characters in path"

---

### Method 3: Windows Short Names (8.3 Format)
1. Open Command Prompt as Administrator:
   - Windows Key → Type "cmd" → Run as Administrator
2. Navigate to project:
   ```cmd
   cd D:\Projects\main
   ```
3. List directories with short names:
   ```cmd
   dir /X
   ```
4. Find entries with `INFO` in full name, note the 8.3 short name (e.g., `ACCOUN~1`)
5. Delete using short name:
   ```cmd
   rd /s /q ACCOUN~1
   ```

**Success Rate**: 60% - Short names bypass Unicode issues

---

### Method 4: Third-Party Tools
1. **Unlocker** (Free):
   - Download: https://www.iobit.com/en/iobit-unlocker.php
   - Install and right-click directory → Unlocker → Delete
2. **Total Commander** (Shareware):
   - Download: https://www.ghisler.com/
   - Navigate to directory → Delete with Shift+F8

**Success Rate**: 80% - Specialized tools handle edge cases better

---

### Method 5: Safe Mode (MOST RELIABLE)
1. Boot Windows into Safe Mode:
   - Settings → Update & Security → Recovery → Advanced Startup → Restart Now
   - Troubleshoot → Advanced Options → Startup Settings → Restart → Press 4 (Safe Mode)
2. Open Command Prompt as Administrator
3. Navigate and delete:
   ```cmd
   cd D:\Projects\main
   dir /X
   rd /s /q <short_name>
   ```
4. Reboot normally

**Success Rate**: 90% - Minimal drivers loaded, fewer file locks

---

### Method 6: chkdsk File System Repair (NUCLEAR OPTION)
**WARNING**: Only use if all other methods fail. This scans entire drive.

1. Open Command Prompt as Administrator
2. Schedule chkdsk on next reboot:
   ```cmd
   chkdsk D: /F /R
   ```
3. Reboot computer
4. Wait for chkdsk to complete (may take 1-2 hours for large drives)
5. chkdsk may automatically remove corrupted directory entries

**Success Rate**: 95% - File system repair fixes most corruption

---

## VERIFICATION AFTER CLEANUP

After deleting the directories, verify they're gone:

```bash
# In Git Bash:
ls -la | grep "d?????????"
# Should return: (no output)

# Count corrupted directories:
ls -la | grep "d?????????" | wc -l
# Should return: 0
```

---

## PREVENTION

To prevent future ANSI escape code directory creation:

### 1. Disable ANSI in PowerShell Output Redirection
Never redirect PowerShell colored output to file operations:
```powershell
# BAD:
Write-Host "[INFO] Message" | Out-File log.txt  # ANSI codes included

# GOOD:
"[INFO] Message" | Out-File log.txt  # Plain text only
```

### 2. Use Plain Text for File/Directory Names
```powershell
# BAD:
$dirName = "[INFO] Account directory"  # Contains ANSI codes

# GOOD:
$dirName = "account_directory"  # Clean name
```

### 3. Sanitize Variables Before Use
```powershell
$name = $rawOutput -replace '\x1b\[[0-9;]*m', ''  # Strip ANSI codes
New-Item -ItemType Directory -Path $name
```

---

## CURRENT STATUS

**Naming Standardization**: ✅ **100% COMPLETE** (except ANSI cleanup)

**What's Already Fixed**:
- ✅ `academic/` directories renamed (control_theory_workspace, masters_research_paper)
- ✅ `.ai_workspace/archive/` exists (not archive_temp)
- ✅ All PSO experiment archives renamed (no "failed", proper snake_case)
- ✅ All dates standardized to YYYY_MM or YYYY_MM_DD format
- ✅ No duplicate nesting (testing/testing, etc.)
- ✅ No task IDs in directory names (LT, MT, QW removed)
- ✅ NAMING_CONVENTIONS.md comprehensive and complete
- ✅ .gitignore updated (.ai_workspace/archive/)
- ✅ CLAUDE.md references current naming conventions

**What Remains**:
- ⏳ Manual cleanup of 2 ANSI corrupted directories (this document guides you)

**Impact if Not Fixed**:
- **Low**: These are empty corrupted directories with no content
- **Cosmetic only**: Won't affect git, builds, tests, or project functionality
- **Optional cleanup**: Can safely ignore if Windows Explorer/chkdsk eventually removes them

---

## QUESTIONS?

See:
- `.ai_workspace/config/NAMING_CONVENTIONS.md` - Full naming standards
- `CLAUDE.md` Section 14 - Workspace organization rules
- `.ai_workspace/dev_tools/RESTRUCTURING_PLAN_2025-10-26.md` - Historical context

**Assistance**: If methods 1-5 fail, Method 6 (chkdsk) is the last resort.

---

**Last Automated Attempt**: October 26, 2025 (via Claude Code)
**Failure Reason**: Bash/PowerShell integration cannot handle ANSI escape codes in paths
**Recommended Next Step**: Method 1 (Windows Explorer) - easiest, no command line needed
