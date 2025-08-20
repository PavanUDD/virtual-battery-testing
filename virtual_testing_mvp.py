import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------
# Title
# --------------------------
st.title("AI-Powered Virtual Battery Testing MVP")
st.write("Interactive demo for battery risk simulation and improvement suggestions.")

# --------------------------
# Sidebar Inputs
# --------------------------
st.sidebar.header("Scenario Parameters")
temp_input = st.sidebar.slider("Temperature (°C)", -10, 50, 25)
load_input = st.sidebar.slider("Load (kg)", 0, 500, 200)
driving_style_input = st.sidebar.selectbox("Driving Style", [1,2,3,4], 
                                           format_func=lambda x: {1:'Calm',2:'Normal',3:'Aggressive',4:'Extreme'}[x])
miles_input = st.sidebar.slider("Miles driven", 0, 200, 50)

# --------------------------
# Risk Calculation Function
# --------------------------
def calculate_battery_risk(temp, load, driving_style, miles):
    risk = 0
    if temp > 35:
        risk += 25
    elif temp < 0:
        risk += 15
    if load > 300:
        risk += 20
    if driving_style >= 3:
        risk += 20
    risk += 0.1 * miles
    return min(risk, 100)

# --------------------------
# Single Scenario Prediction
# --------------------------
predicted_risk = calculate_battery_risk(temp_input, load_input, driving_style_input, miles_input)
risk_A = predicted_risk * 1.0
risk_B = predicted_risk * 0.85  # Hypothetical improved design

# Display
st.subheader(f"Predicted Battery Failure Risk: {predicted_risk:.2f}%")

# --------------------------
# Compare Designs
# --------------------------
st.subheader("Design Comparison")
fig, ax = plt.subplots()
designs = ['Design A', 'Design B']
risks = [risk_A, risk_B]
bars = ax.bar(designs, risks, color=['orange','green'])
ax.set_ylim(0, 100)
ax.set_ylabel("Predicted Risk (%)")
ax.set_title("Design Comparison")
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.1f}%', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0,3), textcoords="offset points", ha='center', va='bottom')
st.pyplot(fig)

# Advice
st.write("Advice:")
for name, risk in zip(designs, risks):
    if risk < 30:
        st.success(f"{name}: Healthy ✅")
    elif risk < 60:
        st.warning(f"{name}: Moderate Risk ⚠️")
    else:
        st.error(f"{name}: High Risk ❌")

# --------------------------
# Scenario History Table
# --------------------------
st.subheader("Scenario History")
history_data = {
    "Temperature (°C)": [temp_input],
    "Load (kg)": [load_input],
    "Driving Style": [driving_style_input],
    "Miles Driven": [miles_input],
    "Design A Risk (%)": [risk_A],
    "Design B Risk (%)": [risk_B]
}
st.dataframe(pd.DataFrame(history_data))

# --------------------------
# Batch Scenario Simulation Gallery
# --------------------------
st.subheader("Scenario Simulation Gallery")
scenarios = [
    {"name":"Hot & Aggressive","temp":45,"load":400,"driving_style":4,"miles":100},
    {"name":"Cold & Calm","temp":-5,"load":100,"driving_style":1,"miles":50},
    {"name":"Normal Day","temp":25,"load":200,"driving_style":2,"miles":80},
    {"name":"Heavy Load & Aggressive","temp":30,"load":450,"driving_style":4,"miles":120},
    {"name":"Hot & Heavy Load","temp":40,"load":480,"driving_style":3,"miles":150}
]

gallery_data = []
for s in scenarios:
    r = calculate_battery_risk(s['temp'], s['load'], s['driving_style'], s['miles'])
    gallery_data.append([s['name'], r, r*0.85])

gallery_df = pd.DataFrame(gallery_data, columns=['Scenario','Design A Risk','Design B Risk'])
st.bar_chart(gallery_df.set_index('Scenario'))

# Highlight highest risk scenario
max_risk = max([row[1] for row in gallery_data])
high_risk_scenario = [row[0] for row in gallery_data if row[1]==max_risk][0]
st.warning(f"⚠️ Highest risk scenario: {high_risk_scenario} with {max_risk:.1f}% risk")

# --------------------------
# Heatmap of Risk vs Temp and Load
# --------------------------
st.subheader("Heatmap: Risk across Temperature & Load (Driving Style & Miles fixed)")

temps = np.arange(-10, 51, 5)
loads = np.arange(0, 501, 25)
heatmap = np.zeros((len(loads), len(temps)))

for i, load in enumerate(loads):
    for j, temp in enumerate(temps):
        heatmap[i, j] = calculate_battery_risk(temp, load, driving_style_input, miles_input)

fig2, ax2 = plt.subplots(figsize=(10,5))
sns.heatmap(heatmap, xticklabels=temps, yticklabels=loads, cmap="YlOrRd", annot=False, ax=ax2)
ax2.set_xlabel("Temperature (°C)")
ax2.set_ylabel("Load (kg)")
ax2.set_title("Battery Risk Heatmap")
st.pyplot(fig2)

# --------------------------
# AI-style Insight & Improvement Suggestion
# --------------------------
st.subheader("AI-style Insight")
insights = []
if temp_input > 35:
    insights.append("High temperature significantly increases risk.")
elif temp_input < 0:
    insights.append("Very cold temperature slightly increases risk.")
if load_input > 300:
    insights.append("Heavy load contributes to higher battery wear.")
if driving_style_input >= 3:
    insights.append("Aggressive driving increases degradation rate.")
if miles_input > 100:
    insights.append("High mileage gradually increases risk.")

if insights:
    for i in insights:
        st.info(f"• {i}")

st.subheader("Suggested Hypothetical Improvements")
if predicted_risk > 30:
    st.success("• Consider improved cooling or material to reduce temperature impact.")
    st.success("• Reduce heavy load where possible or improve battery load tolerance.")
    st.success("• Optimize battery for aggressive driving patterns.")
else:
    st.success("Battery design is currently healthy under these conditions ✅")
