from qiskit_aer import Aer
from qiskit import transpile

from src.circuits import create_hadamard_circuit, create_bell_circuit
from src.noise_models import get_depolarizing_noise


simulator = Aer.get_backend('aer_simulator')


# ---------- Hadamard Circuit ----------
qc = create_hadamard_circuit()

compiled = transpile(qc, simulator)
result = simulator.run(compiled, shots=1000).result()

counts = result.get_counts()

print("Hadamard Circuit Output:", counts)


# ---------- Noisy Hadamard ----------
noise_model = get_depolarizing_noise(0.2)

compiled_noisy = transpile(qc, simulator)
result_noisy = simulator.run(compiled_noisy, shots=1000, noise_model=noise_model).result()

counts_noisy = result_noisy.get_counts()

print("Noisy Hadamard Output:", counts_noisy)

error_h = abs(counts.get('0', 0) - counts_noisy.get('0', 0)) / 1000
print("Hadamard Error Difference:", error_h)


# ---------- Bell Circuit ----------
qc_bell = create_bell_circuit()

compiled_bell = transpile(qc_bell, simulator)
result_bell = simulator.run(compiled_bell, shots=1000).result()

counts_bell = result_bell.get_counts()

print("\nBell Circuit Output:", counts_bell)


# ---------- Noisy Bell ----------
compiled_bell_noisy = transpile(qc_bell, simulator)
result_bell_noisy = simulator.run(compiled_bell_noisy, shots=1000, noise_model=noise_model).result()

counts_bell_noisy = result_bell_noisy.get_counts()

print("Noisy Bell Output:", counts_bell_noisy)

error_b = abs(counts_bell.get('00', 0) - counts_bell_noisy.get('00', 0)) / 1000
print("Bell Error Difference:", error_b)