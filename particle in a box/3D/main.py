from __future__ import annotations

import math
from pathlib import Path
import numpy as np
import scipy as sp
from matplotlib import pyplot as plt

print("Executing 3D version...")
L = 1e-9
MASS_MODE = "electron"
MVAL = float(sp.constants.m_e)
NMAX = 3
COEFFS = [1 / np.sqrt(2), 1 / np.sqrt(2)]
N_VALS = [(1, 1, 1), (2, 1, 1)]


def ej3(nx: int, ny: int, nz: int, m: float, L: float) -> float:
    return (
        ((nx * math.pi) ** 2 + (ny * math.pi) ** 2 + (nz * math.pi) ** 2)
        * (sp.constants.hbar**2)
        / (2.0 * m * (L**2))
    )


def psi3(
    nx: int, ny: int, nz: int, X: np.ndarray, Y: np.ndarray, Z: np.ndarray, L: float
) -> np.ndarray:
    return (
        (2.0 / L) ** 1.5
        * np.sin(nx * math.pi * X / L)
        * np.sin(ny * math.pi * Y / L)
        * np.sin(nz * math.pi * Z / L)
    )


def norm3(x: np.ndarray, y: np.ndarray, z: np.ndarray, psi_arr: np.ndarray) -> float:
    dens = np.abs(psi_arr) ** 2
    tmp = np.trapezoid(dens, x, axis=2)
    tmp = np.trapezoid(tmp, y, axis=1)
    return float(np.trapezoid(tmp, z, axis=0))


def norm_xy(x: np.ndarray, y: np.ndarray, psi_xy: np.ndarray) -> float:
    dens = np.abs(psi_xy) ** 2
    tmp = np.trapezoid(dens, x, axis=1)
    return float(np.trapezoid(tmp, y))


def add_dim_label(label: str) -> None:
    fig = plt.gcf()
    try:
        fig.text(
            0.01, 0.985, label, ha="left", va="top", fontsize=12, fontweight="bold"
        )
    except Exception:
        pass


def plot_psi_levels(
    triplets: list[tuple[int, int, int]], m: float, L: float, out_path: Path
) -> None:
    x = np.linspace(0, L, 1000)
    y0 = L * 0.5
    z0 = L * 0.5
    E = np.array(
        [
            ej3(int(nx), int(ny), int(nz), m, L) / sp.constants.e
            for (nx, ny, nz) in triplets
        ]
    )
    uniq = np.unique(np.sort(E))
    spc = float(np.min(np.diff(uniq))) if len(uniq) > 1 else 1.0
    s = 0.35 * spc
    plt.figure(figsize=(6, 8))
    for (nx, ny, nz), En in zip(triplets, E):
        psi_slice = (
            (2.0 / L) ** 1.5
            * np.sin(nx * math.pi * x / L)
            * np.sin(ny * math.pi * y0 / L)
            * np.sin(nz * math.pi * z0 / L)
        )
        y = En + s * psi_slice
        plt.plot(x, y, color="tab:blue")
        plt.hlines(En, x[0], x[-1], colors="tab:blue", linestyles="dashed", alpha=0.6)
        plt.text(L * 1.02, En, f"({nx},{ny},{nz})", va="center")
    plt.xlim(0, L)
    plt.ylim(E.min() - spc * 0.6, E.max() + spc * 0.6)
    plt.xlabel("x (m)")
    plt.ylabel("Energy (eV)")
    plt.title("Eigenfunctions (y=z=L/2) at energy levels")
    plt.tight_layout()
    add_dim_label("3D")
    plt.savefig(out_path, dpi=200)
    plt.close()


