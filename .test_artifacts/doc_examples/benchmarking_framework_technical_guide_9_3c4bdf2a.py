# Example from: docs\testing\benchmarking_framework_technical_guide.md
# Index: 9
# Runnable: True
# Hash: 3c4bdf2a

# benchmarks/integration/numerical_methods.py

class EulerIntegrator:
    """Forward Euler integration method.

    First-order accurate: O(h)
    """

    def __init__(self, dynamics):
        self.dynamics = dynamics

    def integrate(self, x0: np.ndarray, t_span: tuple, dt: float,
                 controller: Optional[Any] = None) -> dict:
        """Integrate dynamics using Forward Euler.

        Parameters
        ----------
        x0 : np.ndarray
            Initial state
        t_span : tuple
            (t_start, t_end)
        dt : float
            Time step
        controller : object, optional
            Controller for closed-loop simulation

        Returns
        -------
        dict
            {
                't': time vector,
                'x': state history,
                'u': control history (if controller provided)
            }
        """
        t_start, t_end = t_span
        t = np.arange(t_start, t_end + dt, dt)
        n_steps = len(t)

        x = np.zeros((n_steps, len(x0)))
        x[0] = x0

        if controller:
            u = np.zeros(n_steps - 1)

        for i in range(n_steps - 1):
            if controller:
                result = controller.compute_control(x[i], {}, {})
                u[i] = result.get('control_output', result.get('control', 0.0))
                x_dot = self.dynamics.dynamics(x[i], u[i])
            else:
                x_dot = self.dynamics.dynamics(x[i], 0.0)

            x[i+1] = x[i] + dt * x_dot

        result = {'t': t, 'x': x}
        if controller:
            result['u'] = u

        return result


class RK4Integrator:
    """Fourth-order Runge-Kutta integration.

    Fourth-order accurate: O(h⁴)
    """

    def __init__(self, dynamics):
        self.dynamics = dynamics

    def integrate(self, x0: np.ndarray, t_span: tuple, dt: float,
                 controller: Optional[Any] = None) -> dict:
        """Integrate using RK4 method."""
        t_start, t_end = t_span
        t = np.arange(t_start, t_end + dt, dt)
        n_steps = len(t)

        x = np.zeros((n_steps, len(x0)))
        x[0] = x0

        if controller:
            u = np.zeros(n_steps - 1)

        for i in range(n_steps - 1):
            if controller:
                result = controller.compute_control(x[i], {}, {})
                u[i] = result.get('control_output', result.get('control', 0.0))
                u_current = u[i]
            else:
                u_current = 0.0

            # RK4 stages
            k1 = self.dynamics.dynamics(x[i], u_current)
            k2 = self.dynamics.dynamics(x[i] + 0.5*dt*k1, u_current)
            k3 = self.dynamics.dynamics(x[i] + 0.5*dt*k2, u_current)
            k4 = self.dynamics.dynamics(x[i] + dt*k3, u_current)

            x[i+1] = x[i] + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)

        result = {'t': t, 'x': x}
        if controller:
            result['u'] = u

        return result


class AdaptiveRK45Integrator:
    """Adaptive Runge-Kutta 4-5 method (Dormand-Prince).

    Variable step size for error control.
    """

    def __init__(self, dynamics):
        self.dynamics = dynamics

    def integrate(self, x0: np.ndarray, t_span: tuple,
                 rtol: float = 1e-6, atol: float = 1e-9,
                 controller: Optional[Any] = None) -> dict:
        """Integrate using adaptive RK45."""
        from scipy.integrate import solve_ivp

        if controller:
            def dynamics_func(t, x):
                result = controller.compute_control(x, {}, {})
                u = result.get('control_output', result.get('control', 0.0))
                return self.dynamics.dynamics(x, u)
        else:
            def dynamics_func(t, x):
                return self.dynamics.dynamics(x, 0.0)

        sol = solve_ivp(
            dynamics_func,
            t_span,
            x0,
            method='RK45',
            rtol=rtol,
            atol=atol
        )

        return {
            't': sol.t,
            'x': sol.y.T
        }