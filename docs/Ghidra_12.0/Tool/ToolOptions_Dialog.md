[Home](../index.md) > [Tool](index.md) > Tool Options Dialog

# Tool Options Dialog


Each tool has an *Options* dialog that shows options in a tree format. When you click
on the node, the associated options appear in a panel to the right of the tree. At a minimum,
the tree has a node for key bindings and tool options . Select the node to show the
corresponding options that you can change. Plugins may provide their own options, in which case
new nodes in the tree or new options for the tool may show up. Options provide a flexible way
for changing plugin behavior or functionality.


> **Note:** The Tool Options dialog has a filter text field
that can be used to quickly find options relating to a keyword. Any options names or
descriptions that contain the keyword text will be displayed.


To display the *Options* dialog, select **Edit → Tool Options** from the tool menu.


## **Restoring Default Settings**


You can restore any currently selected options panel to its default settings by pressing
the ***Restore Defaults*** button at the bottom of the options panel. Use caution
when executing this action, as it cannot be undone.


![](images/RestoreDefaults.png)


## **Key Bindings**


You can create a new key binding (*accelerator key*) for an action or modify the
default key binding. The key binding that you add can be used to execute the action using the
keyboard. Below we describe the **Key Bindings** options editor.


> **Tip:** Not all key bindings are changeable via
the tool options. For example, the following keys cannot be changed:


- System Action Keybindings - System action default key bindings can be changed, with
added restrictions: 1) The binding for a System action cannot be used by any other action,
2) A key stroke bound to a System action cannot be used by another action until that
key stroke is cleared from the System action.   The UI will show a message when these
restrictions are triggered.
- Menu Navigation Actions: `1-9, Page Up/Down, End, Home` (these key
bindings are usable with a menu or popup menu open and are otherwise available for
assignment to key bindings).


> **Tip:** You can also change key bindings from
within Ghidra by pressing F4 while the mouse is over any toolbar icon or menu item.
Click here for more info.


The **Key Bindings** option editor has a table with the following sortable columns:
*Action Name*, *Key Binding*, and *Plugin Name*. To change a value in the
table, select the row and then edit the text field below the table.


- The text field below the table captures keystroke combinations entered.
- If an action has a description to explain what it does, it will be displayed below the
text field.


The display below shows the key bindings panel for the *Project Window*. Using the
Key Bindings Options panel works the same as for a regular Ghidra Tool.


![](images/KeyBindings.png)


### Change a Key Binding


To change the Key Binding,


1. Select **Edit** →  **Tool Options** from the main
menu.
2. Select the *Key Bindings* node in the options tree.
3. Select an action name to either set a key binding or change the existing key
binding.
4. Click in the text field and type the key or keystroke combination (e.g., Ctrl x).
- When a key is mapped to multiple actions, the action name is listed below the
text field.
5. Click on the **OK** or **Apply**
button.


![](../shared/note.yellow.png) When a key is mapped to multiple
actions, and more than one of these actions is valid in the current context (i.e., the action
is enabled), then a dialog is displayed for you to choose what action you want to
perform.


To avoid the extra step of choosing the action from the dialog, do not map the same key to
actions that are applicable in the same context.


### Remove a Key Binding


To remove a Key Binding,


1. Select **Edit** →  **Tool Options** from the main
menu.
2. Select the *Key Bindings* node in the options tree.
3. Select an action name for the key binding that you want to remove.
4. Click in the text field for the key binding.
5. Press the ![Delete](../icons/edit-delete.png) button to clear it.
6. Click on the **OK** or **Apply**
button.


Import/Export Key Bindings


### Import Key Bindings


To import a Key Binding,


1. Select **Edit** →  **Tool Options** from the main
menu.
2. Select the *Key Bindings* node in the options tree.
3. Press the **Import...** button.
4. On the warning dialog, press the **Yes** button to import key bindings or the
**No** button to cancel the process.
5. On the file chooser dialog, choose a previously exported file from which to import
key bindings.
6. Press **OK** to import the key bindings.


> **Warning:** Importing key bindings will
override your current key bindings settings. It is suggested that you export your key bindings before you import so that you may revert to your
previous settings if necessary.


> **Note:** After importing you must save your
tool ( File Save Tool ) if you want you changes to persist between tool
invocations.


### Key Binding Short-Cut


A key binding can be applied to any menu item or toolbar icon. For example:


**File**  →  **Close**


**Data**  →  **Cycle**  →  **Cycle: Float,
Double**


Apply key bindings to menu items or icons that are frequently accessed.
To do this:


1. Display a menu item.
2. Place the cursor on the menu item or let the mouse hover over an icon
on the toolbar.


> **Note:** This menu item or icon will be
associated with the Key Binding. When the Key Binding key is used, this menu item or action
associated with the icon will be applied.


1. Press the `<F4>` key to display **Set Key
Binding** dialog:


![](images/SetKeyBindings.png)


