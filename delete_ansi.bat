@echo off
echo Attempting to delete ANSI-corrupted directories...
echo.

cd /d D:\Projects\main

echo Method 1: Using wildcard patterns
rd /s /q "[0*" 2>nul && echo Success: Deleted via [0* pattern || echo Failed: [0* pattern

echo.
echo Method 2: Using chkdsk (may require restart)
echo Note: This will scan and fix filesystem errors
chkdsk D: /F /X 2>nul && echo Success: chkdsk completed || echo Failed: chkdsk (may need admin/reboot)

echo.
echo Method 3: Using fsutil (requires admin)
fsutil dirty set D: 2>nul && echo Success: Marked disk for check on next boot || echo Failed: fsutil

echo.
echo Verification: Checking pytest
python -m pytest --collect-only -q 2>&1 | findstr "collected"

pause
