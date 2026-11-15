import numpy as np
import pytest

from solver import initial_condition, laplacian, solve_heat, solve_pde


def test_initial_condition_has_expected_shape_and_zero_boundaries():
    X, Y, U = initial_condition(31, 41, 1.0, 2.0)
    assert X.shape == (31, 41)
    assert Y.shape == (31, 41)
    assert U.shape == (31, 41)
    assert np.allclose(U[0, :], 0.0)
    assert np.allclose(U[-1, :], 0.0)
    assert np.allclose(U[:, 0], 0.0)
    assert np.allclose(U[:, -1], 0.0)


def test_laplacian_of_quadratic_field_is_approximately_four():
    x = np.linspace(-1.0, 1.0, 41)
    y = np.linspace(-1.0, 1.0, 41)
    X, Y = np.meshgrid(x, y, indexing="ij")
    U = X**2 + Y**2
    result = laplacian(U, x[1] - x[0], y[1] - y[0])
    assert np.allclose(result[2:-2, 2:-2], 4.0, atol=1e-10)


def test_heat_equation_gaussian_peak_decays():
    result = solve_pde(
        equation="Heat",
        nx=41,
        ny=41,
        coefficient=0.1,
        steps=100,
    )
    initial_max = np.max(result["snapshots"][0])
    final_max = np.max(result["snapshots"][-1])
    assert final_max < initial_max


def test_boundary_conditions_remain_zero():
    result = solve_pde(equation="Heat", nx=31, ny=31, steps=30)
    for field in result["snapshots"]:
        assert np.allclose(field[0, :], 0.0)
        assert np.allclose(field[-1, :], 0.0)
        assert np.allclose(field[:, 0], 0.0)
        assert np.allclose(field[:, -1], 0.0)


def test_wave_solver_produces_finite_values():
    result = solve_pde(
        equation="Wave",
        nx=41,
        ny=41,
        coefficient=1.0,
        steps=100,
    )
    for field in result["snapshots"]:
        assert np.all(np.isfinite(field))


def test_unstable_time_step_is_rejected():
    with pytest.raises(ValueError, match="stability"):
        solve_pde(
            equation="Heat",
            nx=41,
            ny=41,
            coefficient=0.1,
            dt=1.0,
            steps=10,
        )


def test_heat_solution_matches_sine_mode_analytical_decay():
    # For u(x,y,0)=sin(pi*x)sin(pi*y), the continuous solution is
    # exp(-2*D*pi^2*t)*sin(pi*x)sin(pi*y) on a unit square.
    nx = ny = 41
    lx = ly = 1.0
    diffusivity = 0.1
    x = np.linspace(0.0, lx, nx)
    y = np.linspace(0.0, ly, ny)
    X, Y = np.meshgrid(x, y, indexing="ij")
    U0 = np.sin(np.pi * X) * np.sin(np.pi * Y)

    dt = 0.0005
    steps = 100
    snapshots, times = solve_heat(
        U0, lx, ly, diffusivity, dt, steps, snapshot_count=10
    )
    numerical = snapshots[-1]
    t = times[-1]
    analytical = (
        np.exp(-2.0 * diffusivity * np.pi**2 * t)
        * np.sin(np.pi * X)
        * np.sin(np.pi * Y)
    )
    max_error = np.max(np.abs(numerical - analytical))
    assert max_error < 0.003


def test_invalid_equation_is_rejected():
    with pytest.raises(ValueError, match="equation"):
        solve_pde(equation="Advection")


def test_snapshot_times_match_snapshots():
    result = solve_pde(equation="Wave", steps=23, snapshot_count=7)
    assert len(result["snapshots"]) == len(result["times"])
    assert result["times"][0] == 0.0
    assert result["times"][-1] == pytest.approx(result["final_time"])
