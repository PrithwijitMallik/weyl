""""
Weyl Numerical Solver

Version 0.1.0
Two Dimentional Heat Equation Solver

Method:
Explicit Finite Difference Method (FTCS)

Boundary Conditions:
Homogenous Dirichlet boundaries (zero)
"""

import numpy as np
def solve_heat_equation(
    nx=61,
    ny=61,
    alpha=.01,
    total_time=.01, 
    initial_condition="Gaussian",
    snapshots=30,
):
    """
   Solve the two-dimensional heat equation.

   Parameters
   ----------
   nx, ny : int
       Number of grid points.

       alpha : float
       Thermal diffusivity. 

    total_time : float
    Total simulation time.

    initial_condition : str
    Gaussian or Fourier mode.
    
    snapshots : int
    Number of requested output intervals.

    Returns
    -------
    dict
    Coordinates, simulation frames, timing
    information and numerical diagnostics.
    
    """

    if nx < 5 or ny < 5:
        raise ValueError("Grid size must be at least 5x5.")
    if alpha <= 0:
        raise ValueError("Thermal diffusivity must be positive.")
    if total_time <= 0:
        raise ValueError("Total simulation time must be positive.")
    if snapshots < 1:   
        raise ValueError("Number of snapshots must be at least 1.")

    # Spatial domain
    x = np.linspace(0.0, 1.0, nx)
    y = np.linspace(0.0, 1.0, ny)

    dx = x[1] - x[0]
    dy = y[1] - y[0]    

    X,Y = np.meshgrid(x,y)

    #Initial Temparature Distribution
    if initial_condition == "Gaussian":
        sigma = 0.12 
        u = np.exp
        (
            -(
             (X-.05)**2
            +(Y-.05)**2
            )/(2*sigma**2) 
        )
        if initial_condition == "Fourier Mode":
            u=(
            np.sin(np.pi*X)
                *np.sin(np.pi*Y)
            )
    else:
        raise ValueError("Invalid initial condition. Choose 'Gaussian' or 'Fourier Mode'.")
    #Enforce boundary conditions
    u[0,:] = 0.0
    u[-1,:] = 0.0
    u[:,0] = 0.0
    u[:,-1] = 0.0

    #Numerical Stability Condition
    inverse_spacing = (
        1.0 / dx**2 + 1.0 / dy**2
    )
    maximum_dt = (
       0.45 / (alpha* inverse_spacing )
    )
#Automatically select a stable timestep
steps = max(
    1,
    int(np.ceil(total_time / maximum_dt))
)
dt = total_time / steps
rx= alpha * dt / dx**2
ry= alpha * dt / dy**2
stability_number = rx + ry

#Select snapshot positions
snapshot_steps = np.unique (
    np.linspace(
        0,
        steps,
        min (snapshots + 1, steps + 1),
        dtype=int,
    )
)
frmaes = [u.copy()]
times= [0.0]
next_snapshot=1

#Time integration
for step in range (1, steps +1):

    old= u 
    new= old.copy()
    new[1:-1, 1:-1]=(
        old[1:-1, 1:-1]
        + rx* (
            old [2:, 1:-1]
            -2 * old[1:-1, 1:-1]
            +old [1:-1, :-2]
        )
    )
    u = new
    #store requested snapshots
    if (
        next_snapshot< len(snapshot_steps)
        and step == snapshot_steps[next_snapshot]

    ):
        frames.append(u.copy())
        times.append(step*dt)
        next_snapshot += 1

        return {
            "x":x,
            "ÿ":y,
            "X": X,
            "Y": Y,
            "frmaes": np.array(frames),
            "times": np.array(times),
            "dt":dt,
            "steps":steps,
            "dx":dx,
            "dy":dy,
            "rx":rx,
            "ry":ry,
            "stabilitty_number":stability_number,
            "älpha": alpha,
            "total_time": total_time,
            "ïnitial_condition": initial_condition,
}

def analytical_fourier_solution(
        X,
        Y,
        time,
        alpha,
):
    """"""""""""
    Exact solution for a single Fourier mode
    with homogeneous Dirrichlet boundaries.
    """"""""""""

    spatial_mode= (
        np.sin(np.pi*X)
        *np.sin(np.pi*Y)
    )
    decay = np.exp(
        -2*np.pi**2 * alpha * time
        )

return spatial_mode*decay

def calculate_rms_error(numerical,
                        analytical,
                         ):
    """"""""""""""""""
    Calculate root mean square error.
    """"""""""""""""""
    difference= numerical - analytical
     
     return float(
        np.sqrt(np.mean(difference**2))
    )
    
