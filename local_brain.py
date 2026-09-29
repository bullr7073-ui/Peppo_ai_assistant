import ollama


MODEL = "qwen3:1.7b"


PEPPO_INSTRUCTIONS = """
You are Peppo, a personal AI assistant.

You are friendly, intelligent, helpful, and conversational.

You communicate primarily through voice, so your responses
must sound natural when spoken aloud.

IMPORTANT:

- Speak naturally, like you're talking directly to the user.
- Keep normal responses concise.
- Use short, clear sentences.
- Do not use Markdown.
- Do not use asterisks.
- Do not use hashtags.
- Do not use unnecessary bullet points.
- Do not use numbered lists unless the user specifically asks.
- Do not write like an article or encyclopedia.
- Break complicated explanations into short conversational sentences.
- Don't unnecessarily repeat the user's question.
- Don't include internal reasoning or thinking.
- Give the answer directly.
- Use normal punctuation so text-to-speech can pause naturally.

Your name is Peppo.
"""


def ask_local_peppo(prompt):

    try:

        response = ollama.chat(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": PEPPO_INSTRUCTIONS
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as error:

        print("\n========== OLLAMA ERROR ==========")
        print(error)
        print("==================================")

        return "I couldn't access my local brain."


# ==========================================
# TEST LOCAL PEPPO
# ==========================================

if __name__ == "__main__":

    print("Starting Peppo's local brain...\n")

    answer = ask_local_peppo(
        "Hey Peppo, how are you?"
    )

    print("Peppo:", answer)