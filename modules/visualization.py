import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_pnl_surface(pos_a, pos_c, pos_d):
    """
    Plots the P&L change surface based on yield changes for long, middle, and short maturity portfolios.

    Parameters:
    pos_a (float): Position in portfolio A (long maturity).
    pos_c (float): Position in portfolio C (middle maturity).
    pos_d (float): Position in portfolio D (short maturity).
    """
    yield_changes_a = np.linspace(-200, 200, 50)
    yield_changes_c = np.linspace(-200, 200, 50)
    yield_change_d = -100

    yield_a_grid, yield_c_grid = np.meshgrid(yield_changes_a / 10000, yield_changes_c / 10000)
    yield_d_decimal = yield_change_d / 10000

    port_a_change = (-15.30898 * yield_a_grid + 144.61398 * yield_a_grid**2) * pos_a * 1000
    port_c_change = (-7.55590 * yield_c_grid + 31.92781 * yield_c_grid**2) * pos_c * 1000
    port_d_change = (-3.85018 * yield_d_decimal + 9.57503 * yield_d_decimal**2) * pos_d * 1000

    total_change_grid = port_a_change + port_c_change + port_d_change

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(yield_a_grid * 10000, yield_c_grid * 10000, total_change_grid, cmap='viridis')

    ax.set_xlabel("Long Maturity Yield Change (bps)")
    ax.set_ylabel("Middle Maturity Yield Change (bps)")
    ax.set_zlabel("Total P&L Change")
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.title(f"Total P&L Change vs Yield Changes (Short Maturity Yield Change fixed at {yield_change_d} bps)")
    plt.show()