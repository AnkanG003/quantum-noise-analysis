from qiskit_aer import Aer
from qiskit import transpile

from src.circuits import create_hadamard_circuit, create_bell_circuit
from src.noise_models import get_depolarizing_noise


SHOTS = 20000

simulator = Aer.get_backend('aer_simulator')

noise_levels = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3]


# ---------- Hadamard ----------
qc_h = create_hadamard_circuit()
compiled_h = transpile(qc_h, simulator)

hadamard_errors = []

for noise in noise_levels:
    noise_model = get_depolarizing_noise(noise)

    result = simulator.run(
        compiled_h,
        shots=SHOTS,
        noise_model=noise_model
    ).result()

    counts = result.get_counts()
    zero_count = counts.get('0', 0)

    ideal = SHOTS / 2
    error = abs(ideal - zero_count) / SHOTS

    hadamard_errors.append(error)


# ---------- Bell ----------
qc_b = create_bell_circuit()
compiled_b = transpile(qc_b, simulator)

bell_errors = []

for noise in noise_levels:
    noise_model = get_depolarizing_noise(noise)

    result = simulator.run(
        compiled_b,
        shots=SHOTS,
        noise_model=noise_model
    ).result()

    counts = result.get_counts()

    correct = counts.get('00', 0) + counts.get('11', 0)

    ideal = SHOTS
    error = (ideal - correct) / SHOTS

    bell_errors.append(error)


# ---------- Plot ----------
import matplotlib.pyplot as plt

plt.plot(noise_levels, hadamard_errors, marker='o', label='Hadamard Circuit')
plt.plot(noise_levels, bell_errors, marker='o', label='Bell Circuit')

plt.xlabel("Noise Level")
plt.ylabel("Error")
plt.title("Noise vs Error Comparison")
plt.legend()
plt.grid()

plt.show()