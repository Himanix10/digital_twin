import random
import json
import os

OUTPUT_PATH = "ai/training_data.json"

def generate_sample():

    health = random.randint(40, 100)
    anomalies = random.randint(0, 25)
    noise = round(random.uniform(1, 20), 2)

    if health < 60:
        status = "Critical"
        cause = "severe system degradation"
        action = "immediate maintenance required"
    elif health < 75:
        status = "Warning"
        cause = "moderate instability"
        action = "schedule inspection"
    else:
        status = "Healthy"
        cause = "normal operation"
        action = "no action needed"

    input_text = f"""
    Health: {health}
    Anomalies: {anomalies}
    Noise: {noise}
    Status: {status}
    """

    output_text = f"""
    The system health is {health} percent indicating {status} condition.
    There are {anomalies} detected anomalies with noise level {noise}.
    This suggests {cause}. Recommended action: {action}.
    """

    return {
        "input": input_text.strip(),
        "output": output_text.strip()
    }


def generate_dataset(samples=2000):

    data = [generate_sample() for _ in range(samples)]

    os.makedirs("ai", exist_ok=True)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Dataset generated with {samples} samples.")

if __name__ == "__main__":
    generate_dataset()
