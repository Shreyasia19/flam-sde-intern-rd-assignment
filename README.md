# Curve Parameter Recovery

## Overview
In this project, the goal is to recover the parameters of a parametric curve using only a set of \((x, y)\) points. The challenge is that the original parameter \(t\) is not given, which makes the problem a bit tricky.

We aim to estimate three unknowns:
- Rotation angle (\(\theta\))
- Growth factor (\(M\))
- Horizontal shift (\(X\))

---

## Approach

### Understanding the Structure
After analyzing the equations, the key realization was that the curve is basically a transformed version of a simpler function:

\[
B(t) = e^{M|t|} \cdot \sin(0.3t)
\]

The original point \((t, B(t))\) is:
- Rotated by an angle \(\theta\)
- Shifted by \((X, 42)\)

---

### Key Idea
Instead of trying to guess \(t\) for every point (which would be messy and inefficient), we can reverse the transformation:

1. Shift the points back:
   \[
   (x - X, \; y - 42)
   \]

2. Undo the rotation (rotate by \(-\theta\))

Once we do this, something nice happens:
- The x-part directly gives us \(t\)
- The y-part gives us \(B(t)\)

This avoids solving for \(t\) separately and simplifies the whole problem a lot.

---

### Optimization Setup
Now the task becomes finding the best values of \(\theta\), \(M\), and \(X\) such that:

\[
\text{Recovered } B(t) \approx e^{M|t|} \cdot \sin(0.3t)
\]

We minimize the squared error:

\[
\sum \left(
\text{Im}(W) - e^{M \cdot \text{Re}(W)} \cdot \sin(0.3 \cdot \text{Re}(W))
\right)^2
\]

---

### How It Was Solved
- Used `scipy.optimize.least_squares` for fitting  
- Tried multiple starting points to avoid getting stuck in bad solutions  
- Refined the result with stricter tolerances for better accuracy  

---

## Results

The recovered parameters are:

- \(\theta = 0.523599\) radians (**30°**)  
- \(M = 0.03\)  
- \(X = 55\)

The maximum error across all 1500 points is:

\[
\approx 1.8 \times 10^{-5}
\]

This is extremely small, meaning the fit is almost perfect.

---

## Final Equation

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

## Desmos Version

https://www.desmos.com/calculator/bv01iaqmqn
