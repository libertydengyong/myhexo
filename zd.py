import os
import datetime
from openai import OpenAI
try:
    client = OpenAI(
        api_key=os.environ.get("AI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    )

    response = client.chat.completions.create(
        model="gemini-1.5-flash",
        messages=[
            {"role": "system", "content": "You are an expert blogger."},
            {"role": "user", "content": "Write a post about paid surveys."}
        ]
    )

    print("response =", response)
    print("choices =", getattr(response, "choices", None))

    content = response.choices[0].message.content

    today = datetime.date.today().strftime("%Y-%m-%d")
    filename = f"source/_posts/paid-survey-{today}.md"

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print("Success:", filename)

except Exception as e:
    print("Error:", e)
