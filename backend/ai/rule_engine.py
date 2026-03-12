def structured_reasoning(health, anomalies, noise):

    reasons = []

    if health < 60:
        reasons.append("System performance severely degraded.")

    if anomalies > 15:
        reasons.append("High anomaly frequency detected.")

    if noise > 10:
        reasons.append("Elevated signal noise observed.")

    if not reasons:
        reasons.append("System operating within normal limits.")

    return reasons
