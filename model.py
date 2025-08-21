import numpy as np
import pandas as pd

def run_simulation(df):
    # Ensure correct columns exist
    if "cycles" not in df.columns:
        df["cycles"] = range(1, len(df) + 1)
    if "capacity" not in df.columns:
        # Assume 100% starting capacity, degrading slightly each cycle
        df["capacity"] = 1 - (0.005 * df["cycles"])

    # Simple prediction model
    df["predicted_capacity"] = df["capacity"] * (0.999 ** df["cycles"])
    df["risk_score"] = np.clip(100 - df["predicted_capacity"] * 100, 0, 100)

    return df
