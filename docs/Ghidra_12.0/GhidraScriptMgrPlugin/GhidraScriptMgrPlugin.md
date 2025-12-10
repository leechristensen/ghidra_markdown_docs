[Home](../index.md) > [GhidraScriptMgrPlugin](index.md) > Add and Remove Script Directories

# Ghidra Script Manager


The Ghidra Script Manager allows for rapid development of extended Ghidra functionality.
Unlike conventional Ghidra plugins that require a full IDE for development, Ghidra scripts can
be developed right inside of Ghidra while it is running. You can interactively change your
script and immediately re-run it.


See [Ghidra Script Development](ScriptDevelopment.md) for details on how to
write a script.


![Ghidra Script Manager](images/Script_Manager.png)


### Script Category Tree


The script category tree will organize scripts by category. If you click on
a node of the tree it will only display scripts in the table that are in that category or
any sub-categories. Each script defines its own category, which is arbitrary and optional.
Scripts without explicitly defined categories will appear in the root "Scripts"
category.


### Script Table


The script table displays information about the scripts.


#### In Tool Column


The *In Tool* column provides a checkbox that allows a script to be run directly
from the tool instead of just from the script manager window. If a script has a menu path
(@menupath) defined in its header's meta data section, then an action will be created at
that menu location. Otherwise, a menu item will be created under the tool's
*Scripts* menu and if applicable under any sub-menus corresponding to its category
(@category). In either case, that menu item can be used to run the script.


Also, if the script has a key binding (@keybinding) defined in it's header, then
selecting the *In Tool* option will allow the script to be run by pressing that
key combination. Similarly, having the toolbar meta data set (@toolbar), will result in a
top level toolbar item being created that can be used to run the script.


#### *Status Column*


*The Status* Column indicates the status of the script. A blank field is a happy
field. If the column contains ![Error](../icons/emblem-important.png) , then that
script contains an error.


#### Filename Column


The *Filename* column indicates the filename of the script.


#### Description Column


The *Description* column indicates the description as defined in the meta-data
comment of the script.


#### Key Binding Column


The *Key Binding* column indicates the key binding associated to that script. If
the field is blank, then a key binding has not been assigned to the script.  Setting
a key binding will cause an action to get created and therefore the first column will
become checked.


### Filter


The *Search Filter* allows you to narrow the list of scripts displayed in the
table. Only those scripts, whose name or description contains the string that you enter as
the filter, will be displayed. As you type, the table is updated to reflect the filter.


### Description Panel


The *Description Panel* allows you to view meta data about the **selected**
script in the *Script Table*, including such things as author, description, key
binding, etc.


## Script Manager Actions


### Run Script ![play.png](../icons/play.png)


Runs the selected script. If the script source file or any source in
its script directory are out of date, then it's all (re)compiled. If the compilation is
successful, then the script will be run. If the script does not compile, the compilation
errors will be displayed in the [Console](../ConsolePlugin/console.md) and an error icon ![Error](../icons/emblem-important.png) will be displayed in the first column of the table.


![](images/Console.png)


### Run Last Script ![play_again.png](../icons/play_again.png)


Runs the last run script. This action is available as a keybinding from
within anywhere in the tool, whether or not the Script Manager is showing. To see the
current keybinding for this action, hover over its icon in the toolbar of the Script
Manager.


### Script Quick Launch


This key binding action will show a dialog to allow you to quickly select a
script to be run. You may type any part of the name of the desired script in the dialog's
text field. An asterisc may be used as a globbing character.


You may either use the mouse to choose the desired script from the popup list or press
the Enter key to selected the highlighted list element.


![](images/ScriptQuickLaunchDialog.png)


### Edit Script ![accessories-text-editor.png](../icons/accessories-text-editor.png)


