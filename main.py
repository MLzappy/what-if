import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_script():
    prompt = (
        "Napisz krótki (ok. 100 słów), dynamiczny skrypt w stylu YouTube Shorts "
        "do odcinka 'What if the Earth stopped spinning?'. Użyj emocji, prostego języka, "
        "zacznij od 'Imagine if...' i zakończ czymś szokującym."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Jesteś kreatywnym scenarzystą filmów ciekawostkowych na YouTube."},
            {"role": "user", "content": prompt}
        ],
        temperature=1.0,
        max_tokens=300,
    )

    script = response['choices'][0]['message']['content']
    print(script)

if __name__ == "__main__":
    generate_script()

