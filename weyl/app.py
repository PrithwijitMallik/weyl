"""
WEYL - Scientific Computing Environment
Version: 0.1.0
Initial Module: 2-dimensional Heat Equation Solver
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from weyl.solver import (
    solve_heat_equation,
    analytical_fourier_solution,
    calculate_rms_error,
)

#-----------------
#PAGE CONFIGURATION
#-----------------
st.set_page_config(
    page_title="Weyl : Scientific Computing",
    page_icon=":thermometer:",
    layout="wide",
    initial_sidebar_state="expanded",
)

#-----------------
#VISUAL IDENTITY
#-----------------

st.markdown(
    '''
    <style>
    .stApp {
        background-color: #0b1120;
        color: #e5edf7;
    }

    [data-testid="stSidebar"] {
        background-color: #1a2b42;
    }

    .weyl-title {
        font-size: 3rem;
        color: #f1f5f9;
        letter-spacing: 0.1rem;
        font-weight: bold;
    }

    .section-label {
        font-size: 1.5rem;
        color: #38bdf8;
        letter-spacing: 0.05rem;
        font-weight: bold;
    }
    </style>
    ''',
    unsafe_allow_html=True,
)

#-----------------
# HEADER
#-----------------
st.markdown(
    '<div class="weyl-title">WEYL</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '''
    <div class="weyl-subtitle">
        An accessible computational environment for independent scientific research.
    </div>
    ''',
    unsafe_allow_html=True,
)

st.write('---')

st.markdown(
    '<div class="section-label">'
    'COMPUTATIONAL PHYSICS | MODULE 001'
    '</div>',
    unsafe_allow_html=True,
)

st.title("Two-Dimensional Heat Equation Solver")
st.caption(
    "Numerical solution using an explicit "
    "finite difference method."
)
#-----------------
#SIDEBAR: COMPUTATIONAL PARAMETERS
#-----------------

st.sidebar.title("WEYL")
st.sidebar.caption("Computational Workbench")

alpha = st.sidebar.slider(
    "Thermal Diffusivity (alpha)",
    min_value=0.01,
    max_value=1.00,
    value=0.01,
    step=0.01,
)

grid_size = st.sidebar.slider(
    "Spatial Resolution",
    min_value=0,
    max_value=1000,
    value=1,
    step=1,
)

total_time = st.sidebar.slider(
    "Total Simulation Time",
    min_value=0.1,
    max_value=10.0,
    value=0.01,
    step=0.01,
)

snapshots = st.sidebar.slider(
    "Number of Snapshots",
    min_value=1,
    max_value=100,
    value=1,
    step=1
)

initial_condition = st.sidebar.selectbox(
    "Initial Condition",
    options=["Gaussian", "Fourier Mode"],
    index=0
)
st.sidebar.divider()

st.sidebar.caption(
 "Numerical Method: FTCS (Forward Time Centered Space)"
)
st.sidebar.caption(
    "Boundary Conditions: Dirichlet (zero)"
)
 #-----------------
 #COMPUTATIONAL
 #-----------------
@st.cache_data(show_spinner=False)
def run_simulation(
 nx,
 ny,
 diffusivity,
 duration,
 condition,
 number_of_snapshots,
):

 return solve_heat_equation(
  nx=nx,
  ny=ny,
  alpha=diffusivity,
  total_time=duration,
  initial_condition=condition,
  snapshots=number_of_snapshots,
 )
with st.spinner("Computing numerical solution..."):
    result = run_simulation(
        grid_size,
        grid_size,
        alpha,
        total_time,
        initial_condition,
        snapshots,
    )

#------------
#RESULTS
#------------

st.divider()
col1, col2, col3, col4 = st.columns(4)

col1.metric(
 "Grid resolution",
 f"{grid_size} × {grid_size}"
 )
col2.metric(
 "Time steps",
f"{result['n_steps']:,}",
)
col3.metric(
 "Time step (Δt)",
 f"{result['dt']:.2e}",
 )
col4.metric(
 "Stability number",
 f"{result['stability_number']:.4f}"
)

#----------
# SIMULATION VISUALISATION
#----------

st.subheader("Simulation Output")
st.caption(
        "Explore the evolution of the temparature"
        " distribution across the spatial domain." 
)
frame_index = st.slider(
    "Simulation time frame",
    min_value=0,
    max_value=len(result["frames"])-1,
    value=len(result["frames"])-1,
)
current_frame=result["frames"][frame_index]
current_time=result["times"][frame_index]

#----------
# HEATMAP
#----------
fig, ax = plt.subplots(figsize=(100, 6))
fig.patch.set_facecolor("#0b1120")
ax.set_facecolor("#0b1120")

plot = ax.imshow(
    current_frame,
    origin="lower",
    extent=[0, 1, 0, 1],
    cmap="inferno",
    interpolation="bilinear",
    aspect="equal",
)
ax.set_xlabel(
 "y position",
 color="white",
)
ax.set_title(
 f"Temparature Distribution | t={current_time:.4f}",
 color="white",
 pad=15,
)

ax.tick_params(colors="white")

for spine in ax.spines.values():
    spine.set_color("#334155")

colorbar = fig.colorbar(
    plot,
    ax=ax,
    fraction=0.046,
    pad=0.04,
)

colorbar.set_label(
    "Temperature",
    color="white",
)
plt.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)
#------------------
# SCIENTIFIC VALIDATION
#------------------

st.divider()
st.subheader("Numerical Diagnostics")

if initial_condition == "Fourier Mode":
    analytical = analytical_fourier_solution(
        result["X"],
        result["Y"],
        current_time,
        alpha,
    )

    error = calculate_rms_error(
        current_frame,
        analytical,
    )

    left, right = st.columns(2)

    left.metric(
        "RMS numerical error",
        f"{error:.6e}",
    )

    right.metric(
        "Analytical reference",
        "Available",
    )

    st.info(
        "The Fourier-mode solution is compared "
        "against its known analytical solution."
    )

else:
    left, right = st.columns(2)

    left.metric(
        "Maximum temperature",
        f"{np.max(current_frame):.6f}",
    )
    right.metric(
        "Minimum temparature",
        f"{np.min(current_frame):.6f}",
    )

    st.info(
        "The Gaussian initial condition is evolved "
        "under homogeneous Dirichlet boundaries."
    )
 #------------------
# DATA EXPORT
#------------------

st.divider()
st.subheader("Export Results")

csv_data = np.column_stack(
    (
        result["X"].ravel(),
        result["Y"].ravel(),
        current_frame.ravel(),
    )
)

csv_header = "x,y,temperature"

import io
buffer = io.StringIO()

np.savetxt(
    buffer,
    csv_data,
    delimiter=",",
    header=csv_header,
    comments="",
)

st.download_button(
    label="Download simulation data (CSV)",
    data=buffer.getvalue(),
    file_name="weyl_simulation.csv",
    mime="text/csv",
)

st.caption(
    "Weyl v0.1.0 | Early stage research prototype"
)

st.caption(
    "Numerical results should be independently "
    "validated before scientific use."
)
