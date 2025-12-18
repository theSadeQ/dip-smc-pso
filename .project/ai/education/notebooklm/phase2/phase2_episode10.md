# Episode 10: The Double-Inverted Pendulum System

**Duration**: 15-20 minutes | **Learning Time**: 1.5 hours | **Difficulty**: Intermediate

**Part of**: Phase 2.5 - Understanding the DIP System (Part 1 of 3)

---

## Opening Hook

Balancing one broomstick on your hand is tricky. Now tape a second broomstick to the top of the first and try again - that's the double-inverted pendulum challenge. Two unstable objects stacked vertically, controlled by moving the base horizontally. It sounds impossible, yet control theory makes it work. This episode reveals the physical structure, key parameters, and control objectives that define this benchmark problem in robotics and control engineering.

---

## Physical Structure: Three Components Plus One Input

The double-inverted pendulum consists of:

### 1. Cart

**What It Is**: A wheeled platform that slides horizontally on a track.

**Mass**: Typically M equals one kilogram (though this varies by implementation).

**Position**: x measured in meters from track center (positive right, negative left).

**Velocity**: x-dot measured in meters per second.

**Constraints**: Track has finite length (typically plus-or-minus two meters). Cart must not hit the ends!

### 2. Pendulum One (Lower Pendulum)

**What It Is**: A rigid rod hinged to the cart, swinging freely in the vertical plane.

**Mass**: m1 (typically zero-point-one kilograms, concentrated at center of mass).

**Length**: L1 (from hinge to center of mass, typically zero-point-five meters).

**Angle**: theta-one measured in radians from vertical (theta-one equals zero is perfectly upright, positive angles tilt right).

**Angular Velocity**: theta-one-dot measured in radians per second.

### 3. Pendulum Two (Upper Pendulum)

**What It Is**: A second rigid rod hinged to the TIP of pendulum one, also swinging freely.

**Mass**: m2 (typically zero-point-one kilograms).

**Length**: L2 (typically zero-point-five meters).

**Angle**: theta-two measured in radians from vertical.

**Angular Velocity**: theta-two-dot measured in radians per second.

### 4. Control Input

**What It Is**: Horizontal force F applied to the cart (positive pushes right, negative pushes left).

**Range**: F between negative twenty and positive twenty Newtons (typical actuator limits).

**Source**: In simulation, this is a computed value. In hardware, it's an electric motor or linear actuator producing the force.

---

## Why "Double" and Why "Inverted"

**Double**: Two pendulums stacked vertically. This contrasts with a single-inverted pendulum (just one pendulum on a cart).

**Inverted**: The goal is to keep both pendulums upright (vertical, pointing up), which is the OPPOSITE of their natural hanging-down position. Upright is unstable - without active control, the pendulums fall immediately.

**Analogy**: Balancing a broomstick vertically on your hand is "inverted" (unstable). If you tape a second broomstick to the top of the first, you have a "double-inverted" system - twice as hard to balance!

---

## System Block Diagram

Let's visualize how control closes the loop:

```
Reference (theta-one = 0, theta-two = 0, x = 0)
     |
     v
[Error Calculation] <--- Measured States (x, x-dot, theta-one, theta-one-dot, theta-two, theta-two-dot)
     |                                 ^
     v                                 |
[SMC Controller]                       |
(Computes Force F)                     |
     |                                 |
     v                                 |
[Force F: -20 to +20 N]                |
     |                                 |
     v                                 |
[DIP Plant]                            |
(Cart + 2 Pendulums)                   |
Dynamics: Nonlinear ODEs               |
     |                                 |
     v                                 |
[Actual States] ------------------->[Sensors]
```

**Flow**: Reference angles (zero) compared to measured angles, errors fed to SMC controller, controller computes force F, force applied to cart, cart and pendulums respond according to physics, sensors measure new states, loop repeats at one thousand Hertz.

---

## Key Parameters Summary

**Physical Constants**:
- Gravity: g equals nine-point-eight-one meters per second squared
- Cart mass: M equals one kilogram
- Pendulum one mass: m1 equals zero-point-one kilograms, length L1 equals zero-point-five meters
- Pendulum two mass: m2 equals zero-point-one kilograms, length L2 equals zero-point-five meters

**Control Limits**:
- Force: F between negative twenty and positive twenty Newtons
- Track length: x between negative two and positive two meters

**State Variables** (6 total):
1. x: Cart position
2. x-dot: Cart velocity
3. theta-one: Pendulum one angle
4. theta-one-dot: Pendulum one angular velocity
5. theta-two: Pendulum two angle
6. theta-two-dot: Pendulum two angular velocity

---

## Control Objectives

**Primary Objective**: Stabilize both pendulums upright from any initial condition within the basin of attraction.

**Specifically**:
- **theta-one approaches zero**: Pendulum one vertical
- **theta-two approaches zero**: Pendulum two vertical
- **x approaches zero**: Cart returns to track center (optional, depending on task)
- **All velocities approach zero**: System comes to rest

**Performance Goals**:
- Settling time: Less than five to ten seconds
- Overshoot: Less than twenty percent
- Steady-state error: Less than two degrees (zero-point-zero-three-five radians)
- Control effort: Minimize energy while achieving above
- Chattering: Minimize high-frequency oscillations

---

## Key Takeaways

**1. Structure**: Cart (moves horizontally) + Pendulum One (hinged to cart) + Pendulum Two (hinged to tip of Pendulum One) + Control Force F.

**2. State Space**: Six-dimensional (three positions: x, theta-one, theta-two; three velocities: x-dot, theta-one-dot, theta-two-dot).

**3. Control Input**: One force F (horizontal on cart), limited to negative twenty to positive twenty Newtons.

**4. Challenge**: Underactuated (one input, three outputs), unstable equilibrium, nonlinear dynamics, coupling between pendulums.

**5. Goal**: Drive both angles to zero, cart to center, all velocities to zero, in finite time with minimal overshoot and energy.

---

**Episode 10 of 12** | Phase 2: Core Concepts

**Previous**: [Episode 9 - PSO Algorithm](phase2_episode09.md) | **Next**: [Episode 11 - DIP Challenges & Applications](phase2_episode11.md)

---

**Usage**: Upload to NotebookLM for podcast discussion of the DIP system structure and parameters.
