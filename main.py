from openai import OpenAI

client = OpenAI(
    api_key="sk-proj-...",         # ← Twój pełny klucz API
    project="proj_xxxxxxxxxxxx"    # ← Twój project_id
)

def generate_script():
    prompt = (
        "Napisz krótki skrypt do shorta YouTube na temat: What if the Earth stopped spinning?"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Jesteś kreatywnym scenarzystą filmów."},
            {"role": "user", "content": prompt}
        ]
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    generate_script()