def plot_density_levels(
    triplets: list[tuple[int, int, int]], m: float, L: float, out_path: Path
) -> None:
    x = np.linspace(0, L, 1000)
    y0 = L * 0.5
    z0 = L * 0.5
    E = np.array(
        [
            ej3(int(nx), int(ny), int(nz), m, L) / sp.constants.e
            for (nx, ny, nz) in triplets
        ]
    )
    uniq = np.unique(np.sort(E))
    spc = float(np.min(np.diff(uniq))) if len(uniq) > 1 else 1.0
    plt.figure(figsize=(6, 8))
    for (nx, ny, nz), En in zip(triplets, E):
        r = (
            (2.0 / L) ** 1.5
            * np.sin(nx * math.pi * x / L)
            * np.sin(ny * math.pi * y0 / L)
            * np.sin(nz * math.pi * z0 / L)
        ) ** 2
        a = (0.6 * spc) / float(np.max(r))
        y = En + a * r
        plt.plot(x, y, color="tab:blue")
        plt.hlines(En, x[0], x[-1], colors="tab:blue", linestyles="dashed", alpha=0.6)
        plt.text(L * 1.02, En, f"({nx},{ny},{nz})", va="center")
    plt.xlim(0, L)
    plt.ylim(E.min() - spc * 0.6, E.max() + spc * 0.6)
    plt.xlabel("x (m)")
    plt.ylabel("Energy (eV)")
    plt.title("Densities (y=z=L/2) at energy levels")
    plt.tight_layout()
    add_dim_label("3D")
    plt.savefig(out_path, dpi=200)
    plt.close()


