#======================================================================================
#============ src/utils/monitoring/pso_config_panel.py ============
#======================================================================================
"""
Advanced PSO Configuration Panel for Streamlit.

This module provides an interactive UI for configuring PSO optimization parameters
including gain bounds, swarm hyperparameters (w, c1, c2), and advanced settings.

Components:
    - Gain Bounds Configuration (min/max for each parameter)
    - Swarm Hyperparameters (particles, iterations, seed, w, c1, c2)
    - Advanced Settings (velocity clamping, robust PSO toggle)
    - Parameter Persistence (session state)

Usage:
    >>> import streamlit as st
    >>> from src.utils.monitoring.pso_config_panel import render_pso_config_panel
    >>>
    >>> # Render configuration panel for a controller
    >>> pso_config = render_pso_config_panel("classical_smc")
    >>>
    >>> # Use config to launch PSO optimization
    >>> job_manager.launch_job(
    ...     job_type="reproducibility_test",
    ...     script_path="scripts/mt8_reproducibility_test.py",
    ...     args={
    ...         "controller": "classical_smc",
    ...         "seed": pso_config["random_seed"],
    ...         **pso_config
    ...     }
    ... )

Integration:
    - Loads default bounds from config.yaml
    - Stores user config in st.session_state
    - Compatible with JobManager argument serialization
    - Validates bounds (min < max, positive values)

Author: Claude Code (AI-assisted development)
Date: December 2025
"""

from typing import Dict, Any, List

import streamlit as st

try:
    from src.config import load_config
except ImportError:
    load_config = None


def render_pso_config_panel(controller_name: str) -> Dict[str, Any]:
    """
    Render interactive PSO configuration form.

    Args:
        controller_name: Name of controller (e.g., "classical_smc", "sta_smc")

    Returns:
        Dict with user-configured PSO parameters:
            - bounds_min: List of minimum gain bounds
            - bounds_max: List of maximum gain bounds
            - n_particles: Number of PSO particles
            - n_iterations: Number of PSO iterations
            - random_seed: Random seed for reproducibility
            - w: Inertia weight
            - c1: Cognitive parameter
            - c2: Social parameter
            - velocity_clamp: [min, max] velocity as fraction of bounds
            - robustness_enabled: Whether to use robust PSO
    """
    st.markdown(f"### PSO Configuration: {controller_name.replace('_', ' ').title()}")

    # Load default bounds from config.yaml
    default_bounds_min, default_bounds_max, n_params = _load_default_bounds(controller_name)

    # Create tabs for different parameter categories
    tab1, tab2, tab3 = st.tabs(["Bounds", "Swarm Parameters", "Advanced"])

    with tab1:
        bounds_min, bounds_max = render_bounds_config(
            controller_name, n_params, default_bounds_min, default_bounds_max
        )

    with tab2:
        swarm_params = render_swarm_params()

    with tab3:
        advanced_params = render_advanced_params()

    # Combine all parameters
    pso_config = {
        "bounds_min": bounds_min,
        "bounds_max": bounds_max,
        **swarm_params,
        **advanced_params
    }

    # Display summary
    with st.expander("Configuration Summary", expanded=False):
        st.code(f"""
Controller: {controller_name}
Bounds: {len(bounds_min)} parameters
  Min: [{', '.join(f'{x:.2f}' for x in bounds_min)}]
  Max: [{', '.join(f'{x:.2f}' for x in bounds_max)}]

Swarm:
  Particles: {swarm_params['n_particles']}
  Iterations: {swarm_params['n_iterations']}
  Seed: {swarm_params['random_seed']}
  Inertia (w): {swarm_params['w']}
  Cognitive (c1): {swarm_params['c1']}
  Social (c2): {swarm_params['c2']}

Advanced:
  Velocity Clamp: [{advanced_params['velocity_clamp'][0]:.2f}, {advanced_params['velocity_clamp'][1]:.2f}]
  Robust PSO: {advanced_params['robustness_enabled']}
        """.strip(), language="yaml")

    return pso_config


def render_bounds_config(
    controller_name: str,
    n_params: int,
    default_min: List[float],
    default_max: List[float]
) -> tuple:
    """
    Render gain bounds configuration UI.

    Args:
        controller_name: Controller name
        n_params: Number of gain parameters
        default_min: Default minimum bounds
        default_max: Default maximum bounds

    Returns:
        Tuple of (bounds_min, bounds_max) lists
    """
    st.markdown("**Gain Bounds (min/max for each parameter)**")

    st.markdown("""
    Configure search space for PSO optimization. Each gain parameter has a
    minimum and maximum bound. PSO will explore combinations within these bounds.
    """)

    bounds_min = []
    bounds_max = []

    # Parameter name mapping
    param_names = _get_param_names(controller_name, n_params)

    for i in range(n_params):
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.markdown(f"**{param_names[i]}**")

        with col2:
            min_val = st.number_input(
                f"Min",
                value=float(default_min[i]) if i < len(default_min) else 0.1,
                min_value=0.0,
                max_value=100.0,
                step=0.1,
                key=f"bounds_min_{controller_name}_{i}",
                label_visibility="collapsed"
            )
            bounds_min.append(min_val)

        with col3:
            max_val = st.number_input(
                f"Max",
                value=float(default_max[i]) if i < len(default_max) else 30.0,
                min_value=min_val,
                max_value=100.0,
                step=0.1,
                key=f"bounds_max_{controller_name}_{i}",
                label_visibility="collapsed"
            )
            bounds_max.append(max_val)

    # Reset to defaults button
    if st.button("Reset to Default Bounds", key=f"reset_bounds_{controller_name}"):
        st.info("Rerun page to apply default bounds")
        for key in st.session_state.keys():
            if key.startswith(f"bounds_"):
                del st.session_state[key]
        st.rerun()

    return bounds_min, bounds_max


