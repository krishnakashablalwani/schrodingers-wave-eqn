Schrödinger’s Wave Equation — Particle in a Box (1D/2D) + Interactive Electron Cloud

## Overview

This repository contains small, focused Python tools to explore the time‑independent Schrödinger equation for an infinite potential well (aka the “particle in a box”). It includes:

- An interactive Tkinter app that visualizes the electron probability cloud for a chosen quantum number n in a 1D infinite well using rejection sampling from |Ψ|² (`main.py`).
- Reproducible scripts that generate figures for 1D and 2D infinite wells (energy spectra, eigenfunctions, and probability densities), saving images into `pics/`.

The code is small and hackable—ideal for learning, teaching, and making quick visualizations.

## Math background (quick reference)

For an infinite square well of length L (0 ≤ x ≤ L) in 1D, the stationary states are

$$\psi_n(x) = \sqrt{\frac{2}{L}}\, \sin\left(\frac{n\pi x}{L}\right), \quad n = 1,2,3,\dots$$

with energies

$$E_n = \frac{n^2\pi^2\hbar^2}{2 m L^2}.$$

In 2D on a square domain 0 ≤ x ≤ L, 0 ≤ y ≤ L, the eigenstates and energies separate as

$$
\psi_{n_x,n_y}(x,y) = \frac{2}{L} \sin\left(\frac{n_x\pi x}{L}\right) \sin\left(\frac{n_y\pi y}{L}\right), \quad
E_{n_x,n_y} = \frac{\pi^2\hbar^2}{2 m L^2} (n_x^2 + n_y^2).
$$

The interactive “electron cloud” view draws random points under the curve of |Ψ|² via rejection sampling to convey the relative probability density.

## Project structure

```
main.py                     # Tkinter-based interactive electron cloud for 1D well
README.md                   # You are here
requirements.txt            # Python dependencies for the whole repo
particle in a box/
	requirements.txt          # Minimal deps for plotting scripts
	1D/
		main.py                 # Generates 1D figures into pics/
		pics/                   # Output images (created at runtime)
	2D/
		main.py                 # Generates 2D figures into pics/
		pics/                   # Output images (created at runtime)
```

## Requirements

- Python 3.9+ (3.10 or newer recommended)
- Packages: `numpy`, `scipy`, `matplotlib`
- Tkinter (ships with the standard CPython installers on Windows/macOS; on some Linux distros you may need to install it via your package manager, e.g. `sudo apt-get install python3-tk`).

Install using the root `requirements.txt`:

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows Git Bash
pip install -r requirements.txt
```

Tip: If you use Command Prompt or PowerShell on Windows, the activation command is slightly different (e.g., `.venv\Scripts\activate` for cmd.exe or `.
venv\Scripts\Activate.ps1` for PowerShell).

## How to run

### 1) Interactive electron cloud (Tkinter)

- From the repository root:

```bash
python main.py
```

What you’ll see:

- A black canvas where white dots are drawn according to |Ψ|² for the selected quantum number n.
- An input for n; press Enter or click Update to redraw. For large n, you’ll see more nodes (zeros) where the cloud thins out.

Config knobs in `main.py` you can tweak:

- `L`: Well width in meters (default 1e-9).
- `N`: Spatial discretization for plotting/math (doesn’t affect sampling quality much).
- `NUM_DOTS`: Number of rejection-sampled points. Larger = smoother but slower.
- `CANVAS_WIDTH`, `CANVAS_HEIGHT`: Visualization size.

### 2) 1D figures (energy levels, eigenfunctions, densities)

```bash
python "particle in a box/1D/main.py"
```

This will print a short summary and write several images into `particle in a box/1D/pics/`, including:

- `energy_levels.png` — horizontal lines labeled by n
- `energy_vs_n.png` — E vs n
- `eigenfunctions.png` — ψₙ(x) overlayed for n = 1..4
- `eigenfunction_n{1..4}.png` — individual eigenfunction plots
- `psi_levels.png` — level diagram with eigenfunction slices
- `density_levels.png` — level diagram with |ψ|² slices
- `probability_density_snapshots.png` — time snapshots for a 2-state superposition specified by `COEFFS` and `N_VALS`

Parameters at the top of the script control well size (`L`), mass (`MASS_MODE`/`MVAL`), how many levels to show (`NMAX`), and the superposition (`COEFFS`, `N_VALS`).

### 3) 2D figures (modes on a square well)

```bash
python "particle in a box/2D/main.py"
```

This writes analogous images into `particle in a box/2D/pics/`, e.g. 2D eigenfunctions as imshow heatmaps, energy stacks, and time-snapshot densities for a 2-mode superposition.

## Troubleshooting

- SciPy installation on Windows: use a recent Python (3.10+) and pip; if you hit build errors, upgrade pip and wheel (`pip install -U pip wheel`) or use a Python distribution that ships SciPy wheels.
- Tkinter missing (mostly Linux): install your distro’s Tk package, e.g. `sudo apt-get install python3-tk`.
- Canvas feels slow: reduce `NUM_DOTS` in `main.py` (e.g., from 100000 → 20000) or shrink the canvas size.
- No images appear in `pics/`: ensure the script has permission to create directories/files in those folders.

## Notes and limitations

- The well is “infinite” (hard walls). Finite wells require different boundary conditions and are not modeled here.
- The interactive app uses rejection sampling to produce visually intuitive dot clouds; it’s stochastic and not a line plot of |Ψ|².
- Time evolution in the 1D/2D scripts is limited to simple, user‑defined superpositions to illustrate interference and beat periods.

## Contributing

Issues and PRs are welcome. Ideas that would be great additions:

- Add an option to animate time evolution (matplotlib FuncAnimation or Tkinter loop).
- Add a finite well or harmonic oscillator example for comparison.
- Export figures at publication resolution with consistent style.

## Acknowledgments

- Physical constants from `scipy.constants`.
- Visualization built with Tkinter and Matplotlib; numerics with NumPy and SciPy.

## License

This project is licensed under the MIT License. See the [`LICENSE`](./LICENSE) file for details.
