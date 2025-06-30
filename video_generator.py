import os
from moviepy.editor import *
from datetime import datetime

AUDIO_FOLDER = "audio"
SCRIPTS_FOLDER = "scripts"
VIDEO_FOLDER = "video"
BACKGROUND_VIDEO = "background.mp4"  # plik w katalogu głównym

os.makedirs(VIDEO_FOLDER, exist_ok=True)

# 🧠 Znajdź najnowszy plik skryptu
def get_latest_script():
    files = sorted(
        [f for f in os.listdir(SCRIPTS_FOLDER) if f.endswith(".txt")],
        key=lambda x: os.path.getctime(os.path.join(SCRIPTS_FOLDER, x)),
        reverse=True
    )
    return files[0] if files else None

# 📖 Wczytaj tekst z pliku
def read_script_text(script_path):
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read().split("🎬 SKRYPT:\n")
        return content[1].strip() if len(content) > 1 else content[0].strip()

# 🎬 Stwórz finalne wideo z napisami
def create_video(script_text, audio_path, output_path):
    audio = AudioFileClip(audio_path)
    duration = audio.duration

    # Tło z pętlą
    bg = VideoFileClip(BACKGROUND_VIDEO).without_audio()
    if bg.duration < duration:
        loops = int(duration // bg.duration) + 1
        bg = concatenate_videoclips([bg] * loops)
    bg = bg.subclip(0, duration).resize((1080, 1920))

    # Napisy jako jeden długi TextClip
    text_clip = TextClip(
        script_text,
        fontsize=50,
        color='white',
        stroke_color='black',
        stroke_width=2,
        size=(1080, None),
        method='caption',
        align='center'
    ).set_position(('center', 0.75), relative=True).set_duration(duration)

    final = CompositeVideoClip([bg.set_audio(audio), text_clip])
    final.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")
    print("✅ Wideo zapisane:", output_path)

# 🚀 RUN
if __name__ == "__main__":
    latest_script = get_latest_script()
    if not latest_script:
        print("❌ Brak pliku skryptu.")
        exit()

    script_path = os.path.join(SCRIPTS_FOLDER, latest_script)
    script_text = read_script_text(script_path)

    # Wyciągnij nazwę audio z safe_topic
    safe_topic = latest_script.split("__")[-1].replace(".txt", "")
    audio_path = os.path.join(AUDIO_FOLDER, f"{safe_topic}.mp3")
    output_path = os.path.join(VIDEO_FOLDER, f"{safe_topic}.mp4")

    if not os.path.exists(audio_path):
        print("❌ Brak pliku audio:", audio_path)
        exit()

    create_video(script_text, audio_path, output_path)

