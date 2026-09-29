import os
import re

import numpy as np
import soundfile as sf
import winsound

from kokoro_onnx import Kokoro


# ==========================================
# KOKORO CONFIGURATION
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "kokoro",
    "kokoro-v1.0.onnx"
)

VOICES_PATH = os.path.join(
    BASE_DIR,
    "kokoro",
    "voices-v1.0.bin"
)

VOICE = "af_river"

SPEED = 1.0


# ==========================================
# LOAD KOKORO
# ==========================================

print("Loading Peppo voice...")

kokoro = Kokoro(
    MODEL_PATH,
    VOICES_PATH
)

print("Peppo voice loaded successfully!")


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
# SPLIT TEXT
# ==========================================

def split_text(text):

    chunks = re.split(
        r"(?<=[.!?])\s+",
        text.strip()
    )

    return [
        chunk.strip()
        for chunk in chunks
        if chunk.strip()
    ]


# ==========================================
# GENERATE RIVER AUDIO
# ==========================================

def generate_speech(text):

    if not text:
        return None

    text = clean_for_speech(text)

    if not text:
        return None

    chunks = split_text(text)

    if not chunks:
        return None

    audio_parts = []

    sample_rate = None

    for chunk in chunks:

        samples, sample_rate = kokoro.create(
            chunk,
            voice=VOICE,
            speed=SPEED,
            lang="en-us"
        )

        audio_parts.append(samples)

        pause_duration = 0.30

        silence = np.zeros(
            int(sample_rate * pause_duration),
            dtype=np.float32
        )

        audio_parts.append(silence)

    final_audio = np.concatenate(
        audio_parts
    )

    output_file = os.path.join(
        BASE_DIR,
        "peppo_output.wav"
    )

    sf.write(
        output_file,
        final_audio,
        sample_rate
    )

    return output_file


# ==========================================
# DESKTOP SPEAK
# ==========================================

def speak(text):

    output_file = generate_speech(text)

    if not output_file:
        return

    winsound.PlaySound(
        output_file,
        winsound.SND_FILENAME
    )


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    test_text = """
    Hello buddy. This is Peppo speaking
    using the River voice.
    """

    print("Testing River voice...")

    speak(test_text)