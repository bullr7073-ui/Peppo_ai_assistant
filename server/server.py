import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from brain_manager import ask_peppo
from tts_manager import generate_speech


# ==========================================
# PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

WEB_DIR = BASE_DIR / "web"

# Stores the EXACT audio file generated
# by River / Kokoro for the latest response.
AUDIO_FILE = None


# ==========================================
# FASTAPI
# ==========================================

app = FastAPI()


# ==========================================
# WEB FILES
# ==========================================

app.mount(
    "/web",
    StaticFiles(directory=WEB_DIR),
    name="web"
)


@app.get("/ui")
def peppo_ui():

    return FileResponse(
        WEB_DIR / "index.html"
    )


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():

    return {
        "status": "online",
        "assistant": "Peppo"
    }


# ==========================================
# CHAT
# ==========================================

@app.post("/chat")
def chat(data: dict):

    global AUDIO_FILE

    user_message = data.get(
        "message",
        ""
    ).strip()


    # --------------------------------------
    # EMPTY MESSAGE
    # --------------------------------------

    if not user_message:

        return {
            "response": "I didn't receive anything.",
            "audio": None
        }


    try:

        print(
            "\n================================="
        )

        print(
            "USER:",
            user_message
        )


        # ==================================
        # ASK PEPPO
        # ==================================

        response = ask_peppo(
            user_message
        )


        print(
            "PEPPO:",
            response
        )


        # ==================================
        # GENERATE RIVER AUDIO
        # ==================================

        print(
            "Generating River voice..."
        )


        audio_file = generate_speech(
            response
        )
        print("========== TTS DEBUG ==========")
        print("generate_speech returned:", audio_file)
        print("type:", type(audio_file))

        if audio_file:
            print("Path:", Path(audio_file))
            print("Exists:", Path(audio_file).exists())

        print("===============================")


        print(
            "River audio returned:",
            audio_file
        )


        # ==================================
        # CHECK AUDIO PATH
        # ==================================

        if audio_file:

            generated_file = Path(
                audio_file
            ).resolve()


            print(
                "Checking audio file:"
            )

            print(
                generated_file
            )


            # ------------------------------
            # FILE EXISTS
            # ------------------------------

            if generated_file.exists():

                # Store exact generated file
                AUDIO_FILE = generated_file


                print(
                    "River audio generated successfully!"
                )

                print(
                    "Audio file:",
                    AUDIO_FILE
                )

                print(
                    "Audio URL: /audio"
                )

                print(
                    "================================="
                )


                # IMPORTANT:
                #
                # This MUST contain "audio".
                #
                # scripts.js reads:
                #
                # data.audio
                #
                # and then requests:
                #
                # /audio
                #

                return {
                    "response": response,
                    "audio": "/audio"
                }


        # ==================================
        # AUDIO FAILED
        # ==================================

        print(
            "River audio generation FAILED."
        )

        print(
            "================================="
        )


        return {
            "response": response,
            "audio": None
        }


    except Exception as error:

        print(
            "\nPEPPO ERROR:"
        )

        print(
            error
        )


        return {
            "response": (
                "Sorry buddy, "
                "I ran into a problem."
            ),

            "audio": None
        }


# ==========================================
# RIVER AUDIO
# ==========================================

@app.get("/audio")
def get_audio():

    global AUDIO_FILE


    # ======================================
    # NO AUDIO GENERATED
    # ======================================

    if AUDIO_FILE is None:

        print(
            "No River audio available."
        )


        return JSONResponse(
            status_code=404,

            content={
                "error": "No Peppo audio available."
            }
        )


    # ======================================
    # CONVERT TO PATH
    # ======================================

    audio_path = Path(
        AUDIO_FILE
    ).resolve()


    # ======================================
    # CHECK FILE
    # ======================================

    if not audio_path.exists():

        print(
            "River audio file does not exist:"
        )

        print(
            audio_path
        )


        return JSONResponse(
            status_code=404,

            content={
                "error": "Audio file does not exist."
            }
        )


    # ======================================
    # SEND AUDIO
    # ======================================

    print(
        "Sending River audio to browser:"
    )

    print(
        audio_path
    )


    return FileResponse(

        path=audio_path,

        media_type="audio/wav",

        filename="peppo_output.wav",

        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )


# ==========================================
# FAVICON
# ==========================================

@app.get("/favicon.ico")
def favicon():

    favicon_file = WEB_DIR / "favicon.ico"


    if favicon_file.exists():

        return FileResponse(
            favicon_file
        )


    return {
        "status": "no favicon"
    }


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    import uvicorn


    uvicorn.run(

        app,

        host="127.0.0.1",

        port=8000,

        reload=False
    )