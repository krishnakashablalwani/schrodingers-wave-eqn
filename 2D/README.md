# 2D Infinite Potential Well (Square Box)

[Back to root README](../../README.md) · [1D](../1D/README.md) · [3D](../3D/README.md)

## Background

On a square domain 0 ≤ x ≤ L, 0 ≤ y ≤ L, variables separate and the normalized eigenfunctions are

$$\psi_{n_x,n_y}(x,y) = \frac{2}{L} \sin\left(\frac{n_x\pi x}{L}\right) \sin\left(\frac{n_y\pi y}{L}\right),\quad n_x,n_y=1,2,\dots$$

with energies

$$E_{n_x,n_y} = \frac{\pi^2\hbar^2}{2 m L^2}\,(n_x^2 + n_y^2).$$

Degeneracies occur when different pairs (n_x, n_y) yield the same sum n_x²+n_y².

## Usage

From the repository root or from this folder:

```bash
python "particle in a box/2D/main.py"
```

Outputs are saved in `pics/`.

## Parameters (edit at the top of `main.py`)

- `L` (float, m): box width (default 1e-9)
- `MASS_MODE` ("electron"|other): if "electron", uses electron mass; otherwise `MVAL`
- `MVAL` (float, kg): custom mass (used when `MASS_MODE` != "electron")
- `NMAX` (int): max index for enumerating modes along each axis
- `COEFFS` (list[complex]): coefficients for time‑evolving superposition
- `N_VALS` (list[tuple[int,int]]): corresponding (n_x, n_y) pairs for `COEFFS`

## Generated figures (in `pics/`)

- `energy_levels.png` — stacked level diagram labeled by (n_x, n_y)
- `energy_vs_n.png` — energy vs mode index
- `eigenfunctions.png` — heatmaps of ψ at selected modes
- `eigenfunction_n{1..4}.png` — individual eigenfunction heatmaps
- `psi_levels.png` — level diagram with ψ slices (y=L/2)
- `density_levels.png` — level diagram with |ψ|² slices (y=L/2)
- `probability_density_snapshots.png` — time snapshots of |Ψ(x,y,t)|² for the configured superposition

## Notes

- Energies depend on the sum n_x²+n_y²; multiple modes can share the same energy (degeneracy).
- Visualizations often use a fixed y or x slice for level overlays.

[Back to root README](../../README.md)
