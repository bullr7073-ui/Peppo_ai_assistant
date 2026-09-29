const peppoApp = document.querySelector(".peppo-app");

const orbButton = document.getElementById("orbButton");
const cancelButton = document.getElementById("cancelButton");

const tapText = document.getElementById("tapText");

const responsePanel = document.getElementById("responsePanel");
const responseTitle = document.getElementById("responseTitle");
const responseText = document.getElementById("responseText");


// ==========================================
// SPEECH RECOGNITION
// ==========================================

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

let recognition = null;

let isListening = false;
let isProcessing = false;
let isSpeaking = false;
let cancelled = false;

let currentAudio = null;


// ==========================================
// INITIALIZE SPEECH RECOGNITION
// ==========================================

if (SpeechRecognition) {

    recognition = new SpeechRecognition();

    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-IN";

    recognition.onstart = () => {

        isListening = true;
        isProcessing = false;
        isSpeaking = false;
        cancelled = false;

        peppoApp.className =
            "peppo-app listening";

        tapText.textContent =
            "LISTENING...";

        responseTitle.textContent =
            "Listening";

        responseText.textContent =
            "Go ahead, buddy.";

        showConversation();

        console.log("Peppo: listening...");
    };


    recognition.onresult = (event) => {

        const transcript =
            event.results[0][0].transcript.trim();

        console.log(
            "You said:",
            transcript
        );

        if (!transcript) {
            return;
        }

        isListening = false;
        isProcessing = true;

        peppoApp.className =
            "peppo-app thinking";

        tapText.textContent =
            "THINKING...";

        responseTitle.textContent =
            "Thinking";

        responseText.textContent =
            "Peppo is thinking...";

        showConversation();

        askPeppo(transcript);
    };


    recognition.onerror = (event) => {

        console.error(
            "Speech recognition error:",
            event.error
        );

        isListening = false;

        if (cancelled) {
            return;
        }

        if (
            event.error === "aborted" ||
            event.error === "no-speech"
        ) {

            if (!isProcessing && !isSpeaking) {
                resetPeppoUI();
            }

            return;
        }

        isProcessing = false;

        peppoApp.className =
            "peppo-app idle";

        tapText.textContent =
            "TAP TO SPEAK !";

        responseTitle.textContent =
            "I didn't catch that";

        responseText.textContent =
            "Try speaking again.";

        showConversation();
    };


    recognition.onend = () => {

        isListening = false;

        console.log(
            "Recognition ended."
        );

    };

}


// ==========================================
// SHOW CONVERSATION
// ==========================================

function showConversation() {

    peppoApp.classList.add(
        "conversation-active"
    );

    if (responsePanel) {

        responsePanel.classList.add(
            "visible"
        );

    }
}


// ==========================================
// HIDE CONVERSATION
// ==========================================

function hideConversation() {

    peppoApp.classList.remove(
        "conversation-active"
    );

    if (responsePanel) {

        responsePanel.classList.remove(
            "visible"
        );

    }
}


// ==========================================
// RESET UI
// ==========================================

function resetPeppoUI() {

    isListening = false;
    isProcessing = false;
    isSpeaking = false;
    cancelled = false;

    peppoApp.className =
        "peppo-app idle";

    tapText.textContent =
        "TAP TO SPEAK !";

    responseTitle.textContent =
        "";

    responseText.textContent =
        "";

    hideConversation();
}


// ==========================================
// STOP CURRENT AUDIO
// ==========================================

function stopCurrentAudio() {

    if (currentAudio) {

        try {

            currentAudio.pause();
            currentAudio.currentTime = 0;

        } catch (error) {

            console.log(
                "Audio already stopped."
            );
        }

        currentAudio = null;
    }


    const oldAudio =
        document.getElementById(
            "peppoAudio"
        );

    if (oldAudio) {

        try {

            oldAudio.pause();
            oldAudio.currentTime = 0;
            oldAudio.remove();

        } catch (error) {}
    }
}


// ==========================================
// START LISTENING
// ==========================================

function startListening() {

    if (!recognition) {

        responseTitle.textContent =
            "Microphone unavailable";

        responseText.textContent =
            "Your browser does not support speech recognition.";

        showConversation();

        return;
    }


    if (isListening) {
        return;
    }


    if (isProcessing) {
        return;
    }


    if (isSpeaking) {

        stopCurrentAudio();

        if ("speechSynthesis" in window) {

            window.speechSynthesis.cancel();

        }

        isSpeaking = false;
    }


    cancelled = false;

    showConversation();


    try {

        recognition.start();

    } catch (error) {

        console.warn(
            "Recognition start error:",
            error
        );
    }
}


