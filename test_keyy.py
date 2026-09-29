import os
import time

from dotenv import load_dotenv
from groq import Groq


# ==========================================
# LOAD API KEY
# ==========================================

load_dotenv("keys.env")

groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    print("Groq API key not found.")
    exit()


# ==========================================
# CREATE GROQ CLIENT
# ==========================================

client = Groq(
    api_key=groq_key
)


# ==========================================
# TEST MESSAGE
# ==========================================

print("\nPeppo is thinking...\n")

start_time = time.perf_counter()


response = client.chat.completions.create(
    model="openai/gpt-oss-20b",

    messages=[
        {
            "role": "system",
            "content": (
                "You are Peppo, a fast personal AI assistant. "
                "Keep your answers concise and natural."
            )
        },

        {
            "role": "user",
            "content": "Hello Peppo, how are you?"
        }
    ],

    max_completion_tokens=100
)


end_time = time.perf_counter()


# ==========================================
# GET RESPONSE
# ==========================================

answer = response.choices[0].message.content


# ==========================================
# DISPLAY
# ==========================================

print("Peppo:")
print(answer)

print(
    f"\nResponse time: "
    f"{end_time - start_time:.2f} seconds"
)