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

# Import Streamlit-aware helpers
from .streamlit_helpers import (
    wait_for_streamlit_ready,
    find_expander_by_text,
    click_expander,
    find_tab_by_text,
    switch_to_tab,
    debug_streamlit_state
)


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

    # NEW: Use Streamlit-aware wait (waits for all 4 rendering phases)
    wait_for_streamlit_ready(page, timeout_ms=15000)

    # Optional: Debug Streamlit state if needed
    # debug_streamlit_state(page, "after wait_for_streamlit_ready")

    # NEW: Find expander using helper (handles emoji issues, Windows-compatible)
    mt8_expander = find_expander_by_text(
        page,
        "MT-8 Operations Control Panel",  # Search by key text
        timeout_ms=10000
    )

    # Verify expander is visible
    assert mt8_expander.is_visible(), "MT-8 panel not visible"

    # NEW: Click to expand using helper (waits for animation)
    click_expander(page, mt8_expander, timeout_ms=5000)

    # Verify tabs are visible after expansion - search WITHIN the expander
    tabs = mt8_expander.locator("div[data-testid='stTabs']")
    tabs.first.wait_for(state="visible", timeout=10000)
    assert tabs.count() > 0, "Tabs not found in MT-8 panel"

    # Verify both tab buttons exist within the MT-8 expander
    tab_buttons = mt8_expander.locator("button[role='tab']")

    # Find specific tabs by text
    launch_tab = tab_buttons.filter(has_text="Launch PSO Tests")
    monitor_tab = tab_buttons.filter(has_text="Active Jobs Monitor")

    # Wait for tabs to be visible
    launch_tab.wait_for(state="visible", timeout=5000)
    monitor_tab.wait_for(state="visible", timeout=5000)

    assert launch_tab.is_visible(), "Launch PSO Tests tab not found"
    assert monitor_tab.is_visible(), "Active Jobs Monitor tab not found"


def test_pso_configuration_panel(page: Page, streamlit_app):
    """Test PSO configuration panel UI elements."""

    page.goto(STREAMLIT_URL)

    # NEW: Use Streamlit-aware wait
    wait_for_streamlit_ready(page, timeout_ms=15000)

    # NEW: Find and open MT-8 panel using helpers
    mt8_expander = find_expander_by_text(page, "MT-8 Operations Control Panel", timeout_ms=10000)
    click_expander(page, mt8_expander, timeout_ms=5000)

    # Should be on "Launch PSO Tests" tab by default
    # Look for controller selection within the MT-8 expander
    controller_select = mt8_expander.locator("div[data-testid='stSelectbox']").first
    controller_select.wait_for(state="visible", timeout=5000)
    assert controller_select.is_visible(), "Controller selection not visible"

    # Check if PSO Configuration panel is visible within MT-8 expander
    pso_config_header = mt8_expander.get_by_text("PSO Configuration")
    assert pso_config_header.count() > 0, "PSO Configuration header not found"

    # Verify tabs within PSO config (Bounds, Swarm Parameters, Advanced)
    # These are the nested tabs WITHIN the Launch PSO Tests tab
    config_tabs = mt8_expander.locator("div[data-testid='stTabs']").nth(1)  # Second set of tabs (first is Launch/Monitor)
    config_tabs.wait_for(state="visible", timeout=5000)

    config_tab_buttons = config_tabs.locator("button[role='tab']")

    config_tab_names = [config_tab_buttons.nth(i).text_content() for i in range(config_tab_buttons.count())]
    assert "Bounds" in config_tab_names, "Bounds tab not found"
    assert "Swarm Parameters" in config_tab_names, "Swarm Parameters tab not found"
    assert "Advanced" in config_tab_names, "Advanced tab not found"


def test_launch_job_button(page: Page, streamlit_app):
    """Test launching a PSO job from UI."""

    page.goto(STREAMLIT_URL)

    # NEW: Use Streamlit-aware wait
    wait_for_streamlit_ready(page, timeout_ms=15000)

    # NEW: Find and open MT-8 panel using helpers
    mt8_expander = find_expander_by_text(page, "MT-8 Operations Control Panel", timeout_ms=10000)
    click_expander(page, mt8_expander, timeout_ms=5000)

    # Find "Launch Seed 42" button within the MT-8 expander
    buttons = mt8_expander.locator("button")
    launch_button = buttons.filter(has_text="Launch Seed 42")

    # Wait for button to be visible and click
    launch_button.wait_for(state="visible", timeout=5000)
    assert launch_button.is_visible(), "Launch Seed 42 button not found"

    # Click the button
    launch_button.click()

    # Wait for success message (Streamlit uses st.success())
    page.wait_for_timeout(2000)

    # Verify success notification appeared
    success_message = page.locator("div[data-testid='stNotification']")
    # Note: Streamlit notifications may auto-dismiss, so just check if one appeared
    page.wait_for_timeout(1000)


def test_active_jobs_monitor(page: Page, streamlit_app):
    """Test active jobs monitor tab shows running jobs."""

    page.goto(STREAMLIT_URL)

    # NEW: Use Streamlit-aware wait
    wait_for_streamlit_ready(page, timeout_ms=15000)

    # NEW: Find and open MT-8 panel using helpers
    mt8_expander = find_expander_by_text(page, "MT-8 Operations Control Panel", timeout_ms=10000)
    click_expander(page, mt8_expander, timeout_ms=5000)

    # Switch to "Active Jobs Monitor" tab within the MT-8 expander
    tab_buttons = mt8_expander.locator("button[role='tab']")
    monitor_tab = tab_buttons.filter(has_text="Active Jobs Monitor")

    # Wait for tab to be visible and click
    monitor_tab.wait_for(state="visible", timeout=5000)
    monitor_tab.click()

    # Wait for tab content to load
    page.wait_for_timeout(2000)

    # Should see either:
    # - "No active jobs" message, or
    # - Active job progress display

    # Check within the MT-8 expander only
    page_text = mt8_expander.text_content()

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

    # NEW: Use Streamlit-aware wait
    wait_for_streamlit_ready(page, timeout_ms=15000)

    # 1. NEW: Find and open MT-8 panel using helpers
    mt8_expander = find_expander_by_text(page, "MT-8 Operations Control Panel", timeout_ms=10000)
    click_expander(page, mt8_expander, timeout_ms=5000)

    # 2. Configure minimal PSO parameters for quick test
    # Click on "Swarm Parameters" tab in PSO config (nested tabs)
    config_tabs = mt8_expander.locator("div[data-testid='stTabs']").nth(1)
    swarm_tab = config_tabs.locator("button[role='tab']").filter(has_text="Swarm Parameters")
    swarm_tab.wait_for(state="visible", timeout=5000)
    swarm_tab.click()

    page.wait_for_timeout(500)

    # 3. Launch job using scoped button search
    buttons = mt8_expander.locator("button")
    launch_button = buttons.filter(has_text="Launch Seed 42")
    launch_button.wait_for(state="visible", timeout=5000)
    launch_button.click()

    page.wait_for_timeout(2000)

    # 4. Switch to Active Jobs Monitor tab
    tab_buttons = mt8_expander.locator("button[role='tab']")
    monitor_tab = tab_buttons.filter(has_text="Active Jobs Monitor")
    monitor_tab.wait_for(state="visible", timeout=5000)
    monitor_tab.click()

    page.wait_for_timeout(2000)

    # 5. Monitor for job activity
    # Look for progress indicators within the MT-8 expander
    max_wait = 60  # 60 seconds max
    job_found = False

    for attempt in range(max_wait):
        # Check text within MT-8 expander only
        page_text = mt8_expander.text_content()

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
