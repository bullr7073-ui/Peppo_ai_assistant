import subprocess
import os


# ==========================================
# APPLICATION PATHS
# ==========================================

APP_PATHS = {

    # Browsers
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",

    # Development
    "vs code": r"code",
    "visual studio code": r"code",

    # Windows applications
    "notepad": r"notepad.exe",
    "calculator": r"calc.exe",
    "calc": r"calc.exe",
    "paint": r"mspaint.exe",
    "file explorer": r"explorer.exe",
    "explorer": r"explorer.exe",

}


# ==========================================
# OPEN APPLICATION
# ==========================================

def open_application(app_name):

    app_name = app_name.lower().strip()

    # Find application
    app_path = APP_PATHS.get(app_name)

    if not app_path:

        return (
            False,
            f"I don't know how to open {app_name} yet."
        )

    try:

        # ==================================
        # SPECIAL CASE: COMMAND-LINE APPS
        # ==================================

        if app_path == "code":

            subprocess.Popen(
                ["code"]
            )

        # ==================================
        # NORMAL WINDOWS APPLICATIONS
        # ==================================

        else:

            if os.path.exists(app_path):

                subprocess.Popen(
                    [app_path]
                )

            else:

                # Try launching through Windows
                subprocess.Popen(
                    app_path,
                    shell=True
                )

        return (
            True,
            f"Opening {app_name}."
        )

    except Exception as error:

        print(
            "\nApplication launch error:",
            error
        )

        return (
            False,
            f"Sorry, I couldn't open {app_name}."
        )


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    success, message = open_application(
        "calculator"
    )

    print(message)