[Home](../index.md) > [Selection](index.md) > Selection

# Selecting


Selecting is the process of [highlighting](../SetHighlightPlugin/Highlighting.md) all or portions of a program
in order to perform a task (for example, modular analysis) on the selection. Selecting can be
done manually in providers that support selection, like the [Code Browser](../CodeBrowserPlugin/CodeBrowser.md). Selecting can be done based
on subroutines, functions, or by following certain types of control flows in the program.


Selections can be created manually within the Code Browser. There are also some predefined
types of selections that are available from the tool **Select** menu. Each predefined type
of selection exposes different characteristics of the program.


To create a selection using one of the predefined methods via the menu item
**Select*****→ SelectionType**.*


The ***SelectionTypes*** and their descriptions are as follows:


| Predefined Selection Methods |  |
| --- | --- |
| Selection Type | Description |
| --- | --- |
| Program Changes | Select all program changes. |
| All Flows From | This follows all program flows from the cursor location if no selection                         or from the selected code units if there is a selection. Select All Flows                         will traverse all branches conditional and unconditional. All the code                         units that are traversed are selected. |
| All Flows To | This selects all program flows to the cursor location if no selection                         or to the selected code units if there is a selection. Select All Flows To                         will traverse all branches conditional and unconditional. All the code                         units that are traversed are selected. In other words, this follows all program flows backwards from the                          location or selection. |
| Limited Flows From | The types of program flows to be followed in this case are based on                         options configured on theSelection by Flow                         Options tab. Limited Flows only follows the indicated types of program                         flows from the cursor location if no selection or from the selected code                         units if there is a selection. All the code units that are traversed are                         selected. |
| Limited Flows To | The types of program flows to be followed in this case are based on                         options configured on theSelection by Flow                         Options tab. Limited Flows To only follows the indicated types of program                         flows to the cursor location if no selection or to the selected code                         units if there is a selection. All the code units that are traversed are                         selected. In other words, this follows the types of program flows, as indicated                           by the options, backwards from the location or selection. |
| Subroutine | If there is no selection, this selects the code units of the subroutine                         that contains the current cursor location. If there is a selection, this                         selects all the subroutines that contain the selected code units. |
| Dead Subroutines | Selects the code units of all                       subroutines that not directly referenced, also known as "dead" code. |
| Function | If there is no selection, this selects the code units of the function                         that contains the current cursor location. If there is a selection, this                         selects all the functions that contain the selected code units. |
| All in View | Selects all code units being displayed in the browser view. |
| Clear Selection | Clears the current selection in the browser view. |
| Complement | Changes the selection to everything in the current view that                       is not in the current selection.   |
| Mark and Select | Creates a selection in a two step process. The first time                       the action is invoked, the current location is marked. The second time the                       action is invoked, a selection is created from the marked location to the                       current location.   |
| Data | Selects all the defined data in the                       current program if there isn't a selection. Otherwise, it selects the defined                       data within the current selection. |
| Instructions | Selects all the instructions in the                       current program if there isn't a selection. Otherwise, it selects the                       instructions within the current selection. |
| Undefined                       Data | Selects all the undefined data in                       the current program if there isn't a selection. Otherwise, it selects the                       undefined data within the current selection. |
| Forward                       Refs | Selects all addresses that the                       current address is referring to. |
| Back                       Refs | Selects all addresses that refer to                       the current address. |


Selections are meant to be temporary. For example, a left mouse click outside a selection in
the Code Browser will make the selection go away. Also, creating a new selection replaces any
previous selection rather than adding to it. To retain a selection in a manner that isn't so
transient, change it to a [highlight](../SetHighlightPlugin/Highlighting.md).


> **Note:** At any time you can
restore the previous selection for the current program by pressing the Select Restore Selection.


### Selection by Flow Tool Options


The *Select By Flow* plugin adds options to the tool. To view or edit the option
settings:


- From the tool's menu select **Edit*****→*****Tool Options...**
- Click on the *Selection by Flow* tree node


The *Selection by Flow* tab contains options for indicating the types of flows that
will be followed when selecting *Limited Flows*. The table below lists the Selection by
Flow options and their default settings. To follow a particular flow type simply click on the
box to check it.


| Flow Type to                 Follow | Default |
| --- | --- |
| Follow computed call | false |
| Follow computed jump | false |
| Follow conditional call | false |
| Follow conditional jump | true |
| Follow pointers | false |
| Follow unconditional call | false |
| Follow unconditional jump | true |


Example: Given *Follow conditional jump* and *Follow unconditional jump*
are the only types checked. As the program flow is followed the instructions that are
encountered are added to the selection, wherever the program jumps will also get added to the
selection and the program flow is also followed from there. If a conditional call is
encountered, then this instruction gets added to the selection. But the conditional call is
not followed and the code at the call's destination is not added since this type isn't being
followed. *The code for the subroutine at the call's destination could still end up in the
selection, if it is flowed to by a different flow path using the flow types being
followed.*


*Provided by: *Select By Flow* Plugin*


---


## Navigating Over a Selection


A selection will often consist of one or more address ranges. The address ranges do not have
to be contiguous. The navigation margin can be used to directly move the location to a
particular selected range. To move to the next or previous selection range relative to the
current cursor location use the Next Selected Range and Previous Selected Range buttons.


### Using the Navigation Margin


One or more green markers will appear in the [Navigation Margin](../CodeBrowserPlugin/CodeBrowser.md#cbnavigationmarkers),
where each green marker corresponds to an address range included in the selection. Clicking
on a green marker will cause the Code Browser to navigate to the beginning of the
corresponding address range.


### Next Selected Range


To move the program's cursor location to the beginning of the next selected range of
addresses:


From the menu-bar of the Code Browser, select **Navigation*****→*** **Next Selected Range**


OR


From the tool-bar of the Code Browser, click the **Go to next selected range** (![NextSelectionBlock16.gif](../icons/NextSelectionBlock16.gif)) button


*When the Code Browser is on or after the
last address range in the selection, the "Next Selected Range" menu-bar and tool-bar options
will be disabled.*


### Previous Selected Range


To move the program's cursor location to the beginning of the next selected range of
addresses:


From the menu-bar of the Code Browser, select **Navigation*****→*****Previous Selected Range**


OR


From the tool-bar of the Code Browser, click the **Go to previous selected range**
(![PreviousSelectionBlock16.gif](../icons/PreviousSelectionBlock16.gif)) button


*When the Code Browser is on or before the first
address range in the selection, the "Previous Selected Range" menu-bar and tool-bar options
will be disabled.*


*Provided by: *Go To Next-Previous Selected Range* Plugin*


**Related Topics:**


- [Margin &
Navigation Markers](../CodeBrowserPlugin/CodeBrowser.md#cbnavigationmarkers)
- [Navigation](../Navigation/Navigation.md)
- [Highlighting](../SetHighlightPlugin/Highlighting.md)


---

[← Previous: Margin and Navigation Markers](../CodeBrowserPlugin/CodeBrowser.md) | [Next: Selection by Flow →](../FlowSelection/Selection_By_Flow.md)
