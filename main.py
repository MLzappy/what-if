import os
from openai import OpenAI

# Pobieranie klucza i ID projektu z ENV
api_key = os.getenv("OPENAI_API_KEY")
project_id = os.getenv("PROJECT_ID")

# Inicjalizacja klienta OpenAI
client = OpenAI(
    api_key=api_key,
    project=project_id
)

def generate_script():
    prompt = (
        "Napisz krótki, dynamiczny skrypt w stylu YouTube Shorts do filmu "
        "'What if the Earth stopped spinning?'. Zacznij od 'Imagine if...' i zakończ mocnym twistem."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Jesteś kreatywnym scenarzystą krótkich filmów popularnonaukowych."},
            {"role": "user", "content": prompt}
        ],
        temperature=1.0,
        max_tokens=300,
    )

    script = response.choices[0].message.content
    print(script)

if __name__ == "__main__":
    generate_script()
