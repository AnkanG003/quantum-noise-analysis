from qiskit_aer.noise import NoiseModel
from qiskit_aer.noise.errors import depolarizing_error, pauli_error


def get_custom_noise(p, noise_types):
    noise_model = NoiseModel()

    # ---------------- Depolarizing ----------------
    if "Depolarizing" in noise_types:
        error_1q = depolarizing_error(p, 1)
        error_2q = depolarizing_error(p, 2)

        noise_model.add_all_qubit_quantum_error(error_1q, ['h'])
        noise_model.add_all_qubit_quantum_error(error_2q, ['cx'])

    # ---------------- Bit Flip ----------------
    if "Bit Flip" in noise_types:
        bit_flip = pauli_error([('X', p), ('I', 1 - p)])

        noise_model.add_all_qubit_quantum_error(bit_flip, ['h'])   # only 1-qubit gate
      

    # ---------------- Phase Flip ----------------
    if "Phase Flip" in noise_types:
        phase_flip = pauli_error([('Z', p), ('I', 1 - p)])

        noise_model.add_all_qubit_quantum_error(phase_flip, ['h'])  # only 1-qubit
       

    return noise_model