// ==========================================
// CANCEL EVERYTHING
// ==========================================

function cancelPeppo() {

    console.log(
        "Peppo cancelled."
    );

    cancelled = true;

    isListening = false;
    isProcessing = false;
    isSpeaking = false;


    if (recognition) {

        try {

            recognition.abort();

        } catch (error) {}
    }


    if ("speechSynthesis" in window) {

        window.speechSynthesis.cancel();

    }


    stopCurrentAudio();


    responseTitle.textContent =
        "";

    responseText.textContent =
        "";


    // Return to TAP TO SPEAK

    peppoApp.className =
        "peppo-app idle";

    tapText.textContent =
        "TAP TO SPEAK !";

    hideConversation();
}


// ==========================================
// BROWSER SPEECH FALLBACK
// ==========================================

function speakPeppo(text) {

    if (!text) {

        resetPeppoUI();

        return;
    }


    if (!("speechSynthesis" in window)) {

        resetPeppoUI();

        return;
    }


    window.speechSynthesis.cancel();


    const speech =
        new SpeechSynthesisUtterance(
            text
        );


    speech.lang = "en-IN";
    speech.rate = 1.0;
    speech.pitch = 1.0;
    speech.volume = 1.0;


    speech.onstart = () => {

        if (cancelled) {
            return;
        }

        isSpeaking = true;
        isProcessing = false;

        showConversation();

        peppoApp.className =
            "peppo-app responding";

        tapText.textContent =
            "PEPPO IS SPEAKING...";
    };


    speech.onend = () => {

        if (cancelled) {
            return;
        }

        isSpeaking = false;

        setTimeout(() => {

            if (!cancelled) {

                startListening();

            }

        }, 250);
    };


    speech.onerror = () => {

        if (cancelled) {
            return;
        }

        isSpeaking = false;

        setTimeout(() => {

            if (!cancelled) {

                startListening();

            }

        }, 250);
    };


    window.speechSynthesis.speak(
        speech
    );
}


// ==========================================
// ASK PEPPO
// ==========================================

