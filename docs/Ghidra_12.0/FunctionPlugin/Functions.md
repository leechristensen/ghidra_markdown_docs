[Home](../index.md) > [FunctionPlugin](index.md) > Stack Depth Change

# Functions


Functions store information about locations within a program that may be referenced by a call
instruction, although no direct reference to a function is required. External Functions
may also be defined and associated with a Library
Namespace.  A function definition consists of:


- An entry point address or external location symbol
- A body of instructions (*does not apply to External Functions*)
- A function signature/prototype specification, consisting of:
- Optional function attributes, including:
- Additional function listing markup (*does not apply to External Functions*):


When displayed in the browser, a function includes:


- The entry point is usually called by another instruction, although there may be no direct
reference to the function within the program. The entry point of a function must be an
instruction.
- The body of the function is under user control, but can be automatically calculated when
the function is defined. The body can be a contiguous range of addresses or may be multiple
address ranges. Data may also be included within the body.
- The complete function signature and optional attributes are displayed within the listing at
the function entry point.
This information may also be displayed at pointers which reference a function
provided the appropriate tool option for displaying function headers
is enabled (see [Listing Fields options / Function Pointers](../CodeBrowserPlugin/CodeBrowserOptions.md#function-pointers)).


## Function Signature, Attributes and Variables


Please refer to [Function Signature and Variables](Variables.md) for details
on this subject and how to modify a function signature/prototype specification, including function
attributes and variable storage.


## Create Function


*Create Function* creates a function with an entry point and a body of
instructions.


To Create a Function,


1. Place the cursor in the Code Browser at the address with a defined instruction.
2. Right-mouse-click, select the **Create Function** popup menu item


*As part of creating a function, function parameters
and local variables may also be created. See [Variables](Variables.md) for the
operations on variables.*


*Functions may be automatically created via [Auto Analysis](../AutoAnalysisPlugin/AutoAnalysis.md).*


*If a function starts with an unconditional jump
instruction, the function will be created as a [Thunk Function](#thunkfunctions)
if possible.*


The entry point for the function is the address at the current cursor location when there
is no selection. With a selection, the entry point is the minimum address in the
selection.


The current code browser selection is used as the function body. In the absence of a
selection, *Create Function* will follow the control flow from the entry point to
determine the function body. The resulting code may not be contiguous.


*To see the body of the function that has been
defined, place the cursor on the first instruction within the function and choose
**Select** →  **Functions** from the Code Browser's
main menu.*


The symbol at the entry point is used as the name of the
function. If no symbol exists at the entry point a default label starting with **FUN_** is created. Prior to creating the function, the symbol may have
started with **SUB_** if it was a default symbol and there
were call references to it. If a symbol does exist at the entry, a dialog is displayed so
that you can change the suggested function name, **FUN_**
**`<address>`**. After the function is created, a symbol
is created with the name from the dialog.


If the symbol name is changed, the function name displayed will also change. [Rename Function](#cbannotationfunctionsrename) can be used to rename the function.


In stack-based processors, *Create Function* will try to identify parameters and
local variables used by the function. By default, the variables data type will be
*Undefined**N*** where ***N*** is the size (in bytes) of the stack reference.
See [Function Signature and Variables](Variables.md) on how to modify the stack
variables. See [Stack References](../ReferencesPlugin/References_from.md#stackrefs) on how to add stack variables.


**Select** →  **Subroutines** will display the scope
of a subroutine from any address within the scope of the subroutine. It is helpful to use the
**Subroutines** option to determine what the potential scope of a function would be if you
create it.


## Re-Create Function


*Re Create Function* rebuilds a function's body of addresses without destroying any
parameters or stack references that may have already been created.  This action is
useful when additional code has been found, for example from a computed jump (or switch),
that was not know when the original function was created.  Most likely auto-analysis
will have fixed the function's body already and re-creating the function won't be
necessary.


With no selection, the function's body is
re-calculated based on the flow of the instructions from the function's entry point address.
With a selection, the body of the function is set to the current selection.


To Re Create a Function,


1. Place the cursor in the Code Browser at the top of an already defined function.
The cursor can be on any field at the entry point of the function.
2. Right-mouse-click, select the **Function** → **Re-create Function** popup menu item


To Re Create a Function, with a forced new body


1. Create a selection in the Code Browser that should be the body of the function.
The cursor should be at the top of the already defined function.
The cursor can be on any field at the entry point of the function.
2. Right-mouse-click, select the **Function** → **Re-create Function** popup menu item


*Recreating a function will kick off auto-analysis
on the function if there are any changes to the function's body.  New parameters or
locals may be created since more code may now be part of the function's body. See [Variables](Variables.md) for the operations on variables.*


## Thunk Functions


*Thunk Functions* are a common artifact of compiled code and are frequently used to
facilitate access to external functions, functions located far from the caller, and other
relocation scenarios. Ghidra has the ability to specify a function as being a *thunk*
for another function. A *thunk* has the same function signature and parameter storage as
the real function (also referred to as the *thunked-function*), although its name may differ.
A *thunk* function
within Ghidra acts as a proxy to the real/thunked-function where all parameter and attribute
changes to one are reflected onto the other. One exception to this is the name. If a *thunk*
is created without a name, its name will reflect the name of the *thunked* function.
Renaming the *thunk* allows the thunk to have a name which
differs from the thunked-function. Local variables are not supported for *thunk* functions.



> **Note:** Within the Code Browser, double-clicking on a thunk function name will navigate to the associated thunked function, while thunked functions will display back-references (i.e., XREFs) to
the associated thunk functions with a Ref-Type of 'T'.


To Create a Thunk-Function:


1. Select the instructions which corresponds to the body of the new thunk function, or
place your cursor on a single unconditional jump instruction which jumps to the
thunked-function.
2. Right-mouse-click, select the **Create Thunk Function** popup menu item
3. If unable to determine the thunked-function, the user will be prompted to specify the
thunked-function by label or address. The specified location must correspond to an existing
function.


To Edit a Thunk Function (i.e., set the associated *thunked* function) or
Convert a normal Function to a Thunk Function:


1. Place the cursor in the Code Browser at the top of an already defined *thunk*
function.
The cursor can be on any field at the entry point of the function.
2. Right-mouse-click, select the **Function** → **Set
Thunked Function...** popup menu item
3. The user will be prompted to specify the *thunked* function by label or address. The
specified location must correspond to an existing function.


To Revert a Thunk Function (i.e., revert a Thunk Function to a normal Function):


1. Place the cursor in the Code Browser at the top of an already defined *thunk*
function.
The cursor can be on any field at the entry point of the function.
2. Right-mouse-click, select the **Function** → **Revert
Thunk Function...** popup menu item
3. The user will be prompted to confirm the action.


## External Functions


Defining an *External Function* allows a function to be defined which does not reside within
the current program listing or whose actual memory address is unknown.  Similar to a simple *External Location*,
these external symbols are associated with named *Library* namespaces and are most easily
managed via the [Symbol Table](../SymbolTablePlugin/symbol_table.md) or
[Symbol Tree](../SymbolTreePlugin/SymbolTree.md) under the *Imports* category.
If the actual *Library*
name is unknown, the "`<EXTERNAL>`" *Library* (or any other named Library) may be used as a
parent namespace.


From either the [Symbol Table](../SymbolTablePlugin/symbol_table.md) or
[Symbol Tree](../SymbolTreePlugin/SymbolTree.md), an existing *External Location*
may be converted to a function using the *Create External Function* popup action
on the selected node.  The resulting *External Function* may be converted back to a
simple *External Location* by deleting the function node.  To really remove the function
and its location will require a second delete on the *External Location*.


From either the [Symbol Table](../SymbolTablePlugin/symbol_table.md) or
[Symbol Tree](../SymbolTreePlugin/SymbolTree.md), an existing *External Function*
may be modified using the **Function** → [Edit
Function...](Variables.md#edit-function) popup action on the selected function node.


Creating an [External Reference](../ReferencesPlugin/References_from.md#extrefpanel)
is currently the only mechanism within the Ghidra GUI
to establish an *External Location*.  Once an *External Location* has been established, it can be
converted to a function (see above).  This limitation should hopefully be resolved in
a future release of Ghidra.


## Create Multiple Functions


*Create Multiple Functions* creates functions from a selection in the listing. It
works from the minimum address to the maximum address in the selection trying to create
functions if possible. Any addresses that are already part of a function are discarded and
not used to determine new functions. Also whenever a function is created by this action, all
the addresses in the body of the created function are also discarded from being possible
addresses for starting a new function.


A common use of this action is on a selection containing the entry point addresses of the
functions you want to create.


## Edit Function


For information on editing functions, see [Function
Signature Help.](Variables.md#edit-function)


## Rename
Function


*Rename Function* renames an existing function. As discussed in [Create Function](#create-function), the function name is the same as the primary label at
the functions entry point.


To rename a function,


1. Right-mouse-click on the function header in the Code Browser
2. Select the **Function** → **Rename Function**
popup menu item
3. Enter the new function name and/or namespace, click OK. The name may also be entered
with a fully qualified namespace (e.g., mynamespace::myfunction). The '::' is used as a
namespace delimiter.


## Delete Function


*Delete Function* removes a function. There is no confirmation for the Delete
Function operation. However, the results can be undone using the [Undo operation](../Tool/Undo_Redo.md).


When a function is deleted all stack variable definitions are removed, along with all
references to those variables from instructions within the function's body. If a stack
reference refers to a stack variable that is deleted, any references will be replaced with
Stack [offset], where offset is the relative offset to the
stack.


To Delete a Function,


1. Right mouse-click on the function header
2. Select the **Function** → **Delete Function**
popup menu item


When a function is deleted, all stack and register references from instructions within the
function body are removed. The function comment (which is really the [plate comment](../Glossary/glossary.md#platecomment) for that address) remains
intact if you had made changes to it, or if the plate comment existed before the function was
created.


If there are still *call* references to this address, the label changes from **FUN_** to **SUB_** .


## Function Purge


A **function purge** is the number of additional bytes (not including the return value) a function pops
from the stack when it returns. The value is calculated as the difference between the stack pointer's value exiting
the function and its value coming into the function but excludes the final pop of the return address.


For most calling conventions, the function purge is always zero. A major exception is the 32-bit x86 *stdcall*
calling convention, where the function may pop off its own stack parameters in addition to the return value.
The function purge in this situation can be positive indicating that more values are popped from the stack.
For other unusual situations, a negative function purge can be set indicating that the function *pushes* additional
values.


For architectures where the stack grows in the *positive* direction, the meaning of the function purge sign
is reversed.  A positive function purge indicates additional bytes are *pushed* to the stack, and a negative
function purge indicates bytes are *popped* from the stack.


To change the function purge:


- Right mouse-click on the function header
- Select the **Function** → **Edit Function
Purge...** popup menu item
- Enter the new function purge size in the dialog that appears


## Function Repeatable Comment


When a repeatable comment exists at the entry point of a function, the repeatable comment
is displayed in the *Function Repeatable Comment* field rather than the *EOL
Comment* field. See [Edit
Comments](../CommentsPlugin/Comments.md#edit-comments) for more information on comments.


## Stack Depth
Change


You can specify a relative change in the stack depth at the address of the current
location in the program.


### Set Stack Depth Change


To set a change in stack depth:


- Right mouse-click on the Listing.
- Select **Set Stack Depth Change...** from the popup menu.
- The *Set Stack Depth Change* dialog is displayed. The Stack Depth Change textfield
initially contains the current stack depth change value. If the stack depth change is not
explicitly set at this address, the default value will be based on the instruction. For a
call instruction, the default stack depth change will be based on the function purge value
of the called function.


![](images/SetStackDepthChange.png)


- Enter the desired change in stack depth. This can be either decimal or hexadecimal.
Hexadecimal is indicated by a "0x". For example, `-0x1a`.
- Press the Return key or the **OK** button to set the stack depth change.
- If  you are not on a Call instruction, the stack depth change will be set.
Otherwise, you will you will see a dialog allowing you to choose whether the value should
be applied as a stack depth change at the current address (**Local**) or as a function
purge at the called function (**Global**). Choose **Local** to set the stack depth
change or **Global** to set the function purge.


![](images/StackDepthChangeOrFunctionPurge.png)


### Remove Stack Depth Change


To remove a change in stack depth where it is currently set:


- Put the cursor location on the *StackDepth = StackDepth + ...* line in the
Listing.
- Press the **Delete** key.


or


- Right mouse-click on the *StackDepth = StackDepth + ...* line in the Listing.
- Select *Remove Stack Depth Change* from the popup menu.


*Provided By: *Functions* plugin*


**Related Topics:**


- [Function Signature and Variables](Variables.md)
- [Auto Analysis](../AutoAnalysisPlugin/AutoAnalysis.md)
- [Stack
References](../ReferencesPlugin/References_from.md#stackrefs)
- [Comments](../CommentsPlugin/Comments.md)


---

[← Previous: Function Repeatable Comment](Functions.md) | [Next: Function Signature and Variables →](Variables.md)
