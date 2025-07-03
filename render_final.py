import os
import subprocess
import datetime

# 📂 Nazwy i foldery
AUDIO_FOLDER = "audio"
VIDEO_FOLDER = "video"
MUSIC_PATH = "music/bg_music.mp3"  # ← stała ścieżka do muzyki
OUTPUT_PATH = "finals"
os.makedirs(OUTPUT_PATH, exist_ok=True)

# 🔍 Znajdź najnowszy plik audio (głos)
audio_files = [f for f in os.listdir(AUDIO_FOLDER) if f.endswith(".mp3")]
latest_audio = max(audio_files, key=lambda f: os.path.getmtime(os.path.join(AUDIO_FOLDER, f)))
audio_path = os.path.join(AUDIO_FOLDER, latest_audio)
print("🎤 Audio:", audio_path)

# 🔍 Znajdź najnowszy plik video (tło)
video_files = [f for f in os.listdir(VIDEO_FOLDER) if f.endswith(".mp4")]
latest_video = max(video_files, key=lambda f: os.path.getctime(os.path.join(VIDEO_FOLDER, f)))
video_path = os.path.join(VIDEO_FOLDER, latest_video)
print("🎬 Video:", video_path)

# 🎞 Nazwa pliku wyjściowego
safe_title = os.path.splitext(latest_audio)[0]
out_path = os.path.join(OUTPUT_PATH, f"{safe_title}_final.mp4")

# 🎧 Mix audio głównego + podkład (głos + muzyka)
command = [
    "ffmpeg",
    "-i", video_path,
    "-i", audio_path,
    "-i", MUSIC_PATH,
    "-filter_complex",
    "[1:a]volume=1.0[a1];[2:a]volume=0.2[a2];[a1][a2]amix=inputs=2:duration=first[aout]",
    "-map", "0:v", "-map", "[aout]",
    "-c:v", "copy",
    "-shortest",
    "-y",  # overwrite
    out_path
]

# ▶️ Uruchom renderowanie
print("🎞 Renderowanie...")
subprocess.run(command)

print(f"✅ Gotowe: {out_path}")
