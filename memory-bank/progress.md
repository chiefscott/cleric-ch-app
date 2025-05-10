# Progress

This document tracks the project's current status, what has been completed, what remains, and known issues.

## What Works

- **Conceptualization:** Detailed project idea and requirements have been documented ("Cleric CH Chain Socials Notes.md").
- **Requirement Clarification:** Key questions about functionality, error handling, and technical preferences have been answered.
- **Technical Stack Recommendation:** Python with Tkinter/PyQt and PyInstaller has been recommended and acknowledged.
- **Initial CLINE Memory Bank Population:** The foundational Memory Bank files (`projectbrief.md`, `productContext.md`, `techContext.md`, `systemPatterns.md`, `activeContext.md`, `progress.md`) have been drafted based on the current understanding.
- **Basic GUI Structure:** The main window with Setup, Assignments, and Macros tabs is implemented.
- **Log File Selection and Persistence:** Users can browse for and select a log file, and the path is saved/loaded using `settings.json`.
- **Manual Cleric Management:** Functionality to manually add and remove clerics from the main list is implemented.
- **Basic Drag and Drop Binding:** Initial event bindings for drag and drop were added.
- **Log File Parsing Logic:** Implemented `parse_log_for_clerics` method with efficient reverse log reading (`_reverse_readline` helper). (Note: Accuracy issue identified in testing).
- **Cleric Management (Initial):** Implemented manual add, drag-and-drop between lists (Clerics/Fluffers) with cursor feedback, and a basic (unconnected) remove method. (Note: D&D reliability/intuitiveness issues identified in testing).
- **Assignment Generation Logic:** Implemented methods (`generate_assignments`, `generate_chain_numbers`) for 111...AAA style chain numbering.
- **Macro Generation Logic:** Implemented methods (`generate_single_macro`, `create_macros`, `update_assignments_message`) for generating assignment messages and individual cleric macros based on templates/timings.
- **Copy to Clipboard Functionality:** Implemented copy buttons using Tkinter's clipboard methods.
- **Custom Timing Input:** Implemented dialog prompt for custom timing values.
- **Cleric Channel Setting:** Implemented dropdown in Setup tab, persistence in `settings.json`, and integration into assignment message generation. **(Verified)**
- **Clear All Behavior:** Modified `clear_all` to preserve log file path. **(Verified)**
- **Log Parsing State Machine Simplified (Fifth Pass):** Resolved "no names found" issue.
- **Console Tab and Logging Added:** For troubleshooting.
- **Log Parsing State Machine Corrected (Fourth Pass):** Addressed earlier parsing regression.
- **Log Parsing Overhauled (Third Pass):** Major refactor of parsing logic.
- **Refined Log Parsing (Second Pass):** Improved end-marker handling.
- **Refined Log Parsing (Initial):** Initial start/end marker implementation.
- **Button-Based List Management:** Implemented and verified.
- **Scrollbars Added:** Implemented and verified.
- **Installer Created:** Successfully built `cleric_ch_app.exe`.
- **README.md Created:** Generated.
- **GitHub Prep Files Created:** `.gitignore`, `LICENSE` (MIT), `CONTRIBUTING.md` created.
- **Local Git Repository Initialized:** `git init` successful.
- **Remote GitHub Repository Connected:** `git remote add origin ...` successful.
- **Initial Commit Pushed to GitHub:** `git add .`, `git commit ...`, `git branch -M main`, `git push -u origin main` all successful.
- **Log Parsing Regex for Varied Cleric Titles:** Updated regex in `parse_log_for_clerics` to specifically filter for "Cleric", "Vicar", "Templar", or "High Priest" class titles, addressing an end-user reported bug.

## What's Left to Build (Based on User Feedback)

- **Testing of Cleric Title Parsing Fix:** User to test the latest regex change.
- **Commit and Push Bug Fix:** After successful testing, commit the changes and push to GitHub.
- **Final User Confirmation:** User to confirm satisfaction with the project on GitHub after the bug fix.

## Current Status

**A bug related to log parsing for varied cleric titles has been addressed.** The application code (`cleric_ch_app.py`) has been updated with a more specific regex. Memory bank documentation is being updated. Pending user testing, and then changes will be committed and pushed to GitHub. The project was previously set up on GitHub, with all local files (as per `.gitignore`) committed and pushed to the `main` branch.

## Known Issues (Actively Being Addressed)

- **Log Parsing Fails for Varied Cleric Titles:** Reported by an end-user that clerics were not being found if their in-game class title was not one of the specific known cleric titles. **(Addressed by updating regex to include "Cleric|Vicar|Templar|High Priest")**
- **Log Parsing Accuracy:** **(Previously Resolved - Fifth Pass)**.
- **List Management Usability:** **(Addressed)**.
- **Missing Scrollbars:** **(Addressed)**.

## Evolution of Project Decisions

- Initial discussions confirmed Python as the preferred language.
- Clarified that Discord integration is a future goal, not for the initial version.
- Decided on in-memory data handling for session data, with persistent storage for `log_file_path` and `cleric_channel` in `settings.json`.
- Confirmed Windows as the initial target OS.
- Tkinter was chosen as the initial GUI framework.
- PyInstaller was chosen for creating the Windows installer.
- **Prioritizing Buttons over D&D:** Shifted primary list management interaction (reordering, fluffer assignment) from drag-and-drop to button-based controls due to user feedback on D&D reliability/intuitiveness in Tkinter.
