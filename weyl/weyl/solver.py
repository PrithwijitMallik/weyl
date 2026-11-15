
"""
Weyl Numerical Solver

Version: 0.1.0
Two-Dimensional Heat Equation Solver

Method:
Explicit Finite Difference Method (FTCS)

Boundary Conditions:
Homogeneous Dirichlet boundaries (zero temperature).
"""

import numpy as np


def solve_heat_equation(
    nx=61,
    ny=61,
    alpha=0.01,
    total_time=0.01,
    initial_condition="Gaussian",
    snapshots=30,
):
    """
    Solve the two-dimensional heat equation using FTCS.

    Parameters
    ----------
    nx, ny : int
        Number of grid points in the x and y directions.

    alpha : float
        Thermal diffusivity.

    total_time : float
        Total simulation time.

    initial_condition : str
        "Gaussian" or "Fourier Mode".

    snapshots : int
        Number of requested output snapshots.

    Returns
    -------
    dict
        Coordinates, solution snapshots, times,
        and numerical stability information.
    """

    # Validate inputs
    if nx < 3 or ny < 3:
        raise ValueError("Grid dimensions must be at least 3.")

    if alpha <= 0:
        raise ValueError("Thermal diffusivity must be positive.")

    if total_time <= 0:
        raise ValueError("Total simulation time must be positive.")

    if snapshots < 2:
        raise ValueError("At least 2 snapshots are required.")

    # Create spatial grid
    x = np.linspace(0.0, 1.0, nx)
    y = np.linspace(0.0, 1.0, ny)

    dx = x[1] - x[0]
    dy = y[1] - y[0]

    X, Y = np.meshgrid(x, y)

    # Set initial temperature distribution
    if initial_condition == "Gaussian":

        sigma = 0.12

        U = np.exp(
            -(
                (X - 0.5) ** 2
                + (Y - 0.5) ** 2
            )
            / (2 * sigma ** 2)
        )

    elif initial_condition == "Fourier Mode":

        U = (
            np.sin(np.pi * X)
            * np.sin(np.pi * Y)
        )

    else:
        raise ValueError(
            "Initial condition must be Gaussian or Fourier Mode."
        )

    # Enforce zero-temperature boundaries
    U[0, :] = 0.0
    U[-1, :] = 0.0
    U[:, 0] = 0.0
    U[:, -1] = 0.0

    # Calculate the maximum stable time step
    dt_stable = 0.5 / (
        alpha * (1.0 / dx**2 + 1.0 / dy**2)
    )

    # Select a stable time step with a safety factor
    dt = 0.9 * dt_stable

    # Determine number of time steps
    n_steps = max(
        int(np.ceil(total_time / dt)),
        snapshots - 1,
    )

    # Adjust dt to reach the requested final time exactly
    dt = total_time / n_steps

    # Calculate FTCS stability parameters
    rx = alpha * dt / dx**2
    ry = alpha * dt / dy**2

    stability_number = rx + ry

    # Final stability check
    if stability_number > 0.5:
        raise ValueError("Numerical stability condition violated.")

    # Select snapshot time indices
    snapshot_indices = np.linspace(
        0,
        n_steps,
        snapshots,
        dtype=int,
    )

    snapshot_indices = np.unique(snapshot_indices)

    saved_snapshots = []
    saved_times = []

    # Save initial condition
    saved_snapshots.append(U.copy())
    saved_times.append(0.0)

    # Time integration
    for step in range(1, n_steps + 1):

        U_new = U.copy()

        # Explicit FTCS update
        U_new[1:-1, 1:-1] = (
            U[1:-1, 1:-1]
            + rx * (
                U[1:-1, 2:]
                - 2.0 * U[1:-1, 1:-1]
                + U[1:-1, :-2]
            )
            + ry * (
                U[2:, 1:-1]
                - 2.0 * U[1:-1, 1:-1]
                + U[:-2, 1:-1]
            )
        )

        # Maintain zero-temperature boundaries
        U_new[0, :] = 0.0
        U_new[-1, :] = 0.0
        U_new[:, 0] = 0.0
        U_new[:, -1] = 0.0

        U = U_new

        # Save requested snapshots
        if step in snapshot_indices:
            saved_snapshots.append(U.copy())
            saved_times.append(step * dt)

    # Convert saved data to NumPy arrays
    saved_snapshots = np.array(saved_snapshots)
    saved_times = np.array(saved_times)

    return {
        "X": X,
        "Y": Y,
        "snapshots": saved_snapshots,
        "frames": saved_snapshots,
        "times": saved_times,
        "final_frame": U.copy(),
        "dt": dt,
        "dx": dx,
        "dy": dy,
        "rx": rx,
        "ry": ry,
        "stability_number": stability_number,
        "alpha": alpha,
        "total_time": total_time,
        "initial_condition": initial_condition,
        "n_steps": n_steps,
    }


def analytical_fourier_solution(
    X,
    Y,
    time,
    alpha,
):
    """
    Exact solution for a single Fourier mode.

    Assumes a unit square with zero-temperature boundaries.
    """

    spatial_mode = (
        np.sin(np.pi * X)
        * np.sin(np.pi * Y)
    )

    decay = np.exp(
        -2.0 * np.pi**2 * alpha * time
    )

    return spatial_mode * decay


def calculate_rms_error(
    numerical,
    analytical,
):
    """
    Calculate the root mean square difference
    between numerical and analytical solutions.
    """

    numerical = np.asarray(numerical)
    analytical = np.asarray(analytical)

    if numerical.shape != analytical.shape:
        raise ValueError(
            "Numerical and analytical arrays must have matching shapes."
        )

    difference = numerical - analytical

    return float(
        np.sqrt(np.mean(difference**2))
    )

