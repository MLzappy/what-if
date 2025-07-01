import os
from datetime import datetime

SCRIPTS_FOLDER = "scripts"
BACKGROUND_FOLDER = "backgrounds"

def extract_latest_topic():
    files = [f for f in os.listdir(SCRIPTS_FOLDER) if f.endswith(".txt")]
    latest = max(files, key=lambda f: os.path.getctime(os.path.join(SCRIPTS_FOLDER, f)))

    with open(os.path.join(SCRIPTS_FOLDER, latest), "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Zakładamy, że temat znajduje się w linii zaczynającej się od "What if"
    topic_line = next((l.strip() for l in lines if l.lower().startswith("what if")), lines[0].strip())
    topic = topic_line.replace("What if", "").replace("?", "").strip()

    return topic

def create_prompt(topic):
    return f"{topic.lower().capitalize()}, cinematic, dramatic lighting, 4K, high detail"

if __name__ == "__main__":
    os.makedirs(BACKGROUND_FOLDER, exist_ok=True)

    topic = extract_latest_topic()
    prompt = create_prompt(topic)

    # 📁 Zapisz do backgrounds/prompt.txt (do użycia wideo)
    with open(os.path.join(BACKGROUND_FOLDER, "prompt.txt"), "w", encoding="utf-8") as f:
        f.write(prompt)

    # 📁 Zapisz także z datą (dla historii)
    date_str = datetime.now().strftime("%Y-%m-%d")
    dated_path = os.path.join(BACKGROUND_FOLDER, f"{date_str}__prompt.txt")
    with open(dated_path, "w", encoding="utf-8") as f:
        f.write(prompt)

    print(f"🎯 Temat: {topic}")
    print(f"🎥 Prompt zapisany do prompt.txt i {dated_path}:\n{prompt}")
