import numpy as np
import pandas as pd

def run_simulation(df):
    # Assume dataset has "cycles" and "capacity"
    df["predicted_capacity"] = df["capacity"] * (0.99 ** df["cycles"])
    df["risk_score"] = np.clip(100 - df["predicted_capacity"]*100, 0, 100)
    return df
