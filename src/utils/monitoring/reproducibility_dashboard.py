#======================================================================================
#========== src/utils/monitoring/reproducibility_dashboard.py ==========
#======================================================================================
"""
MT-8 Reproducibility Validation Dashboard for Streamlit.

This module provides a comprehensive dashboard for validating the reproducibility
of MT-8 robust PSO optimization across multiple random seeds.

Components:
    - Seed execution status and progress tracking
    - Statistical analysis across multiple seeds (CV, mean, std, RSD)
    - Convergence comparison visualization
    - Gain reproducibility metrics
    - Improvement reproducibility validation

Usage:
    >>> import streamlit as st
    >>> from src.utils.monitoring.reproducibility_dashboard import render_reproducibility_dashboard
    >>>
    >>> # Render reproducibility validation interface
    >>> render_reproducibility_dashboard()

Integration:
    - Reads results from optimization_results/mt8_repro_seed*.json
    - Launches background PSO runs via subprocess
    - Compares against original MT-8 results
    - Validates success criteria (CV < 5%, RSD < 20%)

Author: Claude Code (AI-assisted development)
Date: December 2025
"""

import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import streamlit as st

try:
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
except ImportError:
    plt = None
    np = None
    pd = None


# Original MT-8 results for comparison
ORIGINAL_MT8_RESULTS = {
    'classical_smc': 2.15,
    'sta_smc': 1.38,
    'adaptive_smc': 0.47,
    'hybrid_adaptive_sta_smc': 21.39
}

ORIGINAL_MT8_AVERAGE = 6.35

# Success criteria thresholds
CV_THRESHOLD = 5.0  # Coefficient of variation < 5%
RSD_THRESHOLD = 20.0  # Relative standard deviation < 20%
IMPROVEMENT_TOLERANCE = 10.0  # Mean improvement within ±10% of original


def render_reproducibility_dashboard() -> None:
    """
    Main entry point for MT-8 reproducibility validation dashboard.

    Displays seed execution status, statistical analysis, and reproducibility metrics.
    """
    st.header("[OK] MT-8 Reproducibility Validation")

    st.markdown("""
    **Objective**: Validate reproducibility of MT-8 disturbance rejection optimization
    by re-running the complete robust PSO workflow with different random seeds.

    **Original MT-8 Results** (Nov 8, 2025):
    - Fitness improvements: Classical (2.15%), STA (1.38%), Adaptive (0.47%), Hybrid (21.39%)
    - Average improvement: 6.35%
    - Configuration: 30 particles × 50 iterations (~4,500 evaluations per controller)
    """)

    st.divider()

    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs([
        "📊 Seed Results Overview",
        "📈 Statistical Analysis",
        "🎯 Reproducibility Metrics"
    ])

    with tab1:
        render_seed_results_overview()

    with tab2:
        render_statistical_analysis()

    with tab3:
        render_reproducibility_metrics()


