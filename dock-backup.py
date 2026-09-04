#!/usr/bin/env python3

import shutil
import subprocess
from pathlib import Path
from datetime import datetime


# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
BACKUP_DIR = BASE_DIR / "backups"
DOCK_PLIST = Path.home() / "Library/Preferences/com.apple.dock.plist"


# ============================================================
# ANSI COLORS
# ============================================================

GREEN = "\033[32m"
BRIGHT_GREEN = "\033[92m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RESET = "\033[0m"
BOLD = "\033[1m"


# ============================================================
# SCREEN
# ============================================================

def clear_screen():
    print("\033[2J\033[H", end="")


# ============================================================
# HEADER
# ============================================================

def header():
    clear_screen()

    print(GREEN + r"""
╔══════════════════════════════════════════════╗
║                                              ║
║   ██████╗  ██████╗  ██████╗██╗  ██╗          ║
║   ██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝          ║
║   ██║  ██║██║   ██║██║     █████╔╝           ║
║   ██║  ██║██║   ██║██║     ██╔═██╗           ║
║   ██████╔╝╚██████╔╝╚██████╗██║  ██╗          ║
║   ╚═════╝  ╚═════╝  ╚═════╝╚═╝  ╚═╝          ║
║                                              ║
║              D O C K   B A C K U P           ║
║                                              ║
║                 macOS Utility                ║
║                    v1.0                      ║
║                                              ║
╚══════════════════════════════════════════════╝
""" + RESET)

    print(
        BRIGHT_GREEN +
        "[ OK ]" +
        RESET +
        " Dock Backup ready."
    )

    print()


# ============================================================
# HELP
# ============================================================

def help_menu():

    print(
        CYAN +
        "[ HELP ]" +
        RESET +
        " Dock Backup v1.0"
    )

    print()

    print("Create Backup")
    print("  Creates a snapshot of your current Dock.")
    print()

    print("Restore Backup")
    print("  Lets you choose a regular or safety backup")
    print("  and restore it to your Dock.")
    print()

    print("List Backups")
    print("  Shows your regular saved backups.")
    print()

    print("Safety Backups")
    print("  Automatically created before every restore.")
    print("  They can also be selected from Restore Backup.")
    print()

    print("Backup Location")
    print("  ~/Desktop/Dock-Backup/")
    print()

    print(
        YELLOW +
        "Tip:" +
        RESET +
        " A safety backup is created automatically"
    )

    print("     before every restore operation.")


# ============================================================
# BACKUP
# ============================================================

def backup():

    BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if not DOCK_PLIST.exists():

        print(
            RED +
            "[ ERROR ]" +
            RESET +
            " Dock configuration not found."
        )

        return

    date = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    backup_file = (
        BACKUP_DIR /
        f"dock-backup_{date}.plist"
    )

    try:

        shutil.copy2(
            DOCK_PLIST,
            backup_file
        )

        print(
            BRIGHT_GREEN +
            "[ OK ]" +
            RESET +
            " Backup created:"
        )

        print(
            f"      {backup_file}"
        )

    except Exception as e:

        print(
            RED +
            "[ ERROR ]" +
            RESET +
            f" {e}"
        )


# ============================================================
# RESTORE
# ============================================================

def restore():

    BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    regular_backups = sorted(
        BACKUP_DIR.glob(
            "dock-backup_*.plist"
        ),
        reverse=True
    )

    safety_backups = sorted(
        BACKUP_DIR.glob(
            "dock-before-restore_*.plist"
        ),
        reverse=True
    )

    if not regular_backups and not safety_backups:

        print(
            YELLOW +
            "[ INFO ]" +
            RESET +
            " No backups found."
        )

        return

    # --------------------------------------------------------
    # REGULAR BACKUPS
    # --------------------------------------------------------

    print(
        CYAN +
        "[ INFO ]" +
        RESET +
        " Regular Backups:"
    )

    print()

    if regular_backups:

        for i, backup_file in enumerate(
            regular_backups,
            1
        ):

            print(
                f"  [{i}] {backup_file.name}"
            )

    else:

        print(
            "  No regular backups found."
        )

    print()

    # --------------------------------------------------------
    # SAFETY BACKUPS
    # --------------------------------------------------------

    print(
        CYAN +
        "[ INFO ]" +
        RESET +
        " Safety Backups:"
    )

    print()

    if safety_backups:

        for i, backup_file in enumerate(
            safety_backups,
            1
        ):

            print(
                f"  [S{i}] {backup_file.name}"
            )

    else:

        print(
            "  No safety backups found."
        )

    print()

    # --------------------------------------------------------
    # BUILD SELECTION MAP
    # --------------------------------------------------------

    choices = {}

    for i, backup_file in enumerate(
        regular_backups,
        1
    ):

        choices[str(i)] = backup_file

    for i, backup_file in enumerate(
        safety_backups,
        1
    ):

        choices[f"s{i}"] = backup_file

    choice = input(
        CYAN +
        "Select backup to restore: " +
        RESET
    ).strip().lower()

    if choice not in choices:

        print(
            RED +
            "[ ERROR ]" +
            RESET +
            " Invalid selection."
        )

        return

    selected = choices[choice]

    print()

    print(
        YELLOW +
        "[ WARNING ]" +
        RESET +
        " You selected:"
    )

    print(
        f"          {selected.name}"
    )

    print()

    answer = input(
        YELLOW +
        "Restore this backup? [y/N]: " +
        RESET
    )

    if answer.lower() != "y":

        print(
            YELLOW +
            "[ INFO ]" +
            RESET +
            " Restore cancelled."
        )

        return

    try:

        # ----------------------------------------------------
        # SAFETY BACKUP OF CURRENT DOCK
        # ----------------------------------------------------

        date = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        safety_backup = (
            BACKUP_DIR /
            f"dock-before-restore_{date}.plist"
        )

        if DOCK_PLIST.exists():

            shutil.copy2(
                DOCK_PLIST,
                safety_backup
            )

        print(
            CYAN +
            "[ INFO ]" +
            RESET +
            " Current Dock configuration backed up."
        )

        # ----------------------------------------------------
        # RESTORE SELECTED BACKUP
        # ----------------------------------------------------

        print(
            CYAN +
            "[ INFO ]" +
            RESET +
            " Restoring Dock..."
        )

        shutil.copy2(
            selected,
            DOCK_PLIST
        )

        # ----------------------------------------------------
        # RESTART DOCK
        # ----------------------------------------------------

        subprocess.run(
            ["killall", "Dock"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        print(
            BRIGHT_GREEN +
            "[ OK ]" +
            RESET +
            " Dock restored successfully."
        )

        print(
            CYAN +
            "[ INFO ]" +
            RESET +
            " A safety backup was created before restore."
        )

    except Exception as e:

        print(
            RED +
            "[ ERROR ]" +
            RESET +
            f" {e}"
        )


# ============================================================
# LIST BACKUPS
# ============================================================

def list_backups():

    BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    backups = sorted(
        BACKUP_DIR.glob(
            "dock-backup_*.plist"
        ),
        reverse=True
    )

    if not backups:

        print(
            YELLOW +
            "[ INFO ]" +
            RESET +
            " No regular backups found."
        )

        return

    print(
        CYAN +
        "[ INFO ]" +
        RESET +
        " Available Backups:"
    )

    print()

    for i, backup_file in enumerate(
        backups,
        1
    ):

        print(
            f"  {i}. {backup_file.name}"
        )


# ============================================================
# WAIT
# ============================================================

def wait():

    input(
        "\nPress Enter to continue..."
    )


# ============================================================
# MENU
# ============================================================

def menu():

    while True:

        header()

        print(
            BOLD +
            "0." +
            RESET +
            " ❓ Help"
        )

        print(
            BOLD +
            "1." +
            RESET +
            " 💾 Create Backup"
        )

        print(
            BOLD +
            "2." +
            RESET +
            " ♻️  Restore Backup"
        )

        print(
            BOLD +
            "3." +
            RESET +
            " 📦 List Backups"
        )

        print(
            BOLD +
            "4." +
            RESET +
            " ❌ Exit"
        )

        print()

        choice = input(
            CYAN +
            "Select an option: " +
            RESET
        ).strip()

        if choice == "0":

            print()
            help_menu()
            wait()

        elif choice == "1":

            print()
            backup()
            wait()

        elif choice == "2":

            print()
            restore()
            wait()

        elif choice == "3":

            print()
            list_backups()
            wait()

        elif choice == "4":

            print()

            print(
                BRIGHT_GREEN +
                "[ OK ]" +
                RESET +
                " Goodbye!"
            )

            print()

            break

        else:

            print()

            print(
                RED +
                "[ ERROR ]" +
                RESET +
                " Invalid option. Please enter 0-4."
            )

            wait()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    menu()
