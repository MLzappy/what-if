
import os
import requests
import random
from datetime import datetime
from PIL import Image
from io import BytesIO
import time

BACKGROUND_DIR = "backgrounds"
VIDEO_DIR = "video"
NUM_IMAGES = 3
PROMPT_FILE = os.path.join(BACKGROUND_DIR, "prompt.txt")

today = datetime.now().strftime("%Y-%m-%d")
output_video = os.path.join(VIDEO_DIR, f"{today}__background.mp4")

def load_prompt():
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

def search_lexica(prompt):
    try:
        url = f"https://lexica.art/api/v1/search?q={prompt.replace(' ', '%20')}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return [img["src"] for img in data.get("images", [])]
    except Exception as e:
        print(f"❌ Błąd Lexica: {e}")
    return []

def generate_pollinations_url(prompt):
    return f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?seed={random.randint(1,99999)}"

def crop_logo_from_image(image_data, crop_height=80):
    image = Image.open(BytesIO(image_data))
    width, height = image.size
    cropped = image.crop((0, 0, width, height - crop_height))
    return cropped

def download_from_lexica(prompt):
    print("🔎 Próbuję pobrać obrazy z Lexica...")
    urls = search_lexica(prompt)
    if len(urls) >= NUM_IMAGES:
        chosen = random.sample(urls, NUM_IMAGES)
        for i, url in enumerate(chosen):
            img_data = requests.get(url).content
            with open(os.path.join(BACKGROUND_DIR, f"{i:03}.jpg"), "wb") as f:
                f.write(img_data)
        print("✅ Obrazy pobrane z Lexica")
        return True
    return False

def download_from_pollinations(prompt):
    print("🔁 Używam Pollinations jako backup...")
    for i in range(NUM_IMAGES):
        url = generate_pollinations_url(prompt)
        response = requests.get(url)
        if response.status_code == 200:
            cropped_img = crop_logo_from_image(response.content)
            file_path = os.path.join(BACKGROUND_DIR, f"{i:03}.jpg")
            cropped_img.save(file_path)
            print(f"✅ Pollinations: zapisano {file_path} (logo usunięte)")
        else:
            print(f"❌ Pollinations błąd {i}: {response.status_code}")
        time.sleep(1)

if __name__ == "__main__":
    os.makedirs(BACKGROUND_DIR, exist_ok=True)
    prompt = load_prompt()
    print(f"🎯 Prompt: {prompt}")
    success = download_from_lexica(prompt)
    if not success:
        download_from_pollinations(prompt)
