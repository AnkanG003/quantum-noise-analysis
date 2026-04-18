from qiskit_aer.noise import NoiseModel, depolarizing_error


def get_depolarizing_noise(p=0.1):
    noise_model = NoiseModel()
    error = depolarizing_error(p, 1)

    noise_model.add_all_qubit_quantum_error(error, ['h'])

    return noise_model