# System Patterns

This document outlines the system architecture, key technical decisions, and design patterns used in the project.

## System Architecture

- **Desktop Application:** Standalone GUI application running on Windows.
- **Single Process:** The application will run as a single process.
- **Event-Driven GUI:** The UI will respond to user inputs (button clicks, selections).
- **Modular Design (Conceptual):**
    - **LogParser Module:** Responsible for reading (efficiently from end) and parsing the Everquest log file, identifying the relevant `/who` block.
    - **MacroGenerator Module:** Responsible for creating assignment messages (using selected channel) and individual cleric macros based on templates, assignments, and user input (timings, slowable).
    - **GUI Module:** Manages the user interface (Tkinter components), user interactions (button clicks, selections, list manipulation), and display updates (including scrollable lists).
    - **StateManager Module (Implicit):** Handles the in-memory state of cleric lists (order matters), assignments, fluffer list, selected timings (including custom), slowable state, trigger phrase, and selected cleric channel. Also handles loading/saving persistent settings (log file path, cleric channel).

## Key Technical Decisions

- **Language Choice: Python:** Chosen due to user familiarity and suitability for text parsing and rapid GUI development.
- **GUI Framework: Tkinter (initial):** Chosen for simplicity and being built-in with Python, reducing external dependencies for basic needs. Open to PyQt/PySide6 if Tkinter proves insufficient.
- **Installer: PyInstaller:** Chosen for its wide adoption and ease of use for packaging Python applications for Windows.
- **Log File Access: Read-only, efficiently from end:** Uses a reverse-readline approach to handle large files without high memory usage when searching for the trigger. Parsing focuses on lines between identified start/end markers.
- **Data Persistence: In-memory for session, config file for settings:** Cleric lists, assignments, fluffers, timings are volatile per session. Log file path and selected Cleric Channel number are persisted in `settings.json`.

## Design Patterns

- **Model-View-Controller (MVC) or Model-View-Presenter (MVP) (Loosely):** While not strictly enforced for a simple application, the separation of concerns is beneficial:
    - **Model:** Data structures holding cleric info, assignments, macro templates, settings. The LogParser and MacroGenerator can be seen as contributing to or acting upon the model.
    - **View:** The Tkinter/PyQt GUI elements.
    - **Controller/Presenter:** The Python code that handles UI events, updates the model, and tells the view to refresh.
- **Template Method Pattern (Implicitly for Macros):** The structure of the macros is fixed (template), but specific parts (alias, numbers, pauses) are filled in based on current data.
- **Observer Pattern (Potentially):** If cleric lists or settings change, relevant parts of the UI could observe these changes and update automatically (e.g., re-generating macro buttons if a cleric is removed). Currently implemented via direct updates triggered by user actions (e.g., button clicks call update methods).
- **Drag and Drop (Manual Implementation):** Tkinter's limited native support requires manual event binding and state management. Used for moving clerics between the main list and Fluffers list, and potentially for reordering within the main list (though button-based alternatives are being prioritized for reliability).
- **Command Pattern (Implicitly):** UI actions (button clicks like "Remove Selected", "Move Up", "Move Down", "Move to Fluffers") trigger specific methods that encapsulate the command to modify the application state (Model) and update the UI (View).

## Component Relationships

1.  **User** interacts with **GUI Module**.
2.  **GUI Module** captures user actions (e.g., "Cleric Who" button click).
3.  For "Cleric Who", **GUI Module** invokes **LogParser Module**, passing the log file path and trigger phrase.
4.  **LogParser Module** reads the log file (using `_reverse_readline`), finds the last trigger, parses subsequent lines between markers, and returns a list of cleric names.
5.  **GUI Module** updates its display (populates scrollable listboxes in "Assignments" tab) and updates the internal **StateManager** (cleric list).
6.  User configures assignments (using Add/Remove/Move buttons), timings (dropdowns, custom dialogs), slowable state (checkbox), and cleric channel (dropdown) via **GUI Module**, which updates the **StateManager**. StateManager recalculates assignments (`generate_assignments`) when cleric list/order/fluffer status changes.
7.  When "Create Macros" button is clicked, **GUI Module** instructs **MacroGenerator Module** (using data from **StateManager** - assignments, timings, slowable state) to produce the individual macro texts (formatted for Discord). GUI Module then creates/updates buttons in the scrollable macro area. The Assignments Message is updated automatically by the StateManager/GUI when assignments change.
8.  When copy buttons (Assignments Message or individual macro buttons) are clicked, **GUI Module** retrieves the relevant text (from the Text widget or generated macro text) and copies it to the clipboard.

## Critical Implementation Paths

- **Log File Parsing:** Accurately and efficiently finding the trigger and extracting cleric names. This includes robust regex and handling cases where the trigger isn't found or no valid names follow.
- **Macro Generation Logic:** Correctly substituting variables into the macro templates based on chain order, selected timings, and the "slowable" state. Calculating correct `/pause` values.
- **GUI Layout and Responsiveness:** Ensuring the GUI is intuitive and doesn't lag, especially the dynamic elements like the cleric assignment list.
- **State Management:** Correctly managing the list of clerics, their order, their "Fluffer" status, and ensuring macros are regenerated when relevant data changes (e.g., a cleric is removed).
