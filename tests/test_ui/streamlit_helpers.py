"""
Playwright helper functions for Streamlit apps.

These helpers address Streamlit's multi-phase rendering cycle and provide
robust wait strategies for E2E testing with Playwright.

Streamlit Rendering Phases:
1. Initial HTML Load → networkidle fires
2. WebSocket Connection → App connects (~100-500ms)
3. React Component Render → Components appear (~200-800ms)
4. Dynamic Content Render → Expanders/tabs render (~300-1200ms)

Usage:
    from tests.test_ui.streamlit_helpers import (
        wait_for_streamlit_ready,
        find_expander_by_text,
        click_expander
    )

    page.goto("http://localhost:8502")
    wait_for_streamlit_ready(page)
    expander = find_expander_by_text(page, "MT-8 Operations Control Panel")
    click_expander(page, expander)
"""

from typing import Optional
from playwright.sync_api import Page, Locator


def wait_for_streamlit_ready(page: Page, timeout_ms: int = 15000):
    """
    Wait for Streamlit app to be fully hydrated and interactive.

    Waits for all 4 phases of Streamlit rendering:
    1. HTML load
    2. WebSocket connection
    3. React hydration
    4. Component render

    Args:
        page: Playwright page object
        timeout_ms: Maximum wait time in milliseconds (default: 15000)

    Raises:
        TimeoutError: If Streamlit doesn't fully load within timeout
    """
    # Phase 1: Wait for network idle
    page.wait_for_load_state("networkidle")
    page.wait_for_load_state("domcontentloaded")

    # Phase 2: Wait for Streamlit app container
    page.wait_for_selector("div[data-testid='stApp']", timeout=timeout_ms)

    # Phase 3 & 4: Wait for React hydration and components
    # Method 1: Wait for app to have non-zero height (indicates render complete)
    page.wait_for_function(
        """() => {
            const app = document.querySelector("div[data-testid='stApp']");
            return app && app.offsetHeight > 0;
        }""",
        timeout=timeout_ms
    )

    # Method 2: Wait for at least one expander to exist (validates full render)
    page.wait_for_selector("div[data-testid='stExpander']", timeout=timeout_ms)

    # Final buffer for any lingering renders (500ms safe buffer)
    page.wait_for_timeout(500)


def find_expander_by_text(page: Page, search_text: str, timeout_ms: int = 10000) -> Locator:
    """
    Find expander by partial text match (emoji-safe, Windows-compatible).

    This function handles the common Windows emoji rendering issue where
    emojis in Streamlit expander titles may not match correctly due to
    encoding issues.

    Args:
        page: Playwright page object
        search_text: Text to search for (e.g., "MT-8 Operations Control Panel")
        timeout_ms: Maximum wait time in milliseconds (default: 10000)

    Returns:
        Playwright locator for the matching expander

    Raises:
        TimeoutError: If expander not found within timeout
        AssertionError: If no expanders match the search text

    Example:
        expander = find_expander_by_text(page, "MT-8 Operations Control Panel")
        expander = find_expander_by_text(page, "Advanced PSO controls")
    """
    # First, ensure expanders have rendered
    page.wait_for_selector("div[data-testid='stExpander']", timeout=timeout_ms)

    # Use Playwright's filter() for cleaner code
    expander = page.locator("div[data-testid='stExpander']").filter(
        has_text=search_text
    ).first

    # Wait for expander to be visible
    expander.wait_for(state="visible", timeout=timeout_ms)

    return expander


def click_expander(page: Page, expander_locator: Locator, timeout_ms: int = 5000):
    """
    Safely click expander and wait for content to appear.

    Args:
        page: Playwright page object
        expander_locator: Locator for the expander element
        timeout_ms: Maximum wait time in milliseconds (default: 5000)

    Example:
        expander = find_expander_by_text(page, "MT-8 Operations Control Panel")
        click_expander(page, expander)
    """
    # Find summary element (the clickable header)
    # Use .first in case there are nested expanders
    summary = expander_locator.locator("summary").first
    summary.wait_for(state="visible", timeout=timeout_ms)

    # Click to expand
    summary.click()

    # Wait for CSS animation to complete
    # Streamlit expanders use CSS transitions (~350ms)
    page.wait_for_timeout(800)  # Safe buffer for animation + content render


