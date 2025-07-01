import os

SCRIPTS_FOLDER = "scripts"

def extract_latest_topic():
    files = [f for f in os.listdir(SCRIPTS_FOLDER) if f.endswith(".txt")]
    latest = max(files, key=lambda f: os.path.getctime(os.path.join(SCRIPTS_FOLDER, f)))

    with open(os.path.join(SCRIPTS_FOLDER, latest), "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Zakładamy, że temat znajduje się w linii zaczynającej się od "What if"
    topic_line = next((l.strip() for l in lines if l.lower().startswith("what if")), lines[0].strip())
    topic = topic_line.replace("What if", "").replace("?", "").strip()

    return topic

def create_runway_prompt(topic):
    # Tworzy cinematic-style prompt na podstawie tematu
    return f"{topic.lower().capitalize()}, cinematic, dramatic lighting, 4K, high detail"

if __name__ == "__main__":
    topic = extract_latest_topic()
    prompt = create_runway_prompt(topic)
    print(f"🎯 Temat: {topic}")
    print(f"🎥 Prompt: {prompt}")
