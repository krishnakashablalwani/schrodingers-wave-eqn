# 1D Infinite Potential Well (Particle in a Box)

[Back to root README](../../README.md) · [2D](../2D/README.md) · [3D](../3D/README.md)

## Background

For a 1D infinite square well on 0 ≤ x ≤ L, the time‑independent Schrödinger equation yields normalized eigenfunctions

$$\psi_n(x) = \sqrt{\frac{2}{L}}\,\sin\left(\frac{n\pi x}{L}\right),\quad n=1,2,3,\dots$$

with energy spectrum

$$E_n = \frac{n^2\pi^2\hbar^2}{2 m L^2}.$$

These form a complete orthonormal set. Superpositions evolve as

$$\Psi(x,t) = \sum_n c_n\,\psi_n(x)\,e^{-i E_n t/\hbar},\quad \sum_n |c_n|^2 = 1.$$

## Usage

From the repository root or from this folder:

```bash
python "particle in a box/1D/main.py"
```

Outputs are saved in `pics/`.

## Parameters (edit at the top of `main.py`)

- `L` (float, m): box width (default 1e-9)
- `MASS_MODE` ("electron"|other): if "electron", uses electron mass; otherwise `MVAL`
- `MVAL` (float, kg): custom mass (used when `MASS_MODE` != "electron")
- `NMAX` (int): number of levels to include in plots
- `COEFFS` (list[complex]): coefficients for time‑evolving superposition
- `N_VALS` (list[int]): corresponding quantum numbers for `COEFFS`

## Generated figures (in `pics/`)

- `energy_levels.png` — horizontal level diagram labeled by n
- `energy_vs_n.png` — E vs n
- `eigenfunctions.png` — ψₙ(x) for n=1..4
- `eigenfunction_n{1..4}.png` — individual eigenfunction plots
- `psi_levels.png` — level diagram with eigenfunction slices
- `density_levels.png` — level diagram with |ψ|² slices
- `probability_density_snapshots.png` — time snapshots for the configured superposition

## Notes

- Energies scale as n² and 1/L². Halving L raises all energy levels by 4×.
- Probability density nodes occur where sin(nπx/L)=0.

[Back to root README](../../README.md)
