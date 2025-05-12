# EverQuest Cleric CH (Complete Heal) Chain Assistant

## Overview

The EverQuest Cleric CH Chain Assistant is a desktop application designed to help EverQuest players, particularly clerics and raid leaders, efficiently manage and generate in-game macros for "Complete Heal (CH) Chains." Organizing CH chains quickly and accurately is crucial during raids and group play, and this tool aims to streamline that process, reducing setup time and minimizing errors.

This application is built with Python and Tkinter for its graphical user interface and is intended for Windows users.

## Key Features

*   **Log File Parsing:** Reads your EverQuest log file (specifically tested with Quarm server format) to automatically detect available clerics after you issue an in-game `/who` command preceded by a customizable trigger phrase (default: `<CLERIC CH WHO>`). The parser now specifically filters for lines containing cleric class titles such as "Cleric", "Vicar", "Templar", or "High Priest".
*   **Cleric Management:**
    *   Displays a list of found clerics.
    *   Allows manual addition or removal of clerics.
    *   Supports reordering of clerics in the main healing chain using "Move Up" / "Move Down" buttons.
    *   Designate clerics as "Fluffers" (patch healers) separate from the main numbered chain.
*   **Chain Assignment:** Automatically assigns chain numbers (111, 222, ... AAA, BBB, etc., up to 18 clerics) based on their order.
*   **Macro Generation:**
    *   Generates a formatted "Assignments Message" for your designated in-game cleric channel, listing all chain assignments and fluffers.
    *   Creates individual, personalized in-game macros for each cleric in the numbered chain.
    *   Macros include appropriate `/pause` commands based on user-selected chain timing (e.g., 2 seconds, 3.5 seconds, or custom values).
    *   Supports different macro timings if the target is "slowable."
    *   Allows selection of the in-game command used for macros (e.g., `/shout`, `/guildsay`, `/groupsay`, `/say`, or your cleric channel).
*   **Clipboard Functionality:** Easily copy the generated assignment message or individual cleric macros to your clipboard for pasting into EverQuest or other applications like Discord.
*   **Customization:**
    *   Set your EverQuest log file path (remembered between sessions).
    *   Customize the in-game trigger phrase for cleric detection.
    *   Select the cleric communication channel number (remembered between sessions).
    *   Choose chain timings, including custom values.
*   **User-Friendly Interface:** Features a tabbed interface (Setup, Assignments, Macros, Console) for easy navigation and operation.
*   **Troubleshooting Console:** Includes a console tab that logs the application's operations, particularly useful for diagnosing log parsing behavior.

## How to Use

1.  **Download:** Obtain the `cleric_ch_app.exe` file from the [Releases page](https://github.com/chiefscott/cleric-ch-app/releases).
2.  **Run:** Execute `cleric_ch_app.exe`. No installation is required.
3.  **Setup Tab:**
    *   Click "Browse" to select your EverQuest log file (e.g., `eqlog_YourCharacter_pq.proj.txt`). This path will be remembered.
    *   Optionally, customize the "Cleric Who Trigger" phrase if you use something other than `<CLERIC CH WHO>`.
    *   Select your preferred "Cleric Channel" number.
4.  **In-Game Action:** In EverQuest, type your trigger phrase followed by a `/who` command that lists clerics (e.g., `<CLERIC CH WHO>` then `/who guild cleric`).
5.  **Assignments Tab:**
    *   Click the "Cleric Who" button in the app. The app will parse your log file for clerics.
    *   Manage the cleric list: Add, Remove, Move Up/Down, Move to Fluffers/Chain.
    *   Select your desired "Chain Timing" and "Slow Timing" (if applicable using the "Slowable?" checkbox).
    *   Select the "Macro Announce Via:" channel for individual cleric macros.
    *   Click "Generate/Refresh Macros".
6.  **Use Generated Text:**
    *   On the "Macros" tab, the "Assignments Message" is displayed line-by-line in separate boxes. Click the "Copy" button next to each line to copy that specific part of the message (e.g., the chain assignments, the timing info, the fluffer list).
    *   On the "Macros" tab, click any cleric's button to copy their personalized macro (using the selected announce channel) to the clipboard for distribution (e.g., via in-game tells or Discord).
7.  **Console Tab:** If you encounter issues with cleric detection, the Console tab provides detailed logs of the parsing process. You can copy this log to help with troubleshooting.

## Current Status

The latest refinements, including the updated log parsing for varied cleric titles, the refined refresh logic, the "Macro Announce Via" dropdown with the "/say" option, and the line-by-line assignments message display, have been implemented and are awaiting user testing.

## Future Enhancements (Potential)

*   Direct Discord integration for sending macros.
*   Integration with other third-party tools for cleric list gathering.

---

Built by [chiefscott]
