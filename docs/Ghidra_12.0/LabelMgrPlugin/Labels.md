[Home](../index.md) > [LabelMgrPlugin](index.md) > Show Label History

# Labels


A label is a name associated with an address. Labels are used to make code easier to read.
For example, instead of "call 0x103f2d", the instruction might read "call printf". The name
"printf" has been associated with the address "0x103f2d". In other words, the address
"0x103f2d" has been labeled printf.


### Label Name


All labels have an assigned symbol name which has either explicitly been established or a
default generated name. When assigning a label name (or any other namespace or symbol name)
the following naming restrictions apply:


- **Reserved Dynamic Name Pattern** - certain dynamic name patterns are reserved for
Ghidra use and may not be explicitly set. A dynamic pattern generally consists of a default
prefix (*SUB_, LAB_, DAT_, UNK_, EXT_, FUN_, OFF_*) followed by an address (e.g.,
*LAB_01234567*).
- **Space and Non-printable Characters Not Allowed** - a blank space character or
other non-printable ASCII character (e.g., backspace, linefeed, etc.) are not permitted
within a name
- **Length Limit of 2000** - the name length may not exceed 2000 characters/bytes


> **Note:** In addition to the above restrictions, the
use of '::' within a label name may cause problems with certain name edit dialogs which may
use this as a namespace separator.


### Label Source


Labels can be created or renamed by importing information, when auto-analysis is
performed, or directly by the user. The label source indicates how the label was created or
renamed.


- **User Defined -** Label name specified by the user.
- **Imported -** Label named during the import of the program or by some other
imported information (for example, external libraries or C libraries.)
- **Analysis -** Label created by auto-analysis that do not have default names.
- **Default -** Label with a default name. (Ghidra generally creates default-named
symbols at any address that is referenced by some other location.)


### Default Labels


Some labels are automatically generated during disassembly. They use a standard naming
convention to derive the symbolic name from the address. The current convention is to use a
prefix that gives some information about what is at the address, followed by the address. For
example, the automatic label generated for address "0x01234" would be "LAB_01234" if there is
code at that address. If there was a data item at that address, the label would be
"DAT_01234". Labels with auto-generated names are known as *default* labels. The
importer, auto-analysis, or the user can also create labels (or rename default labels) using
more meaningful names.

Default label prefixes can be any of the following:


- **EXT -** indicates address is an external entry point.
- **FUN -** indicates there is a function at the address.
- **SUB -** indicates that code at the address has at least one "call" to it.
- **LAB -** indicates there is code at the address.
- **DAT -** indicates there is a data item at the address.
- **OFF -** indicates that the associated address is offcut, i.e. inside of an
instruction or data item.
- **UNK -** default when one of the above cannot be recognized.


### Label Properties


- **Entry Point -** Indicates that the address associated with this label is an external
entry point. External entry points are those addresses that can be used to initiate execution
from outside the program. Most programs have a single "main" entry point. (Usually having the
label "Entry".) Shared libraries (DLLs) usually have many entry points, one for each function
in the library. Since the "entry point" property is really associated with an address and not
a particular label, all labels at an address share this property.
- **Primary -** Indicates that this label will be the one used to
represent the address everywhere the address is displayed, such as in the operand field of an
instruction. Since multiple labels can be associated with an address, one and only one must
be designated as primary.


## Add/Edit Label Dialog


The *Add Label* dialog and the *Edit Label* dialog are identical except for the
title and the way the dialog's fields are initialized. The *Add Label* dialog will be
filled in with suggested values for all fields. The *Edit Label* dialog, on the other hand
will be filled in with the current values of the label being edited.


| ![](images/AddLabel.png) |
| --- |


> **Note:** If you add a label where there is a function
with a default label name, the label you add will become the function's new name.


### Dialog Fields


***Enter Label***


- Text field for entering the name of the label. A combo box is included which allows
selecting recently used label names.
You may enter a namespace path in this text field that follows the format:
  ```
      <namespace_name1>::<namespace_name2>::<...>::<label_text>
  ```
For example, the following string denotes a full namespace path that starts at the
**Global** namespace and ends at the label name `myLabel`:
  ```
      Global::foo::bar::myLabel
  ```
