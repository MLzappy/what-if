import os
import datetime
from openai import OpenAI
import requests

# 🔐 Inicjalizacja klienta OpenAI
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    project=os.getenv("PROJECT_ID")
)

# 🔐 Klucz i ID głosu z ElevenLabs
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "teWbCKrhI72i8jsmUGJ5"  # ← Zamień na swój voice ID

# 📂 Ścieżki
USED_TOPICS_FILE = "used_topics.txt"
OUTPUT_FOLDER = "scripts"
AUDIO_FOLDER = "audio"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# ✅ 1. Pobierz listę użytych tematów
def get_used_topics():
    if not os.path.exists(USED_TOPICS_FILE):
        return set()
    with open(USED_TOPICS_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f.readlines())

# ✅ 2. Zapisz nowy temat do listy
def save_used_topic(topic):
    with open(USED_TOPICS_FILE, "a", encoding="utf-8") as f:
        f.write(topic + "\n")

# ✅ 3. Wygeneruj nowy, unikalny temat
def generate_unique_topic():
    used_topics = get_used_topics()
    tries = 0
    while True:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Come up with a fresh, creative, and surprising topic that starts with 'What if...'. "
                        "The topic should be catchy and ideal for a viral YouTube Shorts or TikTok video. "
                        "Think outside the box, mix genres, and make it sound intriguing. "
                        "Reply with just the title, in English."
                    )
                }
            ],
            temperature=1.3,
            max_tokens=30
        )
        topic = response.choices[0].message.content.strip()
        if topic not in used_topics or tries > 5:
            save_used_topic(topic)
            return topic
        tries += 1


# ✅ 4. Przytnij do max X słów
def limit_words(text, max_words=70):
    words = text.split()
    return ' '.join(words[:max_words])

# ✅ 5. Wygeneruj skrypt
def generate_script(topic):
    prompt = (
        f"Write a punchy, fast-paced script for a viral YouTube Shorts video titled: '{topic}'. "
        f"Start with 'What if...' and end with a surprising or mind-blowing twist. "
        f"The script should sound like a popular TikTok or YouTube voiceover — concise, energetic, and curious. "
        f"Use everyday language. Maximum 70 words. Write in English."
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a creative and engaging short-form scriptwriter."},
            {"role": "user", "content": prompt}
        ],
        temperature=1.1,
        max_tokens=300,
    )
    full_script = response.choices[0].message.content.strip()
    return limit_words(full_script, max_words=80)


# ✅ 6. Zapisz do pliku
def save_script_to_file(topic, script):
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    safe_topic = topic.replace(" ", "_").replace("?", "").replace("...", "")
    filename = f"{OUTPUT_FOLDER}/{date_str}__{safe_topic}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"🎯 TEMAT:\n{topic}\n\n🎬 SKRYPT:\n{script}")
    print(f"\n📁 Zapisano do pliku: {filename}")
    return filename, safe_topic

# ✅ 7. Generuj audio (mp3)
def generate_audio(script_text, safe_topic):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": script_text,
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.8
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        audio_path = f"{AUDIO_FOLDER}/{safe_topic}.mp3"
        with open(audio_path, "wb") as f:
            f.write(response.content)
        print(f"🔊 Audio zapisane: {audio_path}")
    else:
        print("❌ Błąd generowania audio:", response.status_code, response.text)

# ✅ 8. RUN
if __name__ == "__main__":
    topic = generate_unique_topic()
    script = generate_script(topic)
    txt_path, safe_topic = save_script_to_file(topic, script)
    print("\n🎯 Temat:", topic)
    print("\n🎬 Skrypt:\n", script)
    generate_audio(script, safe_topic)

