# Active Context

This document tracks the current focus of work, recent changes, next steps, and active decisions based on the latest user feedback (Post-initial implementation phase).

## Current Work Focus

Completed Phase 1 of GitHub setup: created `.gitignore`, `LICENSE`, and `CONTRIBUTING.md` files. Ready to proceed with local Git initialization and connecting to a GitHub remote repository.

## Recent Changes (Post-Feedback Implementation)

-   **GitHub Prep Files Created:**
    -   Created `.gitignore` file with appropriate entries for Python, PyInstaller, user settings, and common OS/IDE files.
    -   Created `LICENSE` file with standard MIT License text.
    -   Created a minimal `CONTRIBUTING.md` file.
-   **README.md Created:** Previously generated a comprehensive README.md file.
-   **Installer Created:** Previously used PyInstaller to build the executable.
-   **Log Parsing State Machine Simplified (Fifth Pass):** Previously removed the initial "Stage 0" from `parse_log_for_clerics`.
-   **Console Tab and Logging Added:** Previously added a console tab and detailed logging for troubleshooting.
-   **Log Parsing State Machine Corrected (Fourth Pass):** Previously fixed an issue in Stage 2 (handling "---" marker).
-   **Log Parsing Overhauled (Third Pass):** Previously refactored to use a multi-stage state machine and improved regex.
-   **Log Parsing Refined (Second Pass):** Previous update to ensure the end marker (`There is/are...`) is strictly used as a delimiter.
-   **Log Parsing Refined (Initial):** Initial update to use start (`---`) and end (`There is/are...`) markers.
-   **Button-Based List Management Implemented:** (No changes in this iteration)
    -   "Move Up" / "Move Down" buttons and methods for the main "Clerics" listbox.
    -   Removed the drag-and-drop logic for reordering clerics *within* the main listbox.
    -   Added "Move to Fluffers" and "Move to Chain" buttons for managing fluffer assignments between `self.clerics_listbox` and `self.fluffers_listbox`, with corresponding `move_to_fluffers()` and `move_to_chain()` methods. Drag-and-drop *between* these two lists remains functional as a secondary option.
-   **Scrollbars Added:**
    -   Vertical scrollbars were implemented for `self.clerics_listbox` and `self.fluffers_listbox` on the "Assignments" tab.
    -   A vertical scrollbar was implemented for the `self.macros_frame_inner` (via a canvas) on the "Macros" tab to allow scrolling through dynamically generated macro buttons.
-   **`clear_all` Method Verified:** Confirmed that the `clear_all` method correctly preserves the log file path in `settings.json` and the corresponding entry field.
-   **Cleric Channel Feature Verified:** Confirmed that the cleric channel selection, persistence, and usage in the "Assignments Message" are functioning as intended.

## User Feedback Received & Pending Actions

All previously listed pending actions related to user feedback have now been addressed in the latest code update.

-   `Clear All` button incorrectly clears the log file path. **(Addressed & Verified)**
-   Drag-and-drop for reordering clerics in the main list is not working or intuitive. **(Addressed by replacing with buttons)**
-   Drag-and-drop for assigning fluffers (moving between lists) is not working or intuitive. **(Addressed by adding primary buttons; D&D between lists remains secondary)**
-   Log parsing incorrectly identifies "There" as a cleric name, picks up names from outside the `/who` list, or (most recently) picks up no names at all. **(Resolved after Fifth Pass and successful user testing.)**
-   List areas (Assignments tab lists, Macros tab buttons) lack scrollbars for longer lists. **(Previously Addressed)**

## Next Steps (Revised Plan)

1.  **GitHub Setup - Phase 1 (Project Prep):**
    *   Clean up project directory (discussed).
    *   Create `.gitignore` file. **(Completed)**
    *   Create `README.md` file. **(Completed)**
    *   Create `LICENSE` file. **(Completed)**
    *   Create `CONTRIBUTING.md` file. **(Completed)**
2.  **GitHub Setup - Phase 2 (Git & GitHub Repo):**
    *   User to install Git (confirmed done).
    *   User to configure Git global settings (name, email).
    *   User to create a new repository on GitHub.
    *   Connect local project to the GitHub repository (`git init`, `git remote add origin`).
3.  **GitHub Setup - Phase 3 (First Commit & Push):**
    *   Stage files (`git add .`).
    *   Commit files (`git commit -m "Initial commit"`).
    *   Rename default branch to `main` if necessary (`git branch -M main`).
    *   Push to GitHub (`git push -u origin main`).
4.  **Final Review & Closure:** If GitHub setup is successful, this phase is complete.

## Active Decisions and Considerations

- **Button-Based List Management as Primary:** The decision to prioritize buttons for list manipulation has been implemented and is considered the primary interaction method.
- **Log Parsing with Markers:** The refined log parsing using structural markers is now active.
- **Scrollable Areas Implemented:** Scrollbars are now in place for key dynamic content areas.
- **GUI Framework Final Choice:** Remains Tkinter for now, but button-based interactions mitigate some D&D complexity concerns.
- **Detailed Error Handling:** Still needs review, especially around edge cases in list manipulation and parsing.
- **Log File Monitoring:** Remains out of scope for the initial version.

## Important Patterns and Preferences

- **Python for core logic.**
- **User-friendly and simple GUI targeted at non-technical gamers.**
- **Modularity in code design (separating parsing, generation, and GUI logic).**
- **Focus on core functionality for the first version, deferring advanced features like direct Discord integration.**

## Learnings and Project Insights

- The user has a very clear and detailed vision for the application's functionality and UI flow, as evidenced by the "Cleric CH Chain Socials Notes.md".
- The choice of an emulated server (Quarm) means log file formats are likely stable but should be confirmed with the provided sample.
- User familiarity with Python makes it a strong choice for rapid development.
- Implementing drag-and-drop in Tkinter requires manual event binding and logic; can be unreliable/unintuitive, leading to preference for button-based alternatives for core list manipulations.
- Parsing log files requires careful handling of specific formats and markers to ensure accuracy.
