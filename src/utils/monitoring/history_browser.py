#======================================================================================\
#================ src/utils/monitoring/history_browser.py =================\
#======================================================================================\

"""
History Browser for Production Monitoring Dashboard.

This module provides a Streamlit-based UI component for browsing and querying
historical simulation runs stored in the monitoring system.

Features:
- Query filters (date range, controller, scenario, score threshold)
- Pagination (50 runs per page, configurable)
- CSV/JSON export functionality
- Detailed run inspection
- Sorting and search

Usage:
    import streamlit as st
    from src.utils.monitoring.history_browser import render_history_browser

    # In your Streamlit app:
    render_history_browser()

Author: Claude Code (AI)
Date: 2025-12-15
"""

from __future__ import annotations

import io
import json
import csv
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import pandas as pd
import streamlit as st

from src.utils.monitoring.data_manager import DataManager
from src.utils.monitoring.data_model import DashboardData


def _format_timestamp(timestamp: str) -> str:
    """
    Format ISO timestamp for display.

    Args:
        timestamp: ISO format timestamp string

    Returns:
        Human-readable timestamp (e.g., "2025-12-15 14:30:22")
    """
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return timestamp


def _format_duration(duration: float) -> str:
    """
    Format simulation duration for display.

    Args:
        duration: Duration in seconds

    Returns:
        Human-readable duration (e.g., "5.0s", "1m 30s")
    """
    if duration < 60:
        return f"{duration:.1f}s"
    else:
        minutes = int(duration // 60)
        seconds = duration % 60
        return f"{minutes}m {seconds:.1f}s"


def _format_score(score: float) -> str:
    """
    Format performance score for display with color coding.

    Args:
        score: Performance score (0-100)

    Returns:
        Formatted score string
    """
    if score >= 80:
        return f"✓ {score:.1f}/100"
    elif score >= 60:
        return f"⚠ {score:.1f}/100"
    else:
        return f"✗ {score:.1f}/100"


def _create_download_csv(runs: List[DashboardData]) -> bytes:
    """
    Create CSV export of run summaries.

    Args:
        runs: List of DashboardData objects

    Returns:
        CSV data as bytes
    """
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=[
        'run_id', 'timestamp', 'controller', 'scenario',
        'duration', 'score', 'settling_time', 'overshoot'
    ])
    writer.writeheader()

    for run in runs:
        summary = run.summary
        writer.writerow({
            'run_id': run.run_id,
            'timestamp': datetime.fromtimestamp(run.start_time).isoformat(),
            'controller': run.controller,
            'scenario': run.scenario,
            'duration': run.duration_s,
            'score': summary.get_score() if summary else 0.0,
            'settling_time': summary.settling_time_s if summary else None,
            'overshoot': summary.overshoot_pct if summary else None
        })

    return output.getvalue().encode('utf-8')


def _create_download_json(runs: List[DashboardData]) -> bytes:
    """
    Create JSON export of run summaries.

    Args:
        runs: List of DashboardData objects

    Returns:
        JSON data as bytes
    """
    # Convert Dashboard Data objects to dicts for JSON serialization
    data = []
    for run in runs:
        summary = run.summary
        data.append({
            'run_id': run.run_id,
            'timestamp': datetime.fromtimestamp(run.start_time).isoformat(),
            'controller': run.controller,
            'scenario': run.scenario,
            'duration_s': run.duration_s,
            'status': run.status.value,
            'performance': {
                'score': summary.get_score() if summary else 0.0,
                'settling_time_s': summary.settling_time_s if summary else None,
                'overshoot_pct': summary.overshoot_pct if summary else None,
                'steady_state_error': summary.steady_state_error if summary else None,
                'energy_j': summary.energy_j if summary else None,
                'chattering_amplitude': summary.chattering_amplitude if summary else None
            },
            'config': run.config
        })
    return json.dumps(data, indent=2).encode('utf-8')


