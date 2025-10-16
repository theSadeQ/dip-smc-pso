@echo off
REM ==========================================================================
REM Wave 1 Lighthouse Test - Open All Pages in Chrome
REM ==========================================================================

echo.
echo Opening all 5 test pages in Chrome...
echo.

start chrome "http://localhost:9000/"
timeout /t 2 /nobreak >nul

start chrome "http://localhost:9000/guides/getting-started.html"
timeout /t 2 /nobreak >nul

start chrome "http://localhost:9000/reference/controllers/index.html"
timeout /t 2 /nobreak >nul

start chrome "http://localhost:9000/guides/theory/smc-theory.html"
timeout /t 2 /nobreak >nul

start chrome "http://localhost:9000/benchmarks/index.html"
timeout /t 2 /nobreak >nul

echo.
echo All 5 pages opened in Chrome.
echo.
echo Next Steps:
echo 1. Press F12 in each tab to open DevTools
echo 2. Click Lighthouse tab
echo 3. Select Accessibility only, Desktop mode
echo 4. Click "Analyze page load"
echo 5. Save HTML report and take screenshot
echo.
echo See QUICK_CHECKLIST.txt for detailed workflow.
echo.
pause
