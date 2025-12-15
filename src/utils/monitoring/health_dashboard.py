#======================================================================================
#============ src/utils/monitoring/health_dashboard.py ============
#======================================================================================
"""
Health monitoring dashboard for production monitoring system.

This module provides a comprehensive health dashboard for Streamlit that displays
system health, alerts, anomalies, disk usage, and maintenance reports.

Components:
    - System health overview
    - Recent alerts and anomaly detection
    - Disk usage and database statistics
    - Maintenance controls and reports
    - Performance degradation monitoring

Usage:
    >>> import streamlit as st
    >>> from src.utils.monitoring.health_dashboard import render_health_dashboard
    >>>
    >>> # Render complete health dashboard
    >>> render_health_dashboard()

Integration:
    - Works with AlertingSystem for threshold monitoring
    - Uses AnomalyDetector for statistical anomaly detection
    - Integrates MaintenanceManager for cleanup operations
    - Displays DataManager statistics

Author: Claude Code (AI-assisted development)
Date: December 2025
"""

from datetime import datetime
from typing import Optional

import streamlit as st

try:
    import matplotlib.pyplot as plt
    import pandas as pd
except ImportError:
    plt = None
    pd = None

from src.utils.monitoring.alerting import AlertingSystem, AlertThresholds, AlertSeverity
from src.utils.monitoring.anomaly_detection import AnomalyDetector, AnomalyMethod
from src.utils.monitoring.data_manager import DataManager
from src.utils.monitoring.maintenance import MaintenanceManager, RetentionPolicy


def render_health_dashboard() -> None:
    """
    Main entry point for health monitoring dashboard.

    Displays system health, alerts, anomalies, and maintenance controls.
    """
    st.header("[OK] System Health Dashboard")

    # Initialize components
    data_manager = DataManager()
    alerting = AlertingSystem()
    anomaly_detector = AnomalyDetector()
    maintenance = MaintenanceManager()

    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 System Overview",
        "🚨 Alerts & Anomalies",
        "💾 Disk Usage & Maintenance",
        "⚙️ Configuration"
    ])

    with tab1:
        render_system_overview(data_manager, alerting, anomaly_detector)

    with tab2:
        render_alerts_and_anomalies(alerting, anomaly_detector, data_manager)

    with tab3:
        render_disk_usage_and_maintenance(maintenance, data_manager)

    with tab4:
        render_configuration(alerting, anomaly_detector, maintenance)


def render_system_overview(
    data_manager: DataManager,
    alerting: AlertingSystem,
    anomaly_detector: AnomalyDetector
) -> None:
    """Render system overview section."""
    st.subheader("System Health Overview")

    # Get statistics
    all_runs = data_manager.query_runs(limit=1000)

    if not all_runs:
        st.info("No simulation data available. Run simulations with `--save-results` to populate the monitoring system.")
        return

    # Calculate statistics
    total_runs = len(all_runs)
    unique_controllers = len(set(run.controller for run in all_runs))

    # Recent runs (last 24 hours)
    recent_cutoff = datetime.now().timestamp() - (24 * 3600)
    recent_runs = [r for r in all_runs if r.start_time >= recent_cutoff]

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Runs", total_runs)

    with col2:
        st.metric("Controllers", unique_controllers)

    with col3:
        st.metric("Recent (24h)", len(recent_runs))

    with col4:
        # Check for recent alerts
        recent_alerts = alerting.get_recent_alerts(limit=100)
        critical_alerts = [a for a in recent_alerts if a.severity == AlertSeverity.CRITICAL]
        st.metric("Critical Alerts", len(critical_alerts), delta=f"-{len(critical_alerts)}" if critical_alerts else None)

    st.divider()

    # Performance trend (last 50 runs)
    st.subheader("Recent Performance Trend")

    recent_50 = all_runs[:50]
    timestamps = [datetime.fromtimestamp(r.start_time) for r in recent_50]
    scores = [r.summary.get_score() if r.summary else 0.0 for r in recent_50]

    if plt is not None and scores:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(timestamps, scores, 'o-', linewidth=2, markersize=4)
        ax.set_xlabel('Time', fontsize=10)
        ax.set_ylabel('Performance Score', fontsize=10)
        ax.set_title('Performance Trend (Last 50 Runs)', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 100)

        # Add threshold line
        ax.axhline(y=alerting.thresholds.min_score, color='r', linestyle='--', alpha=0.5, label='Alert Threshold')
        ax.legend()

        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)


