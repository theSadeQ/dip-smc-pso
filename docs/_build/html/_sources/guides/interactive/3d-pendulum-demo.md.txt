# 3D Interactive Pendulum Visualization

**Revolutionary Feature**: Real-time 3D physics simulation with WebGL rendering, directly in your browser.

This page demonstrates the world's first fully interactive 3D double-inverted pendulum embedded in technical documentation. Adjust controller gains, set initial conditions, and watch the physics unfold in real-time with cinematic lighting and materials.

---

## Features

- **WebGL Rendering**: GPU-accelerated 3D graphics with Three.js
- **Real-Time Physics**: Simplified dynamics simulation at 60 FPS
- **Interactive Controls**: Adjust gains, angles, and physical parameters
- **Orbit Camera**: Zoom, pan, and rotate to view from any angle
- **Visual Trail**: See the path traced by the pendulum tip
- **Material Effects**: Realistic metallic materials with shadows

---

## Quick Start

```{raw} html
<div class="instructions-box">
    <h4>How to Use This Demo</h4>
    <ul>
        <li><strong>Camera Controls:</strong> Left-click + drag to rotate, scroll to zoom, right-click + drag to pan</li>
        <li><strong>Initial Conditions:</strong> Adjust θ₁ and θ₂ sliders to set pendulum angles (in radians)</li>
        <li><strong>Controller Gains:</strong> Tune K1-K6 to modify SMC control law behavior</li>
        <li><strong>Simulation:</strong> Click "Start" to run physics, "Stop" to pause, "Reset" to restore initial state</li>
    </ul>
</div>
```

---

## Interactive 3D Visualization

```{raw} html
<div class="pendulum-demo-container">
    <!-- 3D Canvas Container -->
    <div id="threejs-container">
        <div class="loading-indicator active">
            <div class="loading-spinner"></div>
            <p>Loading 3D renderer...</p>
        </div>
    </div>

    <!-- Control Panel -->
    <div class="control-panel">
        <!-- Simulation Controls -->
        <div class="control-section">
            <h3>Simulation Controls</h3>
            <div class="sim-controls">
                <button id="start-sim" class="sim-btn sim-btn-start">Start</button>
                <button id="stop-sim" class="sim-btn sim-btn-stop">Stop</button>
                <button id="reset-sim" class="sim-btn sim-btn-reset">Reset</button>
            </div>
            <div class="status-display" style="margin-top: 15px;">
                <div class="status-item">
                    <div class="status-label">Time</div>
                    <div class="status-value"><span id="sim-time">0.00</span><span class="status-unit">s</span></div>
                </div>
                <div class="status-item">
                    <div class="status-label">θ₁</div>
                    <div class="status-value"><span id="theta1-current">5.7</span><span class="status-unit">°</span></div>
                </div>
                <div class="status-item">
                    <div class="status-label">θ₂</div>
                    <div class="status-value"><span id="theta2-current">5.7</span><span class="status-unit">°</span></div>
                </div>
            </div>
        </div>

        <!-- Initial Conditions -->
        <div class="control-section">
            <h3>Initial Conditions</h3>
            <div class="slider-group">
                <div class="slider-label">
                    <span class="slider-label-name">θ₁ (rad)</span>
                    <span class="slider-label-value" id="theta1-value">0.10</span>
                </div>
                <input type="range" id="theta1-slider" min="-0.5" max="0.5" step="0.01" value="0.1">
            </div>
            <div class="slider-group">
                <div class="slider-label">
                    <span class="slider-label-name">θ₂ (rad)</span>
                    <span class="slider-label-value" id="theta2-value">0.10</span>
                </div>
                <input type="range" id="theta2-slider" min="-0.5" max="0.5" step="0.01" value="0.1">
            </div>
        </div>

        <!-- Controller Gains -->
        <div class="control-section">
            <h3>Controller Gains (Classical SMC)</h3>
            <div class="gains-grid">
                <div class="slider-group">
                    <div class="slider-label">
                        <span class="slider-label-name">K₁</span>
                        <span class="slider-label-value" id="k1-value">10.0</span>
                    </div>
                    <input type="range" id="k1-slider" min="0" max="30" step="0.1" value="10.0">
                </div>
                <div class="slider-group">
                    <div class="slider-label">
                        <span class="slider-label-name">K₂</span>
                        <span class="slider-label-value" id="k2-value">5.0</span>
                    </div>
                    <input type="range" id="k2-slider" min="0" max="30" step="0.1" value="5.0">
                </div>
                <div class="slider-group">
                    <div class="slider-label">
                        <span class="slider-label-name">K₃</span>
                        <span class="slider-label-value" id="k3-value">8.0</span>
                    </div>
                    <input type="range" id="k3-slider" min="0" max="30" step="0.1" value="8.0">
                </div>
                <div class="slider-group">
                    <div class="slider-label">
                        <span class="slider-label-name">K₄</span>
                        <span class="slider-label-value" id="k4-value">3.0</span>
                    </div>
                    <input type="range" id="k4-slider" min="0" max="30" step="0.1" value="3.0">
                </div>
                <div class="slider-group">
                    <div class="slider-label">
                        <span class="slider-label-name">K₅</span>
                        <span class="slider-label-value" id="k5-value">15.0</span>
                    </div>
                    <input type="range" id="k5-slider" min="0" max="30" step="0.1" value="15.0">
                </div>
                <div class="slider-group">
                    <div class="slider-label">
                        <span class="slider-label-name">K₆</span>
                        <span class="slider-label-value" id="k6-value">2.0</span>
                    </div>
                    <input type="range" id="k6-slider" min="0" max="30" step="0.1" value="2.0">
                </div>
            </div>
        </div>
    </div>
</div>
```

