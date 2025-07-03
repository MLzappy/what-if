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

def generate_images_with_huggingface(prompt):
    import json
    os.makedirs(BACKGROUND_DIR, exist_ok=True)

    model = "runwayml/stable-diffusion-v1-5"
    API_URL = f"https://api-inference.huggingface.co/models/{model}"
    headers = {
        "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
        "Accept": "image/png"
    }

    for i in range(NUM_IMAGES):
        print(f"🧠 Generating image {i+1}/{NUM_IMAGES}...")

        payload = {
            "inputs": prompt
        }

        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            file_path = os.path.join(BACKGROUND_DIR, f"{i:03}.png")
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"✅ Saved: {file_path}")
        else:
            print(f"❌ HF API Error {response.status_code}: {response.text}")




def main():
    prompt_raw = load_prompt()
    prompt = f"{prompt_raw}, cinematic, ultra detailed, dramatic lighting, concept art, 8K"
    print(f"🎯 Prompt: {prompt}")
    generate_images_with_huggingface(prompt)

if __name__ == "__main__":
    main()
