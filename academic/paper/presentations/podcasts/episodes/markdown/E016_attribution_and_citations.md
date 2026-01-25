# E016: Attribution and Citations

**Part:** Part3 Advanced
**Duration:** 15-20 minutes
**Source:** DIP-SMC-PSO Comprehensive Presentation

---

## Overview

This episode covers attribution and citations from the DIP-SMC-PSO project.

## Configuration System Architecture

**Central Configuration: `config.yaml**`

    **Configuration Domains:**
    
        - **Physics Parameters**
        
            - Cart mass, pole lengths/masses/inertias
            - Gravitational constant, friction coefficients

        - **Controller Settings**
        
            - Gains, boundary layers, adaptation rates
            - Specific parameters per controller type

        - **PSO Parameters**
        
            - Particles (30), generations (50-100)
            - Inertia weight (0.729), cognitive/social coefficients (1.494)

        - **Simulation Settings**
        
            - Time step (0.01s), duration (10s)
            - Initial conditions, solver method (RK45)

        - **HIL Configuration**
        
            - Network addresses, ports, timeouts
            - Safety limits, emergency stop thresholds

---

## Web Interface: Streamlit Dashboard

**Interactive Web UI for Non-Technical Users:**

    **Dashboard Features:**
    
        - **Controller Selection**
        
            - Dropdown menu for 7 controller types
            - Real-time parameter adjustment sliders

        - **Simulation Control**
        
            - Start/stop buttons
            - Duration and time step configuration
            - Initial condition presets

        - **Real-Time Visualization**
        
            - Animated pendulum motion
            - State trajectory plots (angles, velocities)
            - Control input time series

        - **Performance Metrics**
        
            - Settling time calculation
            - Overshoot percentage
            - Energy consumption (∫u²dt)
            - Chattering frequency analysis

        - **PSO Integration**
        
            - One-click gain optimization
            - Convergence curve visualization
            - Gain comparison table

---

## Resources

- **Repository:** https://github.com/theSadeQ/dip-smc-pso.git
- **Documentation:** `docs/` directory
- **Getting Started:** `docs/guides/getting-started.md`

---

*Educational podcast episode generated from comprehensive presentation materials*
