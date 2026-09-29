import os

from dotenv import load_dotenv
from groq import Groq


# ==========================================
# LOAD ENVIRONMENT
# ==========================================

load_dotenv("keys.env")


# ==========================================
# API KEYS
# ==========================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# ==========================================
# GROQ CLIENT
# ==========================================

groq_client = None

if GROQ_API_KEY:

    groq_client = Groq(
        api_key=GROQ_API_KEY
    )


# ==========================================
# CURRENT BRAIN
# ==========================================

CURRENT_BRAIN = "groq"


# ==========================================
# GROQ MODEL
# ==========================================

GROQ_MODEL = "openai/gpt-oss-20b"


# ==========================================
# SYSTEM PROMPT
# ==========================================

SYSTEM_PROMPT = """
You are Peppo, a personal AI voice assistant.

PERSONALITY:
- Friendly, natural and slightly witty.
- Talk like a smart friend.
- Use short, clever humor occasionally.
- Never force jokes.
- Be serious when the topic is serious.
- Match the user's mood and tone.

VOICE:
- Your responses will be spoken aloud.
- Use natural conversational sentences.
- Do not use Markdown.
- Do not use bullet points.
- Do not use headings.
- Do not use emojis.
- Avoid symbols that sound strange when spoken.

RESPONSE LENGTH:
- Keep normal answers short.
- Usually answer in 1 to 4 sentences.
- Give more detail only when the user asks for it.

TECHNICAL QUESTIONS:
- Give the useful answer first.
- Explain clearly and accurately.
- Do not add unnecessary information.

IMPORTANT:
You are Peppo.
Be helpful first.
Be funny sometimes.
Know when to stop.
"""


# ==========================================
# GROQ BRAIN
# ==========================================

def ask_groq(user_input):

    if not groq_client:

        raise RuntimeError(
            "Groq API key is not configured."
        )

    response = groq_client.chat.completions.create(

        model=GROQ_MODEL,

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_input
            }
        ],

        # Faster reasoning for voice conversations
        reasoning_effort="low",

        # Keep responses natural and focused
        temperature=0.4,

        # Shorter output = faster response
        max_completion_tokens=160
    )

    return response.choices[0].message.content.strip()


# ==========================================
# GROQ WEB-GROUNDED ANSWER
# ==========================================

def ask_groq_with_web(
    user_input,
    web_results,
    wikipedia_results
):

    if not groq_client:

        raise RuntimeError(
            "Groq API key is not configured."
        )

    context_parts = []


    # --------------------------------------
    # DUCKDUCKGO RESULTS
    # --------------------------------------

    for result in web_results:

        title = result.get(
            "title",
            ""
        )

        description = result.get(
            "description",
            ""
        )

        url = result.get(
            "url",
            ""
        )

        context_parts.append(
            f"Source: {title}\n"
            f"Description: {description}\n"
            f"URL: {url}"
        )


    # --------------------------------------
    # WIKIPEDIA RESULTS
    # --------------------------------------

    for result in wikipedia_results:

        title = result.get(
            "title",
            ""
        )

        description = result.get(
            "description",
            ""
        )

        summary = result.get(
            "summary",
            ""
        )

        url = result.get(
            "url",
            ""
        )

        context_parts.append(
            f"Source: {title}\n"
            f"Description: {description}\n"
            f"Summary: {summary}\n"
            f"URL: {url}"
        )


    # --------------------------------------
    # COMBINE SOURCES
    # --------------------------------------

    web_context = "\n\n".join(
        context_parts
    )


    # --------------------------------------
    # WEB SYSTEM PROMPT
    # --------------------------------------

    web_system_prompt = """
You are Peppo, a personal AI voice assistant.

Answer the user's question using the supplied web information.

VOICE RULES:
- Use natural spoken sentences.
- Do not use Markdown.
- Do not use bullet points.
- Do not use numbered lists.
- Do not use headings.
- Do not use bold or italic formatting.
- Do not use emojis.
- Keep the answer concise.
- Do not invent facts.
- Use the supplied sources as the primary factual basis.

If the sources do not contain enough information,
say so clearly.
"""


    # --------------------------------------
    # GROQ REQUEST
    # --------------------------------------

    response = groq_client.chat.completions.create(

        model=GROQ_MODEL,

        messages=[
            {
                "role": "system",
                "content": web_system_prompt
            },
            {
                "role": "user",
                "content": (
                    f"User question:\n"
                    f"{user_input}\n\n"
                    f"Web sources:\n"
                    f"{web_context}"
                )
            }
        ],

        reasoning_effort="low",

        temperature=0.4,

        max_completion_tokens=220
    )

    return response.choices[0].message.content.strip()


# ==========================================
# GEMINI BRAIN
# ==========================================

def ask_gemini(user_input):

    raise RuntimeError(
        "Gemini brain is not connected in this version."
    )


# ==========================================
# LOCAL QWEN BRAIN
# ==========================================

def ask_local(user_input):

    try:

        import requests

        response = requests.post(

            "http://localhost:11434/api/chat",

            json={
                "model": "qwen3-vl:4b",

                "messages": [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],

                "stream": False
            },

            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        return data["message"]["content"].strip()

    except Exception as error:

        raise RuntimeError(
            f"Local Qwen error: {error}"
        )


# ==========================================
# MAIN PEPPO FUNCTION
# ==========================================

def ask_peppo(user_input):

    global CURRENT_BRAIN


    # --------------------------------------
    # GROQ
    # --------------------------------------

    if CURRENT_BRAIN == "groq":

        try:

            return ask_groq(
                user_input
            )

        except Exception as error:

            print(
                "\nGroq error:",
                error
            )

            print(
                "Falling back to local Qwen..."
            )

            try:

                return ask_local(
                    user_input
                )

            except Exception as local_error:

                print(
                    "\nQwen fallback error:",
                    local_error
                )

                return (
                    "Sorry Sir, "
                    "I'm having trouble connecting "
                    "to my brain right now."
                )


    # --------------------------------------
    # GEMINI
    # --------------------------------------

    if CURRENT_BRAIN == "gemini":

        try:

            return ask_gemini(
                user_input
            )

        except Exception as error:

            print(
                "\nGemini error:",
                error
            )

            print(
                "Falling back to Groq..."
            )

            try:

                return ask_groq(
                    user_input
                )

            except Exception as groq_error:

                print(
                    "\nGroq fallback error:",
                    groq_error
                )

                return ask_local(
                    user_input
                )


    # --------------------------------------
    # LOCAL
    # --------------------------------------

    if CURRENT_BRAIN == "local":

        return ask_local(
            user_input
        )


    # --------------------------------------
    # UNKNOWN BRAIN
    # --------------------------------------

    return ask_groq(
        user_input
    )


# ==========================================
# BRAIN SWITCHING
# ==========================================

def switch_brain(brain):

    global CURRENT_BRAIN

    brain = brain.lower().strip()


    # --------------------------------------
    # GROQ
    # --------------------------------------

    if brain == "groq":

        CURRENT_BRAIN = "groq"

        return (
            "Alright Sir. "
            "I'm now using Groq."
        )


    # --------------------------------------
    # GEMINI
    # --------------------------------------

    if brain == "gemini":

        CURRENT_BRAIN = "gemini"

        return (
            "Alright Sir. "
            "I'm now using Gemini."
        )


    # --------------------------------------
    # LOCAL
    # --------------------------------------

    if brain == "local":

        CURRENT_BRAIN = "local"

        return (
            "Alright Sir. "
            "I'm now using my local brain."
        )


    return (
        "I don't recognize that brain."
    )