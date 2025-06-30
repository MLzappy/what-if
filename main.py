import os
import datetime
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    project=os.getenv("PROJECT_ID")
)

USED_TOPICS_FILE = "used_topics.txt"
OUTPUT_FOLDER = "scripts"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 1️⃣ Wczytaj poprzednie tematy
def get_used_topics():
    if not os.path.exists(USED_TOPICS_FILE):
        return set()
    with open(USED_TOPICS_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f.readlines())

# 2️⃣ Zapisz nowy temat do listy
def save_used_topic(topic):
    with open(USED_TOPICS_FILE, "a", encoding="utf-8") as f:
        f.write(topic + "\n")

# 3️⃣ Wygeneruj nowy temat, jeśli jeszcze go nie było
def generate_unique_topic():
    used_topics = get_used_topics()
    tries = 0
    while True:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Wymyśl oryginalny temat zaczynający się od 'What if...'"}
            ],
            temperature=1.2,
            max_tokens=30
        )
        topic = response.choices[0].message.content.strip()
        if topic not in used_topics or tries > 5:
            save_used_topic(topic)
            return topic
        tries += 1

# 4️⃣ Wygeneruj skrypt
def generate_script(topic):
    prompt = (
        f"Napisz krótki, dynamiczny skrypt do YouTube Shorts "
        f"na temat: '{topic}'. Zacznij od 'Imagine if...' "
        f"i zakończ zaskakującym twistem. Max 150 słów."
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Jesteś kreatywnym scenarzystą."},
            {"role": "user", "content": prompt}
        ],
        temperature=1.0,
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()

# 5️⃣ Zapisz cały skrypt do pliku z datą
def save_script_to_file(topic, script):
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    safe_topic = topic.replace(" ", "_").replace("?", "").replace("...", "")
    filename = f"{OUTPUT_FOLDER}/{date_str}__{safe_topic}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"🎯 TEMAT:\n{topic}\n\n🎬 SKRYPT:\n{script}")
    print(f"\n📁 Zapisano do pliku: {filename}")

# 6️⃣ RUN
if __name__ == "__main__":
    topic = generate_unique_topic()
    script = generate_script(topic)
    save_script_to_file(topic, script)

    print("\n🎯 Temat:", topic)
    print("\n🎬 Skrypt:\n", script)