def find_tab_by_text(page: Page, tab_text: str, timeout_ms: int = 10000) -> Locator:
    """
    Find tab button by text with retry logic.

    Args:
        page: Playwright page object
        tab_text: Text to search for in tab (e.g., "Launch PSO Tests")
        timeout_ms: Maximum wait time in milliseconds (default: 10000)

    Returns:
        Playwright locator for tab button

    Raises:
        TimeoutError: If tab not found within timeout

    Example:
        tab = find_tab_by_text(page, "Launch PSO Tests")
        tab.click()
    """
    # Wait for tabs container
    page.wait_for_selector("div[data-testid='stTabs']", timeout=timeout_ms)

    # Find specific tab
    tab = page.locator("button[role='tab']").filter(has_text=tab_text)
    tab.wait_for(state="visible", timeout=timeout_ms)

    return tab


def switch_to_tab(page: Page, tab_text: str, timeout_ms: int = 10000):
    """
    Switch to a tab and wait for content to load.

    Args:
        page: Playwright page object
        tab_text: Text of tab to switch to
        timeout_ms: Maximum wait time in milliseconds (default: 10000)

    Raises:
        TimeoutError: If tab doesn't activate within timeout

    Example:
        switch_to_tab(page, "Active Jobs Monitor")
    """
    tab = find_tab_by_text(page, tab_text, timeout_ms)
    tab.click()

    # Wait for tab to be selected (aria-selected="true")
    page.wait_for_selector(
        f"button[role='tab'][aria-selected='true']:has-text('{tab_text}')",
        timeout=timeout_ms
    )

    # Buffer for content to render
    page.wait_for_timeout(300)


def debug_streamlit_state(page: Page, label: str = ""):
    """
    Print debug information about current Streamlit state.

    Useful for diagnosing test failures and understanding what Streamlit
    has rendered at a specific point in time.

    Args:
        page: Playwright page object
        label: Optional label for this debug snapshot (e.g., "after clicking expander")

    Example:
        wait_for_streamlit_ready(page)
        debug_streamlit_state(page, "after wait_for_streamlit_ready")
    """
    print(f"\n{'='*80}")
    print(f"[DEBUG] Streamlit State: {label}")
    print(f"{'='*80}")
    print(f"[DEBUG] URL: {page.url}")

    # Check if app container exists
    app_exists = page.locator("div[data-testid='stApp']").count() > 0
    print(f"[DEBUG] stApp exists: {app_exists}")

    # Count expanders
    expander_count = page.locator("div[data-testid='stExpander']").count()
    print(f"[DEBUG] Expanders found: {expander_count}")

    # List all expanders
    if expander_count > 0:
        expanders = page.locator("div[data-testid='stExpander']")
        for i in range(expander_count):
            text = expanders.nth(i).text_content()
            print(f"[DEBUG]   Expander {i}: {text[:80]}...")
    else:
        print("[DEBUG]   No expanders found on page")

    # Check for error messages
    errors = page.locator("div[data-testid='stException']").count()
    if errors > 0:
        print(f"[DEBUG] Streamlit errors detected: {errors}")
        error_text = page.locator("div[data-testid='stException']").first.text_content()
        print(f"[DEBUG] Error: {error_text[:200]}")
    else:
        print("[DEBUG] No Streamlit errors detected")

    # Check for tabs
    tabs_count = page.locator("div[data-testid='stTabs']").count()
    print(f"[DEBUG] Tabs containers found: {tabs_count}")

    # Check for buttons
    buttons_count = page.locator("button[data-baseweb='button']").count()
    print(f"[DEBUG] Buttons found: {buttons_count}")

    print(f"{'='*80}\n")


def wait_for_element_stable(page: Page, locator: Locator, timeout_ms: int = 5000):
    """
    Wait for element to be stable (not changing position/size).

    Useful for waiting for animations to complete before interacting with elements.

    Args:
        page: Playwright page object
        locator: Element locator to wait for
        timeout_ms: Maximum wait time in milliseconds (default: 5000)

    Raises:
        TimeoutError: If element doesn't stabilize within timeout

    Example:
        button = page.locator("button:has-text('Launch Seed 42')")
        wait_for_element_stable(page, button)
        button.click()
    """
    # Wait for element to be visible
    locator.wait_for(state="visible", timeout=timeout_ms)

    # Wait for element to be stable (Playwright auto-waits for this on .click())
    locator.wait_for(state="stable", timeout=timeout_ms)
