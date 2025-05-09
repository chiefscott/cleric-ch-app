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

## What's Left to Build (Based on User Feedback)

- **GitHub Setup - Phase 2 (Git & GitHub Repo):**
    - User to configure Git global settings (name, email).
    - User to create a new repository on GitHub.
    - Connect local project to the GitHub repository (`git init`, `git remote add origin`).
- **GitHub Setup - Phase 3 (First Commit & Push):**
    - Stage files (`git add .`).
    - Commit files (`git commit -m "Initial commit"`).
    - Rename default branch to `main` if necessary (`git branch -M main`).
    - Push to GitHub (`git push -u origin main`).
- **Final User Confirmation:** After GitHub setup.

## Current Status

**Phase 1 of GitHub preparation is complete.** Essential files (`.gitignore`, `README.md`, `LICENSE`, `CONTRIBUTING.md`) are in place. The application itself is functionally complete and tested. Ready to guide the user through initializing Git locally and connecting to a GitHub repository.

## Known Issues (Actively Being Addressed)

- **Log Parsing Accuracy:** **(Resolved - Fifth Pass)**.
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
