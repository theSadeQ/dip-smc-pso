#======================================================================================
#================== src/utils/monitoring/pso_viz.py ==================
#======================================================================================
"""
PSO visualization components for Streamlit monitoring dashboard.

This module provides interactive visualization tools for PSO optimization runs,
including convergence plots, hyperparameter comparison, and performance analysis.

Components:
    - Convergence plots (gbest fitness over iterations)
    - Hyperparameter comparison tables
    - Final gains visualization
    - Multi-run comparison charts

Usage:
    >>> import streamlit as st
    >>> from src.utils.monitoring.pso_viz import render_pso_convergence, render_pso_comparison
    >>>
    >>> # Single run convergence
    >>> render_pso_convergence(pso_run_id="pso_20251215_205717_adaptive_smc")
    >>>
    >>> # Multi-run comparison
    >>> render_pso_comparison(pso_run_ids=["run1", "run2", "run3"])

Integration:
    - Works with PSORunTracker for data loading
    - Integrates with History Browser for run selection
    - Supports export to PNG/SVG formats

Author: Claude Code (AI-assisted development)
Date: December 2025
"""

from pathlib import Path
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

from src.utils.monitoring.pso_tracker import PSORunTracker


def render_pso_convergence(pso_run_id: str) -> None:
    """
    Render convergence plot for a single PSO run.

    Args:
        pso_run_id: PSO run identifier (e.g., 'pso_20251215_205717_adaptive_smc')
    """
    if plt is None or np is None:
        st.error("matplotlib and numpy required for PSO visualization")
        return

    tracker = PSORunTracker()
    run_data = tracker._load_run_data(pso_run_id)

    if not run_data:
        st.error(f"PSO run {pso_run_id} not found")
        return

    # Extract convergence data
    iterations = [it.iteration for it in run_data.convergence]
    fitness_values = [it.gbest_fitness for it in run_data.convergence]

    if not iterations:
        st.warning("No convergence data available for this run")
        return

    # Create convergence plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(iterations, fitness_values, 'b-', linewidth=2, label='Global Best Fitness')
    ax.set_xlabel('Iteration', fontsize=12)
    ax.set_ylabel('Fitness (Cost)', fontsize=12)
    ax.set_title(f'PSO Convergence - {run_data.controller}', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()

    # Use log scale if fitness values span multiple orders of magnitude
    if len(fitness_values) > 0:
        fitness_range = max(fitness_values) / (min(fitness_values) + 1e-10)
        if fitness_range > 100:
            ax.set_yscale('log')

    st.pyplot(fig)
    plt.close(fig)

    # Display run metadata
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Controller", run_data.controller)

    with col2:
        st.metric("Scenario", run_data.scenario)

    with col3:
        st.metric("Iterations", len(run_data.convergence))

    with col4:
        st.metric("Final Score", f"{run_data.final_score:.6f}" if run_data.final_score else "N/A")

    # Hyperparameters table
    st.subheader("Hyperparameters")
    hp = run_data.hyperparameters
    hp_data = {
        "Parameter": ["Swarm Size", "Iterations", "Inertia (w)", "Cognitive (c1)", "Social (c2)", "Seed"],
        "Value": [
            hp.n_particles,
            hp.iterations,
            f"{hp.inertia:.4f}",
            f"{hp.cognitive:.4f}",
            f"{hp.social:.4f}",
            hp.seed if hp.seed is not None else "Random"
        ]
    }

    if pd is not None:
        st.dataframe(pd.DataFrame(hp_data), use_container_width=True)
    else:
        st.table(hp_data)

    # Final gains
    if run_data.final_gains:
        st.subheader("Optimized Gains")
        gains_str = ", ".join(f"{g:.4f}" for g in run_data.final_gains)
        st.code(f"[{gains_str}]", language="python")


def render_pso_comparison(pso_run_ids: List[str]) -> None:
    """
    Render comparison plots for multiple PSO runs.

    Args:
        pso_run_ids: List of PSO run identifiers to compare
    """
    if plt is None or np is None or pd is None:
        st.error("matplotlib, numpy, and pandas required for PSO comparison")
        return

    if not pso_run_ids:
        st.info("Select at least one PSO run to compare")
        return

    tracker = PSORunTracker()

    # Load all runs
    runs_data = []
    for pso_run_id in pso_run_ids:
        run_data = tracker._load_run_data(pso_run_id)
        if run_data:
            runs_data.append(run_data)

    if not runs_data:
        st.error("No valid PSO runs found")
        return

    # Convergence comparison plot
    st.subheader("Convergence Comparison")

    fig, ax = plt.subplots(figsize=(12, 6))

    for run_data in runs_data:
        iterations = [it.iteration for it in run_data.convergence]
        fitness_values = [it.gbest_fitness for it in run_data.convergence]

        label = f"{run_data.controller} ({run_data.scenario})"
        ax.plot(iterations, fitness_values, linewidth=2, label=label, alpha=0.8)

    ax.set_xlabel('Iteration', fontsize=12)
    ax.set_ylabel('Fitness (Cost)', fontsize=12)
    ax.set_title('PSO Convergence Comparison', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()

    # Use log scale if needed
    all_fitness = []
    for run_data in runs_data:
        all_fitness.extend([it.gbest_fitness for it in run_data.convergence])

    if all_fitness:
        fitness_range = max(all_fitness) / (min(all_fitness) + 1e-10)
        if fitness_range > 100:
            ax.set_yscale('log')

    st.pyplot(fig)
    plt.close(fig)

    # Performance comparison table
    st.subheader("Performance Summary")

    comparison_data = {
        "Run ID": [],
        "Controller": [],
        "Scenario": [],
        "Iterations": [],
        "Final Score": [],
        "Best Iteration": []
    }

    for run_data in runs_data:
        comparison_data["Run ID"].append(run_data.pso_run_id)
        comparison_data["Controller"].append(run_data.controller)
        comparison_data["Scenario"].append(run_data.scenario)
        comparison_data["Iterations"].append(len(run_data.convergence))
        comparison_data["Final Score"].append(f"{run_data.final_score:.6f}" if run_data.final_score else "N/A")

        # Find iteration with best fitness
        if run_data.convergence:
            fitness_values = [it.gbest_fitness for it in run_data.convergence]
            best_iter = int(np.argmin(fitness_values))
            comparison_data["Best Iteration"].append(best_iter)
        else:
            comparison_data["Best Iteration"].append("N/A")

    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True)

    # Hyperparameters comparison
    st.subheader("Hyperparameters Comparison")

    hp_comparison = {
        "Run ID": [],
        "Swarm Size": [],
        "Inertia": [],
        "Cognitive": [],
        "Social": [],
        "Seed": []
    }

    for run_data in runs_data:
        hp = run_data.hyperparameters
        hp_comparison["Run ID"].append(run_data.pso_run_id[:30] + "...")  # Truncate for display
        hp_comparison["Swarm Size"].append(hp.n_particles)
        hp_comparison["Inertia"].append(f"{hp.inertia:.4f}")
        hp_comparison["Cognitive"].append(f"{hp.cognitive:.4f}")
        hp_comparison["Social"].append(f"{hp.social:.4f}")
        hp_comparison["Seed"].append(hp.seed if hp.seed is not None else "Random")

    df_hp = pd.DataFrame(hp_comparison)
    st.dataframe(df_hp, use_container_width=True)


def render_pso_browser() -> None:
    """
    Render PSO run browser with filters and visualization options.

    This is the main entry point for PSO analysis in the Streamlit dashboard.
    """
    st.header("[OK] PSO Optimization Browser")

    tracker = PSORunTracker()

    # Query filters
    st.subheader("Filter PSO Runs")

    col1, col2, col3 = st.columns(3)

    with col1:
        controller_filter = st.selectbox(
            "Controller",
            options=["All", "classical_smc", "adaptive_smc", "sta_smc", "hybrid_adaptive_sta_smc"],
            index=0
        )

    with col2:
        scenario_filter = st.selectbox(
            "Scenario",
            options=["All", "nominal", "robust"],
            index=0
        )

    with col3:
        status_filter = st.selectbox(
            "Status",
            options=["All", "complete", "running", "failed"],
            index=1  # Default to "complete"
        )

    # Query runs
    query_params = {}
    if controller_filter != "All":
        query_params['controller'] = controller_filter
    if scenario_filter != "All":
        query_params['scenario'] = scenario_filter
    if status_filter != "All":
        query_params['status'] = status_filter

    runs = tracker.query_pso_runs(**query_params, limit=50)

    if not runs:
        st.info("No PSO runs found matching the filter criteria.")
        st.markdown("""
        **Tip**: Run PSO optimization with the `--save-results` flag:
        ```bash
        python simulate.py --controller adaptive_smc --run-pso --save-results
        ```
        """)
        return

    st.success(f"Found {len(runs)} PSO run(s)")

    # Display options
    viz_mode = st.radio(
        "Visualization Mode",
        options=["Single Run Analysis", "Multi-Run Comparison"],
        horizontal=True
    )

    if viz_mode == "Single Run Analysis":
        # Single run selection
        run_options = {f"{r.pso_run_id} ({r.controller}, {r.scenario})": r.pso_run_id for r in runs}
        selected_display = st.selectbox("Select PSO Run", options=list(run_options.keys()))
        selected_run_id = run_options[selected_display]

        st.divider()
        render_pso_convergence(selected_run_id)

    else:
        # Multi-run selection
        run_options = {f"{r.pso_run_id} ({r.controller}, {r.scenario})": r.pso_run_id for r in runs}
        selected_displays = st.multiselect(
            "Select PSO Runs (up to 5)",
            options=list(run_options.keys()),
            max_selections=5
        )

        if selected_displays:
            selected_run_ids = [run_options[d] for d in selected_displays]
            st.divider()
            render_pso_comparison(selected_run_ids)
        else:
            st.info("Select at least one PSO run to compare")
