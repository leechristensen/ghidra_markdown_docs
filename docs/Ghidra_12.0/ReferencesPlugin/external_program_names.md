# External Program Names


An external reference is a reference to a location in another program. The reference
destination includes the name of some program. To use an external reference to navigate, the
external program name must be associated with an existing program file in the Ghidra project.
If the association has been defined, then the external reference is said
to have been ***resolved***. The *External Programs* view manages the associations
between external program names and program files. The table shows all external program names
and their associated links to program files. Use the *External Programs* view to add
external names, delete external names, set associations, and clear associations.


## External Programs View


![](images/External_names_dialog.png)


The *External Programs* view consists of a main scrollable list of external program
names and their associated Ghidra program files.


### Name Column


The name of the external program. Many external programs will share the same external
program name. Setting or changing the associated Ghidra file will affect all the external
references to that name. Double-click on this field to edit the name. After you change
the name, hit the `<Enter>` key.


### Ghidra Program Column


The Ghidra file associated with the external program name. This field is blank if
external reference has not been resolved. Ghidra will not be able to "follow" an external
reference if its external program name does not have an associated Ghidra file.


### Add Button


The **Add** ![Plus.png](../icons/Plus.png) button will bring up a text dialog
for entering a new external program name.


### Set
External Name Association Button


The Set ![editbytes.gif](../icons/editbytes.gif) button brings up a *Ghidra program chooser* dialog. Choose a
Ghidra program file to associate it with the selected external program name. This button
is only enabled when a single external program name is selected.


![](images/Choose_external_prog.png)


### Clear External Name Association
Button


This Clear ![edit-delete.png](../icons/edit-delete.png)  button clears the assocated program for all the
selected external program names.


### Delete External Name Button


This Delete ![edit-delete.png](../icons/edit-delete.png) button deletes the selected external program names from the
program.  If a selected external program name contains external locations, it can
not be deleted. The Delete button is enabled
whenever one or more external program names are selected.


## Working with External Program Names


### Adding a New External Program Name


1. Select **Window →  External Programs**
from the main Code Browser menu.
2. Press the **Add** ![Plus.png](../icons/Plus.png) button.
3. Enter the new external program name into the pop-up dialog.
4. &lt;&gt;
*If the table is sorted by Name, then
the name you enter will be placed at the correct position in the table to maintain the
sort order. The sort icon ![Sort Ascending](../icons/sortascending.png) or ![Sort Descending](../icons/sortdescending.png) indicates the order and what column is
being sorted. You can also sort by Ghidra Pathname by clicking on the header for this
column. Click on the sort icon to change the order.*
&lt;/&gt;


### Resolving an External Name to an existing Ghidra program


1. Select Window**→  External Programs** from the main Code Browser
menu.
2. Click on the external program name that is be associated with a Ghidra program
file.
3. Press the **Edit** ![editbytes.gif](../icons/editbytes.gif) button.
4. Use the *[Ghidra Program Chooser](#chooseexternalprogram)* dialog to
select the Ghidra file to associate to the selected program name.
5. The Code Browser updates to indicate that the external reference has been resolved.
(Unresolved references are shown in red.)


### Clearing a Resolved External Program Name


1. Select Window**→  External Programs** from the main Code Browser
menu.
2. Click on the external program name that has an association to be cleared.
3. Press the **Clear** ![erase16.png](../icons/erase16.png) button


### Removing an External Program Name


1. Select Window**→  External Programs** from the main Code Browser
menu.
2. Click on the external program name to be removed.
3. Press the Delete ![edit-delete.png](../icons/edit-delete.png)  button.
- If external references still exist, a dialog is displayed indicating that the
external program name cannot be deleted.  All external references to that external program name must be deleted before it can
be deleted.


*Provided by: *References* Plugin*


**Related Topics:**


- [Set External Reference](References_from.md#extrefs)
- [External Symbols](../SymbolTreePlugin/SymbolTree.md#externals)
