#======================================================================================
#=========== src/utils/monitoring/multi_controller_viz.py ===========
#======================================================================================
"""
Multi-controller comparison visualization for Streamlit dashboard.

This module provides interactive visualization tools for comparing multiple
controllers side-by-side, including box plots, radar charts, and statistical
comparison tables.

Components:
    - Box plots for performance metrics distribution
    - Radar charts for multi-dimensional comparison
    - Statistical significance heatmaps
    - Ranking tables and leaderboards
    - Confidence interval visualizations

Usage:
    >>> import streamlit as st
    >>> from src.utils.monitoring.multi_controller_viz import render_multi_controller_comparison
    >>>
    >>> # Render full comparison dashboard
    >>> render_multi_controller_comparison()

Integration:
    - Works with MultiControllerAnalyzer for statistical analysis
    - Integrates with DataManager for run data
    - Supports filtering by scenario and date range

Author: Claude Code (AI-assisted development)
Date: December 2025
"""

from typing import List, Optional

import streamlit as st

try:
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
except ImportError:
    plt = None
    np = None
    pd = None

from src.utils.monitoring.data_manager import DataManager
from src.utils.monitoring.multi_controller_analyzer import MultiControllerAnalyzer


def render_box_plots(analyzer: MultiControllerAnalyzer, controllers: List[str], scenario: Optional[str] = None) -> None:
    """
    Render box plots comparing performance metrics across controllers.

    Args:
        analyzer: MultiControllerAnalyzer instance
        controllers: List of controller names to compare
        scenario: Optional scenario filter
    """
    if plt is None or np is None:
        st.error("matplotlib and numpy required for visualization")
        return

    # Collect data for each controller
    data_by_metric = {
        'Score': [],
        'Settling Time (s)': [],
        'Overshoot (%)': [],
        'Steady State Error': [],
        'Energy (J)': [],
        'Chattering': []
    }

    labels = []

    for controller in controllers:
        runs = analyzer.data_manager.query_runs(controller=controller, scenario=scenario, limit=1000)

        if not runs:
            continue

        labels.append(controller)

        # Extract metrics
        scores = []
        settling_times = []
        overshoots = []
        steady_state_errors = []
        energies = []
        chatterings = []

        for run in runs:
            if run.summary:
                scores.append(run.summary.get_score())
                if run.summary.settling_time_s is not None:
                    settling_times.append(run.summary.settling_time_s)
                if run.summary.overshoot_pct is not None:
                    overshoots.append(run.summary.overshoot_pct)
                if run.summary.steady_state_error is not None:
                    steady_state_errors.append(run.summary.steady_state_error)
                if run.summary.energy_j is not None:
                    energies.append(run.summary.energy_j)
                if run.summary.chattering_amplitude is not None:
                    chatterings.append(run.summary.chattering_amplitude)

        data_by_metric['Score'].append(scores)
        data_by_metric['Settling Time (s)'].append(settling_times)
        data_by_metric['Overshoot (%)'].append(overshoots)
        data_by_metric['Steady State Error'].append(steady_state_errors)
        data_by_metric['Energy (J)'].append(energies)
        data_by_metric['Chattering'].append(chatterings)

    if not labels:
        st.warning("No data available for selected controllers")
        return

    # Create subplots (2x3 grid)
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Performance Metrics Comparison (Box Plots)', fontsize=16, fontweight='bold')

    metric_names = list(data_by_metric.keys())

    for idx, (metric, data) in enumerate(data_by_metric.items()):
        row = idx // 3
        col = idx % 3
        ax = axes[row, col]

        # Filter out empty lists
        filtered_data = [d for d in data if d]
        filtered_labels = [labels[i] for i, d in enumerate(data) if d]

        if not filtered_data:
            ax.text(0.5, 0.5, 'No Data', ha='center', va='center', transform=ax.transAxes)
            ax.set_title(metric)
            continue

        bp = ax.boxplot(filtered_data, labels=filtered_labels, patch_artist=True)

        # Color boxes
        colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightcoral', 'lavender']
        for patch, color in zip(bp['boxes'], colors[:len(bp['boxes'])]):
            patch.set_facecolor(color)

        ax.set_title(metric, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


def render_radar_chart(analyzer: MultiControllerAnalyzer, controllers: List[str], scenario: Optional[str] = None) -> None:
    """
    Render radar chart for multi-dimensional controller comparison.

    Args:
        analyzer: MultiControllerAnalyzer instance
        controllers: List of controller names to compare
        scenario: Optional scenario filter
    """
    if plt is None or np is None:
        st.error("matplotlib and numpy required for radar chart")
        return

    # Aggregate metrics
    stats = analyzer.aggregate_metrics(controllers, scenario=scenario)

    if not stats:
        st.warning("No statistics available for radar chart")
        return

    # Metrics for radar chart (normalized to 0-1)
    metrics = ['Score', 'Settling Time', 'Overshoot', 'Steady State Error', 'Energy', 'Chattering']

    # Number of variables
    num_vars = len(metrics)

    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Complete the circle

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

    colors = ['blue', 'green', 'red', 'orange', 'purple']

    for idx, controller in enumerate(controllers):
        if controller not in stats:
            continue

        ctrl_stats = stats[controller]

        # Normalize values (higher is better for all metrics in radar chart)
        # For score: already 0-100, normalize to 0-1
        # For others: invert (lower is better)
        values = [
            ctrl_stats.mean_score / 100.0,
            1.0 / (1.0 + ctrl_stats.mean_settling_time),
            1.0 / (1.0 + ctrl_stats.mean_overshoot),
            1.0 / (1.0 + ctrl_stats.mean_steady_state_error),
            1.0 / (1.0 + ctrl_stats.mean_energy),
            1.0 / (1.0 + ctrl_stats.mean_chattering)
        ]

        values += values[:1]  # Complete the circle

        ax.plot(angles, values, 'o-', linewidth=2, label=controller, color=colors[idx % len(colors)])
        ax.fill(angles, values, alpha=0.15, color=colors[idx % len(colors)])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics, fontsize=10)
    ax.set_ylim(0, 1)
    ax.set_title('Multi-Dimensional Controller Comparison', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    ax.grid(True)

    st.pyplot(fig)
    plt.close(fig)


def render_statistical_comparison(analyzer: MultiControllerAnalyzer, controllers: List[str], scenario: Optional[str] = None) -> None:
    """
    Render statistical comparison table with significance testing.

    Args:
        analyzer: MultiControllerAnalyzer instance
        controllers: List of controller names to compare
        scenario: Optional scenario filter
    """
    if pd is None:
        st.error("pandas required for statistical comparison")
        return

    if len(controllers) < 2:
        st.warning("Select at least 2 controllers for comparison")
        return

    # Pairwise comparisons
    st.subheader("Pairwise Statistical Comparisons")

    for i in range(len(controllers)):
        for j in range(i + 1, len(controllers)):
            controller_a = controllers[i]
            controller_b = controllers[j]

            st.markdown(f"**{controller_a} vs {controller_b}**")

            comparison = analyzer.compare_controllers(controller_a, controller_b, scenario=scenario)

            if not comparison:
                st.warning(f"Insufficient data for comparison between {controller_a} and {controller_b}")
                continue

            # Create comparison table
            comparison_data = {
                'Metric': [],
                f'{controller_a} (mean ± std)': [],
                f'{controller_b} (mean ± std)': [],
                't-statistic': [],
                'p-value': [],
                'Significant': [],
                "Cohen's d": []
            }

            for metric, result in comparison.items():
                comparison_data['Metric'].append(metric.replace('_', ' ').title())
                comparison_data[f'{controller_a} (mean ± std)'].append(f"{result.mean_a:.4f} ± {result.std_a:.4f}")
                comparison_data[f'{controller_b} (mean ± std)'].append(f"{result.mean_b:.4f} ± {result.std_b:.4f}")
                comparison_data['t-statistic'].append(f"{result.t_statistic:.4f}")
                comparison_data['p-value'].append(f"{result.p_value:.4f}")
                comparison_data['Significant'].append("[OK] Yes" if result.significant else "No")
                comparison_data["Cohen's d"].append(f"{result.effect_size:.4f}")

            df = pd.DataFrame(comparison_data)
            st.dataframe(df, use_container_width=True)
            st.divider()

    # ANOVA test
    if len(controllers) >= 3:
        st.subheader("One-Way ANOVA Test")
        st.markdown("Tests if controllers have significantly different mean scores.")

        anova_result = analyzer.anova_test(controllers, metric='score', scenario=scenario)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("F-statistic", f"{anova_result['f_statistic']:.4f}")

        with col2:
            st.metric("p-value", f"{anova_result['p_value']:.4f}")

        with col3:
            significant = anova_result['p_value'] < 0.05
            st.metric("Significant (α=0.05)", "[OK] Yes" if significant else "No")

        if significant:
            st.success("Controllers have significantly different mean scores (p < 0.05)")
        else:
            st.info("No significant difference in mean scores (p >= 0.05)")


def render_ranking_leaderboard(analyzer: MultiControllerAnalyzer, controllers: List[str], scenario: Optional[str] = None) -> None:
    """
    Render controller ranking leaderboard.

    Args:
        analyzer: MultiControllerAnalyzer instance
        controllers: List of controller names to rank
        scenario: Optional scenario filter
    """
    if pd is None:
        st.error("pandas required for leaderboard")
        return

    st.subheader("Controller Rankings")

    # Get rankings
    rankings = analyzer.rank_controllers(controllers, scenario=scenario)

    if not rankings:
        st.warning("No ranking data available")
        return

    # Create leaderboard table
    leaderboard_data = {
        'Rank': [],
        'Controller': [],
        'Composite Score': [],
        'Badge': []
    }

    badges = {1: "[OK] Gold", 2: "[INFO] Silver", 3: "[WARNING] Bronze"}

    for rank, (controller, score) in enumerate(rankings, 1):
        leaderboard_data['Rank'].append(rank)
        leaderboard_data['Controller'].append(controller)
        leaderboard_data['Composite Score'].append(f"{score:.2f}/100")
        leaderboard_data['Badge'].append(badges.get(rank, ""))

    df = pd.DataFrame(leaderboard_data)
    st.dataframe(df, use_container_width=True)

    # Display top 3 with metrics
    st.markdown("### Top 3 Controllers")

    # Aggregate stats for detailed view
    stats = analyzer.aggregate_metrics(controllers, scenario=scenario)

    cols = st.columns(min(3, len(rankings)))

    for idx, (controller, score) in enumerate(rankings[:3]):
        if controller not in stats:
            continue

        ctrl_stats = stats[controller]

        with cols[idx]:
            badge = badges.get(idx + 1, "")
            st.markdown(f"**#{idx + 1}: {controller}** {badge}")
            st.metric("Composite Score", f"{score:.2f}/100")
            st.metric("Mean Performance Score", f"{ctrl_stats.mean_score:.2f}/100")
            st.metric("Settling Time", f"{ctrl_stats.mean_settling_time:.3f}s")
            st.metric("Overshoot", f"{ctrl_stats.mean_overshoot:.2f}%")
            st.metric("# Runs", ctrl_stats.n_runs)


def render_multi_controller_comparison() -> None:
    """
    Main entry point for multi-controller comparison dashboard.

    Renders filters, visualization options, and all comparison tools.
    """
    st.header("[OK] Multi-Controller Comparison Dashboard")

    analyzer = MultiControllerAnalyzer()

    # Controller selection
    st.subheader("Select Controllers to Compare")

    available_controllers = ["classical_smc", "adaptive_smc", "sta_smc", "hybrid_adaptive_sta_smc"]

    selected_controllers = st.multiselect(
        "Controllers (select 2-4 for best results)",
        options=available_controllers,
        default=[]
    )

    if not selected_controllers:
        st.info("Select at least one controller to begin analysis")
        st.markdown("""
        **Available Controllers:**
        - `classical_smc`: Classical sliding mode control
        - `adaptive_smc`: Adaptive SMC with parameter estimation
        - `sta_smc`: Super-twisting algorithm SMC
        - `hybrid_adaptive_sta_smc`: Hybrid adaptive STA-SMC

        **Tip**: Run simulations with `--save-results` to populate data:
        ```bash
        python simulate.py --controller adaptive_smc --duration 10.0 --save-results
        ```
        """)
        return

    # Scenario filter
    scenario_filter = st.selectbox(
        "Scenario",
        options=["All", "nominal", "robust"],
        index=0
    )

    scenario = scenario_filter if scenario_filter != "All" else None

    st.divider()

    # Check data availability
    has_data = False
    for controller in selected_controllers:
        runs = analyzer.data_manager.query_runs(controller=controller, scenario=scenario, limit=1)
        if runs:
            has_data = True
            break

    if not has_data:
        st.warning("No simulation data found for selected controllers")
        return

    # Visualization tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Box Plots",
        "🎯 Radar Chart",
        "📈 Statistical Tests",
        "🏆 Rankings"
    ])

    with tab1:
        st.subheader("Performance Distribution Comparison")
        st.markdown("Box plots show the distribution of performance metrics across multiple runs.")
        render_box_plots(analyzer, selected_controllers, scenario)

    with tab2:
        st.subheader("Multi-Dimensional Comparison")
        st.markdown("Radar chart visualizes controller performance across all metrics simultaneously.")
        render_radar_chart(analyzer, selected_controllers, scenario)

    with tab3:
        st.subheader("Statistical Significance Testing")
        st.markdown("Pairwise comparisons using Welch's t-test with Cohen's d effect size.")
        render_statistical_comparison(analyzer, selected_controllers, scenario)

    with tab4:
        st.subheader("Controller Performance Rankings")
        st.markdown("Composite scores based on weighted average of all metrics.")
        render_ranking_leaderboard(analyzer, selected_controllers, scenario)
