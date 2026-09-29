import re
import speech_recognition as sr

from intent_parser import parse_intent

from action_router import handle_intent

from brain_manager import (
    ask_peppo,
    switch_brain,
    ask_groq_with_web
)

from tts_manager import speak

from web_manager import (
    web_search,
    wikipedia_search
)

# ==========================================
# INITIALIZE
# ==========================================

recognizer = sr.Recognizer()

recognizer.pause_threshold = 1.2
recognizer.non_speaking_duration = 0.8
recognizer.dynamic_energy_threshold = True


# ==========================================
# CLEAN TEXT FOR SPEECH
# ==========================================

def clean_for_speech(text):

    # Remove emojis
    text = re.sub(
        r"[\U0001F000-\U0001FAFF"
        r"\U00002700-\U000027BF"
        r"\U0001F1E6-\U0001F1FF"
        r"\U00002600-\U000026FF]+",
        "",
        text
    )

    # Remove code blocks
    text = re.sub(
        r"```.*?```",
        "",
        text,
        flags=re.DOTALL
    )

    # Remove inline code
    text = re.sub(
        r"`([^`]*)`",
        r"\1",
        text
    )

    # Remove Markdown emphasis
    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("*", "")
    text = text.replace("_", " ")

    # Remove headings
    text = re.sub(
        r"^#+\s*",
        "",
        text,
        flags=re.MULTILINE
    )

    # Remove bullet symbols
    text = re.sub(
        r"^\s*[-•]\s*",
        "",
        text,
        flags=re.MULTILINE
    )

    # Remove numbered-list formatting
    text = re.sub(
        r"^\s*\d+\.\s*",
        "",
        text,
        flags=re.MULTILINE
    )

    # Convert Markdown links to visible text
    text = re.sub(
        r"\[([^\]]+)\]\([^)]+\)",
        r"\1",
        text
    )

    # Remove excessive whitespace
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

        corrected_word = corrections.get(
            word.lower(),
            word
        )

        corrected_words.append(
            corrected_word
        )

    return " ".join(
        corrected_words
    )


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

def detect_brain_command(text):

    text = text.lower().strip()

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

    groq_phrases = [

    "switch to groq",
    "use groq",
    "activate groq",
    "use groq brain",
    "switch to groq brain"

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
# EXIT COMMANDS
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
# MAIN
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
        "Hello Sir , How can I help you today?"
    )


    # --------------------------------------
    # MAIN LOOP
    # --------------------------------------

    while True:

        user_input = listen()

        if user_input is None:

            continue


        # ==================================
        # CLEAN TEXT
        # ==================================

        text = user_input.lower().strip()


        # ==================================
        # BRAIN SWITCH
        # ==================================

        brain_command = detect_brain_command(
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
                "Alright Sir" 
                "see you later."
            )

            break


        # ==================================
        # PARSE INTENT
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
        # WEB SEARCH
        # ==================================

        if intent == "web_search":

            try:

                query = intent_data.get(
                    "query",
                    user_input
                )

                print(
                    f"\nWeb query: {query}"
                )


                # --------------------------
                # DUCKDUCKGO
                # --------------------------

                web_data = web_search(
                    query
                )

                web_results = web_data.get(
                    "results",
                    []
                )


                # --------------------------
                # WIKIPEDIA
                # --------------------------

                wiki_data = wikipedia_search(
                    query
                )

                wikipedia_results = wiki_data.get(
                    "results",
                    []
                )


                print(
                    f"\nDuckDuckGo results: "
                    f"{len(web_results)}"
                )

                print(
                    f"Wikipedia results: "
                    f"{len(wikipedia_results)}"
                )


                # --------------------------
                # CHECK RESULTS
                # --------------------------

                if (
                    not web_results
                    and
                    not wikipedia_results
                ):

                    speak(
                        "Sorry Sir, "
                        "I couldn't find anything useful "
                        "on the web."
                    )

                    continue


                # --------------------------
                # GROQ SYNTHESIS
                # --------------------------

                response = ask_groq_with_web(

                    user_input,

                    web_results,

                    wikipedia_results

                )


                speak(
                    response
                )


            except Exception as error:

                print(
                    "\nWeb search error:",
                    error
                )


                # --------------------------
                # FALLBACK
                # --------------------------

                try:

                    response = ask_peppo(
                        user_input
                    )

                    speak(
                        response
                    )

                except Exception as fallback_error:

                    print(
                        "\nFallback error:",
                        fallback_error
                    )

                    speak(
                        "Sorry Sir, "
                        "I couldn't process that "
                        "right now."
                    )

            continue


        # ==================================
        # NORMAL CHAT
        # ==================================

        if intent == "normal_chat":

            try:

                response = ask_peppo(
                    user_input
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
        # HANDLE COMMAND INTENTS
        # ==================================

        try:

            response = handle_intent(
                intent_data
            )

            if response:

                speak(
                    response
                )

            else:

                # --------------------------
                # FALLBACK TO NORMAL AI
                # --------------------------

                response = ask_peppo(
                    user_input
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