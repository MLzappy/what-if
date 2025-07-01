import whisper
import json
import os

AUDIO_FOLDER = "audio"
SEGMENTS_FOLDER = "segments"
os.makedirs(SEGMENTS_FOLDER, exist_ok=True)

# Wybierz najnowszy plik .mp3 z folderu audio
mp3_files = [f for f in os.listdir(AUDIO_FOLDER) if f.endswith(".mp3")]
latest_file = max(mp3_files, key=lambda f: os.path.getctime(os.path.join(AUDIO_FOLDER, f)))
audio_path = os.path.join(AUDIO_FOLDER, latest_file)
print(f"🎧 Transkrypcja pliku: {audio_path}")

# Załaduj model Whisper i transkrybuj
model = whisper.load_model("base")
result = model.transcribe(audio_path)

# Zapisz tylko czyste segmenty start/end/text
segments_clean = [
    {"start": s["start"], "end": s["end"], "text": s["text"]}
    for s in result["segments"]
]

# Zapisz segments.json
output_path = os.path.join(SEGMENTS_FOLDER, latest_file.replace(".mp3", ".json"))
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(segments_clean, f, indent=2, ensure_ascii=False)

print(f"✅ Zapisano do {output_path}")
