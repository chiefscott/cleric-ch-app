# Project Brief

This document serves as the foundational document for the project, outlining its core requirements, goals, and scope.

## Project Name

Everquest Cleric CH (Complete Heal) Chain Assistant

## Project Goals

- To create a desktop application that helps Everquest players (specifically clerics) manage and generate in-game macros for "CH Chains".
- To streamline the process of assigning clerics to a healing chain and generating the necessary text commands for them to use in-game.
- To provide a user-friendly GUI for easy interaction.
- To create an installer for easy sharing of the application with other players.

## Scope

The application will:
- Read an Everquest log file to identify available clerics based on a user-triggered in-game command (e.g., `<CLERIC CH WHO>`).
- Allow users to customize the trigger phrase for identifying clerics.
- Allow users to manually add or remove clerics from an assignment list.
- Enable users to assign clerics to a numbered chain (111, 222, etc., up to 18 clerics).
- Allow users to designate some clerics as "Fluffers" (patch healers) who are not part of the main numbered chain.
- Generate a formatted "Assignments Message" for in-game channels, listing the chain assignments and fluffers.
- Generate individual macros for each cleric in the chain, including appropriate `/pause` commands based on user-selected chain timing (e.g., 2-second chain, 4-second chain).
- Support different macro generation if the target is "slowable" (requiring two sets of timings/macros).
- Provide functionality to copy generated messages and macros to the clipboard.
- Include a GUI with tabs for Setup, Assignments, and Macros.
- Target the Windows operating system initially.
- Store data in-memory during an application session.
- Remember the last used log file path.

Future Scope (Not for initial version):
- Direct Discord integration for sending macros.
- Integration with Zeal pipeline for gathering cleric names.

## Stakeholders

- The primary user and developer (you).
- Other Everquest players in your guild or community who will use the app.

## Key Requirements

- **Log File Parsing:** Must parse Everquest log files (Quarm server format) to find cleric names following a specific trigger. Timestamps should be ignored. The cleric's alias needs to be extracted.
- **GUI:** Must have a graphical user interface with Setup, Assignments, and Macros tabs.
- **Macro Generation:** Must accurately generate macros based on templates, cleric assignments, and selected timings.
- **Customization:** Users must be able to customize the trigger phrase and select chain timings.
- **Installer:** An installer must be created for easy distribution on Windows.
- **Error Handling:**
    - Grey out functionalities if no log file is selected.
    - Error pop-up if no clerics are found after a trigger.
- **Data Management:** In-memory storage for cleric lists and assignments per session. Remember log file path between sessions.