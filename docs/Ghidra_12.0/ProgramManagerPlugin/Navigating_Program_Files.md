[Home](../index.md) > [ProgramManagerPlugin](index.md) > Navigate Programs

# Navigating Programs


Open programs are represented in Ghidra by tabs at the top of the Listing. You may click on
these tabs to change the active program. Also, as described below, there are various actions
that allow you to change the active program.


![](images/ProgramTabs_No_Hidden.png)


*Program Tabs*


When there are more open programs than room to display their
respective tabs, then a button is displayed to access those programs. This button displays the
number of hidden programs.


![](images/ProgramTabs_With_Hidden_More_Button.png)


*Program Tabs 'More Button'*


To access these hidden programs, click the button to display
a menu for selecting programs.


![](images/ProgramTabs_With_Hidden_Popup_Window.png)


*Program Tabs With Popup Window*


The popup window displayed allows you to select a tab
by clicking a program name, or by using the **up** and **down arrow** keys to select a
program name and then pressing the **Enter** key to choose the selected program. Also,
typing text data will filter the displayed program list. You can close the popup window without
making a selection by pressing the **Escape** key or by clicking a component outside of the
window.


Those programs listed in bold are those that are hidden.


> **Tip:** The order of the tabs can be changed
using drag-n-drop. Drag the tab that you wish to move and drop it on the tab where you
like it to appear.


## Navigation Actions


Next and Previous


### Go To Next Program and Go To Previous Program Actions


The next and previous actions are only available via keybindings, which by default are
**Control-F8** and **Control-F9** for previous and next, respectively. You may change
these bindings from the [Key Bindings Options](../Tool/ToolOptions_Dialog.md#key-bindings).


The next and previous actions allow you to move between open tabs. For example, when the
**Go To Next Program** action is executed, the tab to the right of the current tab is
highlighted.


![](images/ProgramTabs_With_Highlighted_Tab.png)


*Next Tab Highlighted*


After a brief pause, the highlighted tab will become the active program. Quick, repeated
executions of the action will continue to move the highlighted tab to the right.


The **Go To Previous Program** action works in the same way as the **Go To Next
Program** action, except that it moves the highlight to the left instead of the
right.


The operation of tab highlighting varies slightly depending upon the existence of [hidden tabs](#hidden-tabs). Without hidden tabs, the highlighting, when starting
from the first or last available tab, will wrap around to the other side of the tab list.
In this mode, you may highlight tabs with no limits with no program being activated until
you stop.


Contrastingly, if there are [hidden tabs](#hidden-tabs), then when the first
or last tab is highlighted, then the next successive highlight action will trigger the [more tabs button](#more-tabs-button) to be executed.


Go to Program...


### Go To Program... Action


The **Go To Program...** action will show the program selection popup window when executed. This menu
allows you to pick a program to go to.


![](images/ProgramTabs_With_Hidden_Go_to_Program.png)


*Go To Program Popup Window*


To execute this action, from the Tool menu, select **Navigation → Go To Program...**.


Go to Last Active Program


### Go To Last Active Program Action


The **Go To Last Active Program Action** will activate the last program that was
active before the currently active program. Thus, this action is disabled when you do not
have a previously active program.


To execute this action, from the Tool menu, select **Navigation → Go To Last Active Program**.


&gt;




*Provided by: *Program Manager* Plugin*


**Related Topics:**


- [Opening Program Files](Opening_Program_Files.md)
- [Closing Program Files](Closing_Program_Files.md)


---

[← Previous: Close Program](Closing_Program_Files.md) | [Next: Rename Program →](../FrontEndPlugin/Ghidra_Front_end.md)
