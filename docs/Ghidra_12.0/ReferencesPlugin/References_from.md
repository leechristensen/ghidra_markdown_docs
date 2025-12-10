[Home](../index.md) > [ReferencesPlugin](index.md) > External References

# Forward References


This page covers the follow topics relating to explicit forward references and the specific
functionality provided by the ReferencesPlugin:


- [Introduction](#introduction)
- [Types of References](#types-of-references)
- [Reference Destination Symbols](#reference-destination-symbols)
- [Ref-Types](#ref-types)
- [Actions for Creating and Deleting References from a Code Unit](#actions-for-creating-and-deleting-references-from-a-code-unit)
- [Viewing and Editing References](#viewing-and-editing-references-addedit-r)
- [Adding a Reference](#adding-a-reference)
- [Editing a Reference](#editing-a-reference)
- [Memory Reference Panel](#memory-reference-panel)
- [External Reference Panel](#external-reference-panel)
- [Stack Reference Panel](#stack-reference-panel)
- [Register Reference Panel](#register-reference-panel)
- [Adding Memory References from a Selection](#adding-memory-references-from-a-selection)


## Introduction


Explicit forward references exist within a program to identify execution flow or a data
relationship between a '*source*' referent and a '*destination*'.  Inferred
forward references are sometimes rendered automatically within the Listing to aid the user
(e.g., inferred function variable references).   This page only covers the management of
"explicit" forward references which are stored within the Program file.


A forward reference *source* is either an instruction or data code unit within the
program identified by a memory address.  In addition, the source is qualified by an
*operand-index* which identifies the mnemonic or operand of an instruction which is making
the reference.  Associating a reference to the correct operand allows the Listing to
render the data or instruction in a more friendly fashion and also facilitates navigation
within the program when you double click on an operand field within the Listing.


> **Note:** When a reference is placed on an operand, it
will only change the rendering of that operand within the program listing if the reference is
marked as 'primary'.


> **Note:** If a reference is placed on an instruction
mnemonic within the Listing, the instruction mnemonic will be underlined .


> **Note:** If a non-primary reference exists for an operand
(i.e., not reflected in the instruction markup), the corresponding instruction operand within
the Listing will be underlined .


## Types of References


The following types of explicit forward references may be defined from a mnemonic or operand
of an instruction or data code unit:


- [Memory Reference](#memory-references) (*includes Offset and Offcut
references*)
- [External Reference](#external-references)
- [Stack Reference](#stack-references)
- [Register Reference](#register-references)


> **Note:** Ghidra does not permit mixing "types of
references" for a given mnemonic or operand.


> **Note:** With the exception of Memory References, only a
single reference may be placed on a given mnemonic/operand.


### Memory References


All *Memory Reference* have a destination defined by a memory address within the
current program.  A variation of the typical memory reference is the *Offset
Reference* which permits the destination address to be specified as some base memory address
plus a 64-bit signed offset.


*Memory References* are used to specify either a data access or execution flow within
the Program.  This distinction is made by specifying an appropriate [Ref-Type](#ref-types) on the reference.  Adding and removing certain flow references
may change the set of instructions which make up subroutine and code blocks.  Since
function bodies are established based upon the [Block Models](../BlockModel/Block_Model.md), it may be necessary to redefine the
body of  [Functions](../FunctionPlugin/Functions.md) affected by a
new flow reference.


Any *Memory Reference* can be characterized as an *Offcut Reference* if its
destination address is contained within a data or instruction code unit and does not correspond
to the minimum address of that code unit.  Such *Offcut References* produce an offcut
label which uses a special label color.  In addition, since the corresponding label is
hidden within a code unit, a special **`OFF_<address>`** label appears on the containing code
unit within the Listing.  Double-clicking the similarly colored XRefs within the Listing
will allow you to quickly identify the *source* of the memory reference (see [Code Browser Navigation](../CodeBrowserPlugin/CodeBrowser.md#navigation)).
In general, the presence of an Offcut Reference may indicate an error within the
disassembly.


### External References


External References are used to define either a data access or execution flow to a memory
destination located within a different Program file.  This type of reference is typically
used when linking to a library module.  An External Reference destination is defined by a
*External Program Name* and memory location which may be identified by a label or address
contained within the *External Program File*.   The resulting destination symbol
takes on the name of the external label or **`EXT_<address>`** if only an external address was
specified.  All external destination symbols have a namespace which corresponds to the
associated *External Program Name* (e.g.,  **`MSVCRT.DLL::_controlfp`**  ).


An *External Program Name* is considered to be "resolved" when it has been linked to a
Program file contained within the same project.   All external symbol names, corresponding
to unresolved *External Program Names,* will be displayed in red.  The [External Program Names...](external_program_names.md) action/dialog can be used to set or
modifying these external Program file linkages.


External References currently utilize the single RefType of EXTERNAL.


### Stack References


*Stack References* define data access to a function parameter or local variable located
on the stack.  All *Stack References* have a destination defined by a stack offset
within the containing function's stack frame.  If a real frame-pointer is not used, the
Function analysis will track the stack pointer usage and establish a virtual stack frame for
the purpose of defining stack parameters and local variables.  When creating a *Stack
Reference*, a corresponding stack parameter/variable may be explcitly bound to the reference
(see [Function Variables](../FunctionPlugin/Variables.md)), although this
is generally unnecessary since this relationship can generally be determined from the stack
offset.   The sign of the stack frame offset makes the distinction between a parameter or
local variable assignment.  Stack usage conventions are established by the Language module
in use.


> **Note:** Stack References should be placed on all stack
parameter/variable data access operands.


> **Note:** Stack References may only be specified for
source code units contained within a function.


### Register References


*Register References* define data access to a function parameter or local variable
located within a register.  All *Register References* have a destination defined by a
register within the context of a containing function.  When creating a *Register
Reference* a corresponding register variable may be explcitly bound to the reference (see [Function Variables](../FunctionPlugin/Variables.md)), although this is
generally unnecessary since this relationship can generally be determined from the register
used.


> **Note:** Register References should be placed only on
register variable data assignment operands.


> **Note:** Register References may only be specified for
source code units contained within a function.


## Reference Destination Symbols


An important characteristic of all references is that a symbol is created for all
destinations.  These symbols generally appear within the listing and can always be found
within the [Symbol Table](../SymbolTablePlugin/symbol_table.md) or [Symbol Tree](../SymbolTreePlugin/SymbolTree.md).  The following default
symbol names are produced by the creation of a reference.


| **Symbol** **Name** **Format**   | **Type**   | **Namespace**   | **Description**   |
| --- | --- | --- | --- |
| LAB_ &lt; address &gt;   | Memory   | Global   | A memory address  "label" identifying a branch flow             memory reference destination.   |
| SUB_ *`<address>`*   | Memory   | Global   | A memory address  "label" identifying a call flow memory             reference destination.   |
| DAT_ &lt; address &gt;   | Memory   | Global   | A memory address  "label" identifying a data memory reference             destination.   If the address correspnds to defined data, the DAT prefix will             be replaced by the corresponding data-type (e.g., BYTE_ &lt; address &gt;, DWORD_ &lt; address &gt;).   |
| OFF_ *`<address>`*   | Memory   | Global   | A memory address "label" identifying a memory reference destination             which is located at an offcut address within a code unit.  These labels only             appears within the listing to flag the existence of a hidden offcut label.              Double-clicking the corresponding offcut XRef will take you to the code unit             which has the offcut reference,   |
| **param_** *`<ordinal>`*   | Stack/Register/   Memory   | Function Name   | A function parameter associated with stack, register or memory              location.  Parameter references identified by a parameter name which by default             includes its ordinal position.   |
| local_ *&lt;* *reg-name&gt;[_&lt;* *firstUseOffset&gt;]*   | Register   | Function Name   | A local function variable associated with register references.              In addition, the first-use-offset within the function is included if             non-zero.   |
| local_ `<offset>`[_`<firstUseOffset>`]   | Stack   | Function Name   | A local function variable associated with stack references identified             by an absolute offset within the stack frame.  In addition, the first-use-offset             within the function is included if non-zero.   |
| &lt;ext-label&gt;   | External   | `EXTERNAL_NAME`   | A external program location associated with external references and             identified by a label name or address within the external program file.  Each *EXTERNAL_NAME* can be associated with a specific program file within your Ghidra             project (see [External Program Names](external_program_names.md) ).  If             only an address is specified when creating an external reference, a label format of `EXT_<addr>` is used.   |


The above symbol name colors correspond to the default color scheme (see [Code Browser Options](../CodeBrowserPlugin/CodeBrowserOptions.md)).  Memory
Reference destinations outside the Program's memory map, and unresolved External Reference
destinations utilize the "Bad Reference Address" color (e.g., `DAT_00010000`) in place of the normal color shown.


The presence of


The actual default label utilized for a memory location can change dynamically and is
produced by considering the following naming precendence (listed highest to lowest).  Note
that some of the following label types are not a result of a reference, but are considered
when producing the default label name.


1. `FUN_<addr>` : Function entry point
2. `EXT_<addr>` : External entry point
3. `SUB_<addr>` : Call flow reference destination
4. `LAB_<addr>` : Branch flow reference destination
5. `DAT_<addr>` : Data reference destination


## Ref-Types


The term **Ref-Type**, as used within Ghidra, is rather ambiguous - and will hopefully be
changed in a future release of Ghidra.  While the following "*types of references*"
are supported in Ghidra: memory, stack, register and external.  We define **Ref-Type**
as the "*type of data access*" or "*type of flow*" associated with a reference.
The following table attempts to clarify the various **Ref-Types** and when they can be
used.


| **Ref-Type**   | ***Reference**   | **Flow/Data**   | **Description**   |
| --- | --- | --- | --- |
| DATA   | MSR   | Data   | General data/pointer reference   |
| DATA_IND   | M   | Data   | General indirect data reference   |
| READ   | MSR   | Data   | Direct data read reference   |
| READ_IND   | M   | Data   | Indirect data read reference   |
| WRITE   | MSR   | Data   | Direct data write reference   |
| WRITE_IND   | M   | Data   | Indirect data write reference   |
| READ_WRITE   | MSR   | Data   | Direct data read/write reference   |
| READ_WRITE_IND   | M   | Data   | Indirect data read/write reference   |
| STACK_READ (Note 1) | S | Data | Direct stack read reference   |
| STACK_WRITE (Note 1) | S | Data | Direct stack write reference   |
| EXTERNAL_REF(Note 2) | E | - | External program reference (flow or data access             unspecified)   |
| INDIRECTION | M | Flow | Indirect flow via a pointer (reference should be from an instruction             to a pointer).  Alternatively, a COMPUTED CALL or JUMP reference could be placed             from an instruction to one or more indirect destination instructions.   |
| COMPUTED_CALL | M | Flow | Computed call flow from an instruction   |
| COMPUTED_JUMP | M | Flow | Computed jump flow from an instruction   |
| UNCONDITIONAL_CALL | M | Flow | Unconditional call flow from an instruction   |
| UNCONDITIONAL_JUMP | M | Flow | Unconditional jump flow from an instruction   |
| CONDITIONAL_CALL | M | Flow | Conditional call flow from an instruction   |
| CONDITIONAL_JUMP | M | Flow | Conditional jump flow from an instruction   |
| CALL_OVERRIDE_UNCONDITIONAL | M | Flow | Used to override the destination of a CALL or CALLIND pcode operation.  CALLIND operations are             changed to CALL operations.  The new call target is the "to" address of the reference.  The override only takes effect             when the reference is primary, and only when there is exactly one primary CALL_OVERRIDE_UNCONDITIONAL reference at the "from"             address of the reference.   |
| JUMP_OVERRIDE_UNCONDITIONAL | M | Flow | Used to override the destination of a BRANCH or CBRANCH pcode operation.  CBRANCH operations are             changed to BRANCH operations.  The new jump target is the "to" address of the reference.  The override only takes effect             when the reference is primary, and only when there is exactly one primary JUMP_OVERRIDE_UNCONDITIONAL reference at the "from"             address of the reference.   |
| CALLOTHER_OVERRIDE_CALL | M | Flow | Used to change CALLOTHER pcode operations to CALL operations. The new call target is the "to" address of the              reference.  Any inputs to the original CALLOTHER op are discarded; the new CALL op may have inputs assigned to it during decompilation.             The override only takes effect when the reference is primary, and only when there is exactly one primary              CALLOTHER_OVERRIDE_CALL reference at the "from" address of the reference. Only the first CALLOTHER operation at the "from"             address of the reference is changed. *Applying this override to instances of a CALLOTHER op that have output is not recommended              and can adversely affect decompilation (e.g., the decompiler may throw an exception).* You can see whether a particular instance has an              output by enabling the "PCode" field of the Listing. Note that this reference override takes precedence over those of CALLOTHER_OVERRIDE_JUMP             references.   |
| CALLOTHER_OVERRIDE_JUMP | M | Flow | Used to change CALLOTHER pcode operations to BRANCH operations. The new jump target is the "to" address of the              reference.  The override only takes effect when the reference is primary, and only when there is exactly one primary              CALLOTHER_OVERRIDE_JUMP reference at the "from" address of the reference. Only the first CALLOTHER operation at the "from"             address of the reference is changed. *Applying this override to an instance of a CALLOTHER op with output is not recommended* (see             the discussion above about CALLOTHER_OVERRIDE_CALL references).   |


*In the above table, the ***Reference*** column indicates the "*type of
reference*" for which the ***Ref-Type*** is applicable: Memory, Stack,
Register and External.


NOTES:


1. The use of STACK_READ and STACK_WRITE Ref-Types will likely be replaced with READ and
WRITE Ref-Types in a future release of Ghidra.
2. The EXTERNAL_REF is a general purpose Ref-Type used for all External references.  At
this time, the type of flow or data access for an external reference is unspecified.
3. If you need to alter the FALL_THROUGH flow behavior of an instruction, modify the [Fallthrough Address](../FallThroughPlugin/Override_Fallthrough.md) instead
of adding a memory reference.


## Actions for Creating and Deleting References From a Code Unit


There are three actions provided by the ReferencesPlugin which are accessible from the
CodeBrowser Listing while the current cursor location is on the mnemonic or operand of an
instruction or data code unit.  The create and delete reference actions may be disabled
under certain conditions.


- [References from](#viewing-and-editing-references-addedit-r)
- [Add Reference from...](#add-reference-from)
- [Create Default Reference](#creating-a-default-reference-alt-r) (menu item varies based
upon current operand)
- [Delete References](#deleting-references-from-a-code-unit-delete) (menu item varies based upon
mnemonic/operand current references)


> **Note:** Default key-bindings for actions are
indicated with {}'s.


### Add Reference From


While there is a separate action for creating a default reference on an operand (see [Creating a Default Reference](#creating-a-default-reference-alt-r) below), an arbitrary
reference may be also be added directly to a mnemonic or operand by using the popup menu action
***References →  Add Reference from...*** .
This will cause the [*Add Reference Dialog*](#addrefdialog) to be
displayed, allowing the user to specify any of the permitted reference types.


### Creating a Default Reference {Alt-R}


While the current cursor location is on the operand of an instruction or data code unit
within the CodeBrowser Listing, the popup menu item ***References →  Create Default Reference**** may be selected to create
the default primary reference for an operand.  This action will be disabled if the current
location does not correspond to an operand field or a default reference can not be determined.


When creating a default *Memory* reference on a scalar operand, for programs with
multiple memory spaces, repeatedly invoking this action will cycle the default reference
through all suitable memory spaces.  If the wrong memory space was used in creating the
*Memory* reference, simply repeat the action.


When adding a *Stack* or *Register* reference, a corresponding parameter or
variable may be created.  If a local variable is created, the first-use-offset of the
variable will correspond to the source instruction location.  For this reason, it is
recommended that the first reference to a variable be created on the first "assignment"
instruction.  If a newly created variable is unwanted, it may be deleted by clicking on it
within the Listing and hitting the "*Delete*" key.  Keep in mind that when a variable
is deleted, any explicit bindings to that variable will be cleared.


> **Note:** *The popup menu item name Create Default
Reference may differ based upon the type of reference which will get created:  Create
Memory Reference, Create Stack Reference, Create Register Reference.


### Deleting References from a Code Unit {Delete}


While the current cursor location is on the mnemonic/operand of an instruction or data code
unit within the CodeBrowser Listing, the popup menu item ***References →  Delete Reference***s* may be selected to delete all
references on the current mnemonic/operand.  This action will be disabled if the current
location does not correspond to a mnemonic/operand field or references do not exist on the
current mnemonic/operand.


> **Note:** *The popup menu item name Delete References may
differ based upon the existing reference(s):  Delete Memory References, Delete Stack
Reference, Delete Register Reference, Delete External Reference.


## Viewing and Editing References (*Add/Edit...*) {'R'}


All references "from" a data or instruction code unit can be edited and/or viewed by
clicking on the code unit (or a specific operand) within the Listing and activating the
***Add/Edit...*** action via the popup menu item ***References →  Add/Edit...*** {'R'}.   Each time this action is
invoked a new instance of the ***References Editor*** panel will be displayed.  Once the panel is
displayed, the ![locationIn.gif](../icons/locationIn.gif)  toggle button may be pushed-in to
have the *source* location follow the current location within the [Listing](../CodeBrowserPlugin/CodeBrowser.md) display.


![](images/RefProvider.png)


### Source


The references displayed and managed within this panel are all "from" a single
*source* instruction or data code unit.  The current *source* code
unit  is displayed at the top of the ***References Editor*** panel as it would
appear in the [Listing](../CodeBrowserPlugin/CodeBrowser.md).
Using this display, you can click on either the code unit Mnemonic or an individual
operand to highlight the corresponding references within the table below and to set the
operand target when adding additional references.  The selected Source operand will be
treated as the "active source operand" used for Add actions.  These operand labels
will also act as drag-n-drop target zones for code unit selections dragged from the [Listing](../CodeBrowserPlugin/CodeBrowser.md) (see [Adding Memory References from a Selection](#adding-memory-references-from-a-selection)).


> **Note:** The table entries that match the selected source element will be gray in color.


The Home Button ![go-home.png](../icons/go-home.png)  can be used to set the
current Listing location to the Source code unit address.


### References Table


All references "from" the current *source* code unit are listed within the table
with the following columns:


- ***Operand*** - Indicates on which portion of the code unit the reference has
been placed (`MNEMONIC,OP-0,OP-1,OP-2,...`).
- ***Destination*** - Indicates the destination location associated with the
reference.  The destination displayed for each type of reference utilizes a
different format:
`<`*address*`>` : indicates a memory destination
*`<address>`**&lt;signed-offset&gt;* : indicates an offset memory
reference relative to a base address.
`Stack[`*&lt;signed-**offset**&gt;*`]` : indicates a
stack reference with a specified stack frame offset.
`<`*register*&gt; : indicates a register reference for the specified
register.
`External` : indicates an external reference
- ***Label*** - Indicates the namespace-qualified symbol name associated with
the destination (See [Reference Destination Symbols](#reference-destination-symbols)).
- ****Ref-Type*** - Identifies the type of data access or instruction flow
associated with a reference.
- ****Primary?*** - Allows the user to choose a single memory reference which
will be reflected in the rendering of a code unit operand.
- ***User Ref?*** - References which were manually added by the user or by
means of auto-analysis will have a check displayed.


> **Note:** *With the exception of External references,
both the Ref-Type and Primary? choices may be changed directly within this
table.


> **Note:** References and symbol names corresponding to
memory references outside of the program's defined memory blocks will be displayed in red
(e.g., DAT_00000000 ).   These red references
frequently correspond to well-known memory locations, although they could point out a bad
reference. Creating memory
blocks for valid fixed memory locations (e.g., memory mapped I/O regions) will help to
resolve some of these apparent " BAD " references.


### Actions


The following actions are available from the ***References Editor*** panel.
For those actions with a default key-binding or mouse-click-binding, this has been
indicated with {}'s.


![Plus.png](../icons/Plus.png) ***Add
Reference*** {Insert-key} - Invoking this action will launch the Add Reference Dialog
for the current code unit (see [Adding a Reference](#adding-a-reference)).


![edit-delete.png](../icons/edit-delete.png) ***Delete
References*** {Delete-key} - Invoking this action will delete all selected
references.


![editbytes.gif](../icons/editbytes.gif) ***Edit
Reference*** {Enter-key or double-click a row} - Invoking this action will popup the
***Edit Reference Dialog*** for the selected reference (see [Editing a Reference](#editing-a-reference)).  This action is  only available when a
single reference row is selected.


![Make Selection](../icons/stack.png) ***Select
Memory Reference Destination*** - With one or more memory references selected in the
table, invoking this action will cause the corresponding locations within the [Listing](../CodeBrowserPlugin/CodeBrowser.md) to become selected.


![locationIn.gif](../icons/locationIn.gif)
***Follow Tool Location Changes*** - Once enabled (i.e., button pushed-in), any
location change within the tool (e.g., Listing panel)  will cause the currently
displayed  *source* code unit and associated references to reflect the new
location.


![locationOut.gif](../icons/locationOut.gif)
***Send Location Change for Selected Reference Destination*** - Once enabled (i.e.,
button pushed-in), selecting a single row within the references table will send a location
change to the tool corresponding to the selected *destination*.  This will have
the effect of  scrolling the [Listing](../CodeBrowserPlugin/CodeBrowser.md) to selected *destination*.
In the case of an external location, an attempt will be made to open the
corresponding program and scrolling to the corresponding external label within that
program.


***![go-home.png](../icons/go-home.png) GoTo
Reference Source Location*** - Invoking this action will send a location change to the
tool corresponding to the *source* code unit.  This will have the effect of
scrolling the [Listing](../CodeBrowserPlugin/CodeBrowser.md) to
the current *source* code unit.


## Adding a Reference


Invoking the ***Add...*** action from the ***References Editor*** window will
cause the ***Add Reference Dialog*** to be displayed for the current *Source* code
unit.  Once displayed, the *Source* code unit mnemonic or operand may be selected by
clicking on it, as well as the *Type of Reference*.  The available choices for Type
of Reference may be constrained based upon the chosen operand.


> **Note:** In general, only flow references should be set
on an instruction mnemonic, unless of course the instruction has no operands.  References
from data code units (e.g., addr/pointer) should always specify the scalar operand as the
source, not the mnemonic (i.e., data-type).


> **Note:** Stack and register references may only be
specified for source code units contained within a function. Register references
may only be set on operands containing a single register and in general should correspond to a
WRITE Ref-Type .


> **Note:** With the exception of memory references, only a
single reference may be set for a given operand or mnemonic.


> **Note:** An External reference
may not be set on a mnemonic.


![](images/AddReferenceDialog.png)


Based upon the chosen *Type of Reference*, the lower portion of the dialog will
change.  The following sections discuss the input panels for each of the four possible
choices:


1. [Memory Reference Panel](#memory-reference-panel) *(includes Offset and Offcut
references)*
2. [External Reference Panel](#external-reference-panel)
3. [Stack Reference Panel](#stack-reference-panel)
4. [Register Reference Panel](#register-reference-panel)


Once the appropriate reference panel has been filled-in as required, the ***Add***
button may be clicked to complete the operation.


When adding a *Stack* or *Register* reference, a corresponding parameter or
variable may be created.  If a local variable is created, the first-use-offset of the
variable will correspond to the source instruction location.  For this reason, it is
recommended that the first reference to a variable be created on the first "assignment"
instruction.  If a newly created variable is unwanted, it may be deleted by clicking on it
within the Listing and hitting the "*Delete*" key.  Keep in mind that when a variable
is deleted, any explicit bindings to that variable will be cleared.


## Editing a Reference


Invoking the ***Edit...*** action from the ***References Editor*** window will
cause the ***Edit Reference Dialog*** to be displayed for the current *Source*
code unit.  Once displayed, the *Source* code unit mnemonic or operand corresponding
to the edited reference will be selected, as well as the *Type of Reference*.
Neither the *Source* operand nor the *Type of Reference* may be changed when
editing a reference.  If you wish to change either of these settings you must delete the
reference and [add a new
reference](References_from.md#adding-a-reference).


The *Edit Reference Dialog* uses the same layout as the [Add
References Dailog](#addrefdialog) with the only exception being the dialog title and the *Add* button
which is named ***Update*** in the Edit mode.  Similarly, the lower portion of the
dialog will vary based upon the *Type of Reference*.  The following sections discuss
the input panels for each of the four possible choices:


1. [Memory Reference
Panel](References_from.md#memory-reference-panel) *(includes Offset and Offcut references)*
2. [External Reference
Panel](References_from.md#external-reference-panel)
3. [Stack Reference
Panel](References_from.md#stack-reference-panel)
4. [Register Reference
Panel](References_from.md#register-reference-panel)


Once the specific reference panel settings have been modified, the ***Update***
button may be clicked to complete the operation.


## Memory Reference Panel


A [Memory Reference](#memory-references) identifies a data access or instruction flow to
another memory location within the same program space.    A memory reference may
optionally be specified as an [Offset Reference](#offsetrefs) relative to a
specified *Base Address*.  The term Offcut is used to characterize a memory
reference or its resulting label whose destination address does not correspond to the start
of a data or instruction code unit (see [Offcut References](#offcutrefs)).


Below is an image of the *Memory Reference Panel* as it might appear in the *Add
Reference* or *Edit Reference Dialog.*The two views reflect a  regular
memory reference and an *Offset* reference (*Note the Address label change based upon
the Offset selection state*).


![](images/MemRefPanel.png)


### Offset


If the *Offset* checkbox is "checked", this memory reference will be treated as
an Offset Reference relative to the specified *Base Address*.  The actual
"to" address will be computed by adding the specified signed *Offset* value to the
*Base Address*.  The number format is assumed to be decimal unless the "0x"
prefix is used when entering a Hex value.


### To Address


[***![](images/unchecked.png)
Offset***] The *To Address* entry is required for normal memory references
and specifies the reference destination as a memory offset within a selected address
space. Enter an address
(or [Address Expression](../Misc/AddressExpressions.md)) to specify
the referenced address.
For those processors with multiple address-spaces, a pull-down is also provided
allowing the address-space to be selected.  Address spaces which overlay the
OTHER non-loaded space are only included if the **Include OTHER overlay spaces**
checkbox is selected.


### Base Address


[***![](images/checked.png)
Offset***] The *Base Address* entry is required for offset memory references
and specifies the offset base location.  See **To Address** entry above for
entry details.


### Include OTHER overlay spaces


The *Include OTHER overlay spaces* checkbox when selected allows address spaces
which overlay the OTHER non-loaded space to be included in the *To Address*
or *Base Address* address space selection pulldown list.  This may be appropriate
when working with special purpose overlay spaces which can facilitate flow overrides
(e.g., *syscall*).


### Address History Button


The *Address History* pulldown button may be used to recall a previously
applied *To Address* or *Base Address* entry.  Only the last ten (10)
address entries are maintained for each open Program.


### Ref-Type


Allows selection of the data access or instruction flow type associated with this
reference (see [Ref-Types](#ref-types)).


## External Reference Panel


An [External Reference](#external-references) identifies a memory destination within another
Program file.  Such references are generally used to indicate a library module linkage.
The memory location within the *External Program* is identified by either a
*Label* or an *Address.*


Below is  an image of the *External Reference Panel* as it might appear in the
*Add Reference* or *Edit Reference Dialogs*:


![](images/ExtRefPanel.png)


### Name


This field identifies a namespace name corresponding to the *External Program* and
may be typed-in or chosen from the pull-down list of those previously defined.   This
is a required input.


### Path (Clear/Edit)


This field identifies the Program file within the Ghidra Project which corresponds to
the selected Name.  Associating the *External Program Name* with a Program file
*Path* is optional, but can be useful to facilitate navigation to an associated
library if it is contained within the same project.  This *Name/Path* association
can easily be "resolved" at a later time via the [External Program Names Dialog](external_program_names.md).


### Label / Address


The specific memory location within the External Program is identified by either a Label
defined within the corresponding Program file, or via a specific Address.  If both a
Label and Address are specified, the Label will take precendence during navigation.
The *Address* field is always interpretted as a hex value  (i.e., the 0x entry
prefix is assumed) offset within the default address space.


## Stack Reference Panel


A [Stack Reference](#stack-references) identifies a data access to a function
parameter or local variable within the containing function's stack frame*.*


Below is  an image of the *Stack Reference Panel* as it might appear in the
*Add Reference* or *Edit Reference Dialogs*:


![](images/StackRefPanel.png)


### Stack Offset


Specifies a signed offset within the containing function's stack frame.  The
number format is assumed to be decimal unless the "0x" prefix is used when entering a
Hex value.


### Ref-Type


Allows selection of the data access or instruction flow type associated with this
reference (see [Ref-Types](#ref-types)).


### Variable Name


An optional entry which identifies the variable name to be associated with
this reference.  Selecting an existing variable will automatically change the
Stack Offset to match the selected variable.  Entering a new name which does not
exist will cause a new stack parameter or variable to be created with the reference.
Clearing this field will have the same effect as keeping the initial default
variable choice.


## Register Reference Panel


A [Register Reference](#register-references) identifies a data access (i.e., value
assignment) to a function local variable within the containing function's stack
frame*.*


Below is  an image of the *Register Reference Panel* as it might appear in the
*Add Reference* or *Edit Reference Dialogs*:


![](images/RegRefPanel.png)


### Register


Indicates the selected operand's register to which a local register variable reference
will be established.


### Ref-Type


Allows selection of the data access or instruction flow type associated with this
reference (see [Ref-Types](#ref-types)).


### Variable Name


An optional entry which identifies the variable name to be associated with this
reference.  Entering a new name which does not exist will attempt to create a new local
register variable with the reference.  Clearing this field will have the same effect as
keeping the initial default variable choice.


## Adding Memory References from a Selection


A code unit selection from the CodeBrowser Listing may be dragged and dropped onto the
***References Editor*** panel to create [Memory References](#memory-references) in bulk
for the current Source.  This capability must be used carefully since a separate reference
will be created "to" every code unit contained within the selection.


The specific mnemonic/operand which will be used as the source for the new memory references
depends on where the selection is "dropped" within the ***References Editor*** panel (see
figure below).  The preferred method is to "drop" the selection on the correct
monc/operand within the ***Source*** code unit area (i.e., *Operand-specific Drop
Zone*).  Alternatively, the selection may be "dropped" on the reference table (i.e.,
*Active-operand Drop Zone*) to utilize the current mnemonic/operand choice from the
***Source*** code unit area.  When "dropping" on the table, be careful "dragging"
the selection across te ***Source*** code unit area since this could change the active
Source mnemonic/operand for the panel.


![](images/DropZones.png)


*Provided By:  *ReferencesPlugin**


**Related Topics:**


- [Resolving External Names](external_program_names.md)
- [Show References to
a location](../LocationReferencesPlugin/Location_References.md)
- [Code Browser
Navigation](../CodeBrowserPlugin/CodeBrowser.md#navigation)


---

[← Previous: Register References](References_from.md) | [Next: Back References →](../LocationReferencesPlugin/Location_References.md)
