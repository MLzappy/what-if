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

    model = "stability-ai/sdxl"
    client = replicate.Client(api_token=os.environ["REPLICATE_API_TOKEN"])

    print("📡 Calling Replicate API...")
    output = client.run(
        model,
        input={
            "prompt": prompt,
            "num_outputs": NUM_IMAGES,
            "width": 768,
            "height": 1024,
            "guidance_scale": 7.5
        }
    )

    for i, img_url in enumerate(output):
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