def _render_query_filters(dm: DataManager) -> Dict[str, Any]:
    """
    Render query filter UI and return selected filter parameters.

    Args:
        dm: DataManager instance

    Returns:
        Dictionary of filter parameters for query_runs()
    """
    st.subheader("📋 Query Filters")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Date range filter
        date_filter = st.selectbox(
            "Date Range",
            options=["All Time", "Last 24 Hours", "Last 7 Days", "Last 30 Days", "Custom"],
            index=0
        )

        if date_filter == "Last 24 Hours":
            since = (datetime.now() - timedelta(days=1)).isoformat()
            until = None
        elif date_filter == "Last 7 Days":
            since = (datetime.now() - timedelta(days=7)).isoformat()
            until = None
        elif date_filter == "Last 30 Days":
            since = (datetime.now() - timedelta(days=30)).isoformat()
            until = None
        elif date_filter == "Custom":
            st.date_input("Start Date", value=datetime.now() - timedelta(days=7))
            st.date_input("End Date", value=datetime.now())
            since = None  # TODO: Convert date inputs to ISO
            until = None
        else:
            since = None
            until = None

    with col2:
        # Controller filter
        controller_filter = st.text_input(
            "Controller Type",
            value="",
            placeholder="e.g., adaptive_smc (leave empty for all)",
            help="Filter by controller type (exact match)"
        )

        # Scenario filter
        scenario_filter = st.selectbox(
            "Scenario",
            options=["All", "nominal", "disturbed", "robust"],
            index=0
        )

    with col3:
        # Score threshold filter
        min_score = st.slider(
            "Minimum Score",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=5.0,
            help="Filter runs with score >= threshold"
        )

        # Limit (pagination)
        limit = st.number_input(
            "Results Per Page",
            min_value=10,
            max_value=200,
            value=50,
            step=10,
            help="Number of runs to display per page"
        )

    # Build filter dict (matching DataManager.query_runs parameters)
    filters: Dict[str, Any] = {}

    if controller_filter:
        filters['controller'] = controller_filter
    if scenario_filter != "All":
        filters['scenario'] = scenario_filter
    if min_score > 0:
        filters['min_score'] = min_score

    filters['limit'] = int(limit)
    filters['ascending'] = False  # Most recent first

    return filters


def _render_run_summary_table(runs: List[DashboardData]) -> None:
    """
    Render table of run summaries.

    Args:
        runs: List of DashboardData objects
    """
    if not runs:
        st.info("No runs found matching the filter criteria.")
        return

    st.subheader(f"📊 Found {len(runs)} Run(s)")

    # Convert to DataFrame for easy display
    table_data = []
    for run in runs:
        summary = run.summary
        table_data.append({
            'Run ID': run.run_id,
            'Timestamp': _format_timestamp(datetime.fromtimestamp(run.start_time).isoformat()),
            'Controller': run.controller,
            'Scenario': run.scenario,
            'Duration': _format_duration(run.duration_s),
            'Score': _format_score(summary.get_score() if summary else 0.0),
            'Status': run.status.value.upper(),
        })

    df = pd.DataFrame(table_data)

    # Display table with formatting
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )


