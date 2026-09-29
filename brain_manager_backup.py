# ==========================================
# PEPPO BRAIN MANAGER
# ==========================================

from brain import ask_peppo as ask_gemini
from rag import ask_peppo_with_memory


# ==========================================
# CURRENT BRAIN
# ==========================================

current_brain = "local"


# ==========================================
# AVAILABLE BRAINS
# ==========================================

BRAINS = {
    "local": "Qwen3 1.7B + RAG",
    "gemini": "Gemini"
}


# ==========================================
# SWITCH BRAIN
# ==========================================

def switch_brain(brain):

    global current_brain

    brain = brain.lower().strip()

    if brain == "local":

        current_brain = "local"

        return (
            "Local brain activated. "
            "I'm now using Qwen3 with my memory."
        )

    elif brain == "gemini":

        current_brain = "gemini"

        return (
            "Cloud brain activated. "
            "I'm now using Gemini."
        )

    else:

        return "I don't recognize that brain."


# ==========================================
# GET CURRENT BRAIN
# ==========================================

def get_current_brain():

    return BRAINS[current_brain]


# ==========================================
# ASK PEPPO
# ==========================================

def ask_peppo(prompt):

    global current_brain

    # ======================================
    # LOCAL BRAIN
    # ======================================

    if current_brain == "local":

        return ask_peppo_with_memory(prompt)


    # ======================================
    # GEMINI
    # ======================================

    elif current_brain == "gemini":

        try:

            return ask_gemini(prompt)

        except RuntimeError as error:

            if str(error) == "GEMINI_QUOTA_EXHAUSTED":

                print("\nGemini quota exhausted.")
                print("Switching Peppo to local brain...")

                current_brain = "local"

                return (
                    "I've reached my Gemini usage limit, "
                    "so I've switched to my local brain."
                )

            raise


    return "I couldn't determine which brain to use."