async function askPeppo(message) {

    if (!message || !message.trim()) {

        startListening();

        return;
    }


    cancelled = false;

    isProcessing = true;
    isListening = false;


    showConversation();


    peppoApp.className =
        "peppo-app thinking";

    tapText.textContent =
        "THINKING...";


    responseTitle.textContent =
        "Thinking";

    responseText.textContent =
        "Peppo is thinking...";


    try {

        console.log(
            "Sending message to Peppo..."
        );


        // ==================================
        // ASK FASTAPI
        // ==================================

        const response =
            await fetch(
                "/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })
                }
            );


        console.log(
            "Chat response:",
            response.status
        );


        if (!response.ok) {

            throw new Error(
                `Server returned ${response.status}`
            );
        }


        const data =
            await response.json();

        console.log("========== PEPPO DEBUG ==========");
    console.log("FULL SERVER DATA:", data);
    console.log("RESPONSE TEXT:", data.response);
    console.log("AUDIO VALUE:", data.audio);
    console.log("AUDIO TYPE:", typeof data.audio);
    console.log("================================");


        console.log(
            "Peppo response:",
            data
        );

        console.log(
        "DATA RESPONSE:",
        data
        );

        console.log(
        "AUDIO URL:",
        data.audio
        );


        if (cancelled) {
            return;
        }


        // ==================================
        // ACTUAL AI ANSWER
        // ==================================

        const answer =
            data.response ||
            "I didn't receive a response.";


        console.log(
            "Actual Peppo answer:",
            answer
        );


        // ==================================
        // DISPLAY ANSWER
        // ==================================

        responseTitle.textContent =
            "Peppo";

        responseText.textContent =
            answer;

        showConversation();


        peppoApp.className =
            "peppo-app responding";

        tapText.textContent =
            "PEPPO IS SPEAKING...";


        isProcessing = false;


        // ==================================
        // RIVER AUDIO
        // ==================================
        //
        // IMPORTANT:
        //
        // /chat already calls:
        //
        // generate_speech(response)
        //
        // and returns:
        //
        // "audio": "/audio"
        //
        // Therefore we ONLY GET /audio.
        //
        // ==================================

        let audioURL =
            data.audio;


        if (!audioURL) {

            console.warn(
                "No audio URL returned by FastAPI."
            );

            speakPeppo(answer);

            return;
        }


        // ----------------------------------
        // CONVERT RELATIVE URL
        // ----------------------------------

        if (
            audioURL.startsWith("/")
        ) {

            audioURL =
                window.location.origin +
                audioURL;
        }


        // ----------------------------------
        // CACHE BUSTER
        // ----------------------------------

        audioURL +=
            (
                audioURL.includes("?")
                    ? "&"
                    : "?"
            ) +
            "t=" +
            Date.now();


        console.log(
            "Playing River audio:",
            audioURL
        );


        // ==================================
        // GET AUDIO
        // ==================================

        const audioResponse =
            await fetch(
                audioURL,
                {
                    method: "GET",
                    cache: "no-store"
                }
            );


        console.log(
            "Audio response:",
            audioResponse.status
        );


        if (!audioResponse.ok) {

            throw new Error(
                `Audio returned ${audioResponse.status}`
            );
        }


        const contentType =
            audioResponse.headers.get(
                "content-type"
            ) || "";


        if (
            !contentType.includes(
                "audio"
            )
        ) {

            throw new Error(
                "Server did not return audio."
            );
        }


        // ==================================
        // CREATE AUDIO BLOB
        // ==================================

        const audioBlob =
            await audioResponse.blob();


        if (cancelled) {
            return;
        }


        const blobURL =
            URL.createObjectURL(
                audioBlob
            );


        const audio =
            new Audio(blobURL);


        audio.id =
            "peppoAudio";


        currentAudio =
            audio;


        isSpeaking = true;


        // ==================================
        // AUDIO START
        // ==================================

        audio.onplay = () => {

            if (cancelled) {
                return;
            }

            isSpeaking = true;

            peppoApp.className =
                "peppo-app responding";

            tapText.textContent =
                "PEPPO IS SPEAKING...";
        };


        // ==================================
        // AUDIO FINISHED
        // ==================================

        audio.onended = () => {

            console.log(
                "River audio finished."
            );


            URL.revokeObjectURL(
                blobURL
            );


            currentAudio = null;
            isSpeaking = false;


            if (cancelled) {
                return;
            }


            // =================================
            // AUTOMATICALLY LISTEN AGAIN
            // =================================

            setTimeout(() => {

                if (!cancelled) {

                    startListening();

                }

            }, 250);
        };


        // ==================================
        // AUDIO ERROR
        // ==================================

        audio.onerror = (event) => {

            console.error(
                "River audio playback error:",
                event
            );


            URL.revokeObjectURL(
                blobURL
            );


            currentAudio = null;
            isSpeaking = false;


            if (cancelled) {
                return;
            }


            // Browser TTS fallback

            speakPeppo(answer);
        };


        // ==================================
        // PLAY RIVER AUDIO
        // ==================================

        try {

            await audio.play();

        } catch (playError) {

            console.error(
                "River audio playback blocked:",
                playError
            );


            URL.revokeObjectURL(
                blobURL
            );


            currentAudio = null;
            isSpeaking = false;


            if (!cancelled) {

                speakPeppo(answer);

            }
        }


    } catch (error) {

        console.error(
            "Peppo error:",
            error
        );


        if (cancelled) {
            return;
        }


        isProcessing = false;
        isSpeaking = false;


        peppoApp.className =
            "peppo-app idle";

        tapText.textContent =
            "TAP TO SPEAK !";


        responseTitle.textContent =
            "Connection problem";

        responseText.textContent =
            "I couldn't connect to my brain.";

        showConversation();
    }
}


// ==========================================
// ORB BUTTON
// ==========================================

if (orbButton) {

    orbButton.addEventListener(
        "click",
        () => {

            console.log(
                "Orb clicked."
            );


            if (!recognition) {

                responseTitle.textContent =
                    "Microphone unavailable";

                responseText.textContent =
                    "Your browser does not support speech recognition.";

                showConversation();

                return;
            }


            if (isProcessing) {

                console.log(
                    "Peppo is processing..."
                );

                return;
            }


            if (isListening) {

                try {

                    recognition.stop();

                } catch (error) {}

                return;
            }


            if (isSpeaking) {

                stopCurrentAudio();

                if (
                    "speechSynthesis"
                    in window
                ) {

                    window.speechSynthesis.cancel();

                }

                isSpeaking = false;
            }


            cancelled = false;


            startListening();

        }
    );

}


// ==========================================
// CANCEL BUTTON
// ==========================================

if (cancelButton) {

    cancelButton.addEventListener(
        "click",
        () => {

            cancelPeppo();

        }
    );

}


// ==========================================
// INITIAL STATE
// ==========================================

resetPeppoUI();


// ==========================================
// DEBUG
// ==========================================

console.log(
    "Peppo UI loaded successfully."
);
// therefore , peppo is ready working with the basic assistive jobs ! 
// still the image showing stuff is remaining !.
