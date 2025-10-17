from __future__ import annotations

import math
from pathlib import Path
import numpy as np
import scipy as sp
from matplotlib import pyplot as plt

L = 1e-9
MASS_MODE = "electron"
MVAL = float(sp.constants.m_e)
NMAX = 4
COEFFS = [1 / np.sqrt(2), 1 / np.sqrt(2)]
N_VALS = [(1, 1), (2, 1)]

def ej(nx: int, ny: int, m: float, L: float) -> float:
    return ((nx * math.pi) ** 2 + (ny * math.pi) ** 2) * (sp.constants.hbar**2) / (2.0 * m * (L**2))

def psi(nx: int, ny: int, X: np.ndarray, Y: np.ndarray, L: float) -> np.ndarray:
    return (2.0 / L) * np.sin(nx * math.pi * X / L) * np.sin(ny * math.pi * Y / L)

def norm(x: np.ndarray, y: np.ndarray, psi_arr: np.ndarray) -> float:
    dens = np.abs(psi_arr) ** 2
    tmp = np.trapezoid(dens, x, axis=1)
    return float(np.trapezoid(tmp, y))


def plot_psi_levels(pairs: list[tuple[int, int]], m: float, L: float, out_path: Path) -> None:
    x = np.linspace(0, L, 1000)
    y0 = L * 0.5
    E = np.array([ej(int(nx), int(ny), m, L) / sp.constants.e for (nx, ny) in pairs])
    spc = float(np.min(np.diff(np.unique(np.sort(E))))) if len(E) > 1 else 1.0
    s = 0.35 * spc
    plt.figure(figsize=(6, 8))
    for (nx, ny), En in zip(pairs, E):
        psi_slice = (2.0 / L) * np.sin(nx * math.pi * x / L) * np.sin(ny * math.pi * y0 / L)
        y = En + s * psi_slice
        plt.plot(x, y, color="tab:blue")
        plt.hlines(En, x[0], x[-1], colors="tab:blue", linestyles="dashed", alpha=0.6)
        plt.text(L * 1.02, En, f"({nx},{ny})", va="center")
    plt.xlim(0, L)
    plt.ylim(E.min() - spc * 0.6, E.max() + spc * 0.6)
    plt.xlabel("x (m)")
    plt.ylabel("Energy (eV)")
    plt.title("Eigenfunctions (y=L/2) at energy levels")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()

def plot_density_levels(pairs: list[tuple[int, int]], m: float, L: float, out_path: Path) -> None:
    x = np.linspace(0, L, 1000)
    y0 = L * 0.5
    E = np.array([ej(int(nx), int(ny), m, L) / sp.constants.e for (nx, ny) in pairs])
    spc = float(np.min(np.diff(np.unique(np.sort(E))))) if len(E) > 1 else 1.0
    plt.figure(figsize=(6, 8))
    for (nx, ny), En in zip(pairs, E):
        r = ((2.0 / L) * np.sin(nx * math.pi * x / L) * np.sin(ny * math.pi * y0 / L)) ** 2
        a = (0.6 * spc) / float(np.max(r))
        y = En + a * r
        plt.plot(x, y, color="tab:blue")
        plt.hlines(En, x[0], x[-1], colors="tab:blue", linestyles="dashed", alpha=0.6)
        plt.text(L * 1.02, En, f"({nx},{ny})", va="center")
    plt.xlim(0, L)
    plt.ylim(E.min() - spc * 0.6, E.max() + spc * 0.6)
    plt.xlabel("x (m)")
    plt.ylabel("Energy (eV)")
    plt.title("Densities (y=L/2) at energy levels")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()