def render_alerts_and_anomalies(
    alerting: AlertingSystem,
    anomaly_detector: AnomalyDetector,
    data_manager: DataManager
) -> None:
    """Render alerts and anomalies section."""
    st.subheader("Alerts & Anomaly Detection")

    # Alert controls
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Check Run for Violations")
        runs = data_manager.query_runs(limit=20)

        if runs:
            run_options = {f"{r.run_id} ({r.controller})": r.run_id for r in runs}
            selected_display = st.selectbox("Select Run", options=list(run_options.keys()))
            selected_run_id = run_options[selected_display]

            if st.button("Check for Threshold Violations"):
                alerts = alerting.check_run(selected_run_id)

                if alerts:
                    st.error(f"Found {len(alerts)} violation(s)!")
                    for alert in alerts:
                        severity_icon = {
                            AlertSeverity.CRITICAL: "[ERROR]",
                            AlertSeverity.WARNING: "[WARNING]",
                            AlertSeverity.INFO: "[INFO]"
                        }[alert.severity]

                        st.markdown(f"**{severity_icon} {alert.metric}**: {alert.message}")
                else:
                    st.success("No violations found - all metrics within thresholds")
        else:
            st.info("No runs available")

    with col2:
        st.markdown("### Check for Anomalies")
        controllers = list(set(run.controller for run in data_manager.query_runs(limit=100)))

        if controllers:
            selected_controller = st.selectbox("Controller", options=controllers)

            anomaly_method = st.selectbox(
                "Detection Method",
                options=[m.value for m in AnomalyMethod],
                index=1  # Default to modified_z_score
            )

            if st.button("Detect Anomalies"):
                with st.spinner("Analyzing runs..."):
                    batch_anomalies = anomaly_detector.detect_batch_anomalies(
                        controller=selected_controller,
                        limit=20,
                        method=AnomalyMethod(anomaly_method)
                    )

                if batch_anomalies:
                    st.warning(f"Found anomalies in {len(batch_anomalies)} run(s)")

                    for run_id, anomalies in batch_anomalies:
                        st.markdown(f"**{run_id}**:")
                        for anomaly in anomalies:
                            st.markdown(f"- {anomaly.reason}")
                else:
                    st.success("No anomalies detected")
        else:
            st.info("No controllers available")

    st.divider()

    # Recent alerts log
    st.markdown("### Recent Alerts (Last 24 hours)")

    recent_alerts = alerting.get_recent_alerts(limit=50)

    if recent_alerts:
        # Filter last 24 hours
        cutoff_time = datetime.now().timestamp() - (24 * 3600)
        recent_24h = [a for a in recent_alerts if a.timestamp >= cutoff_time]

        if recent_24h and pd is not None:
            alert_data = {
                'Time': [datetime.fromtimestamp(a.timestamp).strftime('%Y-%m-%d %H:%M:%S') for a in recent_24h],
                'Severity': [a.severity.value for a in recent_24h],
                'Controller': [a.controller for a in recent_24h],
                'Metric': [a.metric for a in recent_24h],
                'Message': [a.message for a in recent_24h]
            }

            df = pd.DataFrame(alert_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No alerts in the last 24 hours")
    else:
        st.info("No alerts logged yet")


def render_disk_usage_and_maintenance(
    maintenance: MaintenanceManager,
    data_manager: DataManager
) -> None:
    """Render disk usage and maintenance section."""
    st.subheader("Disk Usage & Maintenance")

    # Disk usage report
    st.markdown("### Current Disk Usage")

    usage_report = maintenance.get_disk_usage_report()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Size", f"{usage_report['total_mb']:.1f} MB")

    with col2:
        st.metric("Runs", f"{usage_report['runs_dir_mb']:.1f} MB")

    with col3:
        st.metric("Database", f"{usage_report['database_mb']:.1f} MB")

    with col4:
        st.metric("Run Count", usage_report['run_count'])

    # Visualize disk usage
    if plt is not None:
        fig, ax = plt.subplots(figsize=(8, 4))

        categories = ['Runs', 'PSO Runs', 'Database', 'Logs']
        sizes = [
            usage_report['runs_dir_mb'],
            usage_report['pso_runs_dir_mb'],
            usage_report['database_mb'],
            usage_report['logs_mb']
        ]

        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
        ax.pie(sizes, labels=categories, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        ax.set_title('Disk Usage Breakdown', fontweight='bold')

        st.pyplot(fig)
        plt.close(fig)

    st.divider()

    # Maintenance controls
    st.markdown("### Run Maintenance")

    st.markdown("""
    **Maintenance operations:**
    - Delete old runs based on retention policy
    - Archive runs before deletion (optional)
    - Remove orphaned files
    - Optimize database (VACUUM + ANALYZE)
    """)

    col1, col2 = st.columns(2)

    with col1:
        dry_run = st.checkbox("Dry Run (preview only)", value=True)

    with col2:
        if st.button("Run Maintenance", type="primary"):
            with st.spinner("Running maintenance..."):
                report = maintenance.run_maintenance(dry_run=dry_run)

            st.success("Maintenance complete!")

            st.markdown(f"""
            **Results:**
            - Runs deleted: {report.runs_deleted}
            - Runs archived: {report.runs_archived}
            - Space freed: {report.space_freed_mb:.1f} MB
            - Database size: {report.database_size_before_mb:.1f} MB → {report.database_size_after_mb:.1f} MB
            - Orphaned files removed: {report.orphaned_files_removed}
            """)

            if report.errors:
                st.error(f"Errors: {', '.join(report.errors)}")


def render_configuration(
    alerting: AlertingSystem,
    anomaly_detector: AnomalyDetector,
    maintenance: MaintenanceManager
) -> None:
    """Render configuration section."""
    st.subheader("System Configuration")

    # Alert thresholds
    st.markdown("### Alert Thresholds")

    thresholds = alerting.thresholds

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Performance Thresholds:**")
        st.write(f"- Min Score: {thresholds.min_score}")
        st.write(f"- Max Settling Time: {thresholds.max_settling_time}s")
        st.write(f"- Max Overshoot: {thresholds.max_overshoot}%")

    with col2:
        st.markdown("**Degradation Detection:**")
        st.write(f"- Window: {thresholds.degradation_window} runs")
        st.write(f"- Threshold: {thresholds.degradation_threshold * 100}%")

    st.divider()

    # Anomaly detection
    st.markdown("### Anomaly Detection")

    st.write(f"- Sensitivity: {anomaly_detector.sensitivity}")
    st.write(f"- Method: Modified Z-score (MAD)")
    st.write(f"- Threshold: {anomaly_detector.sensitivity} standard deviations")

    st.divider()

    # Retention policy
    st.markdown("### Retention Policy")

    policy = maintenance.retention_policy

    st.write(f"- Keep Days: {policy.keep_days}")
    st.write(f"- Min Runs per Controller: {policy.keep_min_runs}")
    st.write(f"- Max Total Runs: {policy.max_total_runs}")
    st.write(f"- Archive Before Delete: {policy.archive_before_delete}")

    st.info("To modify these settings, edit the configuration in your code or use environment variables.")
