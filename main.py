import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy import constants
from scipy.integrate import quad


hbar = constants.hbar
m = constants.m_e
L = 1 * 10 ** (-9)
N = 500
energy_end = 5

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 400
NUM_DOTS = 25000

x = np.linspace(0, L, N)


def psi(n, x):
    return np.sqrt(2 / L) * np.sin(n * np.pi * x / L)


def energy(n):
    return (n**2 * np.pi**2 * hbar**2) / (2 * m * L**2)


def psi_squared(n, x):
    if n == 0:
        return np.zeros_like(x)
    return (2 / L) * (np.sin(n * np.pi * x / L)) ** 2


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


class ElectronCloudApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Electron Cloud Visualization")
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)
        self.canvas = tk.Canvas(
            self.main_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black"
        )
        self.canvas.pack()
        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack(pady=5)
        self.n_label = tk.Label(
            self.control_frame, text="Energy Level (n): 1", font=("Arial", 12)
        )
        self.n_label.pack(side=tk.LEFT, padx=10)
        self.n_slider = tk.Scale(
            self.control_frame,
            from_=1,
            to=energy_end,
            orient=tk.HORIZONTAL,
            length=300,
            command=self.update_visualization,
        )
        self.n_slider.set(1)
        self.n_slider.pack(side=tk.LEFT)
        self.update_visualization(self.n_slider.get())

    def update_visualization(self, n_str):
        n = int(n_str)
        self.n_label.config(text=f"Energy Level (n): {n}")
        self.canvas.delete("all")

        self.canvas.create_line(
            0, CANVAS_HEIGHT - 20, CANVAS_WIDTH, CANVAS_HEIGHT - 20, fill="gray"
        )
        self.canvas.create_text(
            CANVAS_WIDTH / 2, CANVAS_HEIGHT - 10, text="Position in Box", fill="white"
        )
        self.canvas.create_text(
            CANVAS_WIDTH / 2,
            20,
            text="|Ψ|² (Probability Density)",
            fill="white",
            font=("Arial", 14),
        )
        max_prob = 2 / L
        for _ in range(NUM_DOTS):
            x_rand = np.random.uniform(0, L)
            y_rand = np.random.uniform(0, max_prob)
            prob_at_x = psi_squared(n, x_rand)
            if y_rand < prob_at_x:
                canvas_x = (x_rand / L) * CANVAS_WIDTH
                canvas_y = (
                    CANVAS_HEIGHT - 25 - (y_rand / max_prob) * (CANVAS_HEIGHT * 0.8)
                )
                self.canvas.create_oval(
                    canvas_x - 1,
                    canvas_y - 1,
                    canvas_x + 1,
                    canvas_y + 1,
                    fill="red",
                    outline="",
                )


if __name__ == "__main__":
    total_probability, error_estimate = quad(lambda x: psi_squared(1, x), 0, L)
    root = tk.Tk()
    app = ElectronCloudApp(root)
    root.mainloop()

plt.show()
