import re
import speech_recognition as sr

from intent_parser import parse_intent
from action_router import handle_intent

from brain_manager import (
    ask_peppo,
    switch_brain
)

from tts_manager import speak


# ==========================================
# INITIALIZE
# ==========================================

recognizer = sr.Recognizer()

recognizer.pause_threshold = 1.2
recognizer.non_speaking_duration = 0.8
recognizer.dynamic_energy_threshold = True


# ==========================================
# WAKE WORDS
# ==========================================

WAKE_WORDS = [
    "hey peppo",
    "hello peppo",
    "hi peppo",
    "peppo",
    "hey pappo",
    "hello pappo",
    "pappo",
    "hey pepo",
    "hello pepo",
    "pepo",
    "hey peppa",
    "hello peppa",
    "peppa",
    "hey paper",
    "hello paper",
    "paper"
]


# ==========================================
# CLEAN TEXT FOR SPEECH
# ==========================================

def clean_for_speech(text):

    text = str(text)

    text = re.sub(
        r"```.*?```",
        "",
        text,
        flags=re.DOTALL
    )

    text = re.sub(
        r"`([^`]*)`",
        r"\1",
        text
    )

    text = re.sub(
        r"\[([^\]]+)\]\([^)]+\)",
        r"\1",
        text
    )

    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("*", "")
    text = text.replace("_", " ")

    text = re.sub(
        r"^#+\s*",
        "",
        text,
        flags=re.MULTILINE
    )

    text = re.sub(
        r"^\s*[-•]\s*",
        "",
        text,
        flags=re.MULTILINE
    )

    text = re.sub(
        r"^\s*\d+\.\s*",
        "",
        text,
        flags=re.MULTILINE
    )

    text = re.sub(
        r"[\U0001F000-\U0001FAFF"
        r"\U00002700-\U000027BF"
        r"\U0001F1E6-\U0001F1FF"
        r"\U00002600-\U000026FF]+",
        "",
        text
    )

    text = text.replace("→", "")
    text = text.replace("←", "")
    text = text.replace("•", "")
    text = text.replace("—", ", ")
    text = text.replace("–", "-")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ==========================================
# CORRECT SPEECH RECOGNITION MISTAKES
# ==========================================

def correct_words(text):

    corrections = {
        "paper": "Peppo",
        "pappu": "Peppo",
        "pappo": "Peppo",
        "pepo": "Peppo",
        "peppa": "Peppo",
        "peppo": "Peppo"
    }

    words = text.split()

    corrected_words = []

    for word in words:

        # Keep punctuation attached to the word
        punctuation = ""

        while word and word[-1] in ",.!?":

            punctuation = word[-1] + punctuation
            word = word[:-1]

        corrected_word = corrections.get(
            word.lower(),
            word
        )

        corrected_words.append(
            corrected_word + punctuation
        )

    return " ".join(corrected_words)


# ==========================================
# EXTRACT WAKE WORD + COMMAND
# ==========================================

def extract_wake_command(text):

    if not text:
        return False, ""

    original_text = text.strip()

    # --------------------------------------
    # NORMALIZE FOR MATCHING
    # --------------------------------------

    normalized = re.sub(
        r"\s+",
        " ",
        original_text.lower()
    ).strip()

    # --------------------------------------
    # SORT LONGEST FIRST
    # --------------------------------------

    sorted_wake_words = sorted(
        WAKE_WORDS,
        key=len,
        reverse=True
    )

    # --------------------------------------
    # CHECK WAKE WORD
    # --------------------------------------

    for wake_word in sorted_wake_words:

        pattern = (
            r"^"
            + re.escape(wake_word)
            + r"\b"
        )

        match = re.match(
            pattern,
            normalized
        )

        if match:

            # Remove the same number of characters
            # from the original recognized text.

            command = original_text[
                match.end():
            ].strip()

            # ----------------------------------
            # REMOVE PUNCTUATION AFTER WAKE WORD
            # ----------------------------------

            command = re.sub(
                r"^[,\-:;.!?\s]+",
                "",
                command
            ).strip()

            print(
                "Wake word detected:",
                wake_word
            )

            if command:

                print(
                    "Command after wake word:",
                    command
                )

                return True, command

            # Wake word only
            return True, ""

    # --------------------------------------
    # NO WAKE WORD
    # --------------------------------------

    return False, original_text


# ==========================================
# MICROPHONE CALIBRATION
# ==========================================

def calibrate_microphone():

    with sr.Microphone() as source:

        print(
            "Calibrating microphone..."
        )

        recognizer.adjust_for_ambient_noise(
            source,
            duration=0.5
        )

        print(
            "Microphone ready."
        )


# ==========================================
# LISTEN
# ==========================================