1. Enter a key combination in the **Set Key Binding** dialog, The panel below the
text field that accepts the key input shows the other actions that are mapped to the key.
These are potential collisions if these actions are enabled at the same time. Press
**OK** to change the key binding.
2. The key combination that is entered in this dialog will be the key binding for the
menu item.


### Export Key Bindings


To export a Key Binding,


1. Select **Edit** →  **Tool Options** from the menu
bar.
2. Select the *Key Bindings* node in the options tree.
3. Press the **Export...** button.
4. If you have made changes, then you will be prompted to apply those changes before
continuing.
5. On the file chooser dialog, choose a file to which to export key bindings.
6. Press **OK** to export the key bindings.


## **Tool**


*Tool* is a default node in the options tree that shows up in each tool's options
window. The *Tool* panel defines the options for the Tool. The table below lists the
basic options. Plugins may add their own options to the *Tool* options. If a tool does
not have a plugin that uses an option, the option will not show up on the *Tool* panel.
For example, the Ghidra Project Window does not have plugins that use the Max Go to Entries
or Subroutine Model, so these options will not appear on the *Tool* panel. If an option
has a description, it will show up in the description panel below the tree when you pass the
mouse pointer over the component in the options panel.


| **Option** | **Description** |
| --- | --- |
| Copy Strings Without Quotes | If selected, copying strings to the clipboard from                 the listing, decompiler, or bytes viewer will remove outer quotes. |
| Docking Windows On Top | Selected means to show each undocked window on top of                 its parent tool window; the undocked window will not get "lost" behind its parent                 window. Unselected means that the undocked window may go behind other windows once                 it loses focus. Use the Windows menu to make the undocked window visible. |
| Goto Dialog Memory | Selected means that the last goto query will                 remain in the dialog the next time the dialog is invoked. |
| Max Goto Entries | Number of past entries to keep in the [Go to Address or                 Label](../Navigation/Navigation.md#go-to-address-label-or-expression) dialog |
| Max Navigation History Size | Max number of items to retain in the navigation                 history. dialog |
| Show Program Tabs Always | If selected, a program tab will be displayed even                 there is only one program open. |
| Subroutine Model | Sets the default subroutine model. This setting is mainly used when creating                   call graphs. See [Block Models](../BlockModel/Block_Model.md#blockmodeldefinition) for a description of the valid Models. |
| Use C-like Numeric Formatting for                 Addresses | Selected means to attempt to interpret the value entered in the [Go To dialog](../Navigation/Navigation.md#go-to-address-label-or-expression) as a                   number as follows: interpret the value as a hex number if it starts with "0x"interpret the value as an octal number if it starts with "0"interpret the value as a binary number if it ends with a "b" |


To change Tool Options,


1. From the tool, select **Edit** →
**Tool Options**
2. Select the *Tool* node in the options tree.
3. Change the value for the option.
4. Click on the **OK** or **Apply**
button**.**


### **Tool**


Some **Tool** options can only be set from the [Front End](../FrontEndPlugin/Ghidra_Front_end.md). Some of those are described
below.


| **Option** | **Description** |
| --- | --- |
| Allow Blinking Cursors | This controls whether text components and other                 components that have a text cursor will blink when they have focus. |
| Automatically Save Tools | This controls whether Ghidra will save tool state                 when the tool is closed. |
| Default Tool Launch Mode | This controls if a new or already running tool should                 be used during default launch. Tool "reuse" mode will open selected file within a                 suitable running tool if one can be identified, otherwise a new tool will be                 launched. |
| Docking Windows On Top | Selected means to show each undocked window on top of                 its parent tool window; the undocked window will not get "lost" behind its parent                 window. Unselected means that the undocked window may go behind other windows once                 it loses focus. Use the Windows menu to make the undocked window visible. |
| Restore Previous Project | This controls whether or not Ghidra automatically                 opens the previously loaded project on startup. |
| Show Tooltips | This controls whether or not Ghidra will show                 tooltips. |
| Use DataBuffer Output Compression | This controls whether or not Ghidra will compress                 data being sent to the server. |
| Use Notification Animation | This controls whether or not Ghidra will use                 automations to provide visual feedback that something is happening, such as                 launching a tool. |


### **Program Caching**


Some features of Ghidra require opening programs briefly. Often the same set of programs
may need to be opened repeatedly. Ghidra provides a caching service to make these uses more
efficient. The following two options are available:


| **Option** | **Description** |
| --- | --- |
| Program Cache Size | This options                 specifies the maximum number of programs to keep open in the cache. |
| Program Cache Duration |  |


**Related Topics:**


- [Go to Address or
Label](../Navigation/Navigation.md#go-to-address-label-or-expression)
- [Subroutine Model](../BlockModel/Block_Model.md)


---

[← Previous: Default Tools](Ghidra_Tool_Administration.md) | [Next: Create Tool →](Ghidra_Tool_Administration.md)
