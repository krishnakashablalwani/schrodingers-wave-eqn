import tkinter as tk
import numpy as np
from scipy import constants
from scipy.integrate import quad

# these are constants
hbar = constants.hbar  # reduced Planck's constant, h/2pi
m = constants.m_e  # mass of electron
L = 1 * 10 ** (-9)  # length of box in meters
N = 500  # number of points in space
energy_end = 50
print("hbar:", hbar)
print("mass of electron", m)

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
NUM_DOTS = 100000  # number of dots for cloud

x = np.linspace(0, L, N)


# psi
def psi(n, x):
    return np.sqrt(2 / L) * np.sin(n * np.pi * x / L)


print("psi(1, L/2):", psi(1, L / 2))


# energy of n
def energy(n):
    return (n**2 * np.pi**2 * hbar**2) / (2 * m * L**2)


print("energy(1):", energy(1))


# probability of electron
def psi_squared(n, x):
    if n == 0:
        return np.zeros_like(x)
    return (2 / L) * (np.sin(n * np.pi * x / L)) ** 2


print("psi_squared(1, L/2):", psi_squared(1, L / 2))


# interactive electron cloud visualization
def update_visualization(n_str, canvas, n_label, root):
    try:
        n = int(n_str)
        if n < 1:
            raise ValueError("Energy level must be a positive integer.")
    except ValueError:
        n_label.config(text="Invalid input")
        return

    n_label.config(text=f"Energy Level (n): {n}")
    canvas.delete("all")

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
            dots_plotted += 1
            canvas_x = (x_rand / L) * CANVAS_WIDTH
            canvas_y = CANVAS_HEIGHT - 25 - (y_rand / max_prob) * (CANVAS_HEIGHT * 0.8)
            canvas.create_oval(
                canvas_x - 1, canvas_y - 1, canvas_x + 1, canvas_y + 1, fill="white"
            )

    print(f"Finished plotting {dots_plotted} dots.")


# set up tkinter window
def setup_electron_cloud_window():
    root = tk.Tk()
    root.title("Electron Cloud Visualization")

    main_frame = tk.Frame(root)
    main_frame.pack(padx=10, pady=10)

    canvas = tk.Canvas(main_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black")
    canvas.pack()

    control_frame = tk.Frame(main_frame)
    control_frame.pack(pady=5)

    n_label = tk.Label(control_frame, text="Energy Level (n): 1", font=("Arial", 12))
    n_label.pack(side=tk.LEFT, padx=10)

    n_entry = tk.Entry(control_frame, width=10)
    n_entry.insert(0, "1")
    n_entry.pack(side=tk.LEFT)

    update_btn = tk.Button(
        control_frame,
        text="Update",
        command=lambda: update_visualization(n_entry.get(), canvas, n_label, root),
    )
    update_btn.pack(side=tk.LEFT, padx=5)

    root.bind(
        "<Return>",
        lambda event: update_visualization(n_entry.get(), canvas, n_label, root),
    )

    # initial render
    update_visualization(n_entry.get(), canvas, n_label, root)

    return root


if __name__ == "__main__":
    # optional check of normalization for n=1
    total_probability, error_estimate = quad(lambda xx: psi_squared(1, xx), 0, L)
    print(
        f"Integral of |Psi|^2 over [0, L] for n=1: {total_probability:.6f} (±{error_estimate:.1e})"
    )

    # start Tk window only
    root = setup_electron_cloud_window()
    root.mainloop()