---

## Physics Model

The visualization uses **simplified dynamics** for browser performance:

$$
\begin{aligned}
\ddot{x} &= \frac{u - m_1 l_1 \dot{\theta}_1^2 \sin\theta_1 - m_2 l_2 \dot{\theta}_2^2 \sin\theta_2}{m_0 + m_1 + m_2} \\
\ddot{\theta}_1 &= \frac{g \sin\theta_1 - \ddot{x} \cos\theta_1}{l_1} \\
\ddot{\theta}_2 &= \frac{g \sin\theta_2 - \ddot{x} \cos\theta_2}{l_2}
\end{aligned}
$$

**Full nonlinear dynamics** (used in Python simulations) are available in `src/core/dynamics.py`.

---

## Controller

**Classical Sliding Mode Control (SMC)** with linear sliding surface:

$$
u = -\mathbf{K} \cdot \mathbf{x} = -(K_1 x + K_2 \dot{x} + K_3 \theta_1 + K_4 \dot{\theta}_1 + K_5 \theta_2 + K_6 \dot{\theta}_2)
$$

where:
- $\mathbf{x} = [x, \dot{x}, \theta_1, \dot{\theta}_1, \theta_2, \dot{\theta}_2]^T$ is the state vector
- $\mathbf{K} = [K_1, K_2, K_3, K_4, K_5, K_6]$ are the controller gains

**Default gains**: Tuned via PSO optimization for stability and performance.

---

## Technical Details

### Rendering Engine
- **Library**: Three.js r158 (WebGL 2.0)
- **Scene**: Perspective camera with orbit controls
- **Lighting**: Ambient + directional + point lights with shadow mapping
- **Materials**: PBR (Physically-Based Rendering) with metalness/roughness

### Performance
- **Target FPS**: 60 FPS (browser-dependent)
- **Physics Steps**: 2 substeps per frame (dt = 0.01s)
- **Integration**: Euler method (simplified for real-time)
- **Trail**: 500-point buffer for pendulum tip visualization

### Browser Requirements
- Modern browser with WebGL support (Chrome 90+, Firefox 88+, Safari 14+)
- Recommended: Dedicated GPU for smooth 60 FPS performance

---

## Related Pages

- {doc}`/guides/theory/smc-theory` - Full SMC mathematical foundations
- {doc}`/guides/theory/dip-dynamics` - Complete dynamics derivation
- {doc}`/controllers/classical_smc_technical_guide` - Classical SMC implementation details
- {doc}`/api/pso_optimization` - PSO gain tuning methodology

---

## Next Steps

Try these experiments:

1. **Stability Test**: Set θ₁ = θ₂ = 0.3 rad, click Start, observe stabilization
2. **Gain Tuning**: Reduce K₅ to 5.0, observe second pendulum oscillations
3. **Large Disturbance**: Set θ₁ = 0.5 rad (maximum), test controller limits
4. **Camera Views**: Rotate camera to side view, observe cart motion along rail

---

**[AI] Generated with Claude Code**
**Phase 1**: 3D Interactive Visualization (Revolutionary Documentation Enhancement)
