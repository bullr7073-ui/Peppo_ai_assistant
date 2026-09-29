import psutil

from app_manager import (
    find_application,
    open_application as launch_application
)


# ==========================================
# APPLICATION PROCESS NAMES
# ==========================================

PROCESS_NAMES = {

    "chrome": [
        "chrome.exe"
    ],

    "google chrome": [
        "chrome.exe"
    ],

    "vs code": [
        "code.exe"
    ],

    "visual studio code": [
        "code.exe"
    ],

    "notepad": [
        "notepad.exe"
    ],

    "calculator": [
        "calculatorapp.exe",
        "calc.exe"
    ],

    "paint": [
        "mspaint.exe"
    ],

    "file explorer": [
        "explorer.exe"
    ],

    "explorer": [
        "explorer.exe"
    ],

    "edge": [
        "msedge.exe"
    ],

    "microsoft edge": [
        "msedge.exe"
    ],

    "spotify": [
        "spotify.exe"
    ],

    "discord": [
        "discord.exe"
    ]
}


# ==========================================
# NORMALIZE APP NAME
# ==========================================

def normalize_app_name(app_name):

    return app_name.lower().strip()


# ==========================================
# FIND PROCESS NAMES
# ==========================================

def get_process_names(app_name):

    app_name = normalize_app_name(
        app_name
    )

    # Known application
    if app_name in PROCESS_NAMES:

        return PROCESS_NAMES[
            app_name
        ]

    # --------------------------------------
    # Dynamic fallback
    # --------------------------------------
    #
    # If we don't know the process name,
    # try finding the application executable.
    #

    application = find_application(
        app_name
    )

    if not application:

        return []

    executable_name = application.split(
        "\\"
    )[-1].lower()

    if executable_name.endswith(
        ".exe"
    ):

        return [
            executable_name
        ]

    return []


# ==========================================
# CHECK IF APPLICATION IS RUNNING
# ==========================================

def is_application_running(app_name):

    app_name = normalize_app_name(
        app_name
    )

    process_names = get_process_names(
        app_name
    )

    if not process_names:

        return False

    process_names = [
        name.lower()
        for name in process_names
    ]

    for process in psutil.process_iter(
        ["name"]
    ):

        try:

            process_name = process.info[
                "name"
            ]

            if (
                process_name
                and
                process_name.lower()
                in process_names
            ):

                return True

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):

            continue

    return False


# ==========================================
# OPEN APPLICATION
# ==========================================

def open_application(app_name):

    app_name = normalize_app_name(
        app_name
    )

    # --------------------------------------
    # Use dynamic app manager
    # --------------------------------------

    success, message = launch_application(
        app_name
    )

    return (
        success,
        message
    )


# ==========================================
# CLOSE APPLICATION
# ==========================================

def close_application(app_name):

    app_name = normalize_app_name(
        app_name
    )

    process_names = get_process_names(
        app_name
    )

    if not process_names:

        return (
            False,
            f"I couldn't find {app_name} running on this computer."
        )

    process_names = [
        name.lower()
        for name in process_names
    ]

    closed = False

    for process in psutil.process_iter(
        ["name"]
    ):

        try:

            process_name = process.info[
                "name"
            ]

            if (
                process_name
                and
                process_name.lower()
                in process_names
            ):

                process.terminate()

                closed = True

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):

            continue

    if closed:

        return (
            True,
            f"Closed {app_name}."
        )

    return (
        False,
        f"{app_name} is not running."
    )


# ==========================================
# LIST RUNNING APPLICATIONS
# ==========================================

def get_running_applications():

    running = []

    known_processes = set()

    for names in PROCESS_NAMES.values():

        known_processes.update(
            names
        )

    known_processes = {
        name.lower()
        for name in known_processes
    }

    for process in psutil.process_iter(
        ["name"]
    ):

        try:

            process_name = process.info[
                "name"
            ]

            if (
                process_name
                and
                process_name.lower()
                in known_processes
            ):

                if process_name not in running:

                    running.append(
                        process_name
                    )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):

            continue

    return running


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print(
        "Chrome running:",
        is_application_running(
            "chrome"
        )
    )

    print(
        "Notepad running:",
        is_application_running(
            "notepad"
        )
    )

    print(
        "Calculator running:",
        is_application_running(
            "calculator"
        )
    )

    print(
        "Running applications:",
        get_running_applications()
    )