def render_seed_results_overview() -> None:
    """Render overview of results from all seed runs."""
    st.subheader("Seed Execution Status")

    # Check which seeds have results
    seeds = [42, 123, 456]
    results_dir = Path("optimization_results")

    seed_status = {}
    for seed in seeds:
        summary_file = results_dir / f"mt8_repro_seed{seed}_summary.json"
        seed_status[seed] = {
            'exists': summary_file.exists(),
            'file': summary_file
        }

    # Display status table
    status_data = []
    for seed in seeds:
        status = seed_status[seed]
        if status['exists']:
            with open(status['file'], 'r') as f:
                data = json.load(f)
            timestamp = data.get('timestamp', 'Unknown')
            n_controllers = len(data.get('results', []))
            status_icon = "[OK]"
        else:
            timestamp = "Not run"
            n_controllers = 0
            status_icon = "[PENDING]"

        status_data.append({
            'Seed': seed,
            'Status': status_icon,
            'Controllers': f"{n_controllers}/4",
            'Timestamp': timestamp
        })

    if pd is not None:
        df = pd.DataFrame(status_data)
        st.dataframe(df, use_container_width=True)
    else:
        for row in status_data:
            st.write(f"**Seed {row['Seed']}**: {row['Status']} - {row['Controllers']} controllers - {row['Timestamp']}")

    st.divider()

    # Launch controls for pending seeds
    st.subheader("Launch Reproducibility Tests")

    pending_seeds = [seed for seed in seeds if not seed_status[seed]['exists']]

    if not pending_seeds:
        st.success("All 3 seeds have been executed! Proceed to Statistical Analysis tab.")
    else:
        st.info(f"Pending seeds: {', '.join(map(str, pending_seeds))}")

        col1, col2 = st.columns(2)

        with col1:
            selected_seed = st.selectbox("Select seed to run", options=pending_seeds)

        with col2:
            st.markdown("**Expected runtime**: ~70 minutes (all 4 controllers)")

        if st.button(f"Launch Seed {selected_seed}", type="primary"):
            with st.spinner(f"Launching reproducibility test with seed {selected_seed}..."):
                launch_reproducibility_test(selected_seed)
            st.success(f"Launched reproducibility test with seed {selected_seed}!")
            st.info("Check back in ~70 minutes for results. You can monitor progress in the PSO Optimization Browser.")
            st.rerun()

    st.divider()

    # Show detailed results for completed seeds
    st.subheader("Detailed Results by Seed")

    completed_seeds = [seed for seed in seeds if seed_status[seed]['exists']]

    if not completed_seeds:
        st.info("No results available yet. Launch a reproducibility test above.")
        return

    for seed in completed_seeds:
        with st.expander(f"Seed {seed} Results", expanded=(seed == 42)):
            display_seed_results(seed, seed_status[seed]['file'])


def display_seed_results(seed: int, summary_file: Path) -> None:
    """Display detailed results for a specific seed."""
    with open(summary_file, 'r') as f:
        data = json.load(f)

    results = data.get('results', [])

    if not results:
        st.warning(f"No results found for seed {seed}")
        return

    # Create results table
    table_data = []
    for result in results:
        controller = result['controller_name']
        improvement = result['improvement_pct']
        original_mt8 = ORIGINAL_MT8_RESULTS.get(controller, 0.0)
        delta = improvement - original_mt8

        table_data.append({
            'Controller': controller.replace('_', ' ').title(),
            'Improvement (%)': f"{improvement:.2f}",
            'Original MT-8 (%)': f"{original_mt8:.2f}",
            'Delta (%)': f"{delta:+.2f}",
            'Converged': "[OK]" if result.get('converged', False) else "[ERROR]"
        })

    if pd is not None:
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True)

    # Show average improvement
    avg_improvement = np.mean([r['improvement_pct'] for r in results]) if np is not None else 0.0
    avg_delta = avg_improvement - ORIGINAL_MT8_AVERAGE

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Improvement", f"{avg_improvement:.2f}%")
    with col2:
        st.metric("Original MT-8 Average", f"{ORIGINAL_MT8_AVERAGE:.2f}%")
    with col3:
        st.metric("Delta", f"{avg_delta:+.2f}%", delta=f"{avg_delta:+.2f}%")