def _render_run_details(dm: DataManager, run_id: str) -> None:
    """
    Render detailed view of a specific run.

    Args:
        dm: DataManager instance
        run_id: Run ID to display
    """
    st.subheader(f"🔍 Run Details: {run_id}")

    # Load run data
    try:
        run_data = dm.load_metadata(run_id)

        if not run_data:
            st.error(f"Run {run_id} not found.")
            return

        # Display metadata in expandable sections
        with st.expander("📝 Metadata", expanded=True):
            col1, col2 = st.columns(2)

            with col1:
                st.write("**Basic Info**")
                st.write(f"- **Run ID**: {run_data.run_id}")
                st.write(f"- **Timestamp**: {_format_timestamp(datetime.fromtimestamp(run_data.start_time).isoformat())}")
                st.write(f"- **Controller**: {run_data.controller}")
                st.write(f"- **Scenario**: {run_data.scenario}")
                st.write(f"- **Duration**: {_format_duration(run_data.duration_s)}")
                st.write(f"- **Status**: {run_data.status.value.upper()}")

            with col2:
                st.write("**Performance**")
                summary = run_data.summary
                if summary:
                    st.write(f"- **Score**: {_format_score(summary.get_score())}")
                    st.write(f"- **Settling Time**: {summary.settling_time_s:.3f}s" if summary.settling_time_s else "N/A")
                    st.write(f"- **Overshoot**: {summary.overshoot_pct:.1f}%" if summary.overshoot_pct else "N/A")
                    st.write(f"- **Steady State Error**: {summary.steady_state_error:.3f}" if summary.steady_state_error else "N/A")
                    st.write(f"- **Energy**: {summary.energy_j:.2f}J" if summary.energy_j else "N/A")
                    st.write(f"- **Chattering**: {summary.chattering_amplitude:.3f}" if summary.chattering_amplitude else "N/A")
                else:
                    st.write("No performance data available")

        with st.expander("⚙️ Configuration"):
            config = run_data.config
            st.json(config)

        with st.expander("📈 Time Series Data"):
            # Load timeseries
            run_dir = dm.runs_path / run_id
            timeseries_path = run_dir / "timeseries.csv"

            if timeseries_path.exists():
                df = pd.read_csv(timeseries_path)
                st.write(f"**Shape**: {df.shape[0]} rows × {df.shape[1]} columns")
                st.write("**Preview** (first 10 rows):")
                st.dataframe(df.head(10), use_container_width=True)

                # Download button
                csv_bytes = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Download Time Series CSV",
                    data=csv_bytes,
                    file_name=f"{run_id}_timeseries.csv",
                    mime="text/csv"
                )
            else:
                st.warning("Time series data not found.")

    except Exception as e:
        st.error(f"Error loading run details: {e}")


def _render_export_buttons(runs: List[DashboardData]) -> None:
    """
    Render export buttons for CSV and JSON downloads.

    Args:
        runs: List of DashboardData objects
    """
    if not runs:
        return

    st.subheader("📥 Export Results")

    col1, col2, col3 = st.columns([1, 1, 3])

    with col1:
        csv_data = _create_download_csv(runs)
        st.download_button(
            label="⬇️ Download CSV",
            data=csv_data,
            file_name=f"run_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

    with col2:
        json_data = _create_download_json(runs)
        st.download_button(
            label="⬇️ Download JSON",
            data=json_data,
            file_name=f"run_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )


def render_history_browser(data_dir: Optional[Path] = None) -> None:
    """
    Render the complete History Browser UI component.

    This is the main entry point for integrating the History Browser
    into a Streamlit app.

    Args:
        data_dir: Optional custom data directory path
                 (defaults to monitoring_data/)

    Example:
        >>> import streamlit as st
        >>> from src.utils.monitoring.history_browser import render_history_browser
        >>>
        >>> st.title("Production Monitoring Dashboard")
        >>> render_history_browser()
    """
    st.title("📚 Run History Browser")
    st.markdown("""
    Browse and query historical simulation runs stored in the monitoring system.
    Use filters to narrow down results, inspect individual runs, and export data.
    """)

    # Initialize DataManager
    try:
        dm = DataManager(base_path=data_dir)
    except Exception as e:
        st.error(f"Failed to initialize DataManager: {e}")
        return

    # Render query filters
    filters = _render_query_filters(dm)

    # Add search button
    if st.button("🔍 Search", type="primary"):
        st.session_state['search_triggered'] = True
        st.session_state['search_filters'] = filters

    # Execute query if search was triggered
    if st.session_state.get('search_triggered', False):
        try:
            with st.spinner("Querying database..."):
                runs = dm.query_runs(**st.session_state.get('search_filters', {}))

            # Render results
            _render_run_summary_table(runs)

            # Export buttons
            _render_export_buttons(runs)

            # Run details inspector
            if runs:
                st.markdown("---")
                st.subheader("🔍 Inspect Run Details")

                selected_run = st.selectbox(
                    "Select a run to view details:",
                    options=[run.run_id for run in runs],
                    index=0
                )

                if selected_run:
                    _render_run_details(dm, selected_run)

        except Exception as e:
            st.error(f"Query failed: {e}")

    else:
        st.info("👆 Click 'Search' to query runs with the current filters.")


# Standalone app for testing
if __name__ == "__main__":
    st.set_page_config(
        page_title="Run History Browser",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    render_history_browser()
