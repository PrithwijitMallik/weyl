# Weyl — Numerical Validation Record

**Version:** 0.1.0  
**Project:** Weyl Computational Physics  
**Validation status:** Preliminary

## 1. Objective

This document records preliminary numerical validation of Weyl, a two-dimensional heat equation solver.

The purpose is to evaluate the numerical accuracy and physical consistency of the Explicit Finite Difference Method (FTCS).

## 2. Numerical Method

Weyl solves the two-dimensional heat equation:

\[
\frac{\partial u}{\partial t}
=
\alpha
\left(
\frac{\partial^2 u}{\partial x^2}
+
\frac{\partial^2 u}{\partial y^2}
\right)
\]

The solver uses:
- Explicit Forward Time Centered Space (FTCS) method.
- Homogeneous Dirichlet boundary conditions.
- A uniform spatial grid.
- A stability condition of \(r_x+r_y\leq 0.5\).

## 3. Fourier Mode Validation

The numerical solution was compared against the analytical solution for a single Fourier mode.

### Test parameters

| Parameter | Value |
|---|---:|
| Thermal diffusivity | 0.05 |
| Total simulation time | 0.50 |
| Initial condition | Fourier Mode |
| Number of snapshots | 30 |
| Grid resolutions | 51, 101, 201 |

### Results

| Grid resolution | RMS numerical error |
|---|---:|
| 51 × 51 | 7.510506 × 10⁻⁵ |
| 101 × 101 | 1.897736 × 10⁻⁵ |
| 201 × 201 | 4.768473 × 10⁻⁶ |

## 4. Interpretation

The RMS numerical error decreases as the spatial resolution increases.

Approximately doubling the grid resolution reduces the measured error by a factor of four.

This behaviour is consistent with approximately second-order convergence.

However, the time step also changes with grid resolution to maintain numerical stability. Therefore, these results represent a combined spatial and temporal refinement study rather than an isolated spatial convergence study.

## 5. Gaussian Diffusion Test

A Gaussian initial temperature distribution was also tested.

Observed behaviour:
- Initial maximum temperature: approximately 1.00.
- Final maximum temperature: approximately 0.22.
- Minimum temperature: 0.00.
- The Gaussian distribution spreads over time.
- The zero-temperature boundaries are maintained.

These observations are consistent with the expected qualitative behaviour of heat diffusion.

## 6. Limitations and Future Work

Further validation is required, including:

- Independent testing of boundary conditions.
- More systematic grid and time-step convergence studies.
- Automated unit tests.
- Testing over a wider range of physical parameters.
- Independent verification of numerical results.

## 7. Conclusion

Preliminary tests indicate that Weyl produces physically consistent heat diffusion behaviour and promising numerical convergence for a Fourier-mode initial condition.

These results are preliminary and do not yet constitute a complete scientific verification of the solver.