def render_swarm_params() -> Dict[str, Any]:
    """
    Render swarm hyperparameters UI.

    Returns:
        Dict with swarm parameters
    """
    st.markdown("**Swarm Hyperparameters**")

    col1, col2, col3 = st.columns(3)

    with col1:
        n_particles = st.number_input(
            "Particles",
            min_value=10,
            max_value=100,
            value=30,
            step=5,
            help="Number of particles in swarm (default: 30). More particles = better exploration but slower."
        )

    with col2:
        n_iterations = st.number_input(
            "Iterations",
            min_value=10,
            max_value=200,
            value=50,
            step=10,
            help="Number of PSO iterations (default: 50). More iterations = better convergence but slower."
        )

    with col3:
        random_seed = st.number_input(
            "Random Seed",
            min_value=1,
            max_value=10000,
            value=42,
            step=1,
            help="Seed for reproducibility. Same seed = same results."
        )

    st.divider()

    st.markdown("**PSO Hyperparameters (w, c1, c2)**")

    col1, col2, col3 = st.columns(3)

    with col1:
        w = st.slider(
            "Inertia Weight (w)",
            min_value=0.1,
            max_value=1.5,
            value=0.9,
            step=0.05,
            help="Controls exploration vs exploitation. High = more exploration, Low = faster convergence."
        )

    with col2:
        c1 = st.slider(
            "Cognitive (c1)",
            min_value=0.5,
            max_value=3.0,
            value=1.5,
            step=0.1,
            help="Personal best influence. Higher = particles trust their own experience more."
        )

    with col3:
        c2 = st.slider(
            "Social (c2)",
            min_value=0.5,
            max_value=3.0,
            value=2.0,
            step=0.1,
            help="Global best influence. Higher = particles follow swarm leader more."
        )

    return {
        "n_particles": n_particles,
        "n_iterations": n_iterations,
        "random_seed": random_seed,
        "w": w,
        "c1": c1,
        "c2": c2
    }


def render_advanced_params() -> Dict[str, Any]:
    """
    Render advanced PSO settings UI.

    Returns:
        Dict with advanced parameters
    """
    st.markdown("**Advanced Settings**")

    col1, col2 = st.columns(2)

    with col1:
        velocity_clamp_min = st.slider(
            "Velocity Clamp Min",
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.05,
            help="Min velocity as fraction of bounds. Prevents particles from stagnating."
        )

    with col2:
        velocity_clamp_max = st.slider(
            "Velocity Clamp Max",
            min_value=0.1,
            max_value=1.0,
            value=0.5,
            step=0.05,
            help="Max velocity as fraction of bounds. Prevents particles from overshooting."
        )

    robustness_enabled = st.checkbox(
        "Enable Robust PSO (nominal + disturbance scenarios)",
        value=True,
        help="Evaluate fitness on both nominal and disturbed conditions for better real-world performance."
    )

    return {
        "velocity_clamp": [velocity_clamp_min, velocity_clamp_max],
        "robustness_enabled": robustness_enabled
    }


def _load_default_bounds(controller_name: str) -> tuple:
    """
    Load default bounds from config.yaml.

    Args:
        controller_name: Controller name

    Returns:
        Tuple of (bounds_min, bounds_max, n_params)
    """
    if load_config is None:
        # Fallback if config loading fails
        return ([0.1] * 6, [30.0] * 6, 6)

    try:
        config = load_config("config.yaml")

        # Try controller-specific bounds first
        controller_bounds = getattr(config.pso.bounds, controller_name, None)

        if controller_bounds:
            return (
                list(controller_bounds.min),
                list(controller_bounds.max),
                len(controller_bounds.min)
            )
        else:
            # Fallback to default bounds
            default_bounds = config.pso.bounds
            return (
                list(default_bounds.min),
                list(default_bounds.max),
                len(default_bounds.min)
            )

    except Exception as e:
        # Fallback to hardcoded defaults
        return ([0.1] * 6, [30.0] * 6, 6)


def _get_param_names(controller_name: str, n_params: int) -> List[str]:
    """
    Get parameter names for a controller.

    Args:
        controller_name: Controller name
        n_params: Number of parameters

    Returns:
        List of parameter names
    """
    param_mappings = {
        "classical_smc": ["k1", "k2", "k3", "k4", "k5", "k6"],
        "sta_smc": ["K1", "K2", "k1", "k2", "λ1", "λ2"],
        "adaptive_smc": ["k1", "k2", "k3", "k4", "k5"],
        "hybrid_adaptive_sta_smc": ["c1", "λ1", "c2", "λ2"]
    }

    names = param_mappings.get(controller_name, [f"Gain {i+1}" for i in range(n_params)])

    # Ensure we have enough names
    while len(names) < n_params:
        names.append(f"Gain {len(names)+1}")

    return names[:n_params]
