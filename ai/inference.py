import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_PATH = "ai/model"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

def generate_explanation(health, anomalies, noise, status):

    prompt = f"""
    Health: {health}
    Anomalies: {anomalies}
    Noise: {noise}
    Status: {status}
    Explanation:
    """

    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    output = model.generate(
        **inputs,
        max_length=200,
        temperature=0.7,
        do_sample=True
    )

    text = tokenizer.decode(output[0], skip_special_tokens=True)

    return text.split("Explanation:")[-1].strip()