The namespace in the *Namespace* combo box will be used as the parent namespace
for the label name and any included namespaces. However, if the you provide a namespace
path that starts with **Global**, then the value of the *Namespace* combo box
will be ignored.


***Namespace***


- The defining scope of the label. The available namespaces are based upon the current
address. When editing a label, the available namespaces are not necessarily those in the
namespace hierarchy in which the label is located, but rather are those based upon the
address of that label. The **Global** namespace is always included by default, as well
as the parent namespace of the current label, if one is being edited.


> **Note:** This field is disabled, if there is a
function with a default name at this address. The namespace will stay set to the parent
namespace of the function and the label name you enter will become the new function
name.


***Entry Point***


- Sets the entry point property for address associated with this label. Setting this
property on one symbol, changes it for all symbols at the same address.


***Primary***


- Sets the primary property for this symbol. If there is only one symbol at this
address, the checkbox will be selected and disabled, since it must be primary. Whenever
the checkbox is selected, it will be disabled because the only way to make a symbol
become non-primary is to select another symbol at the same address and make it primary.
This ensures that there will always be one label that is primary. If there is a function
at this address and you add a new label, the checkbox will be enabled such that if you
select the checkbox, the function is renamed to the new label that you entered.  The
function symbol must always be the primary symbol.


***Pinned***


- Sets the label to pinned.  A pinned label will not move if the image base is changed
or a memory block is moved.  A label that is not pinned, will move with the code
or data if a memory block is moved or the image base is changed.  Also, a pinned
label will not be removed if the memory block that contains it is removed.  Only code,
data, or function labels may be pinned.


## Set Label Dialog


Normally, the primary label is used to replace an address reference in the operand field
of an instruction or data item. Ghidra allows users to change which symbol is used to replace
the address using the *Set Label* dialog.


| ![](images/SetLabel.png) |
| --- |


### Label


The list in the combo box will show all symbols associated with the address shown in the
dialog title. Choosing a label from the list will cause that symbol to be associated with
the operand reference being modified. Typing in a new name will cause a new symbol to be
created at the target address before associating it with the operand reference.


## Label Operations


### Adding a Label


Adding a label will place a label at a particular address in a listing. Labels may be of
any length but may not contain spaces. To add a label:


