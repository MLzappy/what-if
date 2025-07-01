
import os
from mutagen.mp3 import MP3
from datetime import datetime
import math
import subprocess

BACKGROUND_DIR = "backgrounds"
AUDIO_DIR = "audio"
VIDEO_DIR = "video"
TEMP_LIST = "filelist.txt"

# 🔍 Znajdź najnowszy plik .mp3
latest_audio = max(
    (os.path.join(AUDIO_DIR, f) for f in os.listdir(AUDIO_DIR) if f.endswith(".mp3")),
    key=os.path.getctime
)
audio = MP3(latest_audio)
duration = audio.info.length
duration_rounded = math.ceil(duration)

# 📅 Dzisiejsza data
os.makedirs(VIDEO_DIR, exist_ok=True)
date_str = datetime.now().strftime("%Y-%m-%d")
output_video = os.path.join(VIDEO_DIR, f"{date_str}__background.mp4")

# 🔁 Oblicz ile obrazów potrzeba (każdy trwa 3 sekundy)
clips_needed = math.ceil(duration / 3)
pattern = [f"{BACKGROUND_DIR}/{i:03}.jpg" for i in range(3)]
looped_images = [pattern[i % 3] for i in range(clips_needed)]

# 📝 Stwórz filelist.txt z odpowiednimi powtórzeniami
with open(TEMP_LIST, "w", encoding="utf-8") as f:
    for img in looped_images:
        f.write(f"file '{img}'\n")
        f.write("duration 3\n")
    f.write(f"file '{looped_images[-1]}'\n")  # ostatni raz bez duration

# 🎬 Tworzenie zapętlonego wideo bez audio
print("🎬 Tworzę zapętlone tło wideo (bez dźwięku)...")
subprocess.call([
    "ffmpeg", "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", TEMP_LIST,
    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p",
    "-r", "30",
    output_video
])

# 🧹 Usuń śmieci
os.remove(TEMP_LIST)

print(f"✅ Gotowe: {output_video}")
