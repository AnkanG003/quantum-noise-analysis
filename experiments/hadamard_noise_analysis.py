from qiskit_aer import Aer
from qiskit import transpile

from src.circuits import create_hadamard_circuit
from src.noise_models import get_depolarizing_noise


SHOTS = 20000

simulator = Aer.get_backend('aer_simulator')

qc = create_hadamard_circuit()
compiled = transpile(qc, simulator)

noise_levels = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3]

results = []

for noise in noise_levels:
    noise_model = get_depolarizing_noise(noise)

    result = simulator.run(
        compiled,
        shots=SHOTS,
        noise_model=noise_model
    ).result()

    counts = result.get_counts()

    zero_count = counts.get('0', 0)

    ideal = SHOTS / 2
    error = abs(ideal - zero_count) / SHOTS

    results.append((noise, error))

    print(f"Noise: {noise} → Counts: {counts} → Error: {error}")


# ---------- Plot ----------
import matplotlib.pyplot as plt

results.sort()

x = [r[0] for r in results]
y = [r[1] for r in results]

plt.plot(x, y, marker='o')
plt.xlabel("Noise Level")
plt.ylabel("Error")
plt.title("Noise vs Error (Hadamard Circuit)")
plt.grid()

plt.show()