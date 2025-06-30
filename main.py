from openai import OpenAI

client = OpenAI(
    api_key="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",
    project="proj_X97B21pdMBTFHNmESfPYkXR2"
)

def generate_script():
    prompt = (
        "Napisz krótki (ok. 100 słów), dynamiczny skrypt w stylu YouTube Shorts "
        "do odcinka 'What if the Earth stopped spinning?'. Zacznij od 'Imagine if...' i zakończ czymś zaskakującym."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Jesteś kreatywnym scenarzystą filmów ciekawostkowych na YouTube."},
            {"role": "user", "content": prompt}
        ],
        temperature=1.0,
        max_tokens=300,
    )

    script = response.choices[0].message.content
    print(script)

if __name__ == "__main__":
    generate_script()
