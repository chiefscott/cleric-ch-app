Cleric CH Chain Socials Notes

Create an app that creates the CH Chain and their macros for the Guild.

Things we need to figure out:
Discord Integration
Zeal Pipeline (ALTERNATIVE: Trigger word for like <CLERIC CH WHO> and then a /who guild cleric to get the names from there)

Functions:
Gather Cleric Names
Create the chain list via GUI
Create the chain list macro (Assignments Message)
Create the macro for each cleric

Template:
(Assignments Call)
/2 CH Chain: 111 Fester, 222 Nadi, 333 Haeler, 444 Friar
/2 2 sec cheal chain pre-slow (/pause 20). 4 sec cheal chain pre-slow (/pause 40)
/2 Patch Heals(Fluffers):

(CH Macro)
/pause 1, /stand 
/cast #
/cast # 
/pause 20, /shout 111 CH on %t 111 2 Second Chain %n mana
/shout 222 Go  222! 2 Second Chain

Variables:
111 through III (18 in total possible chain)
Seconds: 1, 1.1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6
Patch Healer Roles

GUI:
    Tabs at top (Setup, Assignments, Macros)
    Assignments: (Bars with each name; Populated by Cleric Who Button; Dynamic Bar Amounts by Cleric Who, A Fluffers Section)
    Macros: (Buttons with each clerics name,on click copies their macros in a formatted msg for discord copy paste dm)

Buttons:
    Setup:
        Log File
        Clear

    Assignments: 
        Cleric Who
        Add Cleric
        Remove Cleric
        Slowable? (Checkbox)
        Seconds (Drop Down Box)
        Create Macros

    Macros:
        Cleric Channel Message
        Send Macros (Discord Implementation)
        Invidual Buttons Per Cleric (On click copies their macros in a formated msg)


Button & App Logic:
Assignments list from top to bottom are:
First: 111
Second: 222
Third: 333

After 999 it would AAA
Tenth: AAA
Eleventh: BBB
Twelth: CCC
etc.

Fluffers:
A section that clerics can be dragged dropped to
If a cleric is in this section, they are not part of the "Chain"
They will have no macro created for them and only be recognized in the Assignments Message that's created.

Log File:
Tells App to look at this file for the <CLERIC CH WHO> trigger word to find list of cleric names
System File Browse Prompt (Remembers last choice)

Cleric Who:
Looks for most recent <CLERIC CH WHO> in the log and then receives the list based on that

Seconds Dropdown:
List of Seconds which then would signify which /pause to use when creating the macros
List of options: Custom, 1, 1.1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6
Custom = Set your own pause amount

Pause:
/pause 20 = 2 seconds
/pause 1 = 1 seconds
etc. (Use math to figure rest)

Add Cleric:
Adds a dynamic cleric to the Assignments Tab
Textbox Prompt to enter the name

Remove Cleric:
Each Bar with each clerics name should have an X on the right side to remove them from the list.
If a set of macros was created already, it would signify a recreation of the macros and adjust them accordingly
IE:
Example Cleric is assigned 222
Example Cleric is removed from list
The cleric that was assigned 333 would be shifted down to be 222 and all other clerics as well would need to altered

Clear:
Clears everything on App: Assignments and Macros Tab
Would need to re-initialize with Cleric Who to repopulate

Slowable? (Checkbox):
Indicates that the target is slowable which means we would need two sets of Seconds Selection and two sets of Macros for each cleric made
On checkbox a 2nd "Seconds" Dropbox Menu would apear
2nd "Seconds" Dropbox would be titled "Slow Seconds" and the same options

Macro Copy:
On the macro tab there will be each clerics alias listed in order of assignment
It should look like:
111 ALIAS 111
222 ALIAS 222
333 ALIAS 333 etc.
Each will be a button formatted for a discord message

Macro Template Logic:
/pause 1, /stand 
/cast #
/cast # 
/pause 20, /shout 111 CH on %t 111 2 Second Chain %n mana
/shout 222 Go  222! 2 Second Chain

Using the above as example.. Here is a Syntax Explanation:
111 = Assignment of THAT Player
222 = Assignment of NEXT Player
/pause 20 = 2 Second Chain was selected
2 Second Chain = 2 Second Chain was selected

If Slowable? was selected there would be a second macro created for each player, tailored to the slowable seconds but the assignment order would be the same.

All the rest of the template that WASNT mentioned would be constant and does not need to be altered.

Discord Message Template:
Hello %ALIAS%,

Here is your CH Macro.
Please change # to what ever your Complete Heal is on your spell gems.
Macro:
/pause 1, /stand 
/cast #
/cast # 
/pause %Seconds Variable%, /shout %Assignment% CH on %t %Assignment% %Selected Seconds% Second Chain %n mana
/shout %Next Player Assignment% Go  %Next Player Assignment%! %Selected Seconds% Second Chain

If Slowable? was selected there would be a different message.
An Example:
Slowable? Discord Message Template:
Hello %ALIAS%,

Here is your CH Macro.
Please change # to what ever your Complete Heal is on your spell gems.
First Macro:
/pause 1, /stand 
/cast #
/cast # 
/pause %Seconds Variable%, /shout %Assignment% CH on %t %Assignment% %Selected Seconds% Second Chain %n mana
/shout %Next Player Assignment% Go  %Next Player Assignment%! %Selected Seconds% Second Chain

Slow Macro:
/pause 1, /stand 
/cast #
/cast # 
/pause %Slow Seconds Variable%, /shout %Assignment% CH on %t %Assignment% %Selected Slow Seconds% Second Chain %n mana
/shout %Next Player Assignment% Go  %Next Player Assignment%! %Selected Slow Seconds% Second Chain

Cleric Channel Message:
This button would copy the Assignments Template to be sent to the "Cleric Channel" ingame.
Here is the template:
/2 CH Chain: 111 %Alias1%, 222 %Alias2%, 333 %Alias3%, 444 %Alias4%, etc.
/2 %Selected Seconds% sec cheal chain pre-slow (/pause %Pause Variable%). %Selected Slow Seconds% sec cheal chain slowed (/pause %Slow Pause Variable%)
/2 Patch Heals(Fluffers): (%Fluff Alias1%, %Fluff Alias2%, %Fluff Alias 3%)

~~~~~~~~~~

Future Improvements:
Discord Integration
Zeal Pipeline (ALTERNATIVE: Trigger word for like <CLERIC CH WHO> and then a /who guild cleric to get the names from there)

Future Functions:
Get Cleric List of Raid from Zeal
Associate Cleric Names with Discord Names
Message Macros to each cleric in discord