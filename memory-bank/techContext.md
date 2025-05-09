# Technical Context

This document details the technologies, development setup, and technical constraints of the project.

## Technologies Used

- **Programming Language:** Python (version 3.x)
- **GUI Framework:** Tkinter (recommended starting point due to Python familiarity and built-in nature) or potentially PyQt/PySide6 if more advanced features/styling are needed later.
- **Installer Creation:** PyInstaller
- **Operating System Target:** Windows (initially)

## Development Setup

- A standard Python development environment.
- VS Code with Python extension (or preferred Python IDE).
- Installation of PyInstaller for creating the distributable.
- (If PyQt/PySide6 is chosen): Installation of the respective library.

## Technical Constraints

- The application must parse plain text log files specific to the Everquest (Quarm emulated server) format, identifying names listed between start/end markers after a trigger phrase.
- GUI must be responsive enough for smooth user interaction, including scrollable lists for potentially long cleric/macro lists.
- Must run on Windows without requiring users to install Python separately (achieved via PyInstaller).
- Log file parsing must be efficient (reading from end) to handle large files without freezing the app.
- In-memory data storage for session information (cleric lists, assignments, etc.). Configuration file (`settings.json`) for persisting `log_file_path` and `cleric_channel`.
- Installer to be hosted on GitHub.

## Dependencies

- **Python Standard Library:** `os`, `re`, `json`, `tkinter` (including `tkinter.ttk`, `tkinter.filedialog`, `tkinter.messagebox`, `tkinter.simpledialog`)
- **External (if not purely Tkinter/stdlib):**
    - PyInstaller (for building)
    - PyQt/PySide6 (if chosen over Tkinter)

## Tool Usage Patterns

- **Log Parsing:** Efficiently read file backwards line-by-line using a generator (`_reverse_readline`). Identify the last trigger phrase. Parse subsequent lines, identifying start/end markers (`---`, `There is/are...`) to isolate the player list block. Use regular expressions (`re.search`) within this block to extract cleric aliases.
- **GUI Event Handling:** Standard event-driven programming for button clicks (`ttk.Button`), dropdown selections (`ttk.Combobox`, `<<ComboboxSelected>>`), checkbox changes (`ttk.Checkbutton`), listbox selections (`tk.Listbox`, `<<ListboxSelect>>`), and dialog interactions (`simpledialog`).
- **List Management:** Use Python lists (`self.clerics`, `self.fluffers`) as the model. Update lists based on user actions (Add, Remove, Move Up/Down, Move to Fluffers/Chain buttons). Refresh `tk.Listbox` content from the model lists.
- **Text Manipulation:** String formatting (`f-strings`) and templating for generating macros and assignment messages.
- **Clipboard Interaction:** Using Tkinter's root window clipboard methods (`clipboard_clear`, `clipboard_append`).
- **Drag and Drop:** Manual implementation using Tkinter event bindings (`<ButtonPress-1>`, `<B1-Motion>`, `<ButtonRelease-1>`) and state management (`self.drag_data`) primarily for moving items between the Clerics and Fluffers listboxes. Button-based interactions are preferred for reordering within a list.
- **Scrolling:** Use `ttk.Scrollbar` attached to `tk.Listbox` widgets. For the macro button area, a scrollable frame/canvas pattern might be needed.
- **Configuration:** Use `json` module to load/save settings (`log_file_path`, `cleric_channel`) from/to `settings.json`.
