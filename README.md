# Curve Parameter Recovery

## Overview
We are given 1500 \((x, y)\) points sampled from a curve for \(6 \leq t \leq 60\), but the corresponding value of \(t\) is not provided. The goal is to recover the parameters \( \theta \), \( M \), and \( X \).

---

## Approach

### Step 1 — Identify the structure

Rewriting the equations:

\[
x - X = t\cos(\theta) - B\sin(\theta)
\]
\[
y - 42 = t\sin(\theta) + B\cos(\theta)
\]

where:

\[
B = e^{M|t|} \cdot \sin(0.3t)
\]

This matches the standard 2D rotation of the point \((t, B)\).  
So, \((x - X, y - 42)\) is simply \((t, B)\) rotated by angle \(\theta\).

---

### Step 2 — Undo the rotation

Since rotation is invertible, we rotate back by \(-\theta\).

Using complex numbers:

\[
Z = (x - X) + i(y - 42)
\]
\[
W = Z \cdot e^{-i\theta} = t + iB
\]

So:
- \( \text{Re}(W) = t \)
- \( \text{Im}(W) = B \)

This avoids having to estimate \(t\) separately for each point.

---

### Step 3 — Optimization

For correct parameters:

\[
\text{Im}(W) = e^{M|\text{Re}(W)|} \cdot \sin(0.3 \cdot \text{Re}(W))
\]

Error per point:

\[
\text{error} = \text{Im}(W) - e^{M \cdot \text{Re}(W)} \cdot \sin(0.3 \cdot \text{Re}(W))
\]

We minimize the sum of squared errors over all points.

---

### Step 4 — Solve

- Used `scipy.optimize.least_squares`
- Multi-start initialization within bounds:
  - \(0^\circ < \theta < 50^\circ\)
  - \(-0.05 < M < 0.05\)
  - \(0 < X < 100\)
- Final refinement for high precision

---

## Results

| Parameter | Value |
|----------|------|
| \( \theta \) | 0.523599 rad (30°) |
| \( M \) | 0.03 |
| \( X \) | 55 |

**Max residual:**
\[
\approx 1.8 \times 10^{-5}
\]

---

## Final Parametric Equation

\[
\left(
t \cos(0.523599)
- e^{0.03|t|} \cdot \sin(0.3t)\sin(0.523599)
+ 55,\;
42 + t \sin(0.523599)
+ e^{0.03|t|} \cdot \sin(0.3t)\cos(0.523599)
\right)
\]

---

## Desmos Visualization
https://www.desmos.com/calculator/bv01iaqmqn
