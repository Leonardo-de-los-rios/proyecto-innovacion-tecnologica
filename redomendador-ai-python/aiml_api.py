import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

base_url = "https://api.aimlapi.com/v1"
api_key = os.environ["AI_ML_API_KEY"]
system_prompt = "Eres un experto en política y economía de Argentina"
user_prompt = (
    "Cual es el ultimo precio que tienes del dolar y de que fecha es en argentina?"
)


api = OpenAI(api_key=api_key, base_url=base_url)


def main():
    completion = api.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=256,
    )

    response = completion.choices[0].message.content

    print("User:", user_prompt)
    print("AI:", response)


if __name__ == "__main__":
    main()
