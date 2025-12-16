#======================================================================================
#============ src/utils/monitoring/progress_monitor.py ============
#======================================================================================
"""
Real-Time Progress Monitor for Background Jobs.

This module provides a Streamlit UI component for monitoring active background
jobs (PSO optimization, validation tests, report generation) with real-time
progress updates, ETA calculation, and job control.

Components:
    - Active jobs list with progress bars
    - Real-time status updates (iteration/particle tracking)
    - Elapsed time and ETA display
    - Job control (view logs, kill jobs)
    - Auto-refresh every 2 seconds

Usage:
    >>> import streamlit as st
    >>> from src.utils.monitoring.progress_monitor import render_progress_monitor
    >>> from src.utils.monitoring.job_manager import JobManager
    >>>
    >>> # Initialize job manager in session state
    >>> if 'job_manager' not in st.session_state:
    ...     st.session_state.job_manager = JobManager()
    >>>
    >>> # Render progress monitor
    >>> render_progress_monitor(st.session_state.job_manager)

Integration:
    - Works with JobManager for job tracking
    - Polls progress.json files for real-time updates
    - Auto-refreshes UI every 2 seconds when jobs active
    - Displays logs from .live_state/<job_id>/output.log

Author: Claude Code (AI-assisted development)
Date: December 2025
"""

import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import streamlit as st

from src.utils.monitoring.job_manager import JobManager


def render_progress_monitor(job_manager: JobManager):
    """
    Display real-time progress for all active jobs.

    Args:
        job_manager: JobManager instance for tracking jobs
    """
    st.subheader("Active Background Jobs")

    # Get active jobs
    active_jobs = job_manager.list_active_jobs()

    if not active_jobs:
        st.info("No active jobs. Launch a reproducibility test or validation suite to see progress here.")

        # Show recent completed jobs
        st.divider()
        st.markdown("### Recently Completed Jobs")

        completed_jobs = job_manager.list_completed_jobs(limit=5)

        if completed_jobs:
            for job in completed_jobs:
                status_icon = {
                    "completed": "[OK]",
                    "failed": "[ERROR]",
                    "killed": "[WARNING]"
                }.get(job.status, "[INFO]")

                duration = (job.end_time - job.start_time) / 60 if job.end_time else 0

                st.markdown(f"**{status_icon} {job.job_type}** (Job ID: `{job.job_id[:8]}`) - Duration: {duration:.1f} min")
        else:
            st.info("No completed jobs yet.")

        return

    # Display each active job
    for job in active_jobs:
        render_job_progress(job, job_manager)

    st.divider()

    # Auto-refresh controls
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.markdown(f"**Refreshing every 2 seconds** | Active Jobs: {len(active_jobs)}")

    with col2:
        if st.button("Refresh Now", key="refresh_now"):
            st.rerun()

    with col3:
        if st.button("Clear Completed", key="clear_completed"):
            # Cleanup old jobs
            cleaned = job_manager.cleanup_old_jobs(max_age_hours=1)
            st.success(f"Cleaned up {cleaned} old jobs")
            st.rerun()

    # Auto-refresh every 2 seconds if jobs are active
    time.sleep(2)
    st.rerun()


def render_job_progress(job, job_manager: JobManager):
    """
    Render progress display for a single job.

    Args:
        job: BackgroundJob instance
        job_manager: JobManager instance
    """
    # Job header
    with st.expander(f"{job.job_type} - {job.job_id[:8]}", expanded=True):
        # Progress bar
        progress_value = job.progress_pct / 100.0
        st.progress(progress_value)

        # Status message
        st.markdown(f"**Status:** {job.current_status}")

        # Time metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            elapsed = time.time() - job.start_time
            st.metric("Elapsed", f"{elapsed/60:.1f} min")

        with col2:
            if job.eta_seconds and job.eta_seconds > 0:
                st.metric("ETA", f"{job.eta_seconds/60:.1f} min")
            else:
                st.metric("ETA", "Calculating...")

        with col3:
            st.metric("Progress", f"{job.progress_pct:.1f}%")

        with col4:
            started_at = datetime.fromtimestamp(job.start_time).strftime("%H:%M:%S")
            st.metric("Started", started_at)

        st.divider()

        # Job details
        with st.expander("Job Details", expanded=False):
            st.code(f"""
Job ID: {job.job_id}
Type: {job.job_type}
Script: {job.script_path}
Status: {job.status}
Process ID: {job.process_id}
Arguments:
{_format_args(job.args)}
            """.strip(), language="yaml")

        # Controls
        col1, col2 = st.columns(2)

        with col1:
            if st.button("View Logs", key=f"logs_{job.job_id}"):
                render_job_logs(job)

        with col2:
            if st.button("Kill Job", key=f"kill_{job.job_id}", type="secondary"):
                if job_manager.kill_job(job.job_id):
                    st.warning(f"Killed job {job.job_id[:8]}")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"Failed to kill job {job.job_id[:8]}")


def render_job_logs(job):
    """
    Display logs for a job.

    Args:
        job: BackgroundJob instance
    """
    st.markdown("### Job Logs")

    # Check for log files in job directory
    job_dir = Path(".live_state") / job.job_id

    # Progress log
    progress_file = job_dir / "progress.json"
    if progress_file.exists():
        st.markdown("**Progress JSON:**")
        with open(progress_file) as f:
            st.json(f.read())

    # Output log (if exists)
    output_log = job_dir / "output.log"
    if output_log.exists():
        st.markdown("**Output Log:**")
        with open(output_log) as f:
            log_content = f.read()

        if log_content:
            st.code(log_content, language="log")
        else:
            st.info("No output logs yet")
    else:
        st.info("Output logs not available for this job")

    # Result file (if completed)
    result_file = job_dir / "result.json"
    if result_file.exists():
        st.markdown("**Result:**")
        with open(result_file) as f:
            st.json(f.read())


def _format_args(args: dict) -> str:
    """
    Format arguments dictionary for display.

    Args:
        args: Arguments dictionary

    Returns:
        Formatted YAML-style string
    """
    lines = []
    for key, value in args.items():
        if isinstance(value, list):
            lines.append(f"  {key}: [{', '.join(map(str, value))}]")
        else:
            lines.append(f"  {key}: {value}")

    return "\n".join(lines)


def render_job_history(job_manager: JobManager, limit: int = 20):
    """
    Display job history (completed/failed/killed jobs).

    Args:
        job_manager: JobManager instance
        limit: Maximum number of jobs to display
    """
    st.subheader("Job History")

    completed_jobs = job_manager.list_completed_jobs(limit=limit)

    if not completed_jobs:
        st.info("No completed jobs yet.")
        return

    # Create table data
    table_data = []

    for job in completed_jobs:
        status_icon = {
            "completed": "[OK]",
            "failed": "[ERROR]",
            "killed": "[WARNING]"
        }.get(job.status, "[INFO]")

        duration = (job.end_time - job.start_time) / 60 if job.end_time else 0

        started = datetime.fromtimestamp(job.start_time).strftime("%Y-%m-%d %H:%M")
        ended = datetime.fromtimestamp(job.end_time).strftime("%H:%M") if job.end_time else "N/A"

        table_data.append({
            "Status": status_icon,
            "Type": job.job_type,
            "Job ID": job.job_id[:8],
            "Started": started,
            "Ended": ended,
            "Duration (min)": f"{duration:.1f}",
            "Result": job.result_path if job.result_path else "-"
        })

    # Display as dataframe
    import pandas as pd
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True)
