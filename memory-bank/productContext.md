# Product Context

This document describes the purpose and function of the project from a product perspective.

## Why this project exists

This project exists to solve the manual and potentially error-prone process of organizing and communicating "Complete Heal (CH) Chains" for cleric groups in the game Everquest. Setting up these chains quickly and accurately during raids or group play is crucial for success. This tool aims to automate the generation of assignments and the corresponding in-game macros, reducing setup time and ensuring consistency.

## How it should work

The user (an Everquest player, likely a cleric or raid leader) will:
1.  **Setup:**
    *   Specify the path to their Everquest log file. The app will remember this path.
    *   Optionally customize the in-game trigger phrase the app looks for to identify clerics (default: `<CLERIC CH WHO>`).
    *   Select the in-game channel number used for cleric communication (e.g., `/2`, `/3`) from a dropdown (default: 2). This setting is remembered.
2.  **Gather Clerics:**
    *   In-game, the user types the trigger phrase, followed by a command like `/who guild cleric`.
    * In the app, the user clicks a "Cleric Who" button. The app reads the log file from the bottom up, finds the most recent trigger, and parses the subsequent lines to list available clerics (extracting their aliases).
3.  **Assign Clerics:**
    *   On the "Assignments" tab, the app displays the list of found clerics in the main "Clerics" listbox. Scrollbars are provided for long lists.
    *   The user can manually add clerics using an "Add Cleric" button.
    *   The user can remove a selected cleric from the main list using a "Remove Selected Cleric" button.
    *   The user can change the order of clerics in the main list (which determines their chain number) using "Move Up" and "Move Down" buttons acting on the selected cleric.
    *   Clerics are automatically assigned a chain number (111, 222, ..., AAA, BBB, ...) based on their final order in the main list.
    *   The user can designate clerics as "Fluffers" (patch healers not in the numbered chain) by selecting a cleric in either the main list or the Fluffers list and using "Move to Fluffers" or "Move to Chain" buttons. (Drag-and-drop between lists might also be supported but buttons provide primary mechanism). The Fluffers list also has a scrollbar.
    *   The user selects the desired chain timing (e.g., 2 seconds, 3.5 seconds, or Custom) from a dropdown. If "Custom" is chosen, a dialog prompts for the specific value.
    *   The user can check a "Slowable?" box, which reveals a second timing dropdown (also supporting "Custom") for macros used when a target is slowed. The layout ensures this second dropdown is visible.
    * The user clicks a "Create Macros" button.
4.  **Use Macros:**
    *   The "Assignments" tab will display a generated "Assignments Message" (based on a template using the selected Cleric Channel number) listing all chain assignments and fluffers. A button allows copying this message for pasting into the designated in-game cleric channel.
    *   The "Macros" tab will display individual buttons for each cleric in the numbered chain, within a scrollable area. Clicking a cleric's button copies their personalized in-game macro (formatted within a user-friendly message template, including their assignment, the next cleric's assignment, and selected timings) to the clipboard for easy distribution (e.g., via Discord DM or in-game tells).
    *   If "Slowable?" was checked, the copied text for each cleric will include both the normal macro and the slow macro.

## User Experience Goals

- **Efficiency:** Significantly reduce the time and effort required to set up CH chains.
- **Accuracy:** Minimize errors in macro creation and assignments.
- **Ease of Use:** Provide an intuitive and straightforward GUI that is easy for non-technical Everquest players to understand and use.
- **Clarity:** Clearly display assignments and generated macros.
- **Helpfulness:** The app should feel like a helpful assistant for a common in-game task.
