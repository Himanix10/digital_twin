import json
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForCausalLM
from torch.optim import AdamW
import os

MODEL_NAME = "distilgpt2"
SAVE_PATH = "ai/fine_tuned_model"


# ================= Dataset =================
class TwinDataset(Dataset):

    def __init__(self, data, tokenizer, max_len=256):
        self.data = data
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sample = self.data[idx]

        text = sample["input"] + "\nExplanation:\n" + sample["output"]

        encoding = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=self.max_len,
            return_tensors="pt"
        )

        return {
            "input_ids": encoding["input_ids"].squeeze(),
            "attention_mask": encoding["attention_mask"].squeeze(),
            "labels": encoding["input_ids"].squeeze()
        }


# ================= Training =================
def train():

    # Load training data
    with open("ai/training_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token

    # Create dataset
    dataset = TwinDataset(data, tokenizer)
    loader = DataLoader(dataset, batch_size=4, shuffle=True)

    # Load base model
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

    optimizer = AdamW(model.parameters(), lr=5e-5)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    model.train()

    # Training loop
    for epoch in range(2):
        total_loss = 0

        for batch in loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )

            loss = outputs.loss
            total_loss += loss.item()

            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

        avg_loss = total_loss / len(loader)
        print(f"Epoch {epoch+1} completed. Avg Loss: {avg_loss:.4f}")

    # ================= SAVE MODEL =================
    os.makedirs(SAVE_PATH, exist_ok=True)

    model.save_pretrained(SAVE_PATH)
    tokenizer.save_pretrained(SAVE_PATH)

    print("Model saved successfully to:", SAVE_PATH)


# ================= Run =================
if __name__ == "__main__":
    train()
