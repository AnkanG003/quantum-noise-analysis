import streamlit as st
import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qiskit_aer import Aer
from qiskit import transpile

from src.circuits import create_hadamard_circuit, create_bell_circuit
from src.noise_models import get_depolarizing_noise

import matplotlib.pyplot as plt
import pandas as pd


# ---------- Title ----------
st.title("Quantum Noise Analysis & Comparison Dashboard")

st.markdown("""
This dashboard analyzes the effect of quantum noise on quantum circuits.

- **Hadamard Circuit** → Single-qubit (more stable)
- **Bell Circuit** → Entangled (more sensitive to noise)
""")


# ---------- Sidebar ----------
mode = st.sidebar.radio("Mode", ["Single Circuit", "Compare Both"])

max_noise = st.sidebar.slider("Max Noise Level", 0.0, 0.5, 0.3)
shots = st.sidebar.slider("Shots", 1000, 20000, 10000, step=1000)

noise_levels = [round(x, 2) for x in [i * 0.05 for i in range(int(max_noise / 0.05) + 1)]]

simulator = Aer.get_backend('aer_simulator')


# ===========================
# ---------- SINGLE ----------
# ===========================
if mode == "Single Circuit":

    circuit_type = st.sidebar.selectbox("Select Circuit", ["Hadamard", "Bell"])

    if circuit_type == "Hadamard":
        qc = create_hadamard_circuit()
    else:
        qc = create_bell_circuit()

    compiled = transpile(qc, simulator)

    errors = []
    data = []

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
            error = (shots - correct) / shots

        errors.append(error)

        data.append({
            "Noise": noise,
            "Error": round(error, 4),
            "Counts": str(counts)
        })

    # ---------- Table ----------
    st.subheader("Results Table")
    df = pd.DataFrame(data)
    st.dataframe(df)

    # ---------- Plot ----------
    fig, ax = plt.subplots()
    ax.plot(noise_levels, errors, marker='o')
    ax.set_xlabel("Noise Level")
    ax.set_ylabel("Error")
    ax.set_title(f"{circuit_type} Circuit Noise Analysis")
    ax.grid()

    st.pyplot(fig)

    # ---------- Insight ----------
    st.subheader("Insight")

    if circuit_type == "Hadamard":
        st.success("Hadamard circuits remain relatively stable under noise.")
    else:
        st.error("Bell circuits degrade rapidly due to entanglement and two-qubit gate errors.")


# ===========================
# ---------- COMPARE ----------
# ===========================
elif mode == "Compare Both":

    qc_h = create_hadamard_circuit()
    qc_b = create_bell_circuit()

    compiled_h = transpile(qc_h, simulator)
    compiled_b = transpile(qc_b, simulator)

    hadamard_errors = []
    bell_errors = []

    for noise in noise_levels:
        noise_model = get_depolarizing_noise(noise)

        # Hadamard
        result_h = simulator.run(
            compiled_h,
            shots=shots,
            noise_model=noise_model
        ).result()

        counts_h = result_h.get_counts()
        zero_count = counts_h.get('0', 0)
        error_h = abs((shots / 2) - zero_count) / shots
        hadamard_errors.append(error_h)

        # Bell
        result_b = simulator.run(
            compiled_b,
            shots=shots,
            noise_model=noise_model
        ).result()

        counts_b = result_b.get_counts()
        correct = counts_b.get('00', 0) + counts_b.get('11', 0)
        error_b = (shots - correct) / shots
        bell_errors.append(error_b)

    # ---------- Table ----------
    st.subheader("Comparison Table")

    df_compare = pd.DataFrame({
        "Noise": noise_levels,
        "Hadamard Error": [round(e, 4) for e in hadamard_errors],
        "Bell Error": [round(e, 4) for e in bell_errors]
    })

    st.dataframe(df_compare)

    # ---------- Plot ----------
    fig, ax = plt.subplots()
    ax.plot(noise_levels, hadamard_errors, marker='o', label='Hadamard')
    ax.plot(noise_levels, bell_errors, marker='o', label='Bell')

    ax.set_xlabel("Noise Level")
    ax.set_ylabel("Error")
    ax.set_title("Comparison: Hadamard vs Bell")
    ax.legend()
    ax.grid()

    st.pyplot(fig)

    # ---------- Insight ----------
    st.subheader("Insight")

    st.success("Hadamard circuits remain relatively stable under noise.")
    st.error("Bell circuits show significantly higher sensitivity due to entanglement.")


# ===========================
# ---------- DOWNLOAD ----------
# ===========================
fig.savefig("temp.png")

with open("temp.png", "rb") as file:
    st.download_button(
        label="Download Graph",
        data=file,
        file_name="noise_analysis.png",
        mime="image/png"
    )