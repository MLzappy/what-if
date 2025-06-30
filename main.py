from openai import OpenAI

client = OpenAI(
    api_key="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",         
    project="proj_X97B21pdMBTFHNmESfPYkXR2"
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