Edits the selected script. For more information on script meta data, see [Ghidra Script Development](ScriptDevelopment.md#meta-data)


![](images/Edit_Script.png)


#### Refresh ![Refresh](../icons/reload3.png)


Will load the contents of the current script from the file on the
filesystem. This action is useful if you have edited the script outside of Ghidra and
would like to have the editor update to show those changes.


#### Save ![disk.png](../icons/disk.png)


Saves the changed script back to the original file. The *Save*
option is only enabled when changes have been made.


#### Save As... ![disk_save_as.png](../icons/disk_save_as.png)


Saves the script (with any changes) to a new script file. The default
directory is your home directory, however if additional script directories exist, then
you will be prompted to select a directory. This new script file becomes the active
script in the editor. When selecting *Save As...*, Ghidra will prompt for a
filename.


![](images/SaveAs.png)


#### Undo ![Undo](../icons/edit-undo.png)


Undo reverts the editor to the state prior to the last edit. You can undo
up to 50 edits.


#### Redo ![Redo](../icons/edit-redo.png)


Redo returns the last edit back into the editor.


#### Select Font ![text_lowercase.png](../icons/text_lowercase.png)


Changes the font for all open editors. It will also set the default font
that will be used for all future editors. The dialog allows you to specify the font type,
size, and style.


![](images/Select_Font.png)


### Edit Script with Eclipse ![eclipse.png](../icons/eclipse.png)


Edits the selected script in Eclipse using the GhidraDev plugin.


*Before a script can
be edited in Eclipse, an Eclipse installation and workspace directory must be defined in
the Tool's [Eclipse
Integration](../EclipseIntegration/EclipseIntegration.md) options.*


*For more information
on developing Ghidra scripts in Eclipse, see
Extensions/Eclipse/GhidraDev/GhidraDev_README.html.*


### Edit Script with Visual Studio Code ![vscode.png](../icons/vscode.png)


Edits the selected script in Visual Studio Code.


*Before a script can
be edited in Visual Studio Code, a Visual Studio Code executable path must be defined in
the Tool's [Visual Studio
Code Integration](../VSCodeIntegration/VSCodeIntegration.md) options if Visual Studio Code is installed in a non-default
location.*


### Assign Key Binding ![key.png](../icons/key.png)


Allows you to assign a key binding the selected script.


1. Click in the text field and type the key or keystroke combination that you wish to
assign to the script.


![](images/Assign_Key_Binding.png)


*The script key
bindings are stored in the Tool's [Key Binding](../Tool/ToolOptions_Dialog.md#key-bindings)
options.*


### Delete Script ![table_row_delete.png](../icons/table_row_delete.png)


Deletes the selected script. You will receive a confirmation
dialog.


![](images/Delete_Script_Confirm.png)


***This is a permanent operation.***


You cannot delete scripts in the [system
directory](#script-directories-bundle-manager), as this may affect other users. If you attempt to delete a system script,
you will receive a warning dialog.


### Rename Script ![textfield_rename.png](../icons/textfield_rename.png)


Renames the selected script. When selecting *Rename*, Ghidra will
prompt for a new filename.


![](images/Rename.png)


### Create New Script ![script_add.png](../icons/script_add.png)


Creates a new empty script and displays it in a Script Editor.


If more than one `GhidraScriptProvider`
exists, then you will have to choose what type of script to create.


![](images/Pick.png)


See `Ghidra Script
Development` for details on how to write a script.


### Refresh Script List ![Refresh](../icons/reload3.png)


Refreshes the script list by re-scanning the script directories.


### Script Directories / Bundle Manager ![text_list_bullets.png](../icons/text_list_bullets.png)


Allows you to add and remove directories to search for scripts and other
dependencies for use by scripts. The default directories are your home directory and the
various system directories (e.g., `$GHIDRA_HOME/Features/Base/ghidra_scripts`). You
can save directories, but ignore them in the Script Manager dialog by selecting/deselecting
the "Enable" column checkbox.


For more information on Ghidra's dynamic module support, see [Ghidra Bundles](../BundleManager/BundleManager.md).


![](images/Script_Dirs.png)


### Help ![red-cross.png](../icons/red-cross.png)


Opens the Ghidra help viewer on the GhidraScript API.


*Provided by: *Ghidra Script Manager Plugin**


**Related Topics:**


- [Key
Bindings](../Tool/ToolOptions_Dialog.md#key-bindings)


---

[← Previous: Refresh Script List](GhidraScriptMgrPlugin.md) | [Next: Console →](../ConsolePlugin/console.md)