def main() -> None:
    m = float(sp.constants.m_e) if MASS_MODE == "electron" else float(MVAL)
    out = Path(__file__).resolve().parent; pics = out / "pics"; pics.mkdir(parents=True, exist_ok=True)
    for fn in ("energy_levels.png", "energy_vs_n.png", "eigenfunctions.png", "probability_density_snapshots.png", "psi_levels.png", "density_levels.png",
               "eigenfunction_n1.png", "eigenfunction_n2.png", "eigenfunction_n3.png", "eigenfunction_n4.png"):
        (pics / fn).unlink(missing_ok=True)

    modes = [(nx, ny) for nx in range(1, NMAX + 1) for ny in range(1, NMAX + 1)]
    modes_sorted = sorted(modes, key=lambda p: ej(p[0], p[1], m, L))
    K = len(modes_sorted)
    E = np.array([ej(nx, ny, m, L) / sp.constants.e for (nx, ny) in modes_sorted])
    plt.figure(figsize=(6, 4))
    for (nx, ny), Ek in zip(modes_sorted, E):
        plt.hlines(Ek, 0.8, 1.2, colors="tab:blue"); plt.text(1.22, Ek, f"({nx},{ny})", va="center")
    plt.xlim(0.7, 1.55); plt.ylim(0, E[-1] * 1.1); plt.ylabel("Energy (eV)"); plt.title("Energy levels (2D infinite well)"); plt.xticks([]); plt.tight_layout(); plt.savefig(pics / "energy_levels.png", dpi=200); plt.close()

    plt.figure(figsize=(6, 4))
    plt.plot(np.arange(1, K + 1), E, marker="o")
    plt.xlabel("mode index k"); plt.ylabel("Energy (eV)"); plt.title("Energy vs mode index (2D)"); plt.tight_layout(); plt.savefig(pics / "energy_vs_n.png", dpi=200); plt.close()

    Nplot = 4
    sel = modes_sorted[:Nplot]
    Ngrid = 300
    x = np.linspace(0, L, Ngrid); y = np.linspace(0, L, Ngrid)
    X, Y = np.meshgrid(x, y)
    fig, axs = plt.subplots(2, 2, figsize=(8, 7))
    for ax, (nx, ny) in zip(axs.ravel(), sel):
        P = psi(nx, ny, X, Y, L)
        im = ax.imshow(P, extent=[0, L, 0, L], origin="lower", cmap="RdBu")
        ax.set_title(f"ψ (nx,ny)=({nx},{ny})")
        ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)")
    plt.tight_layout(); plt.savefig(pics / "eigenfunctions.png", dpi=200); plt.close()

    for i, (nx, ny) in enumerate(sel, start=1):
        P = psi(nx, ny, X, Y, L)
        plt.figure(figsize=(5.5, 4.5))
        plt.imshow(P, extent=[0, L, 0, L], origin="lower", cmap="RdBu")
        plt.xlabel("x (m)"); plt.ylabel("y (m)"); plt.title(f"Eigenfunction ψ for (nx,ny)=({nx},{ny})")
        plt.tight_layout(); plt.savefig(pics / f"eigenfunction_n{i}.png", dpi=200); plt.close()

    c = np.asarray(COEFFS, dtype=np.complex128); c = c / np.sqrt(np.vdot(c, c).real)
    populated = [pair for pair, cc in zip(N_VALS, c) if abs(cc) > 1e-12]
    if len(populated) >= 2:
        (n1x, n1y), (n2x, n2y) = populated[0], populated[1]
        w = (ej(n2x, n2y, m, L) - ej(n1x, n1y, m, L)) / sp.constants.hbar
        T = 2 * math.pi / w; times = [0.0, 0.25 * T, 0.5 * T]
    else:
        times = [0.0, 1e-15, 2e-15]
    X2, Y2 = X, Y
    plt.figure(figsize=(9, 3.6))
    for t in times:
        p = np.zeros_like(X2, dtype=np.complex128)
        for cc, (nx, ny) in zip(c, N_VALS):
            p += cc * psi(int(nx), int(ny), X2, Y2, L) * np.exp(-1j * ej(int(nx), int(ny), m, L) * t / sp.constants.hbar)
        plt.subplot(1, 3, times.index(t) + 1)
        plt.imshow(np.abs(p) ** 2, extent=[0, L, 0, L], origin="lower", cmap="viridis")
        plt.title(f"t={t:.2e}s  N={norm(x, y, p):.3f}")
        plt.xlabel("x (m)"); plt.ylabel("y (m)")
    plt.tight_layout(); plt.savefig(pics / "probability_density_snapshots.png", dpi=200); plt.close()

    E11 = ej(1, 1, m, L) / sp.constants.e
    E21 = ej(2, 1, m, L) / sp.constants.e
    print("Particle in a 2D infinite well"); print(f"L={L:.2e} m, m={m:.4e} kg"); print(f"E(1,1)={E11:.3f} eV, E(2,1)={E21:.3f} eV")
    plot_psi_levels(sel, m, L, pics / "psi_levels.png")
    plot_density_levels(sel, m, L, pics / "density_levels.png")
    print("Saved: pics/energy_levels.png, pics/energy_vs_n.png, pics/eigenfunctions.png, pics/probability_density_snapshots.png, pics/psi_levels.png, pics/density_levels.png, "
        "pics/eigenfunction_n1.png, pics/eigenfunction_n2.png, pics/eigenfunction_n3.png, pics/eigenfunction_n4.png")

    

if __name__ == "__main__":
    main()
