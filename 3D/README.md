# 3D Infinite Potential Well (Cubic Box)

[Back to root README](../../README.md) · [1D](../1D/README.md) · [2D](../2D/README.md)

## Background

In a cubic domain 0 ≤ x ≤ L, 0 ≤ y ≤ L, 0 ≤ z ≤ L, variables separate and the normalized eigenfunctions are

$$\psi_{n_x,n_y,n_z}(x,y,z) = \left(\frac{2}{L}\right)^{3/2} \sin\left(\frac{n_x\pi x}{L}\right) \sin\left(\frac{n_y\pi y}{L}\right) \sin\left(\frac{n_z\pi z}{L}\right),\quad n_x,n_y,n_z=1,2,\dots$$

with energies

$$E_{n_x,n_y,n_z} = \frac{\pi^2\hbar^2}{2 m L^2}\,(n_x^2 + n_y^2 + n_z^2).$$

Degeneracies are common because many triples can share the same sum n_x²+n_y²+n_z².

## Usage

From the repository root or from this folder:

```bash
python "particle in a box/3D/main.py"
```

Outputs are saved in `pics/`.

## Parameters (edit at the top of `main.py`)

- `L` (float, m): box width (default 1e-9)
- `MASS_MODE` ("electron"|other): if "electron", uses electron mass; otherwise `MVAL`
- `MVAL` (float, kg): custom mass (used when `MASS_MODE` != "electron")
- `NMAX` (int): max index for enumerating modes along each axis
- `COEFFS` (list[complex]): coefficients for time‑evolving superposition
- `N_VALS` (list[tuple[int,int,int]]): corresponding (n_x, n_y, n_z) triplets for `COEFFS`

## Generated figures (in `pics/`)

- `energy_levels.png` — level diagram (grouped by unique energies with degeneracies)
- `energy_vs_n.png` — energy vs mode index
- `eigenfunctions.png` — heatmaps of ψ on the z=L/2 slice for selected modes
- `eigenfunction_n{1..4}.png` — individual eigenfunction heatmaps on z=L/2
- `psi_levels.png` — level diagram with ψ slices (y=z=L/2)
- `density_levels.png` — level diagram with |ψ|² slices (y=z=L/2)
- `probability_density_snapshots.png` — time snapshots of |Ψ(x,y,z=L/2,t)|² for the configured superposition

## Notes

- Energies depend on n_x²+n_y²+n_z²; degeneracy grows with the number of partitions of the sum.
- For visualizations, 2D slices (e.g., z=L/2) are used to show structure.

[Back to root README](../../README.md)
