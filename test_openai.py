import os
from openai import OpenAI

import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("OpenAI client initialized successfully")

# Test a simple API call
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
    max_tokens=10
)
print(response.choices[0].message.content)
