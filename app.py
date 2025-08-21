import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from auth import login, check_auth
from model import run_simulation
from utils import export_pdf

st.set_page_config(page_title="Battery SaaS MVP", layout="wide")

# Authentication
if not check_auth():
    login()
    st.stop()

st.title("🔋 Battery Digital Twin SaaS (MVP)")

# Upload or use demo dataset
uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.info("No file uploaded. Using demo dataset...")
    df = pd.DataFrame({
        "cycles": list(range(1, 101)),
        "capacity": [1 - (i*0.005) for i in range(1, 101)]
    })

# Run Simulation
if st.button("Run Simulation"):
    results = run_simulation(df)

    # Plot degradation
    fig, ax = plt.subplots()
    ax.plot(results["cycles"], results["predicted_capacity"], label="Predicted Capacity")
    ax.set_xlabel("Cycles")
    ax.set_ylabel("Capacity")
    ax.legend()
    st.pyplot(fig)

    # Risk Score
    avg_risk = results["risk_score"].mean()
    st.metric("Average Risk Score", f"{avg_risk:.2f}%")

    # Download CSV & PDF
    st.download_button("Download Results (CSV)", results.to_csv(index=False), "results.csv")
    pdf_file = export_pdf(results)
    with open(pdf_file, "rb") as f:
        st.download_button("Download Report (PDF)", f, file_name="report.pdf")