def render_statistical_analysis() -> None:
    """Render statistical analysis across all completed seeds."""
    st.subheader("Statistical Analysis Across Seeds")

    # Load all available seed results
    seeds = [42, 123, 456]
    results_dir = Path("optimization_results")

    all_results = {}
    for seed in seeds:
        summary_file = results_dir / f"mt8_repro_seed{seed}_summary.json"
        if summary_file.exists():
            with open(summary_file, 'r') as f:
                data = json.load(f)
            all_results[seed] = data.get('results', [])

    if len(all_results) < 2:
        st.info("At least 2 seeds required for statistical analysis. Launch more seeds in the Seed Results tab.")
        return

    st.success(f"Analyzing {len(all_results)} seed(s): {', '.join(map(str, all_results.keys()))}")

    # Compute statistics by controller
    controllers = ['classical_smc', 'sta_smc', 'adaptive_smc', 'hybrid_adaptive_sta_smc']

    stats_data = []
    for controller in controllers:
        improvements = []
        for seed, results in all_results.items():
            for result in results:
                if result['controller_name'] == controller:
                    improvements.append(result['improvement_pct'])

        if not improvements or np is None:
            continue

        mean_improvement = np.mean(improvements)
        std_improvement = np.std(improvements)
        cv = (std_improvement / mean_improvement * 100) if mean_improvement != 0 else 0.0
        original_mt8 = ORIGINAL_MT8_RESULTS.get(controller, 0.0)
        delta_from_original = mean_improvement - original_mt8

        stats_data.append({
            'Controller': controller.replace('_', ' ').title(),
            'Mean (%)': f"{mean_improvement:.2f}",
            'Std (%)': f"{std_improvement:.2f}",
            'CV (%)': f"{cv:.2f}",
            'Original MT-8 (%)': f"{original_mt8:.2f}",
            'Delta (%)': f"{delta_from_original:+.2f}",
            'CV Status': "[OK]" if cv < CV_THRESHOLD else "[WARNING]"
        })

    if pd is not None and stats_data:
        df = pd.DataFrame(stats_data)
        st.dataframe(df, use_container_width=True)

    st.divider()

    # Visualize improvement distribution
    if plt is not None and len(all_results) >= 2:
        st.subheader("Improvement Distribution Across Seeds")

        fig, ax = plt.subplots(figsize=(10, 6))

        x_positions = []
        labels = []
        for i, controller in enumerate(controllers):
            improvements = []
            for seed, results in all_results.items():
                for result in results:
                    if result['controller_name'] == controller:
                        improvements.append(result['improvement_pct'])

            if improvements:
                positions = [i * 2 + j * 0.3 for j in range(len(improvements))]
                ax.scatter(positions, improvements, s=100, alpha=0.6, label=f"{controller} (n={len(improvements)})")
                x_positions.append(i * 2 + 0.15)
                labels.append(controller.replace('_', ' ').title())

                # Add horizontal line for original MT-8
                original = ORIGINAL_MT8_RESULTS.get(controller, 0.0)
                ax.axhline(y=original, xmin=i/len(controllers), xmax=(i+1)/len(controllers),
                          color='red', linestyle='--', alpha=0.3)

        ax.set_ylabel('Improvement (%)', fontsize=12)
        ax.set_title('Fitness Improvement Across Seeds', fontsize=14, fontweight='bold')
        ax.set_xticks(x_positions)
        ax.set_xticklabels(labels, rotation=15, ha='right')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right', fontsize=8)

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)


