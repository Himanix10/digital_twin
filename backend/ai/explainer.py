import re


def compute_status(health):

    if health >= 80:
        return "Healthy"

    elif health >= 50:
        return "Warning"

    else:
        return "Critical"


def analyze_risk(anomalies, noise):

    risk_notes = []

    if anomalies >= 10:
        risk_notes.append("High anomaly frequency detected.")
    elif anomalies >= 3:
        risk_notes.append("Moderate anomaly activity observed.")

    if noise >= 20:
        risk_notes.append("Elevated sensor noise affecting stability.")
    elif noise >= 10:
        risk_notes.append("Minor signal noise detected.")

    if not risk_notes:
        risk_notes.append("System operating within normal parameters.")

    return " ".join(risk_notes)


def compute_confidence(health, anomalies, noise):

    confidence = health

    confidence -= anomalies * 2
    confidence -= noise * 0.5

    confidence = max(min(confidence, 100), 5)

    return round(confidence, 2)


def extract_value(prompt, name):

    match = re.search(rf"{name}:(\d+)", prompt)

    if match:
        return int(match.group(1))

    return 0


def generate_explanation(prompt):

    health = extract_value(prompt, "health")
    anomalies = extract_value(prompt, "anomalies")
    noise = extract_value(prompt, "noise")

    status = compute_status(health)

    risk = analyze_risk(anomalies, noise)

    confidence = compute_confidence(health, anomalies, noise)

    explanation = f"""
System Health: {health}%
Status: {status}
Confidence Score: {confidence}%

Operational Analysis:
The hybrid digital twin evaluated sensor fusion outputs and predictive model results.

Detected anomalies: {anomalies}
Signal noise level: {noise}

Risk Assessment:
{risk}

Recommendation:
"""

    if status == "Healthy":

        explanation += "System functioning normally. Continue routine monitoring."

    elif status == "Warning":

        explanation += "Early signs of degradation detected. Schedule preventive inspection."

    else:

        explanation += "Critical condition detected. Immediate maintenance recommended."

    return explanation