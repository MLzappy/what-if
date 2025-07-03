import os
import replicate
import requests
from datetime import datetime

NUM_IMAGES = 3
BACKGROUND_DIR = "backgrounds"
PROMPT_FILE = os.path.join(BACKGROUND_DIR, "prompt.txt")

def load_prompt():
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

def generate_images_with_replicate(prompt):
    os.makedirs(BACKGROUND_DIR, exist_ok=True)

    # ✅ Correct model + version
    model = "stability-ai/sdxl:fd6fce3c5c39c513593fb0a1b1d93d03a7c893c868bf41ce5b3c5f2cda5c38a3"
    client = replicate.Client(api_token=os.environ["REPLICATE_API_TOKEN"])

    print("📡 Calling Replicate SDXL...")

    for i in range(NUM_IMAGES):
        output = client.run(
            model,
            input={
                "prompt": prompt,
                "width": 1024,
                "height": 1024,
                "refine": "no_refiner",       # Required for SDXL
                "scheduler": "K_EULER_ANCESTRAL"
            }
        )

        img_url = output[0]
        img_data = requests.get(img_url).content
        file_path = os.path.join(BACKGROUND_DIR, f"{i:03}.jpg")
        with open(file_path, "wb") as f:
            f.write(img_data)
        print(f"✅ Image saved: {file_path}")


def main():
    prompt_raw = load_prompt()
    prompt = f"{prompt_raw}, cinematic, ultra detailed, dramatic lighting, concept art, 8K"
    print(f"🎯 Prompt: {prompt}")
    generate_images_with_replicate(prompt)

if __name__ == "__main__":
    main()
