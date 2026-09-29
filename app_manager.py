import os
import subprocess
import winreg


# ==========================================
# APP CACHE
# ==========================================

APP_CACHE = {}


# ==========================================
# COMMON APPLICATION PATHS
# ==========================================

COMMON_PATHS = [

    os.environ.get("ProgramFiles", ""),

    os.environ.get("ProgramFiles(x86)", ""),

    os.environ.get("LOCALAPPDATA", ""),

    os.path.expandvars(
        r"%APPDATA%"
    ),

    os.path.expandvars(
        r"%LOCALAPPDATA%\Programs"
    ),

    r"C:\Windows\System32",

    r"C:\Windows"
]


# ==========================================
# NAME NORMALIZATION
# ==========================================

def normalize_app_name(name):

    name = name.lower().strip()

    replacements = {

        "google chrome": "chrome",

        "visual studio code": "vs code",

        "microsoft visual studio code": "vs code",

        "microsoft edge": "edge",

        "windows calculator": "calculator",

        "file explorer": "explorer",

    }

    return replacements.get(
        name,
        name
    )


# ==========================================
# SEARCH START MENU
# ==========================================

def search_start_menu(app_name):

    app_name = normalize_app_name(
        app_name
    )

    locations = [

        os.path.expandvars(
            r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"
        ),

        os.path.expandvars(
            r"%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs"
        )

    ]

    for location in locations:

        if not os.path.exists(location):
            continue

        for root, directories, files in os.walk(
            location
        ):

            for file in files:

                if not file.lower().endswith(
                    ".lnk"
                ):
                    continue

                shortcut_name = os.path.splitext(
                    file
                )[0].lower()

                if (
                    app_name == shortcut_name
                    or app_name in shortcut_name
                    or shortcut_name in app_name
                ):

                    return os.path.join(
                        root,
                        file
                    )

    return None


# ==========================================
# SEARCH COMMON WINDOWS LOCATIONS
# ==========================================

def search_common_paths(app_name):

    app_name = normalize_app_name(
        app_name
    )

    clean_name = app_name.replace(
        " ",
        ""
    )

    # Known executable aliases
    executable_aliases = {

        "calculator": [
            "calculatorapp",
            "calc"
        ],

        "notepad": [
            "notepad"
        ],

        "chrome": [
            "chrome"
        ],

        "vs code": [
            "code"
        ],

        "edge": [
            "msedge"
        ],

        "paint": [
            "mspaint"
        ],

        "explorer": [
            "explorer"
        ]
    }

    possible_names = executable_aliases.get(
        app_name,
        [clean_name]
    )

    for base_path in COMMON_PATHS:

        if not base_path:
            continue

        if not os.path.exists(base_path):
            continue

        try:

            for root, directories, files in os.walk(
                base_path
            ):

                # Limit search depth
                relative = os.path.relpath(
                    root,
                    base_path
                )

                depth = (
                    0
                    if relative == "."
                    else relative.count(os.sep) + 1
                )

                if depth > 4:

                    directories[:] = []

                    continue

                for file in files:

                    if not file.lower().endswith(
                        ".exe"
                    ):
                        continue

                    executable_name = (
                        os.path.splitext(file)[0]
                        .lower()
                        .replace(" ", "")
                    )

                    # Exact executable matching
                    if executable_name in possible_names:

                        return os.path.join(
                            root,
                            file
                        )

        except (
            PermissionError,
            OSError
        ):

            continue

    return None

# ==========================================
# SEARCH WINDOWS REGISTRY
# ==========================================

