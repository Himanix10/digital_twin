import json
import torch
from torch.utils.data import Dataset, DataLoader
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from torch.optim import AdamW
import os

MODEL_NAME = "distilgpt2"
SAVE_PATH = "ai/model"

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


def train():

    with open("ai/training_data.json") as f:
        data = json.load(f)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token

    dataset = TwinDataset(data, tokenizer)
    loader = DataLoader(dataset, batch_size=4, shuffle=True)

    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    optimizer = AdamW(model.parameters(), lr=5e-5)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    model.train()

    for epoch in range(2):
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
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

        print(f"Epoch {epoch+1} completed.")

    os.makedirs(SAVE_PATH, exist_ok=True)
    model.save_pretrained(SAVE_PATH)
    tokenizer.save_pretrained(SAVE_PATH)

    print("Model training completed.")

if __name__ == "__main__":
    train()
