## Approach

The problem: we are given 1500 \((x, y)\) points sampled from a curve for \(6 \leq t \leq 60\), but the corresponding value of \(t\) for each point is not provided. The goal is to recover the parameters \( \theta \), \( M \), and \( X \).

---

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

This is exactly the formula for rotating the point \((t, B)\) by an angle \(\theta\).  
So, \((x - X, y - 42)\) is simply a rotated version of \((t, B)\).

---

### Step 2 — Undo the rotation

Since rotation is reversible, we can rotate the points back by \(-\theta\) to recover the original values.

Using complex numbers makes this very clean:

\[
Z = (x - X) + i(y - 42)
\]
\[
W = Z \cdot e^{-i\theta} = t + iB
\]

This directly gives:
- \( \text{Re}(W) = t \)
- \( \text{Im}(W) = B \)

So we recover \(t\) **without needing to guess or match it per point**, which avoids a much slower fitting process.

---

### Step 3 — Reduce to an optimization problem

For the correct parameters:

\[
\text{Im}(W) = e^{M|\text{Re}(W)|} \cdot \sin(0.3 \cdot \text{Re}(W))
\]

So the error for each point becomes:

\[
\text{error} = \text{Im}(W) - e^{M \cdot \text{Re}(W)} \cdot \sin(0.3 \cdot \text{Re}(W))
\]

We minimize the sum of squared errors over all points.

This reduces the problem to a **3-parameter nonlinear least-squares fit**.

---

### Step 4 — Solve

- Used `scipy.optimize.least_squares`
- Ran multiple initial guesses across bounds:
  - \(0^\circ < \theta < 50^\circ\)
  - \(-0.05 < M < 0.05\)
  - \(0 < X < 100\)
- Selected the best result and refined it with tighter tolerances

---

## Result

| Parameter | Value |
|----------|------|
| \( \theta \) | 0.523599 rad (30°) |
| \( M \) | 0.03 |
| \( X \) | 55 |

**Maximum residual across all 1500 points:**

\[
\approx 1.8 \times 10^{-5}
\]

This is extremely small and mainly due to floating-point precision, indicating an essentially exact fit.

---

## Verification

The recovered curve was plotted in Desmos over \(6 \leq t \leq 60\), and it visually matches the provided data points very closely in both shape and scale.

---

## Conclusion

By recognizing the hidden rotation structure, the problem was simplified from a complex curve-fitting task into a small 3-parameter optimization problem. This made the solution both efficient and highly accurate.