def search_registry(app_name):

    app_name = normalize_app_name(
        app_name
    )

    registry_locations = [

        (
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        ),

        (
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ),

        (
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        )

    ]

    for hive, path in registry_locations:

        try:

            key = winreg.OpenKey(
                hive,
                path
            )

        except OSError:

            continue

        try:

            count = winreg.QueryInfoKey(
                key
            )[0]

            for index in range(count):

                try:

                    subkey_name = winreg.EnumKey(
                        key,
                        index
                    )

                    subkey = winreg.OpenKey(
                        key,
                        subkey_name
                    )

                except OSError:

                    continue

                try:

                    display_name = None

                    try:

                        display_name = winreg.QueryValueEx(
                            subkey,
                            "DisplayName"
                        )[0]

                    except OSError:

                        pass

                    if not display_name:

                        continue

                    display_name = str(
                        display_name
                    ).lower()

                    if (
                        app_name not in display_name
                        and display_name not in app_name
                    ):

                        continue

                    # ----------------------------------
                    # INSTALL LOCATION
                    # ----------------------------------

                    try:

                        install_location = (
                            winreg.QueryValueEx(
                                subkey,
                                "InstallLocation"
                            )[0]
                        )

                    except OSError:

                        install_location = None

                    if install_location:

                        executable = search_directory_for_exe(
                            install_location,
                            app_name
                        )

                        if executable:

                            return executable

                    # ----------------------------------
                    # DISPLAY ICON
                    # ----------------------------------

                    try:

                        display_icon = (
                            winreg.QueryValueEx(
                                subkey,
                                "DisplayIcon"
                            )[0]
                        )

                    except OSError:

                        display_icon = None

                    if display_icon:

                        display_icon = (
                            str(display_icon)
                            .split(",")[0]
                            .strip('"')
                        )

                        if os.path.isfile(
                            display_icon
                        ):

                            return display_icon

                finally:

                    subkey.Close()

        finally:

            key.Close()

    return None


# ==========================================
# SEARCH DIRECTORY FOR EXE
# ==========================================

def search_directory_for_exe(
    directory,
    app_name
):

    if not directory:
        return None

    directory = os.path.expandvars(
        directory
    )

    if not os.path.exists(directory):
        return None

    clean_name = normalize_app_name(
        app_name
    ).replace(
        " ",
        ""
    )

    try:

        for root, directories, files in os.walk(
            directory
        ):

            relative = os.path.relpath(
                root,
                directory
            )

            depth = (
                0
                if relative == "."
                else relative.count(os.sep) + 1
            )

            if depth > 3:

                directories[:] = []

                continue

            for file in files:

                if not file.lower().endswith(
                    ".exe"
                ):
                    continue

                executable_name = os.path.splitext(
                    file
                )[0].lower().replace(
                    " ",
                    ""
                )

                if (
                    clean_name == executable_name
                    or clean_name in executable_name
                    or executable_name in clean_name
                ):

                    return os.path.join(
                        root,
                        file
                    )

    except (
        PermissionError,
        OSError
    ):

        pass

    return None


# ==========================================
# FIND APPLICATION
# ==========================================

def find_application(app_name):

    app_name = normalize_app_name(
        app_name
    )

    # --------------------------------------
    # CACHE
    # --------------------------------------

    if app_name in APP_CACHE:

        cached = APP_CACHE[
            app_name
        ]

        if os.path.exists(cached):

            return cached

        del APP_CACHE[
            app_name
        ]

    # --------------------------------------
    # START MENU
    # --------------------------------------

    result = search_start_menu(
        app_name
    )

    if result:

        APP_CACHE[
            app_name
        ] = result

        return result

    # --------------------------------------
    # COMMON PATHS
    # --------------------------------------

    result = search_common_paths(
        app_name
    )

    if result:

        APP_CACHE[
            app_name
        ] = result

        return result

    # --------------------------------------
    # REGISTRY
    # --------------------------------------

    result = search_registry(
        app_name
    )

    if result:

        APP_CACHE[
            app_name
        ] = result

        return result

    return None


# ==========================================
# OPEN APPLICATION
# ==========================================

def open_application(app_name):

    app_name = normalize_app_name(
        app_name
    )

    application = find_application(
        app_name
    )

    if not application:

        return (
            False,
            f"I couldn't find {app_name} on this computer."
        )

    try:

        # ----------------------------------
        # START MENU SHORTCUT
        # ----------------------------------

        if application.lower().endswith(
            ".lnk"
        ):

            os.startfile(
                application
            )

        # ----------------------------------
        # EXECUTABLE
        # ----------------------------------

        else:

            subprocess.Popen(
                [application],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        return (
            True,
            f"Opening {app_name}."
        )

    except Exception as error:

        print(
            "Application launch error:",
            error
        )

        return (
            False,
            f"I couldn't open {app_name}."
        )


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    test_apps = [

        "chrome",

        "notepad",

        "calculator",

        "vs code",

    ]

    for app in test_apps:

        print(
            f"\nSearching for: {app}"
        )

        result = find_application(
            app
        )

        print(
            "Found:",
            result
        )