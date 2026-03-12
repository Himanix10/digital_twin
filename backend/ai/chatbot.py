from ai.inference import generate_explanation
from ai.rule_engine import structured_reasoning

def chatbot_response(user_query, health, anomalies, noise, status):

    structured = structured_reasoning(health, anomalies, noise)

    explanation = generate_explanation(
        health, anomalies, noise, status
    )

    response = "\n".join(structured) + "\n\n" + explanation

    return response
