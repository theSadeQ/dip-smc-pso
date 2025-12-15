#======================================================================================\
#=============== src/utils/monitoring/live_monitor_ui.py ===============\
#======================================================================================\

"""
Streamlit UI component for live simulation monitoring.

This module provides an interactive Streamlit interface for starting simulations,
tracking progress in real-time, and aborting if needed.

Features:
- Start/stop simulation controls
- Real-time progress bar and metrics
- Live charts (error, control over time)
- Abort functionality
- Session history

Author: Claude Code (AI)
Date: 2025-12-15
"""

from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import streamlit as st
except ImportError:
    # Stub for testing
    class _StreamlitStub:
        def __getattr__(self, name: str):
            return lambda *args, **kwargs: None
    st = _StreamlitStub()  # type: ignore

import pandas as pd
import matplotlib.pyplot as plt

from src.utils.monitoring.live_monitor import LiveMonitor, LiveRunStatus


def render_live_monitor_ui(config: Optional[dict] = None) -> None:
    """
    Render the live monitoring UI component.

    This is the main entry point for integrating live monitoring
    into a Streamlit app.

    Args:
        config: Optional configuration dict (from config.yaml)

    Example:
        >>> import streamlit as st
        >>> from src.utils.monitoring.live_monitor_ui import render_live_monitor_ui
        >>>
        >>> st.title("Live Monitoring Dashboard")
        >>> render_live_monitor_ui()
    """
    st.title("🔴 Live Simulation Monitor")
    st.markdown("""
    Start a simulation and watch it run in real-time!
    Track progress, view live metrics, and abort if needed.
    """)

    # Initialize LiveMonitor
    try:
        monitor = LiveMonitor()
    except Exception as e:
        st.error(f"Failed to initialize LiveMonitor: {e}")
        return

    # Check for active sessions
    active_sessions = monitor.list_active_sessions()

    # Session tabs
    tab1, tab2 = st.tabs(["📊 Active Sessions", "➕ Start New Simulation"])

    # Tab 1: Active sessions
    with tab1:
        if active_sessions:
            st.subheader(f"Active Sessions ({len(active_sessions)})")

            for session in active_sessions:
                _render_active_session(monitor, session)
        else:
            st.info("No active sessions. Start a new simulation in the 'Start New Simulation' tab!")

    # Tab 2: Start new simulation
    with tab2:
        _render_start_new_simulation(monitor, config)


