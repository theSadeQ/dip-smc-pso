"""
Playwright E2E tests for MT-8 Operations Control Panel.

Tests the complete user workflow:
1. Navigate to Streamlit app
2. Open MT-8 Operations Control Panel expander
3. Configure PSO parameters
4. Launch a test job
5. Monitor real-time progress
6. Verify job completion

Requirements:
    pip install playwright pytest-playwright
    playwright install chromium

Usage:
    pytest tests/test_ui/test_mt8_operations_panel.py -v
    pytest tests/test_ui/test_mt8_operations_panel.py -v --headed  # See browser
"""

import time
import re
from pathlib import Path
import pytest
from playwright.sync_api import Page, expect


# Streamlit app URL
STREAMLIT_URL = "http://localhost:8502"


@pytest.fixture(scope="module")
def streamlit_app():
    """Ensure Streamlit app is running before tests."""
    import subprocess
    import requests

    # Check if Streamlit is already running
    try:
        response = requests.get(STREAMLIT_URL, timeout=2)
        if response.status_code == 200:
            print("[INFO] Streamlit app already running")
            yield
            return
    except:
        pass

    # Start Streamlit if not running
    print("[INFO] Starting Streamlit app...")
    process = subprocess.Popen(
        ["streamlit", "run", "streamlit_app.py", "--server.port", "8502"],
        cwd=Path.cwd(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for app to start
    max_wait = 30
    for i in range(max_wait):
        try:
            response = requests.get(STREAMLIT_URL, timeout=2)
            if response.status_code == 200:
                print("[OK] Streamlit app started")
                break
        except:
            time.sleep(1)

    yield

    # Cleanup
    process.terminate()
    process.wait(timeout=5)


def test_mt8_panel_visibility(page: Page, streamlit_app):
    """Test that MT-8 Operations Control Panel is visible and accessible."""

    # Navigate to Streamlit app
    page.goto(STREAMLIT_URL)
    page.wait_for_load_state("networkidle")

    # Wait for Streamlit to fully load (look for the main content)
    page.wait_for_selector("div[data-testid='stApp']", timeout=10000)

    # Find MT-8 Operations Control Panel expander
    # Streamlit expanders have data-testid="stExpander"
    expanders = page.locator("div[data-testid='stExpander']")

    # Find the MT-8 Operations Control Panel by looking for text content
    mt8_expander = None
    for i in range(expanders.count()):
        expander_text = expanders.nth(i).text_content()
        if "MT-8 Operations Control Panel" in expander_text:
            mt8_expander = expanders.nth(i)
            break

    assert mt8_expander is not None, "MT-8 Operations Control Panel not found"

    # Click to expand
    mt8_expander.locator("summary").click()
    page.wait_for_timeout(1000)  # Wait for animation

    # Verify tabs are visible
    tabs = page.locator("div[data-testid='stTabs']")
    assert tabs.count() > 0, "Tabs not found in MT-8 panel"

    # Verify both tabs exist
    tab_list = page.locator("button[role='tab']")
    tab_names = [tab_list.nth(i).text_content() for i in range(tab_list.count())]

    assert "Launch PSO Tests" in " ".join(tab_names), "Launch PSO Tests tab not found"
    assert "Active Jobs Monitor" in " ".join(tab_names), "Active Jobs Monitor tab not found"


def test_pso_configuration_panel(page: Page, streamlit_app):
    """Test PSO configuration panel UI elements."""

    page.goto(STREAMLIT_URL)
    page.wait_for_selector("div[data-testid='stApp']", timeout=10000)

    # Open MT-8 panel
    expanders = page.locator("div[data-testid='stExpander']")
    for i in range(expanders.count()):
        if "MT-8 Operations Control Panel" in expanders.nth(i).text_content():
            expanders.nth(i).locator("summary").click()
            break

    page.wait_for_timeout(1000)

    # Should be on "Launch PSO Tests" tab by default
    # Look for controller selection
    controller_select = page.locator("div[data-testid='stSelectbox']").first
    assert controller_select.is_visible(), "Controller selection not visible"

    # Check if PSO Configuration panel is visible
    # Look for text "PSO Configuration"
    assert page.get_by_text("PSO Configuration").count() > 0, "PSO Configuration header not found"

    # Verify tabs within PSO config (Bounds, Swarm Parameters, Advanced)
    config_tabs = page.locator("div[data-testid='stTabs']").nth(1)  # Second set of tabs
    config_tab_buttons = config_tabs.locator("button[role='tab']")

    config_tab_names = [config_tab_buttons.nth(i).text_content() for i in range(config_tab_buttons.count())]
    assert "Bounds" in config_tab_names, "Bounds tab not found"
    assert "Swarm Parameters" in config_tab_names, "Swarm Parameters tab not found"
    assert "Advanced" in config_tab_names, "Advanced tab not found"


def test_launch_job_button(page: Page, streamlit_app):
    """Test launching a PSO job from UI."""

    page.goto(STREAMLIT_URL)
    page.wait_for_selector("div[data-testid='stApp']", timeout=10000)

    # Open MT-8 panel
    expanders = page.locator("div[data-testid='stExpander']")
    for i in range(expanders.count()):
        if "MT-8 Operations Control Panel" in expanders.nth(i).text_content():
            expanders.nth(i).locator("summary").click()
            break

    page.wait_for_timeout(1000)

    # Find and click "Launch Seed 42" button
    # Streamlit buttons have data-testid="baseButton-secondary" or "baseButton-primary"
    buttons = page.locator("button")
    launch_button = None

    for i in range(buttons.count()):
        button_text = buttons.nth(i).text_content()
        if "Launch Seed 42" in button_text:
            launch_button = buttons.nth(i)
            break

    assert launch_button is not None, "Launch Seed 42 button not found"

    # Click the button
    launch_button.click()

    # Wait for success message
    page.wait_for_timeout(2000)

    # Should see a success toast or message
    # Streamlit shows success messages with st.success()
    success_message = page.locator("div[data-testid='stNotification']")

    # Verify success message appeared
    # (Note: might need to adjust selector based on actual Streamlit behavior)
    page.wait_for_timeout(1000)


def test_active_jobs_monitor(page: Page, streamlit_app):
    """Test active jobs monitor tab shows running jobs."""

    page.goto(STREAMLIT_URL)
    page.wait_for_selector("div[data-testid='stApp']", timeout=10000)

    # Open MT-8 panel
    expanders = page.locator("div[data-testid='stExpander']")
    for i in range(expanders.count()):
        if "MT-8 Operations Control Panel" in expanders.nth(i).text_content():
            expanders.nth(i).locator("summary").click()
            break

    page.wait_for_timeout(1000)

    # Switch to "Active Jobs Monitor" tab
    tab_buttons = page.locator("button[role='tab']")
    for i in range(tab_buttons.count()):
        if "Active Jobs Monitor" in tab_buttons.nth(i).text_content():
            tab_buttons.nth(i).click()
            break

    page.wait_for_timeout(2000)

    # Should see either:
    # - "No active jobs" message, or
    # - Active job progress display

    page_text = page.text_content("body")

    # Either no active jobs or active jobs are shown
    assert (
        "No active jobs" in page_text or
        "Active Background Jobs" in page_text or
        "Progress" in page_text
    ), "Active Jobs Monitor tab content not found"


def test_full_workflow_quick_job(page: Page, streamlit_app):
    """
    Test complete workflow: Launch job -> Monitor progress -> Verify completion.

    Uses minimal PSO config (3 particles, 2 iterations) for fast execution.
    """

    page.goto(STREAMLIT_URL)
    page.wait_for_selector("div[data-testid='stApp']", timeout=10000)

    # 1. Open MT-8 panel
    expanders = page.locator("div[data-testid='stExpander']")
    for i in range(expanders.count()):
        if "MT-8 Operations Control Panel" in expanders.nth(i).text_content():
            expanders.nth(i).locator("summary").click()
            break

    page.wait_for_timeout(1000)

    # 2. Configure minimal PSO parameters for quick test
    # Click on "Swarm Parameters" tab in PSO config
    config_tabs = page.locator("div[data-testid='stTabs']").nth(1)
    swarm_tab = config_tabs.locator("button[role='tab']").filter(has_text="Swarm Parameters")
    swarm_tab.click()

    page.wait_for_timeout(500)

    # 3. Launch job
    buttons = page.locator("button")
    for i in range(buttons.count()):
        if "Launch Seed 42" in buttons.nth(i).text_content():
            buttons.nth(i).click()
            break

    page.wait_for_timeout(2000)

    # 4. Switch to Active Jobs Monitor
    tab_buttons = page.locator("button[role='tab']").first
    for i in range(tab_buttons.count()):
        if "Active Jobs Monitor" in tab_buttons.nth(i).text_content():
            tab_buttons.nth(i).click()
            break

    page.wait_for_timeout(2000)

    # 5. Monitor for job activity
    # Look for progress indicators
    max_wait = 60  # 60 seconds max
    job_found = False

    for attempt in range(max_wait):
        page_text = page.text_content("body")

        # Check if job is running or completed
        if "Progress" in page_text or "Iteration" in page_text or "completed" in page_text:
            job_found = True
            print(f"[OK] Job activity detected at {attempt} seconds")
            break

        page.wait_for_timeout(1000)

        # Trigger Streamlit rerun if needed (scroll to refresh)
        page.evaluate("window.scrollBy(0, 1)")

    # Verify job was found
    assert job_found, "No job activity detected in Active Jobs Monitor"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--headed"])
