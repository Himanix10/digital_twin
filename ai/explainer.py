import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_PATH = "ai/fine_tuned_model"

model = None
tokenizer = None
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_model():
    global model, tokenizer
    if model is None:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
        model.to(device)
        model.eval()


def generate_explanation(metrics, user_question, max_tokens=250):
    load_model()

    prompt = f"""
    Model: {metrics['model']}
    Health: {metrics['health']:.2f}%
    Status: {metrics['status']}
    Anomalies: {metrics['anomalies']}
    Horizon: {metrics['horizon']}
    Error: {metrics['error']:.4f}

    User Question: {user_question}
    Provide technical explanation and corrective suggestions.
    """

    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=max_tokens,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)