def listen():

    with sr.Microphone() as source:

        print(
            "\nListening..."
        )

        try:

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=30
            )

        except sr.WaitTimeoutError:

            print(
                "I didn't hear anything."
            )

            return None

        try:

            text = recognizer.recognize_google(
                audio
            )

            text = correct_words(
                text
            )

            print(
                "You:",
                text
            )

            return text

        except sr.UnknownValueError:

            print(
                "I couldn't understand you."
            )

            return None

        except sr.RequestError:

            print(
                "Speech recognition service "
                "is unavailable."
            )

            return None


# ==========================================
# BRAIN SWITCHING
# ==========================================

def detect_brain_switch(text):

    text = text.lower().strip()

    groq_phrases = [

        "switch to groq",
        "use groq",
        "activate groq",
        "use groq brain",
        "switch to groq brain"

    ]

    gemini_phrases = [

        "switch to gemini",
        "use gemini",
        "activate gemini",
        "use cloud brain",
        "switch to cloud",
        "activate cloud brain"

    ]

    local_phrases = [

        "switch to local",
        "use local",
        "use qwen",
        "switch to qwen",
        "activate local brain",
        "use local brain"

    ]

    for phrase in groq_phrases:

        if phrase in text:

            return "groq"

    for phrase in gemini_phrases:

        if phrase in text:

            return "gemini"

    for phrase in local_phrases:

        if phrase in text:

            return "local"

    return None


# ==========================================
# EXIT COMMAND
# ==========================================

def is_exit_command(text):

    text = text.lower().strip()

    exit_phrases = [

        "goodbye",
        "good bye",
        "bye",
        "bye bye",
        "see you",
        "see ya",
        "see you later",
        "talk to you later",
        "catch you later",
        "i'm off",
        "im off",
        "i am off",
        "i'm done",
        "im done",
        "i am done",
        "that's all",
        "thats all",
        "that is all",
        "good night",
        "goodnight",
        "peace",
        "gotta go",
        "have to go"

    ]

    return any(
        phrase in text
        for phrase in exit_phrases
    )


# ==========================================
# MAIN CONVERSATION LOOP
# ==========================================

def main():

    # --------------------------------------
    # MICROPHONE
    # --------------------------------------

    calibrate_microphone()

    # --------------------------------------
    # GREETING
    # --------------------------------------

    speak(
        "Hello Sir! How can I assist you?"
    )

    # --------------------------------------
    # MAIN LOOP
    # --------------------------------------

    while True:

        user_input = listen()

        if user_input is None:
            continue

        # ==================================
        # WAKE WORD PROCESSING
        # ==================================

        wake_detected, command = extract_wake_command(
            user_input
        )

        # ----------------------------------
        # WAKE WORD ONLY
        # ----------------------------------

        if wake_detected and not command:

            speak(
                "Hello buddy. What can I help you with?"
            )

            continue

        # ----------------------------------
        # IMPORTANT
        #
        # If the user said:
        #
        # "Hey Peppo, describe New Delhi"
        #
        # command becomes:
        #
        # "describe New Delhi"
        #
        # This command is now sent to the AI.
        # ----------------------------------

        if wake_detected:

            user_input = command

        # ==================================
        # BRAIN SWITCH
        # ==================================

        brain_command = detect_brain_switch(
            user_input
        )

        if brain_command:

            try:

                response = switch_brain(
                    brain_command
                )

                speak(
                    response
                )

            except Exception as error:

                print(
                    "\nBrain switch error:",
                    error
                )

                speak(
                    "Sorry Sir, I couldn't switch brains."
                )

            continue

        # ==================================
        # EXIT
        # ==================================

        if is_exit_command(
            user_input
        ):

            speak(
                "Alright Sir, see you later."
            )

            break

        # ==================================
        # INTENT PARSER
        # ==================================

        try:

            intent_data = parse_intent(
                user_input
            )

            print(
                "\nIntent:",
                intent_data
            )

        except Exception as error:

            print(
                "\nIntent parser error:",
                error
            )

            intent_data = {
                "intent": "normal_chat"
            }

        # ==================================
        # GET INTENT
        # ==================================

        intent = intent_data.get(
            "intent"
        )

        # ==================================
        # NORMAL CHAT
        # ==================================

        if intent == "normal_chat":

            try:

                response = ask_peppo(
                    user_input
                )

                print(
                    "\nPeppo:",
                    response
                )

                speak(
                    response
                )

            except Exception as error:

                print(
                    "\nAI error:",
                    error
                )

                speak(
                    "Sorry buddy, I ran into a problem "
                    "while processing that."
                )

            continue

        # ==================================
        # HANDLE INTENT
        # ==================================

        try:

            response = handle_intent(
                intent_data
            )

            if response:

                print(
                    "\nPeppo:",
                    response
                )

                speak(
                    response
                )

            else:

                response = ask_peppo(
                    user_input
                )

                print(
                    "\nPeppo:",
                    response
                )

                speak(
                    response
                )

        except Exception as error:

            print(
                "\nAction router error:",
                error
            )

            speak(
                "Sorry buddy, I ran into a problem "
                "while processing that."
            )


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":

    main()