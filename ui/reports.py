import base64
import json
import pandas as pd
from io import BytesIO
from datetime import datetime
import streamlit as st

def render_report_download(model_type, health, status, anomalies, horizon, report_format):

    report = {
        "timestamp": datetime.now().isoformat(),
        "model": model_type,
        "health": health,
        "status": status,
        "anomalies": len(anomalies),
        "prediction_horizon": horizon
    }

    buffer = BytesIO()

    if report_format == "CSV":
        pd.DataFrame([report]).to_csv(buffer, index=False)

    elif report_format == "JSON":
        buffer.write(json.dumps(report, indent=2).encode())

    else:
        buffer.write("\n".join(f"{k}: {v}" for k,v in report.items()).encode())

    b64 = base64.b64encode(buffer.getvalue()).decode()

    st.markdown(
        f"<a class='download-btn' href='data:application/octet-stream;base64,{b64}' "
        f"download='digital_twin_report.{report_format.lower()}'>Download Report</a>",
        unsafe_allow_html=True
    )
