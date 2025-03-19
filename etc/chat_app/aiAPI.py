from openai import OpenAI

q = "3.11 vs 3.19"

client = OpenAI(api_key="")
response = client.chat.completions.with_raw_response.create(
    messages=[{
        "role": "user",
        "content": q,
    }],
    model="gpt-4o-mini",
)

completion = response.parse()
print(completion.choices[0].message.content)