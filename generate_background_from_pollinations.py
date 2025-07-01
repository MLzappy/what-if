import os
import requests
from moviepy.editor import ImageClip, concatenate_videoclips
from PIL import Image
from io import BytesIO
from datetime import datetime

# 📁 Ustawienia folderów i nazw
BACKGROUND_DIR = "backgrounds"
VIDEO_DIR = "video"
NUM_IMAGES = 3
DURATION_PER_IMAGE = 3  # sekundy

# 📅 Dzisiejsza data do nazw plików
today = datetime.now().strftime("%Y-%m-%d")
prompt_file = os.path.join(BACKGROUND_DIR, "prompt.txt")
output_video = os.path.join(VIDEO_DIR, f"{today}__background.mp4")

# 1️⃣ Wczytaj prompt z pliku
def load_prompt():
    with open(prompt_file, "r", encoding="utf-8") as f:
        return f.read().strip()

# 2️⃣ Zbuduj URL Pollinations na podstawie promptu
def generate_pollinations_url(prompt):
    return f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}"

# 3️⃣ Pobierz 3 obrazy i zapisz jako backgrounds/0.jpg, 1.jpg, ...
def download_images(prompt):
    os.makedirs(BACKGROUND_DIR, exist_ok=True)
    url = generate_pollinations_url(prompt)

    for i in range(NUM_IMAGES):
        response = requests.get(url)
        if response.status_code == 200:
            try:
                img = Image.open(BytesIO(response.content)).convert("RGB")
                img.save(os.path.join(BACKGROUND_DIR, f"{i}.jpg"))
                print(f"✅ Zapisano obraz {i}")
            except Exception as e:
                print(f"⚠️ Błąd przy zapisie obrazu {i}: {e}")
        else:
            print(f"❌ Błąd pobierania obrazu {i}: HTTP {response.status_code}")

# 4️⃣ Stwórz background.mp4 z przejściami fade
def create_background_video():
    clips = []
    for i in range(NUM_IMAGES):
        img_path = os.path.join(BACKGROUND_DIR, f"{i}.jpg")
        if os.path.exists(img_path):
            clip = ImageClip(img_path).set_duration(DURATION_PER_IMAGE).fadein(0.5).fadeout(0.5)
            clips.append(clip)
    if clips:
        final = concatenate_videoclips(clips, method="compose")
        os.makedirs(VIDEO_DIR, exist_ok=True)
        final.write_videofile(output_video, fps=30)
        print(f"🎬 Zapisano: {output_video}")
    else:
        print("⚠️ Nie znaleziono żadnych obrazów do renderowania.")

# 5️⃣ RUN
if __name__ == "__main__":
    prompt = load_prompt()
    print(f"🎯 Prompt: {prompt}")
    download_images(prompt)
    create_background_video()
