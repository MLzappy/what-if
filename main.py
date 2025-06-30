import os
from openai import OpenAI

# Debug: sprawdź, czy zmienne są widoczne
print("API_KEY:", os.getenv("OPENAI_API_KEY"))
print("PROJECT_ID:", os.getenv("PROJECT_ID"))

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    project=os.getenv("PROJECT_ID")
)

def generate_script():
    prompt = (
        "Napisz krótki, dynamiczny skrypt w stylu YouTube Shorts do filmu "
        "'What if the Earth stopped spinning?'. Zacznij od 'Imagine if...' i zakończ mocnym twistem."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Jesteś kreatywnym scenarzystą filmów."},
            {"role": "user", "content": prompt}
        ],
        temperature=1.0,
        max_tokens=300,
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    generate_script()
