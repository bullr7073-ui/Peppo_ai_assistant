import os
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro


# ==============================
# PATHS
# ==============================

MODEL_PATH = os.path.join("kokoro", "kokoro-v1.0.onnx")
VOICES_PATH = os.path.join("kokoro", "voices-v1.0.bin")


# ==============================
# LOAD KOKORO
# ==============================

print("Loading Kokoro...")

kokoro = Kokoro(
    MODEL_PATH,
    VOICES_PATH
)

print("Kokoro loaded successfully!\n")


# ==============================
# SETTINGS
# ==============================

VOICE = "af_river"
SPEED = 1.0



# ==============================
# SPEECH SEGMENTS
# ==============================

segments = [
    ("The Porsche engineers knew exactly what they wanted to achieve.", 0.8),

    ("A machine that could deliver incredible speed, without sacrificing control.", 1.0),

    ("Every curve of the body was designed with a purpose.", 0.7),

    ("Every line was shaped to move air more efficiently.", 0.8),

    ("And beneath it all was an engine built to respond the moment the driver demanded more.", 1.2),

    ("This isn't simply a car built to go fast.", 1.0),

    ("It's a machine built around the idea that speed should feel effortless.", 1.3),

    ("Push the throttle.", 0.9),

    ("And the world begins to disappear behind you.", 1.2),

    ("The road becomes narrower.", 0.7),

    ("The corners arrive faster.", 0.9),

    ("And for a moment, there is nothing left to think about.", 1.4),

    ("Just the engine.", 0.7),

    ("The road.", 0.7),

    ("And the next turn.", 1.5),

    ("This is what happens when engineering stops being about numbers, and becomes something you can feel.", 2.0),
]


# ==============================
# GENERATE AUDIO
# ==============================

audio_parts = []

print(f"Generating voice: {VOICE}")
print(f"Speed: {SPEED}\n")

for index, (text, pause) in enumerate(segments, start=1):

    print(f"[{index}/{len(segments)}] {text}")

    samples, sample_rate = kokoro.create(
        text,
        voice=VOICE,
        speed=SPEED,
        lang="en-us"
    )

    audio_parts.append(samples)

    # Add controlled silence after each sentence
    silence = np.zeros(
        int(sample_rate * pause),
        dtype=np.float32
    )

    audio_parts.append(silence)


# ==============================
# COMBINE EVERYTHING
# ==============================

final_audio = np.concatenate(audio_parts)


# ==============================
# SAVE
# ==============================

output_file = "peppo_river_cinematic.wav"

sf.write(
    output_file,
    final_audio,
)


print("\n===================================")
print("River cinematic test complete!")
print(f"Created: {output_file}")
print("===================================")