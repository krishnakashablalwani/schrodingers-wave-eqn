import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy import constants
from scipy.integrate import quad
import csv
import os


hbar = constants.hbar
m = constants.m_e
L = 1 * 10 ** (-9)
N = 500
energy_end = 50
print("hbar:", hbar)
print("mass of electron", m)

CANVAS_WIDTH = 1600
CANVAS_HEIGHT = 800
NUM_DOTS = 100000

x = np.linspace(0, L, N)


def psi(n, x):
    return np.sqrt(2 / L) * np.sin(n * np.pi * x / L)

print("psi(1, L/2):", psi(1, L/2))


def energy(n):
    return (n**2 * np.pi**2 * hbar**2) / (2 * m * L**2)

print("energy(1):", energy(1))


def psi_squared(n, x):
    if n == 0:
        return np.zeros_like(x)
    return (2 / L) * (np.sin(n * np.pi * x / L)) ** 2

print("psi_squared(1, L/2):", psi_squared(1, L/2))


c1 = 1 / np.sqrt(2)
c2 = 1 / np.sqrt(2)

psi1 = psi(1, x)
psi2 = psi(2, x)
E1 = energy(1)
E2 = energy(2)

fig, ax = plt.subplots()

max_amplitude = 2 / np.sqrt(L)

ax.set_xlim(0, L)
ax.set_ylim(-1.2 * max_amplitude, 1.2 * max_amplitude)
ax.set_xlabel("Position (x) [meters]")
ax.set_ylabel("Amplitude / Probability / Energy")
ax.set_title("Particle in a 1nm Box: Superposition of n=1 and n=2 States")
ax.grid(True, linestyle="--", alpha=0.6)

E1_scaled = 0.25 * max_amplitude
E2_scaled = 0.5 * max_amplitude
ax.axhline(y=E1_scaled, color="k", linestyle=":", lw=1.5, label=f"Energy E1 (scaled)")
ax.axhline(y=E2_scaled, color="k", linestyle="--", lw=1.5, label=f"Energy E2 (scaled)")

(line_real,) = ax.plot([], [], "b-", lw=2, label="Re(Ψ)")
(line_imag,) = ax.plot([], [], "r-", lw=2, label="Im(Ψ)")
fill_prob = ax.fill_between(x, 0, color="g", alpha=0.4, label="|Ψ|² (Electron Cloud)")
ax.legend()


def animate(t):
    term1 = c1 * psi1 * np.exp(-1j * E1 * t / hbar)
    term2 = c2 * psi2 * np.exp(-1j * E2 * t / hbar)
    psi_t = term1 + term2

    real_part = np.real(psi_t)
    imag_part = np.imag(psi_t)

    prob_density = np.abs(psi_t) ** 2

    line_real.set_data(x, real_part)
    line_imag.set_data(x, imag_part)

    verts = np.vstack([x, prob_density]).T
    fill_prob.set_paths([np.vstack([[x[0], 0], verts, [x[-1], 0]])])

    return line_real, line_imag, fill_prob


time_steps = np.linspace(0, 5e-15, 300)
ani = FuncAnimation(fig, animate, frames=time_steps, interval=20, blit=True)


def save_animation_data(filename="animation_data.csv"):
    """Calculates and saves all data points from the animation to a CSV file."""
    filepath = os.path.join("csv", filename)
    print(f"Saving animation data to {filepath}...")
    with open(filepath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "time",
                "x_position",
                "real_part",
                "imaginary_part",
                "probability_density",
            ]
        )

        for t in time_steps:
            term1 = c1 * psi1 * np.exp(-1j * E1 * t / hbar)
            term2 = c2 * psi2 * np.exp(-1j * E2 * t / hbar)
            psi_t = term1 + term2

            real_part = np.real(psi_t)
            imag_part = np.imag(psi_t)
            prob_density = np.abs(psi_t) ** 2

            for i in range(len(x)):
                writer.writerow(
                    [t, x[i], real_part[i], imag_part[i], prob_density[i]]
                )
    print("Finished saving animation data.")


def update_visualization(n_str, canvas, n_label):
    try:
        n = int(n_str)
        if n < 1:
            raise ValueError("Energy level must be a positive integer.")
    except ValueError:
        n_label.config(text="Invalid input")
        return

    n_label.config(text=f"Energy Level (n): {n}")
    canvas.delete("all")

    # --- Save electron cloud data to a CSV file ---
    filename = f"electron_cloud_n_{n}.csv"
    filepath = os.path.join("csv", filename)
    print(f"Saving electron cloud data to {filepath}...")
    with open(filepath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["x_position", "y_position"])  # Write header

        canvas.create_line(
            0, CANVAS_HEIGHT - 20, CANVAS_WIDTH, CANVAS_HEIGHT - 20, fill="gray"
        )
        canvas.create_text(
            CANVAS_WIDTH / 2, CANVAS_HEIGHT - 10, text="Position in Box", fill="white"
        )
        canvas.create_text(
            CANVAS_WIDTH / 2,
            20,
            text="|Ψ|² (Probability Density)",
            fill="white",
            font=("Arial", 14),
        )
        max_prob = 2 / L
        dots_plotted = 0
        for _ in range(NUM_DOTS):
            x_rand = np.random.uniform(0, L)
            y_rand = np.random.uniform(0, max_prob)
            prob_at_x = psi_squared(n, x_rand)
            if y_rand < prob_at_x:
                # A dot is valid, save its coordinates
                writer.writerow([x_rand, y_rand])
                dots_plotted += 1

                # Draw the dot on the canvas
                canvas_x = (x_rand / L) * CANVAS_WIDTH
                canvas_y = (
                    CANVAS_HEIGHT - 25 - (y_rand / max_prob) * (CANVAS_HEIGHT * 0.8)
                )
                canvas.create_oval(
                    canvas_x - 1, canvas_y - 1, canvas_x + 1, canvas_y + 1, fill="white"
                )
    print(f"Finished saving. Plotted and saved {dots_plotted} dots.")


def setup_electron_cloud_window():
    root = tk.Tk()
    root.title("Electron Cloud Visualization")
    main_frame = tk.Frame(root)
    main_frame.pack(padx=10, pady=10)
    canvas = tk.Canvas(
        main_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black"
    )
    canvas.pack()
    control_frame = tk.Frame(main_frame)
    control_frame.pack(pady=5)
    n_label = tk.Label(
        control_frame, text="Energy Level (n): 1", font=("Arial", 12)
    )
    n_label.pack(side=tk.LEFT, padx=10)

    n_entry = tk.Entry(control_frame, width=10)
    n_entry.insert(0, "1")
    n_entry.pack(side=tk.LEFT)

    update_btn = tk.Button(
        control_frame,
        text="Update",
        command=lambda: update_visualization(n_entry.get(), canvas, n_label),
    )
    update_btn.pack(side=tk.LEFT, padx=5)

    # Bind the Enter key to the update function
    root.bind('<Return>', lambda event: update_visualization(n_entry.get(), canvas, n_label))

    update_visualization(n_entry.get(), canvas, n_label)
    return root


if __name__ == "__main__":
    # Create a folder for CSV output if it doesn't exist
    if not os.path.exists("csv"):
        os.makedirs("csv")

    # Save the data for the animated plot to a CSV file
    save_animation_data()

    total_probability, error_estimate = quad(lambda x: psi_squared(1, x), 0, L)
    electron_cloud_window = setup_electron_cloud_window()
    electron_cloud_window.mainloop()

plt.show()
