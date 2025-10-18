from __future__ import annotations

import math
from pathlib import Path
import numpy as np
import scipy as sp
from matplotlib import pyplot as plt

L = 1e-9
MASS_MODE = "electron"
MVAL = float(sp.constants.m_e)
NMAX = 6
COEFFS = [1 / np.sqrt(2), 1 / np.sqrt(2)]
N_VALS = [1, 2]

def ej(n: int, m: float, L: float) -> float:
    return (n * math.pi) ** 2 * (sp.constants.hbar**2) / (2.0 * m * (L**2))

def psi(n: int, x: np.ndarray, L: float) -> np.ndarray:
    return np.sqrt(2.0 / L) * np.sin(n * math.pi * x / L)

def norm(x: np.ndarray, psi_arr: np.ndarray) -> float:
    return float(np.trapezoid(np.abs(psi_arr) ** 2, x))


def plot_psi_levels(n_list: list[int], m: float, L: float, out_path: Path) -> None:
    x = np.linspace(0, L, 1000)
    E = np.array([ej(int(n), m, L) / sp.constants.e for n in n_list])
    spc = float(np.min(np.diff(E))) if len(E) > 1 else 1.0
    s = 0.35 * spc
    plt.figure(figsize=(6, 8))
    for n, En in zip(n_list, E):
        y = En + s * psi(int(n), x, L)
        plt.plot(x, y, color="tab:blue")
        plt.hlines(En, x[0], x[-1], colors="tab:blue", linestyles="dashed", alpha=0.6)
        plt.text(L * 1.02, En, f"n={n}", va="center")
    plt.xlim(0, L)
    plt.ylim(E.min() - spc * 0.6, E.max() + spc * 0.6)
    plt.xlabel("x (m)")
    plt.ylabel("Energy (eV)")
    plt.title("Eigenfunctions at energy levels")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()

def plot_density_levels(n_list: list[int], m: float, L: float, out_path: Path) -> None:
    x = np.linspace(0, L, 1000)
    E = np.array([ej(int(n), m, L) / sp.constants.e for n in n_list])
    spc = float(np.min(np.diff(E))) if len(E) > 1 else 1.0
    plt.figure(figsize=(6, 8))
    for n, En in zip(n_list, E):
        r = np.abs(psi(int(n), x, L)) ** 2
        a = (0.6 * spc) / float(r.max())
        y = En + a * r
        plt.plot(x, y, color="tab:blue")
        plt.hlines(En, x[0], x[-1], colors="tab:blue", linestyles="dashed", alpha=0.6)
        plt.text(L * 1.02, En, f"n={n}", va="center")
    plt.xlim(0, L)
    plt.ylim(E.min() - spc * 0.6, E.max() + spc * 0.6)
    plt.xlabel("x (m)")
    plt.ylabel("Energy (eV)")
    plt.title("Densities at energy levels")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()

def main() -> None:
    m = float(sp.constants.m_e) if MASS_MODE == "electron" else float(MVAL)
    out = Path(__file__).resolve().parent; pics = out / "pics"; pics.mkdir(parents=True, exist_ok=True)
    for fn in ("energy_levels.png", "energy_vs_n.png", "eigenfunctions.png", "probability_density_snapshots.png", "psi_levels.png", "density_levels.png",
               "eigenfunction_n1.png", "eigenfunction_n2.png", "eigenfunction_n3.png", "eigenfunction_n4.png"):
        (pics / fn).unlink(missing_ok=True)

    n = np.arange(1, max(1, NMAX) + 1)
    E = np.array([ej(int(k), m, L) / sp.constants.e for k in n])
    plt.figure(figsize=(6, 4))
    for k, Ek in zip(n, E):
        plt.hlines(Ek, 0.8, 1.2, colors="tab:blue"); plt.text(1.22, Ek, f"n={int(k)}", va="center")
    plt.xlim(0.7, 1.45); plt.ylim(0, E[-1] * 1.1); plt.ylabel("Energy (eV)"); plt.title("Energy levels (1D infinite well)"); plt.xticks([]); plt.tight_layout(); plt.savefig(pics / "energy_levels.png", dpi=200); plt.close()

    plt.figure(figsize=(6, 4))
    plt.plot(n, E, marker="o")
    plt.xlabel("n"); plt.ylabel("Energy (eV)"); plt.title("Energy vs n (1D infinite well)"); plt.tight_layout(); plt.savefig(pics / "energy_vs_n.png", dpi=200); plt.close()

    x = np.linspace(0, L, 1000)
    plt.figure(figsize=(7, 4))
    for k in [1, 2, 3, 4]:
        plt.plot(x, psi(int(k), x, L), label=f"n={k}")
    plt.xlabel("x (m)"); plt.ylabel("psi_n(x)"); plt.title("Eigenfunctions ψn(x)"); plt.legend(); plt.tight_layout(); plt.savefig(pics / "eigenfunctions.png", dpi=200); plt.close()

    for k in [1, 2, 3, 4]:
        plt.figure(figsize=(6, 3.5))
        plt.plot(x, psi(int(k), x, L), color="tab:blue")
        plt.xlabel("x (m)"); plt.ylabel("ψ(x)"); plt.title(f"Eigenfunction ψ for n={k}"); plt.tight_layout(); plt.savefig(pics / f"eigenfunction_n{k}.png", dpi=200); plt.close()

    c = np.asarray(COEFFS, dtype=np.complex128); c = c / np.sqrt(np.vdot(c, c).real)
    populated = [n for n, cc in zip(N_VALS, c) if abs(cc) > 1e-12]
    if len(populated) >= 2:
        n1, n2 = populated[0], populated[1]
        w = (ej(n2, m, L) - ej(n1, m, L)) / sp.constants.hbar
        T = 2 * math.pi / w; times = [0.0, 0.25 * T, 0.5 * T]
    else:
        times = [0.0, 1e-15, 2e-15]
    x2 = np.linspace(0, L, 2000)
    plt.figure(figsize=(7, 4.5))
    for t in times:
        p = np.zeros_like(x2, dtype=np.complex128)
        for cc, n in zip(c, N_VALS):
            p += cc * psi(int(n), x2, L) * np.exp(-1j * ej(int(n), m, L) * t / sp.constants.hbar)
        plt.plot(x2, np.abs(p) ** 2, label=f"t={t:.2e}s  N={norm(x2, p):.3f}")
    plt.xlabel("x (m)"); plt.ylabel("|psi|^2"); plt.title("Probability density snapshots"); plt.legend(); plt.tight_layout(); plt.savefig(pics / "probability_density_snapshots.png", dpi=200); plt.close()

    E1, E2 = ej(1, m, L) / sp.constants.e, ej(2, m, L) / sp.constants.e
    print("Particle in a 1D infinite well"); print(f"L={L:.2e} m, m={m:.4e} kg"); print(f"E1={E1:.3f} eV, E2={E2:.3f} eV, E2/E1={E2/E1:.2f}")
    plot_psi_levels([1, 2, 3, 4], m, L, pics / "psi_levels.png")
    plot_density_levels([1, 2, 3, 4], m, L, pics / "density_levels.png")
    print("Saved: pics/energy_levels.png, pics/energy_vs_n.png, pics/eigenfunctions.png, pics/probability_density_snapshots.png, pics/psi_levels.png, pics/density_levels.png, "
        "pics/eigenfunction_n1.png, pics/eigenfunction_n2.png, pics/eigenfunction_n3.png, pics/eigenfunction_n4.png")

    

if __name__ == "__main__":
    main()

print("Executing 1D version...")