def _render_active_session(monitor: LiveMonitor, session_state) -> None:
    """
    Render a single active session with live updates.

    Args:
        monitor: LiveMonitor instance
        session_state: LiveRunState object
    """
    session_id = session_state.session_id

    # Create expander for each session
    with st.expander(f"🟢 {session_state.controller} - {session_id}", expanded=True):
        # Refresh state
        current_state = monitor.get_state(session_id)

        if not current_state:
            st.error(f"Session {session_id} not found")
            return

        # Status indicator
        status_emoji = {
            LiveRunStatus.STARTING: "🟡",
            LiveRunStatus.RUNNING: "🟢",
            LiveRunStatus.COMPLETE: "✅",
            LiveRunStatus.FAILED: "❌",
            LiveRunStatus.ABORTED: "⛔"
        }

        status_color = {
            LiveRunStatus.STARTING: "orange",
            LiveRunStatus.RUNNING: "green",
            LiveRunStatus.COMPLETE: "blue",
            LiveRunStatus.FAILED: "red",
            LiveRunStatus.ABORTED: "gray"
        }

        emoji = status_emoji.get(current_state.status, "❓")
        color = status_color.get(current_state.status, "black")

        st.markdown(f"**Status:** {emoji} <span style='color:{color}'>{current_state.status.value.upper()}</span>",
                   unsafe_allow_html=True)

        # Progress bar
        progress = current_state.metrics.progress_pct / 100.0
        st.progress(progress)

        # Metrics columns
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="Progress",
                value=f"{current_state.metrics.progress_pct:.1f}%"
            )

        with col2:
            st.metric(
                label="Elapsed Time",
                value=f"{current_state.metrics.elapsed_s:.1f}s"
            )

        with col3:
            st.metric(
                label="Current Error",
                value=f"{current_state.metrics.current_error:.3f}"
            )

        with col4:
            st.metric(
                label="Control Output",
                value=f"{current_state.metrics.current_control:.2f}"
            )

        # Detailed info
        with st.expander("📝 Session Details"):
            col1, col2 = st.columns(2)

            with col1:
                st.write("**Session Info**")
                st.write(f"- **ID**: {session_id}")
                st.write(f"- **Controller**: {current_state.controller}")
                st.write(f"- **Scenario**: {current_state.scenario}")
                st.write(f"- **Duration**: {current_state.duration_s:.1f}s")

            with col2:
                st.write("**Progress Info**")
                st.write(f"- **Samples**: {current_state.metrics.samples_completed}/{current_state.metrics.samples_total}")
                st.write(f"- **Sim Time**: {current_state.metrics.timestamp:.2f}s")
                started = datetime.fromtimestamp(current_state.start_time)
                st.write(f"- **Started**: {started.strftime('%H:%M:%S')}")

        # Real-time chart (simple line showing last few updates)
        if current_state.metrics.samples_completed > 0:
            with st.expander("📈 Live Metrics Chart", expanded=False):
                st.caption("Note: Full charts available after completion in History Browser")
                # For now, just show current values as a simple bar chart
                metrics_df = pd.DataFrame({
                    'Metric': ['Error', 'Control', 'Progress'],
                    'Value': [
                        current_state.metrics.current_error,
                        abs(current_state.metrics.current_control) / 10,  # Scale for visibility
                        current_state.metrics.progress_pct / 100
                    ]
                })
                st.bar_chart(metrics_df.set_index('Metric'))

        # Errors and warnings
        if current_state.errors:
            st.error("**Errors:**")
            for err in current_state.errors:
                st.write(f"- {err}")

        if current_state.warnings:
            st.warning("**Warnings:**")
            for warn in current_state.warnings:
                st.write(f"- {warn}")

        # Control buttons
        col1, col2, col3 = st.columns([1, 1, 3])

        with col1:
            if st.button("🔄 Refresh", key=f"refresh_{session_id}"):
                st.rerun()

        with col2:
            if current_state.status in [LiveRunStatus.STARTING, LiveRunStatus.RUNNING]:
                if st.button("⛔ Abort", key=f"abort_{session_id}", type="secondary"):
                    if monitor.abort_run(session_id):
                        st.success("Simulation aborted!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Failed to abort simulation")

        # Auto-refresh for running sessions
        if current_state.status in [LiveRunStatus.STARTING, LiveRunStatus.RUNNING]:
            time.sleep(1)
            st.rerun()

        # Show completion info
        if current_state.status == LiveRunStatus.COMPLETE and current_state.run_id:
            st.success(f"✅ Simulation complete! Results saved as: {current_state.run_id}")
            st.info("View detailed results in the **History Browser**.")


def _render_start_new_simulation(monitor: LiveMonitor, config: Optional[dict] = None) -> None:
    """
    Render UI for starting a new simulation.

    Args:
        monitor: LiveMonitor instance
        config: Optional configuration dict
    """
    st.subheader("Start New Live Simulation")

    # Controller selection
    controller_options = [
        "classical_smc",
        "sta_smc",
        "adaptive_smc",
        "hybrid_adaptive_sta_smc"
    ]

    col1, col2 = st.columns(2)

    with col1:
        selected_controller = st.selectbox(
            "Controller Type",
            options=controller_options,
            index=2,  # Default to adaptive_smc
            help="Choose which controller to test"
        )

        scenario = st.selectbox(
            "Scenario",
            options=["nominal", "disturbed", "robust"],
            index=0,
            help="Simulation scenario"
        )

    with col2:
        duration = st.slider(
            "Duration (seconds)",
            min_value=5.0,
            max_value=120.0,
            value=30.0,
            step=5.0,
            help="How long to run the simulation"
        )

        dt = st.select_slider(
            "Time Step (seconds)",
            options=[0.001, 0.005, 0.01, 0.02, 0.05],
            value=0.01,
            help="Simulation time step (smaller = more accurate but slower)"
        )

    # Estimated sample count
    estimated_samples = int(duration / dt)
    st.caption(f"Estimated samples: {estimated_samples:,} timesteps")

    # Start button
    if st.button("🚀 Start Simulation", type="primary"):
        try:
            with st.spinner("Starting simulation..."):
                session_id = monitor.start_live_run(
                    controller=selected_controller,
                    scenario=scenario,
                    duration=duration,
                    dt=dt
                )

            st.success(f"✅ Simulation started! Session ID: {session_id}")
            st.info("Switch to the 'Active Sessions' tab to watch progress.")

            # Wait a moment then switch to active sessions tab
            time.sleep(2)
            st.rerun()

        except Exception as e:
            st.error(f"Failed to start simulation: {e}")
            st.exception(e)


# Standalone app for testing
if __name__ == "__main__":
    st.set_page_config(
        page_title="Live Simulation Monitor",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    render_live_monitor_ui()
