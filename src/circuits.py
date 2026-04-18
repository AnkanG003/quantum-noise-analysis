# circuits.py
from qiskit import QuantumCircuit


# Hadamard circuit
def create_hadamard_circuit():
    """
    Creates a single qubit circuit with a Hadamard gate.

    Returns:
        QuantumCircuit: the constructed circuit
    """
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)

    return qc



# Bell State Circuit
def create_bell_circuit():
    """
    Creates a 2-qubit Bell state (entangled circuit).

    Returns:
        QuantumCircuit: Bell state quantum circuit
    """
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    return qc