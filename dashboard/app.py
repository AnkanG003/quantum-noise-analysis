import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qiskit_aer import Aer
from qiskit import transpile

from src.circuits import create_hadamard_circuit, create_bell_circuit
from src.noise_models import get_depolarizing_noise

import matplotlib.pyplot as plt


st.title("Quantum Noise Analysis Dashboard")

# ---------- Sidebar ----------
circuit_type = st.sidebar.selectbox(
    "Select Circuit",
    ["Hadamard", "Bell"]
)

max_noise = st.sidebar.slider("Max Noise Level", 0.0, 0.5, 0.3)
shots = st.sidebar.slider("Shots", 1000, 20000, 10000, step=1000)

noise_levels = [round(x, 2) for x in [i * 0.05 for i in range(int(max_noise / 0.05) + 1)]]

simulator = Aer.get_backend('aer_simulator')


# ---------- Choose Circuit ----------
if circuit_type == "Hadamard":
    qc = create_hadamard_circuit()
else:
    qc = create_bell_circuit()

compiled = transpile(qc, simulator)

errors = []

for noise in noise_levels:
    noise_model = get_depolarizing_noise(noise)

    result = simulator.run(
        compiled,
        shots=shots,
        noise_model=noise_model
    ).result()

    counts = result.get_counts()

    if circuit_type == "Hadamard":
        zero_count = counts.get('0', 0)
        ideal = shots / 2
        error = abs(ideal - zero_count) / shots
    else:
        correct = counts.get('00', 0) + counts.get('11', 0)
        ideal = shots
        error = (ideal - correct) / shots

    errors.append(error)

    st.write(f"Noise: {noise} → Counts: {counts} → Error: {round(error,4)}")


# ---------- Plot ----------
fig, ax = plt.subplots()
ax.plot(noise_levels, errors, marker='o')
ax.set_xlabel("Noise Level")
ax.set_ylabel("Error")
ax.set_title(f"{circuit_type} Circuit Noise Analysis")
ax.grid()

st.pyplot(fig)