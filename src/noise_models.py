from qiskit_aer.noise import NoiseModel, depolarizing_error


def get_depolarizing_noise(p=0.1):
    noise_model = NoiseModel()

    error_1q = depolarizing_error(p, 1)
    error_2q = depolarizing_error(p, 2)

    # Apply to single-qubit gates
    noise_model.add_all_qubit_quantum_error(error_1q, ['h'])

    # Apply to two-qubit gates (CRITICAL for Bell)
    noise_model.add_all_qubit_quantum_error(error_2q, ['cx'])

    return noise_model