1. Right-click and choose the **Add Label** menu option.
2. Enter the name of the label in the text field (or accept the suggested default).
3. Change any of the default options (see [Label Dialog](#addedit-label-dialog))
4. Press the **OK** button.


> **Note:** Adding a label to an address where there is a
function with a default name results in the function name becoming the new label name.


### Renaming a Label


To change the name of a label or referenced label appearing in an operand:


1. Right-click on the label, or referenced label appearing in an operand, then
choose the **Edit Label** item from the popup menu.
2. Enter the new name of the label in the text field in the **[Label](#addedit-label-dialog)** dialog.
3. Press the **OK** button.


> **Note:** If the label appearing in an operand corresponds
to an external location the Edit Label action will be replaced by Edit External Location .


### Edit External Location


Similar to editing a label associated with the primary reference of an operand, an
external location referenced by an operand may be renamed or modified.  Right-click on the operand which references an external location
and choose the **Edit External Location** menu option
(see Symbol Tree -
[Edit External Location](../SymbolTreePlugin/SymbolTree.md#edit-external-location)
for more discussion on the use of the edit dialog).


### Removing a Label


Labels may or may not be eligible for removal depending on the following rules:


- Labels that have no references to them can always be removed.
- Labels at addresses that contain more than one label can always be removed.
- "Default" labels with at least one references and no other labels at that address can
not be removed. (The menu option will be disabled.)
- "User-defined" labels with at least one reference and no other labels at that address
can be removed, but will be replaced with a "default" label at that address.
- A "default" function label cannot be removed if there are no other labels at the
address. To remove a "default" function label, you must remove the function itself.
- A "user-defined" function label can be removed. If there are no other labels at the
address then the function label becomes a "default" label. If there are other labels at the
address, one of these will become the new function label.


To remove a label:


1. Right-click on the label to be removed and choose the **Remove Label** menu
option.


> **Note:** Ghidra gives no confirmation
on Remove Label . A status message is displayed if you try to remove a default function
label.


### Setting the Namespace


A *Namespace* defines a scope, such that symbol names are unique *within* a
namespace. The types of namespaces that Ghidra supports are *Global*, *External*,
*Function*, *Class*, and *Generic* namespaces that reside in the global
namespace.


To set the namespace:


1. Right click on a symbol and choose the **Edit Label** menu option.
2. Select a namespace from the *namespace* combo-box in the **[Label](#addedit-label-dialog)** dialog.  Or, you may enter a new namespace with the label using "::" as a
name separator.  If a specified namespace does not exist a simple-namespace
will be created.


> **Note:** Any use of a class-namespace requires that it first be
created prior to associating a label or other namespace with that
class-namespace. This is most easily accomplished via the Symbol Tree


### Setting an External Entry Point


External Entry points can only be created at addresses that have at least one symbol. To
set an external entry point:


1. Right click on a symbol and choose the **Edit Label** menu option.
2. Check the *Entry Point* checkbox in the **[Label](#addedit-label-dialog)**
dialog.


### **Making a Label Primary**


Making a label primary gives it priority over other labels that are associated with the
same address. The primary label is displayed by other Ghidra features instead of the address.
For example, in the subroutine view, the subroutine names are primary labels. If another
label were added and made the primary label, then the subroutine view will display that label
instead of the label bearing the subroutine name.

If a function exists at an address, its name is the primary label; if you set another label
at this address to be primary, then the symbol for this label is removed, and the function is
renamed to that label that you were editing.  The function symbol must always be
primary.


To make a label primary:


1. Right click on a symbol and choose the **Edit Label** menu option.
2. Check the *primary* checkbox in the **[Label](#addedit-label-dialog)**
dialog.


### Selecting a referenced Label for an Operand


Referenced labels appear in instruction operands. By default, the primary label associated with the
primary reference from an operand will be displayed within the operand.
To have the operand display a different label corresponding to the primary memory reference:


1. Right click on the operand symbol and choose the **Set Associated Label...** menu option from the
pop-up menu.  This action only appears if the primary reference is a memory reference.
2. Choose a label from the drop-down list on the **[Set
Label](#set-label-dialog)** dialog or type in a name for a new label that will appear at the referred-to
address.


*Provided by: the ***Edit Labels*** Plugin*


### Show Label History


You can show the history of changes on labels at a given address. You can also search the
label history for all lables looking for old label names that no longer exist.  Either
way, a dialog is shown containing a table of lable changes. The "Action" column indicates
whether the label was added, removed, or renamed. If the label was renamed, the "Label"
column shows the old name renamed to the new name. The "User" is the user who made the
change. The "Modification Date" is when the change was made. Labels that were added as a
result of disassembly are not recorded in the history; however, if you rename a default
label, you will see an entry in the table, as shown below.


*A column for "Address" shows up in the
table if you are viewing the history of changes on labels at all addresses.*


| ![](images/ShowLabelHistory.png) |
| --- |


To display the history of label changes at a specific address,


1. Right mouse click on a label (either in the label field or the operand field).
2. Choose the **Show Label History** option.


> **Tip:** You can sort the label history by any of the
columns and in ascending or descending order. By default, the history is sorted by ascending
modification date (i.e., oldest date first). You can also reorder the columns by dragging the
header to another column position.


To seach for label history for a past or present label
name:


1. Select Search → **Label History**...


![](images/LabelHistoryInputDialog.png)


1. A dialog is displayed so that you can enter a label name (or part of a label
name)
- Enter a string you would like to see matches for.
- To display the label history for all the label changes, leave the field blank.
2. Select the OK button or press the `<Enter>` key in the text field.
- If label history was found, a dialog similar to the one shown above is displayed
with the addition of an "Address" column. The input dialog remains displayed if no
label history was found.
- From the label history dialog, you can navigate to each address by clicking on the
row in the table.


*Provided by: the ***Edit Labels*** Plugin*


**Related Topics:**


- [Symbol Table](../SymbolTablePlugin/symbol_table.md)
- [Symbol Tree](../SymbolTreePlugin/SymbolTree.md)
- [Edit Field Names](FieldNames.md)


---

[← Previous: Setting a Label in an Operand](Labels.md) | [Next: Comments →](../CommentsPlugin/Comments.md)
