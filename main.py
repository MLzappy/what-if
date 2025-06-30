from openai import OpenAI

client = OpenAI(api_key="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")  # <<< bez spacji

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
