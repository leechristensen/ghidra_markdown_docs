[Home](../index.md) > [DataTypeEditors](index.md) > Enum Editor

# Enum Data Type Editor


An *Enumeration* data type ("Enum") is a C-style data type that allows
the substitution of a value for a more meaningful name. Ghidra provides a
special editor for Enum data types.


[Create an Enum data type](../DataTypeManagerPlugin/data_type_manager_description.md#creating-new-user-defined-data-types)
using the
[Data Type Manager](../DataTypeManagerPlugin/data_type_manager_description.md#editing-a-data-type) display. The editor for an Enum is shown below.


![](images/EnumEditor.png)


### Enum Editor Fields


- The *Name* column in the table is the name of the enum entry.
- The *Value* column in the table is the value of the enum entry.
- The *Comment* column in the table is the comment for the enum entry.
- The *Name* field below the table shows the name of the enum.
Edit this field to change the name.
- The *Description* field shows a short description for the enum;
edit this field to update the description.
- The *Category* field shows where the enum resides which corresponds to the folder
you were selecting when creating the enum;
the field is not editable, however, you can move it using the Data Type Manager after
you have created it if you want to move it.
- The *Size* field shows the number of bytes required when you apply
the enum. To edit this field, use the drop-down menu to choose a new size. Note: If you
are applying an enum to a data definition and do not see expected results in the
decompiler it is probably because the size is incorrect.


When you make any change to the enum, the
![disk.png](../icons/disk.png)
(**Apply**) button is enabled.


## Edit an Enum Entry


To edit an entry in the enum table,
select an entry; double click in the field that you want to change,
OR press **F2**.
A cell editor is displayed; enter the value   (press the `<Enter>` key).


> **Note:** While editing, you can use the Tab key to navigate the editing to the next cell,
the Shift-Tab key to navigate backwards, the Up key to move editing to the cell
above, and the Down to move editing to the cell below the currently edited cell.


> **Note:** Names and values must be unique.


## Toggle Hex Mode


Changes the Enum value column to show values in hex or decimal.


## Add an Enum Entry


Create an new enum entry by selecting the
![Plus.png](../icons/Plus.png)
(**Add**) button on the editor's tool bar.
An entry with default values is added to the table; the default name is
"New Name;" the default value is the next highest value.
Double click on the fields to change the entries.


## Delete an Enum Entry


To delete enum entries, select the entries that you want to remove.
Right mouse-click and choose the **Delete** option, OR select the
![edit-delete.png](../icons/edit-delete.png)
button on the editor's tool bar.


## Apply Changes


When you have completed making changes, select the
![disk.png](../icons/disk.png)
button on the editor's tool bar. If you have changed the name of the enum,
the *Data Type Manager* display is updated to reflect the new name in the tree.


## Show In Data Type Manager


Select the ![go-home.png](../icons/go-home.png) icon in the toolbar to have the editor's
data type be highlighted in the Data Type Manager's tree.


Change the Sort Order


As with most tables in Ghidra, you can change the sort order of a column by
clicking on the column header. The icons on the header indicates the sort order,
ascending (![Sort Ascending](../icons/sortascending.png) ),
or descending (![Sort Descending](../icons/sortdescending.png) ).
You can also rearrange the columns in the table by clicking on the column
header and dragging it to the new position. Changing the sort order has no
effect on the enum.


*Provided By: *Data Type Manager* Plugin*


**Related Topics:**


- [Create Enum using the Data Manager](../DataTypeManagerPlugin/data_type_manager_description.md#creating-new-user-defined-data-types)


---

[← Previous: Structure Editor](StructureEditor.md) | [Next: Memory Map →](../MemoryMapPlugin/Memory_Map.md)
