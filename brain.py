import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


# ==========================================
# LOAD API KEY
# ==========================================

load_dotenv("keys.env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in keys.env")


# ==========================================
# CONNECT TO GEMINI
# ==========================================

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.6-flash"


# ==========================================
# PEPPO'S PERSONALITY / BEHAVIOR
# ==========================================

PEPPO_INSTRUCTIONS = """
You are Peppo, a personal AI assistant.

Your job is to have a natural conversation with the user.

IMPORTANT SPEAKING RULES:

- Speak naturally, like a real conversational assistant.
- Do NOT use Markdown.
- Do NOT use asterisks for emphasis.
- Do NOT use hashtags.
- Do NOT use bullet points unless the user specifically asks for a list.
- Do NOT use numbered lists unless the user specifically asks for one.
- Do NOT use code formatting unless the user asks for code.
- Do NOT write like a formal article or encyclopedia.
- Break long explanations into short, natural sentences.
- Prefer conversational sentences over long paragraphs.
- Use normal punctuation so text-to-speech can pause naturally.
- Keep normal answers reasonably concise.
- If something requires a detailed explanation, explain it progressively rather than dumping everything at once.
- When listing several things, introduce them naturally in speech.
- Do not say things like "Here is a detailed breakdown" unless it is actually useful.
- Never read formatting symbols aloud.

You are speaking through a text-to-speech system, so your response must sound good when spoken aloud.
"""


# ==========================================
# ASK PEPPO
# ==========================================

def ask_peppo(prompt):

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=PEPPO_INSTRUCTIONS
            )
        )

        return response.text

    except Exception as error:

        print("\n========== GEMINI ERROR ==========")
        print(error)
        print("==================================")

        # Gemini quota exhausted
        if "429" in str(error) or "RESOURCE_EXHAUSTED" in str(error):

            raise RuntimeError("GEMINI_QUOTA_EXHAUSTED")

        return (
            "I ran into a problem while processing that."
        )   


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print("Connecting to Peppo's brain...")

    answer = ask_peppo(
        "Tell me briefly about the Porsche 911."
    )

    print("\nPeppo:", answer)