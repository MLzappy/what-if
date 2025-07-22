import os
import whisper
from pathlib import Path
import pysubs2
import subprocess

# === CONFIGURATION ===
FINAL_FOLDER = "finals"
SUBTITLE_FOLDER = "subtitles"
OUTPUT_FOLDER = "output"

def sanitize_filename(name: str) -> str:
    # Zastępujemy problematyczne znaki podkreślnikiem
    forbidden_chars = ["'", "\"", ",", ":", ";", " "]
    for ch in forbidden_chars:
        name = name.replace(ch, "_")
    return name

def get_latest_video():
    files = [f for f in os.listdir(FINAL_FOLDER) if f.endswith((".mp4", ".mov", ".mkv"))]
    if not files:
        raise Exception("No video files found in 'finals'")
    latest = max(files, key=lambda f: os.path.getctime(os.path.join(FINAL_FOLDER, f)))
    return os.path.join(FINAL_FOLDER, latest)

def transcribe_word_level(video_path):
    print("🔍 Transcribing with Whisper (word-level)...")
    model = whisper.load_model("medium")  # Możesz zmienić na "large" dla lepszej jakości
    result = model.transcribe(video_path, word_timestamps=True, verbose=False)

    word_entries = []
    for segment in result['segments']:
        for word in segment['words']:
            word_entries.append({
                "word": word['word'].strip(),
                "start": word['start'],
                "end": word['end']
            })

    return word_entries

def convert_words_to_ass(word_entries, ass_path):
    print("🎨 Generating .ass subtitles...")
    subs = pysubs2.SSAFile()

    style = subs.styles["Default"]
    style.fontname = "Arial"
    style.fontsize = 36
    style.bold = True
    style.primarycolor = pysubs2.Color(255, 255, 255)
    style.outline = 2
    style.shadow = 1
    style.alignment = 5       # Middle center
    style.margin_v = -100     # Trochę niżej na ekranie

    for word in word_entries:
        styled = f"{{\\fad(100,100)}}{word['word']}"
        subs.append(pysubs2.SSAEvent(
            start=word['start'] * 1000,
            end=word['end'] * 1000,
            text=styled
        ))

    os.makedirs(SUBTITLE_FOLDER, exist_ok=True)
    subs.save(ass_path, encoding="utf-8")
    return ass_path

def burn_captions(video_path, ass_path):
    print("🔥 Rendering video with kinetic captions...")
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    clean_stem = sanitize_filename(Path(video_path).stem)
    output_path = os.path.join(OUTPUT_FOLDER, f"{clean_stem}_captioned.mp4")

    # Windows: absolutna ścieżka i escape backslashy
    ass_path_win = str(Path(ass_path).resolve())
    ass_path_escaped = ass_path_win.replace("\\", "\\\\")

    vf_arg = f"ass='{ass_path_escaped}'"

    command = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vf", vf_arg,
        "-c:a", "copy",
        str(output_path)
    ]

    print("Running ffmpeg command:")
    print(" ".join(command))

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("❌ ffmpeg failed. Check subtitle path or libass support.")
        raise e

    return output_path

if __name__ == "__main__":
    video_path = get_latest_video()
    print(f"🎞 Found video: {video_path}")

    word_entries = transcribe_word_level(video_path)

    clean_stem = sanitize_filename(Path(video_path).stem)
    ass_path = os.path.join(SUBTITLE_FOLDER, f"{clean_stem}.ass")

    ass_file = convert_words_to_ass(word_entries, ass_path)

    final_video = burn_captions(video_path, ass_file)
    print(f"✅ Final kinetic captioned video saved to: {final_video}")
