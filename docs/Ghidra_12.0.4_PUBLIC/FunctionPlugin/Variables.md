[Home](../index.md) > [FunctionPlugin](index.md) > Function Signature and Variables

# Function Signature, Attributes and Variables


## Function Signature


A function's signature conveys the following information about a
function:


1. The compiler-specific named calling convention
2. The function's return data type (void indicates no return value)
3. The function's name
4. Ordered list of named parameters and associated data types.


> **Note:** While certain changes may be made without commiting all return and parameter details, those
changes which are made that require a full commit will cause the Commit all return/parameter details checkbox to be enabled.
The user may choose to alter this full commit by checking or unchecking the corresponding
checkbox.


## Function Attributes


The following function attributes affect disassembly and semantic analysis and may be set
via the [Edit Function](Variables.md#edit-function) dialog.


### Custom Storage


The *Custom Storage* option, if enabled, provides the ability to
explicitly specify return/parameter storage.  By default, storage will be dynamically
computed based upon calling convention and return/parameter data types.  When dynamic
storage is computed, hidden "auto-parameters" may be injected as well as the use of
"forced-indirect" storage.



### Inline


Any *Inline* function called by another function may be treated as inline code
instead of a function call during analysis.


### No Return


While a typical function call is always assumed to return and continue flowing to the next
instruction, marking a function as *No Return* forces an implied return immediately
following a call to such a function. Depending upon the state of disassembly, marking a
function as *No Return* may help to prevent a call to such a function from falling-thru
to the next instruction during disassembly. If disassembly has already been done and the
fall-thru has been improperly disassembled, the [Clear Flow and Repair](../ClearPlugin/Clear.md#clear-flow-and-repair) action
may be used to cleanup the bad fall-through.


### Varargs


Designated by a trailing '...' in the function signature, indicates that a variable number
of parameters is allowed. Common C functions which employ Varargs are *printf* and
*scanf*.


### Call-Fixup


A function may be tagged with a predefined *Call-Fixup* which can be used to
alter/simplify the semantic effect of calling such a function. The available set of
predefined call-fixups are defined within the compiler specification (*.cspec file)
associated with a program. This feature is typically used when the effects of calling a
well-known function need to be simplified so that the caller can be more easily analyzed
and/or understood.


## Variables


There are two classes of function variables: Parameters and Local Variables.  The term Parameter
also includes the Function return value which has an associated data type and storage but has no
ordinal.


Many processors use a stack as part of their calling conventions and/or for local variable storage.
In some cases, the return address is pushed onto the stack during the call operation. Any references to the
stack (e.g., references and variable storage) are relative to the stack pointer when the function is entered. For a negative growing
stack (like the X86 processor), the stack would look something like this:


| -n |
| --- |
| . . . |
| Local Variables |
| . . . |
| Saved Registers |
| Return Address |
| Parameter 1 |
| . . . |
| Parameters |
| n |


Structures, Unions, and Arrays can be used to define variables as well as the built in
primitive [data types](../DataPlugin/Data.md#data-types).  To define
structures, see [Data Structure
Editor](../DataTypeEditors/StructureEditor.md)


### Parameters (includes Function Return)


Storage for return/parameters can be computed dynamically based upon
the associated calling convention and data types (i.e., complete function signature).  The ability
to properly compute the correct storage is limited by the current capabilities of the
function prototype models and Decompiler within Ghidra.  In some cases it will be necessary to enable
Custom Storage for a function and specify the correct storage locations for the return/parameters
including the ability to join multiple storage elements (i.e., varnodes) for a single parameter.


When parameter storage is determined dynamically, the calling convention may dictate the
use of hidden parameters which we refer to as "*auto-parameters*" **(auto)**.
In addition, the "*forced-indirect*" **(ptr)** condition may be imposed on
parameters when large data is forced to be passed by reference.  When either of these
is in use for the return or parameters, the **(auto)** or **(ptr)** designation
will appear with the storage location displayed for each parameter.  The parameter names **'this'**
and **'__return_storage_ptr__'** are reserved for the two supported auto-parameter cases.
The **'this'** *auto-parameter* is imposed by the *__thiscall* calling convention,
while *forced-indirect* is imposed by certain calling conventions which limit the maximum size
of any parameter passed by value.  If *forced-indirect* is imposed on the return storage, the
**'__return_storage_ptr__'** *auto-parameter* will be imposed to allow the function caller
to specify a pointer to the full return storage data location.  When using custom storage,
it is assumed any *auto-parameters* will be explicitly defined as normal parameters if applicable.
Within the Program API, *auto-parameters* may not be directly manipulated and are immutable.


The [Function Editor](#edit-function) is the most affective means of modifying the
function signature either via the Code Browser listing or within the Decompiler


### Local Variables


*Currently, there is no specific user interface
action for creating Local Variables.  Stack and register variables will be created
automatically when a suitable stack or register reference is created via the user
interface.  Additionally, the Decompiler's commit actions will create Local Variables as
needed.* *They can also be created programmatically.*


In addition to register and stack locations, Local Variables
also have the ability to be defined by the Decompiler to reflect temporary storage identified
by a hash value.  Please note that these hash type variables can sometimes not work as expected within the
Decompiler.  In addition, the scope of a local register variable is determined by its *first-use-offset*
which reflects the instruction offset relative to the function entry point at which the variable
is first written.  The variable will remain in scope from that point forward until another
local variable comes into scope for the same storage location. Local stack variables assume a
*first-use-offset* of zero (0).


## Define Variable Data Type or Function Return Type


Variables can be annotated with one of the [built in](../DataPlugin/Data.md#data-types) or [user
defined data types](../DataTypeManagerPlugin/data_type_manager_description.md#creating-new-user-defined-data-types).  The undefined or previously defined variable will be redefined
to the new data type.


Variable data types, including parameters and return, can be defined one of four ways:


- Using right-mouse-click on the return type or a parameter within a function signature
displayed within the listing.


1. Right mouse click on the return type or parameter within the function signature
2. If the cursor is over the return type, Select **Set Data Type** →  ; if the cursor is over a parameter, select **Set Data
Type** →
  - The pull right menu lists data types that you have marked as "[favorites](../DataTypeManagerPlugin/data_type_manager_description.md#setting-favorite-data-types)."
  - After you apply a data type, this becomes your [most
recently used data type](#recently-used-data-type) and is shown on the menu with the 'Y' as the "hot
key."


- Using right-mouse-click on a parameter, `<RETURN>` or local variable listed within the function
variable listing


1. Right mouse click on a parameter, `<RETURN>` or local variable
2. Select **Set Data Type** →
  - The pull right menu lists data types that you have marked as "[favorites](../DataTypeManagerPlugin/data_type_manager_description.md#setting-favorite-data-types)."
  - After you apply a data type, this becomes your [most
recently used data type](#recently-used-data-type) and is shown on the menu with the 'Y' as the "hot
key."


- Using the *[Data Type Manager](../DataTypeManagerPlugin/data_type_manager_description.md)*
window (drag and drop)


1. From the Code Browser tool bar select Display Data Types  ![dataTypes.png](../icons/dataTypes.png)   icon
2. In the *Data Type Manager* window select the appropriate data type
3. Drag and Drop the data type onto the target parameter, `<RETURN>` or local variable in the Code Browser


- [Assigned Quick key](../DataPlugin/Data.md#cycle-groups),


- Place the cursor on the target parameter, `<RETURN>` or local variable
- Press a quick key set to specify a data type  (i.e., "*b"*-byte,
"*p*"-pointer, ...)


## Edit Function


Once a function has been created, there are many attributes of the function and its
parameters that can be changed. The **Function Editor Dialog** allows you to make those
changes. To edit a function do the following:


1. Place the cursor on a function signature
2. Right-mouse-click, and select *Edit Function*.
3. Edit any attributes of the function using the dialog.
4. Consider [committing all return/parameter details](#commit-all-returnparameter-details)
5. Press *OK* to save your changes.


![](images/FunctionEditor.png)


### Function Signature Field


The area at the top of the dialog is used to show the complete function signature. It
will update as you make changes to the various fields in the dialog.


You may also use this field to directly edit the signature, but **beware** that your changes
will have to be parsed and the current parser is severely limited.
Once you make a change in this field, all the
other fields will be disabled temporarily until you complete your changes and press either
`<TAB>` or `<RETURN>` to continue. You may also complete the edit by clicking outside
of the signature field.


If the parser fails to successfully parse your changed signature field, a dialog will appear
giving you the option to continue typing in the field or aborting your edits in that field.


*Due to limitations in the parser, there are many
function signatures that Ghidra supports that you cannot directly enter by typing in the
function signature field.  For example, you cannot use the signature field to enter templated types.
Also, the parser currently only supports common datatypes and datatypes that are currently used in your program.
To enter more complicated values or find datatypes from open archives, use the more precise controls that the dialog provides.*


### Function Name


This text field can be used to change the name of the function.


### Calling Convention


This field is a combobox that allows you to choose a calling convention from the list of
known calling conventions for this processor and compiler specification. This choice
will have no affect on storage if the **Custom Storage** checkbox has been selected.


### Function Attributes


This sections contains a set of miscellaneous checkboxes that affect the function.


- **Varargs** - sets the function to have a variable number of arguments.
- **In Line** - indicates this functions code is placed in line with the calling
function.
- **No Return** - used to indicate if this function does not return.
- **Use Custom Storage** - If selected, the user can edit and change the storage of
the return value and the parameters. Otherwise, the storage is deteremind by the selected
calling convention.


### Parameters/Return Type Table


The parameters/return type table allows the user to add or remove parameters as well as changing their
names and datatypes. It also displays the return value datatype and storage.
Also, if the **Use Custom Storage** checkbox is selected, the storage
of the parameters and return type can be changed.


#### Table fields


- **Index** - indicates its ordinal position in the signature (starts with 1). This field can't be edited
directly, but can be affected by the **Up** and **Down** buttons. Note: this field
is blank for the return value.
- **Datatype** - indicates the datatype of the parameter or return type. Clicking on this field will
bring up a [DataType
Chooser Dialog](../DataTypeEditors/DataTypeSelectionDialog.md).
- **Name** - the name of the parameter. This field can be edited directly in the table
cell. Note: the name of the "return value" is `<RETURN>` and can't be changed.
- **Storage** - the storage for the parameter or return value. If the **Use Custom Storage**
checkbox is selected, this field can be edited by clicking on it and bringing up the
parameter editor dialog.  If not using custom storage, *auto-parameters* or *forced-indirect*
storage may be imposed as determined by the selected calling convention and is designated by **(auto)**
or **(ptr)** with the displayed computed storage.


#### Table Buttons


- **Add** - Adds a new parameter to the function
- **Remove** - Removes the selected row (parameter) from the table.
- **Up** - Moves the selected parameter earlier in the signature.
- **Down** - Moves the selected parameter later in the signature.


### Call Fixup


This field is a combobox that allows use to use a predefined Call-Fixup. A function may be
tagged with a predefined Call-Fixup which can be used to alter/simplify the semantic effect
of calling such a function. The available set of predefined Call-Fixups are defined within
the compiler specification (*.cspec file) associated with a program. This feature is
typically used when the effects of calling a well-known function need to be simplified so
that the caller can be more easily analyzed and/or understood.


### Commit all return/parameter details


This checkbox controls whether a complete function update will be performed, including
datatype and optional custom-storage details, for the return and all parameters.
This checkbox will enable itself when
specific changes are made which require a complete commit in order to preserve what is seen
in the editor.  Use of custom storage or altering return or parameter datatypes will require
a full commit in order to retain such changes.  It is important to note that a full Commit
with storage and/or datatype changes will impose a *USER_DEFINED* **Signature Source**
which will lock-in parameter details within the Decompiler.  The **Signature Source**
Function Listing Field can be useful for monitoring this state.


![warning.help.png](../icons/warning.help.png)
If the signature has been autogenerated by the decompiler and changes have been made to
things other than the signature, like calling convention or callfixup, that may affect the
generated signature.  Consider changing the calling convention only to check if the
decompiler would generate the same signature unless you are sure the generated signature
is correct.


Prior to clicking the dialog's **OK** button the user may uncheck this control to
prevent return/parameter changes from being committed.  Once datatype or custom-storage
choices have been changed, any parameter name changes will also require a full commit to
preserve such changes.  A full commit is not required if only parameter names have been
changed.  The exception to this is when the Function Editor is used within the Decompiler
and parameters have not previously be committed.


## Edit Parameter Storage Dialog


This dialog is invoked by clicking on the storage column in the [Edit Function](#edit-function) dialog. This dialog allows your to precisely specify the
storage of a parameter. The parameter can even be divided amongst multiple storage locations.
Each row of the table specifies a storage location used by the parameter.


![](images/EditStorage.png)


### Size Information


The top of the dialog shows two sizes. The **Datatype** size is the size required to
store the parameter based on its current datatype. The **Allocated Size** shows how much
storage as been allocated based on the rows in the table.


### Storage Table


A table of storage locations where each row represents a storage location. You must add
enough storage location rows to get enough storage space for the size of the parameters
datatype.


#### Table Columns


- **Type** - the type of storage. Can be either Stack, Register, or Memory. Clicking on
the field will bring up a table version of a combo-box.
- **Location** - Indicates the specific location for the type. For stack, it will be an
integer offset. For register, it will be the name of the register. For memory, it will be the
address. Clicking on this field will bring up an editor appropriate for the storage
type.
- **Size** - The size for this storage. For stack and memory, it will be the number of
consecutive bytes to use for this storage. For a register, it will the number of bytes to use
within the register, up to the size of the register.


#### Table Buttons


- **Add** - Adds a new storage location
- **Remove** - Removes the selected row (storage location) from the table.
- **Up** - Moves the selected storage location earlier in the allocation.
- **Down** - Moves the selected storage location later in the allocation.


## Create Function Definition


Once you have defined a function, you can make a function signature definition which is a
new data type that can be applied to another function so that it has the same signature. The
data type appears under the [program
node](../DataTypeManagerPlugin/data_type_manager_window.md#the-data-type-tree) in the *[Manage Data
Types](../DataTypeManagerPlugin/data_type_manager_description.md)* window.


To create a function definition, position the cursor on a function signature, right mouse
click and select *Create Function Definition*.


A new data type is created; the name of the data type is the same name as the
function.


To create a new function signature definition using the one you created, drag the data
type from the *Data Type Manager* window and drop it on the existing function where you
want the new function signature to be created.


*If you attempt to create a function definition on one
that you have already defined, nothing happens.*


## Rename Variable


Rename Variable will change the name of a variable from its default name to a user-defined
name.


To Rename a Variable,


1. Place the cursor on the target variable within the function variable listing
2. Right-mouse-click, select **Function Variables** → **Rename Parameter...** or **Function Variables** → **Rename Local Variable...**
3. Type the new variable name in the dialog and press**`<Enter>`**, OR click on
the **OK** button


## Delete Variable


*Delete Variable* will remove the target variable from the listing.  There is no
confirmation with *Delete Variable*.  However, the operation can be undone using
the [Undo operation](../Tool/Undo_Redo.md).


To delete a variable,


1. Place the cursor on the target variable within the function variable listing
2. Right-mouse-click, select **Function Variables** → **Delete Parameter** or **Function Variables** → **Delete Local Variable**


## Edit Comment


Stack Parameters and Local variables can have comments associated with them.  The
comment is free form text.  If a comment already exists, the comment is modified.


To add/edit a comment to a variable,


1. Place the cursor on the target variable
2. Right-mouse-click, select *Edit Comment*
3. Enter the comment.
4. Select *OK*


## Remove Comment


To remove a function variable comment,


1. Place the cursor on the variable comment
2. Hit the &lt;**Delete**&gt; key


## Recently Used Data Type


The data menu shows an option for the data type that was most recently used. By default, the
"hot key" assigned to this option is 'y,' however, you can change the key assignment through
the [key bindings panel](../Tool/ToolOptions_Dialog.md#key-bindings)
on the [Edit Options dialog](../Tool/ToolOptions_Dialog.md).


*Provided By: *Function* Plugin*


**Related Topics:**


- [Data Structure Editor](../DataTypeEditors/StructureEditor.md)
- [Data Type
Manager](../DataTypeManagerPlugin/data_type_manager_description.md)
- [Functions](Functions.md)


---

[← Previous: Stack Depth Change](Functions.md) | [Next: Function Tags →](../FunctionTagPlugin/function_tag_window.md)
