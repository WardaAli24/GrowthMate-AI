
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Connect to Groq
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Send a message to the AI model
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "I am a QA Engineer. Suggest 3 professional goals for me."
        }
    ]
)

# Display AI response
print(response.choices[0].message.content)