def render_reproducibility_metrics() -> None:
    """Render reproducibility success criteria and validation."""
    st.subheader("Reproducibility Validation")

    # Load all available seed results
    seeds = [42, 123, 456]
    results_dir = Path("optimization_results")

    all_results = {}
    for seed in seeds:
        summary_file = results_dir / f"mt8_repro_seed{seed}_summary.json"
        if summary_file.exists():
            with open(summary_file, 'r') as f:
                data = json.load(f)
            all_results[seed] = data.get('results', [])

    if len(all_results) < 3:
        st.warning(f"All 3 seeds required for final validation. Current: {len(all_results)}/3 complete.")
        return

    st.success("[OK] All 3 seeds complete! Performing final validation...")

    # Compute reproducibility metrics
    controllers = ['classical_smc', 'sta_smc', 'adaptive_smc', 'hybrid_adaptive_sta_smc']

    validation_results = []
    all_pass = True

    for controller in controllers:
        improvements = []
        gains_matrix = []

        for seed, results in all_results.items():
            for result in results:
                if result['controller_name'] == controller:
                    improvements.append(result['improvement_pct'])
                    gains_matrix.append(result['optimized_gains'])

        if not improvements or np is None:
            continue

        # A. Fitness Reproducibility
        mean_improvement = np.mean(improvements)
        std_improvement = np.std(improvements)
        cv_fitness = (std_improvement / mean_improvement * 100) if mean_improvement != 0 else 0.0

        # B. Gain Reproducibility (average RSD across all gain parameters)
        gains_array = np.array(gains_matrix)
        rsds = []
        for i in range(gains_array.shape[1]):
            gain_mean = np.mean(gains_array[:, i])
            gain_std = np.std(gains_array[:, i])
            rsd = (gain_std / gain_mean * 100) if gain_mean != 0 else 0.0
            rsds.append(rsd)
        avg_rsd = np.mean(rsds)

        # C. Improvement Reproducibility
        original_mt8 = ORIGINAL_MT8_RESULTS.get(controller, 0.0)
        delta_from_original = abs(mean_improvement - original_mt8)
        tolerance_range = original_mt8 * (IMPROVEMENT_TOLERANCE / 100)
        within_tolerance = delta_from_original <= tolerance_range

        # Success criteria
        cv_pass = cv_fitness < CV_THRESHOLD
        rsd_pass = avg_rsd < RSD_THRESHOLD
        improvement_pass = within_tolerance

        overall_pass = cv_pass and rsd_pass and improvement_pass
        if not overall_pass:
            all_pass = False

        validation_results.append({
            'Controller': controller.replace('_', ' ').title(),
            'CV (%)': f"{cv_fitness:.2f}",
            'CV Pass': "[OK]" if cv_pass else "[ERROR]",
            'Avg RSD (%)': f"{avg_rsd:.2f}",
            'RSD Pass': "[OK]" if rsd_pass else "[ERROR]",
            'Delta from MT-8 (%)': f"{delta_from_original:.2f}",
            'Within Tolerance': "[OK]" if improvement_pass else "[ERROR]",
            'Overall': "[OK]" if overall_pass else "[ERROR]"
        })

    if pd is not None and validation_results:
        df = pd.DataFrame(validation_results)
        st.dataframe(df, use_container_width=True)

    st.divider()

    # Success criteria summary
    st.subheader("Success Criteria")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        **Fitness Reproducibility**
        - Threshold: CV < {CV_THRESHOLD}%
        - Status: {'[OK] PASS' if all_pass else '[WARNING] Some failures'}
        """)

    with col2:
        st.markdown(f"""
        **Gain Reproducibility**
        - Threshold: RSD < {RSD_THRESHOLD}%
        - Status: {'[OK] PASS' if all_pass else '[WARNING] Some failures'}
        """)

    with col3:
        st.markdown(f"""
        **Improvement Match**
        - Tolerance: ±{IMPROVEMENT_TOLERANCE}%
        - Status: {'[OK] PASS' if all_pass else '[WARNING] Some failures'}
        """)

    if all_pass:
        st.success("""
        [OK] REPRODUCIBILITY VALIDATED!

        All controllers passed reproducibility criteria:
        - Low variance in fitness (CV < 5%)
        - Consistent gain values (RSD < 20%)
        - Improvements match original MT-8 (±10%)

        The MT-8 robust PSO optimization demonstrates reliable reproducibility across
        different random seeds, validating the methodology for research publication.
        """)
    else:
        st.warning("""
        [WARNING] PARTIAL REPRODUCIBILITY

        Some controllers failed reproducibility criteria. This may indicate:
        - High sensitivity to initialization (increase PSO iterations)
        - Multi-modal fitness landscape (use ensemble methods)
        - Stochastic variation inherent to PSO (acceptable within limits)

        Review individual controller metrics above for details.
        """)


def launch_reproducibility_test(seed: int) -> None:
    """
    Launch reproducibility test for a specific seed in background.

    Args:
        seed: Random seed for PSO optimization
    """
    # Launch in background (fire and forget - user can monitor via PSO Browser)
    script_path = Path("scripts/mt8_reproducibility_test.py")

    cmd = [
        "python",
        str(script_path),
        "--seed", str(seed),
        "--save-prefix", f"mt8_repro_seed{seed}",
        "--controller", "all",
        "--particles", "30",
        "--iterations", "50"
    ]

    # Start process in background
    subprocess.Popen(cmd, cwd=Path.cwd())