def main() -> None:
    m = float(sp.constants.m_e) if MASS_MODE == "electron" else float(MVAL)
    out = Path(__file__).resolve().parent
    pics = out / "pics"
    pics.mkdir(parents=True, exist_ok=True)
    for fn in (
        "energy_levels.png",
        "energy_vs_n.png",
        "eigenfunctions.png",
        "probability_density_snapshots.png",
        "psi_levels.png",
        "density_levels.png",
        "eigenfunction_n1.png",
        "eigenfunction_n2.png",
        "eigenfunction_n3.png",
        "eigenfunction_n4.png",
    ):
        (pics / fn).unlink(missing_ok=True)

    modes = [
        (nx, ny, nz)
        for nx in range(1, NMAX + 1)
        for ny in range(1, NMAX + 1)
        for nz in range(1, NMAX + 1)
    ]
    modes_sorted = sorted(modes, key=lambda p: ej3(p[0], p[1], p[2], m, L))
    K = len(modes_sorted)
    groups: dict[int, list[tuple[int, int, int]]] = {}
    for nx, ny, nz in modes_sorted:
        S = nx * nx + ny * ny + nz * nz
        groups.setdefault(S, []).append((nx, ny, nz))
    Econst = (sp.constants.hbar**2 * (math.pi**2)) / (2.0 * m * (L**2) * sp.constants.e)
    uniq_S = sorted(groups.keys())
    uniq_E = np.array([Econst * S for S in uniq_S])
    plt.figure(figsize=(7.5, 4.2))
    for S, En in zip(uniq_S, uniq_E):
        states = groups[S]
        plt.hlines(En, 0.8, 1.2, colors="tab:blue")
        sample = ", ".join([f"({a},{b},{c})" for (a, b, c) in states[:3]])
        more = f", … (g={len(states)})" if len(states) > 3 else f"  (g={len(states)})"
        plt.text(1.24, En, sample + more, va="center")
    plt.xlim(0.7, 1.8)
    plt.ylim(0, float(uniq_E[-1]) * 1.1)
    plt.ylabel("Energy (eV)")
    plt.title("Energy levels (3D) — unique energies with degeneracy g")
    plt.xticks([])
    plt.tight_layout()
    add_dim_label("3D")
    plt.savefig(pics / "energy_levels.png", dpi=200)
    plt.close()

    E_sorted = np.array(
        [ej3(nx, ny, nz, m, L) / sp.constants.e for (nx, ny, nz) in modes_sorted]
    )
    plt.figure(figsize=(6, 4))
    plt.plot(np.arange(1, K + 1), E_sorted, marker="o")
    plt.xlabel("mode index k")
    plt.ylabel("Energy (eV)")
    plt.title("Energy vs mode index (3D)")
    plt.tight_layout()
    add_dim_label("3D")
    plt.savefig(pics / "energy_vs_n.png", dpi=200)
    plt.close()

    Nplot = 4
    sel = modes_sorted[:Nplot]
    Ngrid = 250
    x = np.linspace(0, L, Ngrid)
    y = np.linspace(0, L, Ngrid)
    z0 = L * 0.5
    X, Y = np.meshgrid(x, y)
    fig, axs = plt.subplots(2, 2, figsize=(8, 7))
    for ax, (nx, ny, nz) in zip(axs.ravel(), sel):
        Zs = np.full_like(X, z0)
        P = psi3(nx, ny, nz, X, Y, Zs, L)
        ax.imshow(P, extent=[0, L, 0, L], origin="lower", cmap="RdBu")
        ax.set_title(f"ψ z=L/2  ({nx},{ny},{nz})")
        ax.set_xlabel("x (m)")
        ax.set_ylabel("y (m)")
    plt.tight_layout()
    add_dim_label("3D")
    plt.savefig(pics / "eigenfunctions.png", dpi=200)
    plt.close()

    for i, (nx, ny, nz) in enumerate(sel, start=1):
        Zs = np.full_like(X, z0)
        P = psi3(nx, ny, nz, X, Y, Zs, L)
        plt.figure(figsize=(5.5, 4.5))
        plt.imshow(P, extent=[0, L, 0, L], origin="lower", cmap="RdBu")
        plt.xlabel("x (m)")
        plt.ylabel("y (m)")
        plt.title(f"Eigenfunction ψ z=L/2 ({nx},{ny},{nz})")
        plt.tight_layout()
        add_dim_label("3D")
        plt.savefig(pics / f"eigenfunction_n{i}.png", dpi=200)
        plt.close()

    c = np.asarray(COEFFS, dtype=np.complex128)
    c = c / np.sqrt(np.vdot(c, c).real)
    populated = [trip for trip, cc in zip(N_VALS, c) if abs(cc) > 1e-12]
    if len(populated) >= 2:
        (n1x, n1y, n1z), (n2x, n2y, n2z) = populated[0], populated[1]
        w = (ej3(n2x, n2y, n2z, m, L) - ej3(n1x, n1y, n1z, m, L)) / sp.constants.hbar
        T = 2 * math.pi / w
        times = [0.0, 0.25 * T, 0.5 * T]
    else:
        times = [0.0, 1e-15, 2e-15]
    X2, Y2 = X, Y
    Z2 = np.full_like(X2, z0)
    plt.figure(figsize=(9, 3.6))
    for idx, t in enumerate(times, start=1):
        p = np.zeros_like(X2, dtype=np.complex128)
        for cc, (nx, ny, nz) in zip(c, N_VALS):
            p += (
                cc
                * psi3(int(nx), int(ny), int(nz), X2, Y2, Z2, L)
                * np.exp(
                    -1j * ej3(int(nx), int(ny), int(nz), m, L) * t / sp.constants.hbar
                )
            )
        plt.subplot(1, 3, idx)
        plt.imshow(np.abs(p) ** 2, extent=[0, L, 0, L], origin="lower", cmap="viridis")
        plt.title(f"t={t:.2e}s  N={norm_xy(x, y, p):.3f}")
        plt.xlabel("x (m)")
        plt.ylabel("y (m)")
    plt.tight_layout()
    add_dim_label("3D")
    plt.savefig(pics / "probability_density_snapshots.png", dpi=200)
    plt.close()

    E111 = ej3(1, 1, 1, m, L) / sp.constants.e
    E211 = ej3(2, 1, 1, m, L) / sp.constants.e
    print("Particle in a 3D infinite well")
    print(f"L={L:.2e} m, m={m:.4e} kg")
    print(f"E(1,1,1)={E111:.3f} eV, E(2,1,1)={E211:.3f} eV")
    plot_psi_levels(sel, m, L, pics / "psi_levels.png")
    plot_density_levels(sel, m, L, pics / "density_levels.png")
    print(
        "Saved: pics/energy_levels.png, pics/energy_vs_n.png, pics/eigenfunctions.png, pics/probability_density_snapshots.png, pics/psi_levels.png, pics/density_levels.png, "
        "pics/eigenfunction_n1.png, pics/eigenfunction_n2.png, pics/eigenfunction_n3.png, pics/eigenfunction_n4.png"
    )


if __name__ == "__main__":
    main()
