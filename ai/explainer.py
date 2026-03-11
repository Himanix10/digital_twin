import torch
import re
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_PATH = "ai/fine_tuned_model"

# Disable gradient computation for inference
torch.set_grad_enabled(False)

# Lazy loading variables
_tokenizer = None
_model = None


def get_model():
    global _tokenizer, _model

    if _tokenizer is None or _model is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        _tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        _model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)

        _model.to(device)
        _model.eval()

    return _tokenizer, _model


def compute_status(health):
    if health >= 80:
        return "Healthy"
    elif health >= 50:
        return "Warning"
    else:
        return "Critical"


def analyze_risk(anomalies, noise):
    risk_notes = []

    if anomalies >= 30:
        risk_notes.append("Extremely high anomaly count detected.")
    elif anomalies >= 15:
        risk_notes.append("High anomaly rate observed.")
    elif anomalies >= 5:
        risk_notes.append("Moderate anomaly presence detected.")

    if noise >= 40:
        risk_notes.append("Severe noise disturbance affecting stability.")
    elif noise >= 20:
        risk_notes.append("Elevated noise levels detected.")
    elif noise >= 10:
        risk_notes.append("Slight noise fluctuations observed.")

    return " ".join(risk_notes)


def compute_confidence(health, anomalies, noise):
    base_confidence = health

    anomaly_penalty = min(anomalies * 0.5, 20)
    noise_penalty = min(noise * 0.3, 20)

    confidence = base_confidence - anomaly_penalty - noise_penalty
    confidence = max(min(confidence, 100), 5)

    return round(confidence, 2)


def extract_health(prompt):
    match = re.search(r'health\s*:\s*(\d+)', prompt, re.IGNORECASE)

    if match:
        return int(match.group(1))

    return 50


def extract_metric(prompt, metric_name):
    pattern = rf'{metric_name}\s*:\s*(\d+)'
    match = re.search(pattern, prompt, re.IGNORECASE)

    if match:
        return int(match.group(1))

    return 0


def generate_explanation(prompt, max_new_tokens=120):
    tokenizer, model = get_model()

    # Extract metrics
    health_value = extract_health(prompt)
    anomalies = extract_metric(prompt, "anomalies")
    noise = extract_metric(prompt, "noise")

    # Rule-based reasoning
    status = compute_status(health_value)
    risk_analysis = analyze_risk(anomalies, noise)
    confidence_score = compute_confidence(health_value, anomalies, noise)

    # Structured prompt
    structured_prompt = (
        "You are an industrial system monitoring AI.\n"
        "Only discuss mechanical performance, anomalies, vibration, and system stability.\n\n"
        f"System Health: {health_value}%\n"
        f"Status: {status}\n"
        f"Anomalies: {anomalies}\n"
        f"Noise: {noise}\n"
        f"Risk Assessment: {risk_analysis}\n\n"
        "Provide a detailed industrial explanation:"
    )

    device = next(model.parameters()).device
    inputs = tokenizer(structured_prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.eos_token_id,
            use_cache=True
        )

    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    if generated_text.startswith(structured_prompt):
        generated_text = generated_text[len(structured_prompt):].strip()

    final_output = (
        f"System Health: {health_value}%\n"
        f"Status: {status}\n"
        f"Confidence: {confidence_score}%\n\n"
        f"{generated_text}"
    )

    return final_output


if __name__ == "__main__":
    user_input = input("Enter system condition: ")

    explanation = generate_explanation(user_input)

    print("\nAI Explanation:\n")
    print(explanation)