from fpdf import FPDF

def export_pdf(df, filename="report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Battery Simulation Report", ln=True, align="C")
    pdf.ln(10)
    for i, row in df.head(20).iterrows():
        pdf.cell(200, 10, f"Cycle {row['cycles']} | Capacity: {row['predicted_capacity']:.2f} | Risk: {row['risk_score']:.2f}", ln=True)
    pdf.output(filename)
    return filename
