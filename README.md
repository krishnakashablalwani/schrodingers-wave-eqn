# Electron in a 1D Box — Electron Cloud Visualization

This project visualizes the probability density |Ψ|^2 of an electron in a 1D infinite potential well (“particle in a box”). It uses a Tkinter window to draw a “cloud” of dots where the electron is most likely to be found for a chosen energy level n.

## What it shows

- A black window with a white “electron cloud.” Denser regions = higher probability.
- A text box to enter an integer energy level n (1, 2, 3, …). Click Update or press Enter to redraw.
- Console prints of constants and a normalization check.

## Controls

- Energy level input: type a positive integer (n ≥ 1).
- Update: button or Enter key.
- The label shows “Invalid input” if the entry is not a positive integer.

## What prints in the terminal

- hbar (ħ), electron mass m.
- psi(1, L/2), energy(1), psi_squared(1, L/2).
- Integral of |Ψ|^2 over [0, L] for n=1 (should be = 1), computed with scipy.integrate.quad.

## Physics background (formulas with sources)

- Wavefunction (stationary state n):
  - Ψₙ(x) = √(2/L) · sin(nπx/L)
  - Source: “Particle in a box,” standard solution to the time‑independent Schrödinger equation (see Wikipedia: https://en.wikipedia.org/wiki/Particle_in_a_box)
- Energy levels:
  - Eₙ = (n^2 π^2 ħ^2) / (2 m L^2)
  - Source: same as above.
- Probability density:
  - |Ψₙ(x)|^2 = (2/L) · sin^2(nπx/L)
  - Source: Born rule (probability = |Ψ|^2).

Example calculations (use radians calc!!!!!!!!!!!):

- Constants (from SciPy):
  - hbar = 1.054571817×10^-34 J·s
  - m (electron) = 9.1093837015×10^-31 kg
- Given L = 1×10^-9 m:
  - psi(1, L/2) = √(2/L)·sin(π/2) = √(2/1e-9) = 44721.36
  - energy(1) = (π^2 ħ^2)/(2 m L^2)
    = (9.8696 × 1.1121×10^-68) / (2 × 9.1094×10^-31 × 1×10^-18)
    = 6.02×10^-20 J
  - psi_squared(1, L/2) = (2/L)·sin^2(π/2) = 2/1e-9 = 2×10^9 m^-1

## How the code works (main pieces)

- Constants and grid:
  - hbar, m from scipy.constants; L (box length), N (points), x = linspace(0, L, N).
- psi(n, x):
  - Implements Ψₙ(x) = √(2/L)·sin(nπx/L).
- energy(n):
  - Implements Eₙ = (n^2 π^2 ħ^2)/(2 m L^2).
- psi_squared(n, x):
  - Returns (2/L)·sin^2(nπx/L). If n == 0, returns zeros.
- update_visualization(n_str, canvas, n_label, root):
  - Parses n; updates label; clears canvas.
  - Draws axis labels.
  - Rejection sampling to draw the cloud:
    - Repeat NUM_DOTS times:
      - Pick random x_rand in [0, L] and y_rand in [0, 2/L].
  - Compute p = |Ψₙ(x_rand)|^2.
    - If y_rand < p, draw a white dot.
  - Result: more dots where probability is high.
- setup_electron_cloud_window():
  - Creates Tk window, canvas, controls (Entry + Update button), and bindings (Enter key).

## Tuning and performance

- NUM_DOTS: Higher → smoother cloud but slower (default 100,000). Reduce if it lags (e.g., 30,000).
- CANVAS_WIDTH/HEIGHT: Resize the visualization window.
- L: Box length in meters (affects scales and energies).
- N: Spatial resolution for calculations (not directly used in dot drawing).

## Common issues

- Module not found:
  - py -m pip install numpy scipy
- Window not showing:
  - Ensure you run: py main.py from the project folder.
- Slow redraw:
  - Lower NUM_DOTS.

## References

- Particle in a box: https://en.wikipedia.org/wiki/Particle_in_a_box
- Born rule: https://en.wikipedia.org/wiki/Born_rule
- SciPy constants: https://docs.scipy.org/doc/scipy/reference/constants.html
- SciPy quad: https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.quad.html
