[Home](../index.md) > [DecompilePlugin](index.md) > Register Values

# Program Annotations Affecting the Decompiler


## Machine Instructions


Individual **machine instructions**
make up the biggest source of information when the
Decompiler analyzes a function.  Instructions are translated from their
processor-specific form into Ghidra's IR language (see [P-code](DecompilerConcepts.md#p-code)),
which provides both the control-flow behavior of the instruction and the detailed
semantics describing how the processor and memory state are affected. The translation is controlled by
the underlying processor model and, except in limited circumstances, cannot be directly altered
from the tool. Flow Overrides (see below) can change how certain control flow is translated
and, depending on the processor, how context registers affect p-code (see [Context Registers](DecompilerAnnotations.md#context-registers)).


Outside of the tool, users *can* modify the model specification itself.
See the document "SLEIGH: A Language for Rapid Processor Specification."


Decompiling a function starts by analyzing the control flow of machine instructions.
Control flow is traced from the first instruction, through additional instructions depending
on their flow semantics (see [P-code Control Flow](DecompilerConcepts.md#p-code-control-flow)).  All paths are traced through instructions with
any form of *fall-through* or *jump*
semantics until an instruction with *terminator* semantics is
reached, which is usually a formal *return* (return from subroutine) instruction.
Flow is not traced into called functions, in this situation.  Instructions
with *call* semantics are treated only as if they fall through.


An **entry point** is the address of the instruction first
executed when the function is called.


A **function body** is the set of addresses reached by control-flow
analysis and the machine instructions at those addresses.


### Entry Point


The *entry point* address for a function plays a pivotal role for
analysis using the Decompiler. Ghidra generally associates
a formal *Function Symbol* and an underlying
*Function* object at this address, which are the key elements that
need to be present to trigger decompilation
(see [Functions](../FunctionPlugin/Functions.md)).
The Function object stores the function body, parameters, local variables, and
other information critical to the decompilation process.


Function Symbols and Function objects are generally created automatically by a Ghidra
analyzer when initially importing a binary executable and running Auto Analysis.
If necessary, however, a user can manually create a Function object from a Listing window
by using the *Create Function* command (pressing the 'F' key), when the cursor
is placed on the function's entry point
(see [Create Function](../FunctionPlugin/Functions.md#create-function)).


### Formal Function Body


When a function is created, Ghidra stores its function body as a set of addresses in the
Program database. This *formal* function body delineates the function
from all the other kinds of data within the Program and lets Ghidra immediately link addresses
in the middle of the function to the entry point and the Function object.  Decompiler windows
in particular use the formal function body to know which function to decompile in response
to a navigation event to an arbitrary address.


> **Warning:** The Decompiler does not use the formal function body when it computes
control flow; it recomputes its own idea of the function body starting from the entry point
it is handed.  If the formal function body was created manually, using a selection for instance,
or in other extreme circumstances, the Decompiler's view of the function body may not match
the formal view. This can lead to confusing behavior, where clicking in a Decompiler window
may unexpectedly navigate the window away from the function.


### Flow Overrides


Control-flow behavior for a machine instruction is generally determined by its underlying
p-code (see [P-code Control Flow](DecompilerConcepts.md#p-code-control-flow)), but this can be changed by applying a Flow Override.
A **Flow Override** maintains the overall semantics of a branching instruction
but changes how the branch is interpreted.  For instance, a `JMP` instruction, which traditionally
represents a branch within a single function, can be overridden to represent a call to a new function.
Flow Overrides are applied by Analyzers or manually by the user.


The Decompiler automatically incorporates any relevant Flow Overrides into its
analysis of a function. This can have a significant impact on results. The
types of possible Flow Overrides include:


> BRANCH Override Treats the primary CALL or RETURN behavior of the instruction as if it were a BRANCH within the function.  For CALL instructions,
the call target becomes the branch destination,
and the instruction is no longer assumed
to fall through. RETURN instructions become an
indirect branch, and the Decompiler will attempt to recover branch
destinations using switch analysis. CALL Override Treats the primary BRANCH or RETURN behavior of the instruction as if it were a CALL .
A BRANCH becomes a fall through instruction, and the destination address becomes
the call target, which may no longer be considered part of the function.  The computed
address for an indirect BRANCH or RETURN instruction becomes
the target address of an indirect CALL . CALL_RETURN Override Treats the primary BRANCH or RETURN behavior of the instruction as if it executed a CALL followed
by a RETURN operation.
The destination address of a BRANCH becomes the call target,
which may no longer be considered part of the function.  The computed address for
an indirect BRANCH or RETURN instruction becomes
the target address of an indirect CALL . RETURN Override Treats an indirect BRANCH or CALL instruction as if it were a RETURN instruction, terminating
the control-flow path within the function. The computed destination address is
considered part of the return mechanism of the function and may no longer be
explicitly displayed in the output.
An indirect BRANCH no longer invokes switch analysis during
decompilation.


## Comments


The Decompiler automatically incorporates comments from the Program database into its
output.  Comments in Ghidra are centralized and can be created and displayed by multiple
Program views, including the Decompiler.  Comments created from a Decompiler window will
show up in a Listing window for instance, and vice versa.


For the purposes of understanding comments within the Decompiler, keep in mind that:


> An individual comment is associated with a specific address in the Program. There are 5 different types of comments: Plate Pre Post End-of-line (EOL) Repeatable


For general documentation on creating and editing comments within Ghidra, see
[Comments](../CommentsPlugin/Comments.md).


### Display


The Decompiler collects and displays comments associated with any address in the
formal *function body* currently decompiling.
The comments are integrated line by line into the decompiled code, and an
individual comment is displayed on the line *before* the
line of code incorporating the instruction associated with the comment's
address.


Because a single line of code typically encompasses multiple machine instructions,
there is a possibility that multiple comments at different addresses apply to
the same line.  In this case, the Decompiler displays each comment on its
own line, in address order, directly before the line of code.


Because the output of the Decompiler can be a heavily transformed version compared
to the original machine instructions, it is possible that individual instructions
no longer have explicit tokens representing them in the output.  Comments attached
to these instruction will still be displayed in the Decompiler output with the
closest associated line of code, usually within the same basic block.


By default, the Decompiler displays only the *Pre* comments
within the body of the function.  It also displays *Plate*
comments, but only if they are attached to the *entry point*
of the function. In this case, they are displayed first in the Decompiler output,
along with WARNING comments, before the function declaration.  Other comment
types can be configured to be part of Decompiler output by changing the
Decompiler display options (see [Display <kind-of> Comments](DecompilerOptions.md#commentoptions)).


> **Warning:** Unlike a Listing window, the Decompiler does not alter how a comment is
displayed based on its type.
All enabled types of comment are displayed in the same way, on
a separate line before the line of code associated with the address.


### Unreachable Blocks


The Decompiler may decide as part of its analysis that individual
*basic blocks* are unreachable and not display them in the output.
In this case, any comments associated with addresses in the unreachable block
will also not be displayed.


### Warning Comments


The Decompiler can generate internal warnings during its analysis and will incorporate
them into the output as comments in the same way as the user-defined
comments described above. They are not part of Ghidra's comment system, however, and
cannot be edited.  They can be distinguished from normal comments by the word
'WARNING' at the beginning of the comment.


> /* WARNING: ... */


## Variable Annotations


Variable annotations are the most important way to get names and data-types
that are meaningful to the user incorporated into the Decompiler's output.
A **variable** in this context is loosely defined
as any piece of memory that code in the Program treats as a logical entity.
The Decompiler works to incorporate all forms of annotation into its output
for any variable pertinent to the function being analyzed.


At a minimum, a variable annotation in Ghidra provides a:


> Symbol name , Data-type , and Storage location .


### Creating Variable Annotations


Ghidra provides various ways that a name and other attributes can be ascribed
to a variable.  These break up roughly into *global* variables,
defined directly on memory in the Program image, and variables that are
*local* to a function.


Global variable annotations are created from the tool by applying a data-type to a memory
location in a Listing window, either by invoking a command from the *Data*
pop-up menu or by dragging a data-type from the *Data Type Manager*
window directly onto the memory location.  Refer to the documentation:


> Applying Data Type


Local variables annotations are created from the Listing using various editor dialogs. See, in particular:


> Function Signature Dialog Stack Frame Editor Creating a Default Reference


The *Decompiler* window also provides numerous ways of annotating variables, both local and global. In particular,
see the commands:


> Rename Variable Retype Variable Commit Params/Return Commit Local Names


### Variable Symbols


Ghidra maintains its own symbol table that supports namespaces and function
scopes, and variable names are automatically incorporated into this.
In order to widely accommodate different use cases, Ghidra's symbol
table has extremely lax naming rules.  Ghidra
may allow names that conflict with the stricter rules of the language
the Decompiler is attempting to produce. The Decompiler does not currently
have an option that checks for this. Users should be aware of:


> Illegal Characters Ghidra symbols allow almost every printable character except
a space in a symbol name; punctuation and keywords can be incorporated. Duplicate Symbols Ghidra allows different functions to have the same name, even within the same
namespace, in order to model languages that support function overloading .
In most languages, such functions would be expected to have distinct prototypes to allow
the symbols to be distinguished in context.   Ghidra and the Decompiler, however, do not check
for this, as prototypes may not be known.


#### Variable Scope


All variables belong to either a *global* or *local*
scope, which directly affects how the variable is treated in the Decompiler's data-flow
analysis.
Annotations created by applying a data-type directly to a memory location in the Listing
are automatically added to the formal *global* namespace.
Ghidra can create other custom namespaces that are considered global in this sense, and
renaming actions provide options that let individual global annotations be moved into
these namespaces.
Dialogs that are brought up in the context of a function, like the Function Signature Editor,
create variable annotations that are local to that function.


A global variable annotation forces the Decompiler to treat the memory location as if its value
persists beyond the end of the function. The variable must *exist*
at all points of the function body, generally at the same memory location.


Local variables,
in contrast, do not generally exist across the whole function, but come into scope
at the instruction that first writes to them, and then exist only up to the last
instruction that reads them.  The memory location storing a local variable
at one point of the function may be reused for different variables at other points.
This can cause ambiguity in how the Decompiler should treat a given memory location used
for storing local variables, which the user may want to steer. See the discussion
in [Variable Storage](DecompilerAnnotations.md#variable-storage).


### Variable Data-types


Ghidra provides extensive support for naming and describing
**data-types** that are tailored for the Program
being analyzed. Data-types that are explicitly part of a variable annotation
are, to the extent possible, automatically incorporated
into the Decompiler's analysis.


#### Data-types Supported by the Decompiler


The Decompiler understands traditional primitive data-types in all their various sizes,
like integers, floating-point numbers, booleans, and characters. It also understands
pointers, structures, and arrays, letting it support
arbitrarily complicated composite data-types. Ghidra provides
some data-types with specialized display capabilities that don't have a natural representation
in the high-level language output by the Decompiler. The Decompiler treats these as
black-box data-types, preserving the name, but treating the underlying data either as an integer
or simply as an array of bytes.


##### Undefined


The *undefined* data-types are supported in their various sizes:
**undefined1**, **undefined2**,
**undefined4**, etc.  In Ghidra, the undefined
data-types let the user specify the size of a variable, while formally declaring that
other details about the data-type are unknown.


For the Decompiler, undefined data-types, as an annotation, have the important special meaning
that the Decompiler should let its analysis determine the final data-type presented in the
output for the variable (see [Forcing Data-types](DecompilerAnnotations.md#forcing-data-types) below).


##### Void


The **void** data-type is supported but treated specially by
the Decompiler, as does Ghidra in general.  A **void** can be
used to indicate the absence of a return value in function prototypes, but cannot be used
as a general annotation on variables.  A void pointer, **void ***,
is possible; the Decompiler treats it as a pointer to an unknown data-type.


##### Integer


Integer data-types, both signed and unsigned, are supported up to a size of 8 bytes. Larger
sizes are supported internally but are generally represented as an array of bytes in
Decompiler output.  Nonstandard integer sizes of 3, 5, 6, and 7 bytes are also supported.


The standard C data-type names: **int**, **short**,
**long**, and **long long** are mapped to specific sizes
based on the processor and compiler selected when importing the Program.


##### Boolean


A 1-byte boolean data-type is supported. Boolean constants are rendered as either the
token **true** or the token **false**.


##### Floating-point


Floating-point sizes of 4, 8, 10, and 16 are supported, mapping in all cases currently to the
**float**, **double**,
**float10**, and **float16**
data-types, respectively.  The Decompiler currently cannot display floating-point constants
that are bigger than 8 bytes.


##### Character


ASCII- and Unicode-encoded character data-types are supported for sizes of 1, 2, and 4.  The size effectively
chooses between the UTF8, UTF16, and UTF32 character encodings, respectively. The standard
C data-type names **char** and **wchar_t** are
mapped to one of these sizes based on the
processor and compiler selected when importing the Program.


##### String


Terminated strings, encoded either in ASCII or Unicode, are supported.  The Decompiler converts
Ghidra's dedicated string data-types like **string** to
an array-of-characters data-type, such as **char[]**,
where the character size matches the encoding.
A pointer-to-character data-type like


> char * or wchar_t *


is also treated as a potential string reference. The Decompiler can infer terminated strings if this
kind of data-type propagates to constant values during its analysis.


Strings should be fully rendered in Decompiler output,
with non-printable characters escaped using either traditional sequences like '\r', '\n' or using Unicode
escape sequences like '\xFF'.


##### Pointer


Pointer data-types are fully supported.  A pointer to any other supported data-type is
possible.  The data-type being pointed to, whether it is a primitive, structure, or another pointer,
informs how the Decompiler renders a dereferenced pointer or other pointer expression.


The Decompiler automatically assumes that a pointer may reference an array of the underlying data-type.
If an integer value is added to the pointer and the value is known to be a multiple of the data-type's size,
the expression is treated as either *pointer arithmetic* or as an array access, and the multiplication
factor is hidden. Adding smaller integers to a structure pointer typically results in a
*field access* expression using the '-&gt;' or other language specific token. See the discussion
on *Structures* below.


The default pointer size is set based on the processor and compiler selected when the Program is
imported and generally matches the size of the **ram** or equivalent
address space. Different pointer sizes within the same Program are possible. The Decompiler generally
expects the pointer size to match the size of the address space being pointed to, but individual
architectures can model different size pointers into the space (such as *near* pointers).


For processors with more than one memory address space, pointer data-types do not by default indicate
a preferred address space and can be used to reference data in any address space.
Where there is ambiguity, the Decompiler attempts to determine the correct address space from the context
of its use within the function.  It is possible to create pointer data-types with an
explicitly preferred address space, see [Address Space Pointers](DecompilerAnnotations.md#address-space-pointers).


##### Array


Array data-types are fully supported. The array element can be any other supported data-type
with a fixed size.


For code that accesses arrays, the Decompiler keeps track of the array index and automatically
hides the underlying multiplication needed to account for the size of an element.  The access is
displayed as an expression using standard square brace notation, '[' and ']'.
For an access that covers more than one array element simultaneously, the Decompiler will either
generate a pointer expression that casts to a data-type of the correct size or may generate a
special token representing the accessed portion of the array.


```

	      text[iVar1] = 'a';           // Assigning a character to a variable index of the array
	      cVar2 = text[7];             // Reading a fixed element from an array
	      text._8_2_ = 0x7677;         // Auto-generated token indicating multiple elements are assigned at once

```


For an auto-generated token like `_8_2_`, the first integer indicates the offset in bytes
of the access from the start of the array, and the second integer indicates the number of bytes being accessed.


If more then one element is being accessed simultaneously, the Decompiler may try to split
the access into logical pieces. See the description of the analysis option for
[Splitting Array Accesses](DecompilerOptions.md#analysissplitarray).


##### Structure


Structure data-types are fully supported. The Decompiler does not automatically infer structures
when analyzing a function; it propagates them into the function from explicitly
annotated sources, like input parameters or global variables.  Decompiler-directed creation of
structures can be triggered by the user (see [Auto Create Structure](DecompilerWindow.md#auto-create-structure)).


For variables that are known to be structures, or pointers to structures, the Decompiler keeps
track of offsets into the variable and will render the name of the specific field being
accessed, using language specific access operators such as '.' or '-&gt;'. If the part of the
structure being accessed does not have a normal field name, either because the structure data-type
does not list a name at that position or because more than one field is being accessed
simultaneously, the Decompiler will either cast a pointer to a data-type of the correct size or
may automatically generate a token name representing the accessed portion.


```

	      struct1.a = 1;                // Assigning an integer to a field named "a"
	      fVar1 = ptr->b;               // Reading field "b" through a pointer
	      struct1._20_4_ = 0xff00ff00;  // Auto-generated name for assigning multiple fields at once

```


For an auto-generated token like `_20_4_`, the first integer indicates the offset in bytes
of the access from the start of the structure, and the second integer indicates the number of bytes being accessed.


If more than one field is being accessed simultaneously, the Decompiler may try to split
the access into logical pieces. See the description of the analysis option for
[Splitting Structure Accesses](DecompilerOptions.md#analysissplitstruct).


##### Enumeration


Enumerations are fully supported. The Decompiler can propagate enumerations from explicitly
annotated sources throughout a function onto constants, which are then displayed with the
appropriate label from the definition of the enumeration.  If the constant does not match a
single value in the enumeration definition, the Decompiler attempts to build a matching
value by *or*-ing together multiple labels.
The Decompiler can be made to break out constants representing packed *flags*,
for instance, by labeling individual bit values within an enumeration.


##### Function Definition


A **Function Definition** in Ghidra is a data-type that encodes
information about the parameters and return value for a generic/unspecified function.
A formal **function pointer** is supported by the Decompiler as a pointer
data-type that points to a Function Definition. A Function Definition specifically encodes:


> The name and data-type of each parameter. Whether the function takes a variable number of parameters. The data-type associated with the return value. The name of a generic calling convention associated with the function.


The Function Definition itself does not encode any storage information.  Once the Function
Definition is associated with a Program, its generic calling convention maps to one of the
specific prototype models for the processor and compiler. The prototype model is then used
to assign storage for parameters and return values, wherever the Function Definition is applied.
A Function Definition is currently limited to a prototype model
with one of the following names:


> __stdcall __thiscall __fastcall __cdecl __vectorcall


##### Unions


Unions data-types are fully supported.  The Decompiler does not automatically infer unions
when analyzing a function; it propagates them into the function from explicitly
annotated sources, like input parameters or global variables.


A union data-type, similarly to a structure, is made up of component data-types
called *fields*.  But unlike a structure, a union's fields all share the same underlying
storage.  When the union is applied to a variable, each field potentially describes the whole variable.
At any given point where the variable is read or written, a different field may be in effect, even if the
underlying data hasn't changed.  The decompiler attempts to infer the particular field by following data-flow
to or from the point of use to determine which field best aligns with the specific operations being applied to the
variable.  The name of this recovered field is then printed in Decompiler output using syntax similar to that
used for structure fields.


Depending on the number and variety of fields within the union, it may not be possible
to fully distinguish which field is being used in a specific context. In this situation,
the Decompiler chooses the first field from the list of best matches.  The user has the
option of changing this choice with the [Force Field](DecompilerWindow.md#force-field) action.


##### Typedefs


Typedef data-types are fully supported.  The Decompiler does not automatically infer typedefs
when analyzing a function; it propagates them into the function from explicitly annotated sources.


A **typedef** is copy of another data-type but with an alternate name.
In most cases it can be used interchangeably with the data-type it copies.
In general, the Decompiler treats a typedef as a distinct data-type, and it will maintain its identify
when it is assigned to variables and is propagated through data-flow.


Ghidra supports a specific set of attributes that can be placed directly on a typedef
that then distinguish it from the data-type it copies. This allows Ghidra to support some
non-standard data-types, although the typedef and its copy are no longer interchangeable.
The decompiler supports the following typedef properties:


- Component Offset - See [Offset Pointers](DecompilerAnnotations.md#offset-pointers)
- Address Space - See [Address Space Pointers](DecompilerAnnotations.md#address-space-pointers)


#### Pointer Attributes


The Decompiler supports some specialized attributes that can be applied to pointer data-types, like offsets
and address spaces (See below).  Ghidra implements these attributes on top of *typedef* data-types only. In
order to add attributes to pointers, a typedef of the underlying pointer data-type must be created first.
Attributes can then be placed directly on the typedef from the Data Type Manager window
(See [Pointer-Typedef Settings](../DataTypeManagerPlugin/data_type_manager_description.md#pointer-typedef-settings)).


##### Offset Pointers


An **offset pointer** points at a fixed offset relative to the start of its
underlying data-type. Typically the underlying data-type is a structure and the pointer points at a
specific field in the interior of the structure. But in general, the underlying data-type can be anything,
and the offset can point anywhere relative to that data-type, including either before or after.


An offset pointer is defined with all the same properties of a normal pointer.  It has an underlying
data-type and a size. On top of this an **offset** is specified
as an integer attribute on the pointer (typedef). This is the number of bytes that need to be
added to the start of the underlying data-type to obtain the address actually being pointed at.


Because the *underlying* data-type does not start directly at the address
contained in the offset pointer, one can also refer to the offset pointer's
**direct** data-type, i.e. the data-type that *is*
directly at the address contained in the pointer. If the pointer's offset is positive (and small),
the direct data-type will generally be that of a field of the *underlying*
data-type.  If the offset is bigger than the size of the underlying data-type or is negative,
the direct data-type will be *undefined*.


Offset pointers occur in code where the compiler has maintained knowledge of the position of
an underlying data-type relative to a pointer, even if the pointer no longer points directly at the data-type.
Because of this, the code may still access fields of the underlying data-type through the pointer.
Annotating a variable with an offset pointer allows the Decompiler to recover these accesses.


Within the Decompiler's output, the token `ADJ` is used to indicate that the code is
accessing the underlying data-type through the offset pointer. The token uses functional syntax
to indicate the particular offset pointer. Then, once the `ADJ` token is
applied, additional pointer syntax is used, i.e. `->`, to indicate what part
of the underlying data-type is being accessed.


```

              ADJ(structoffptr)->field1 = 2;  // Accessing the underlying structure's field
              iVar1 = *ADJ(intoffptr);        // Accessing the underlying integer data-type
              ADJ(arrayoffptr)[4] = iVar2;    // Accessing the underlying array

```


If the offset pointer appears in Decompiler output without the `ADJ` token being
applied, it is being treated as if it were a normal pointer to its direct
data-type.  This generally indicates the pointer is being used to access data outside the
underlying data-type.


##### Address Space Pointers


An **address space pointer** is a normal pointer data-type with a specific
address space associated to it (See [Address Space](DecompilerConcepts.md#address-space)).  Its created by setting
the Address Space attribute on a typedef of a pointer. The attribute value is the name of the specific
address space.


Address space pointers are useful, when a program architecture supports more than one address space
containing addressable memory, such as separate `code` and `data` address spaces.
For a program and a specific section of its code that manipulates a pointer, it may not be easy to determine
which address space is being referred to. Address space pointers provide an additional annotation mechanism
to help the decompiler identify the correct address space for a pointer in context.


The Decompiler will automatically propagate an address space pointer data-type from parameters and
other annotated variables associated with a function. Any constant that the pointer reaches via propagation
is assumed to point into the address space associated with the pointer.  The correct symbol can then
be looked up, further informing the Decompiler output.


#### Forcing Data-types


The Decompiler performs **type propagation** as part of its analysis
on functions. Data-type information is collected from variable annotations and other sources,
which is then propagated via data flow throughout the function to other variables and
constants where the data-type may not be immediately apparent.


With few exceptions, a variable annotation is *forcing* on the Decompiler in the sense
that the storage location being annotated is considered an unalterable data-type source.  During
type propagation, the data-type may propagate to other variables,
but the variable representing the storage location being annotated is guaranteed to have
the given name and that data-type; it will not be overridden.


> **Warning:** Users should be aware that variable annotations are forcing on the Decompiler and may directly
override aspects of its analysis.  Because of this, variable annotations are the most powerful way
for the user to affect Decompiler output, but setting an incomplete or incorrect data-type as
part of an annotation may produce poorer Decompiler output.


The major exception to forcing annotations is if the data-type in the annotation is *undefined*.
Ghidra reserves specific names to represent formally undefined data-types, such as:


> undefined1 undefined2 undefined4 undefined8


These allow annotations to be made even when the user doesn't have information about a variable's data-type.
The number in the name only specifies the number of bytes in the variable.


The Decompiler views a variable annotation with an undefined data-type only as an indication of what name
should be used if a variable at that storage address exists.  The data-type for the variable is filled in,
using type propagation from other sources.


For annotations that specifically label a function's formal parameters or return value,
the [Signature Source](DecompilerAnnotations.md#signature-source) also affects how they're treated by the Decompiler.
If the Signature Source is set to anything other than *DEFAULT*, there is a forced
one-to-one correspondence between variable annotations and actual parameters in the Decompiler's
view of the function.  This is stronger than just forcing the data-type; the existence or nonexistence of
the variable itself is forced by the annotation in this case.  If the Signature Source is forcing and
there are no parameter annotations, a *void* prototype is forced on the function.


A forcing Signature Source is set typically if debug symbols for the function are read in during
Program import (*IMPORTED*) or if the user manually edits the function prototype
directly (*USER_DEFINED*).


If an annotation and the Signature Source force a parameter to exist, specifying an
*undefined* data-type in the annotation still directs the Decompiler to fill in
the variable's data-type using type propagation.  The same holds true for the return value; an
*undefined* annotation fixes the size of the return value, but the Decompiler
fills in its own data-type.


> **Note:** The Decompiler may still use an undefined data-type to label a variable,
even after type propagation.  If a variable is simply copied around within a function and there
are no other substantive operations or annotations on the variable, the Decompiler may decide the undefined
data-type is appropriate.


### Variable Storage


Every variable annotation is associated with a single *storage location*, where the
value of the variable is stored during execution: generally a register, stack location, or an address
in the load image of the Program.  The storage location does not necessarily hold the value for that
variable at all points of execution, and it is possible for the variable value to be held in
*different* storage locations at different points of execution.  The set of execution
points where the storage location *does* hold the variable value is called the annotation
**scope**; this is distinct from, but influenced by, the scope of the
variable itself. The different types of storage location are listed below.


#### Load-image Address


A **load-image address** is a concrete address in the load image of the Program,
typically in the **ram** address space. This kind of
storage must be backed by a formal memory block for the Program, which typically corresponds to a specific
program section, such as the `.text` or `.bss` section.  Because it is in the
load image directly, an annotation with this storage shows up directly in any Listing
window and can be directly manipulated there. In much of the Ghidra documentation, these annotations
are referred to as **Data**. See the
[Data](../DataPlugin/Data.md) section, in particular.


Although specific architectures may vary, a storage location at a load image address generally
represents a formal *global* variable, and the annotation is in scope
across all Program execution. For the Decompiler, the storage location is treated as a
a single *persistent* variable in all functions that reference it. Within a
function, all distinct references (varnodes) to the storage location are merged. The Decompiler
expects a value at the storage location to exist from *before* the start of
the function, and any change to the value must be explicitly represented as an assignment to
the variable in Decompiler output.


#### Stack Address


A **stack address** is an address in the *stack frame*
of a particular function in the Program.  Formally, a stack address is defined as an offset relative to the
incoming value of the *stack pointer* and exists in the
**stack** address space associated with the function. See the discussion
in [Address Space](DecompilerConcepts.md#address-space). A **stack annotation** then is a variable annotation
with a stack address as its storage location. It exists only in the scope of a
single function and the variable must be *local* to that function.


Within a *Listing* window, a stack annotation is displayed as part of the function header
at the entry point address of the function, with a syntax similar to:


> undefined4 Stack[-0x14]:4 local_14


The middle field (the *Variable Location* field) indicates that the storage location is on the
stack, and the value in brackets indicates the offset of the storage location relative to the incoming
stack pointer. The value after the colon indicates the number of bytes in the storage location.


Currently, the entire body of the function is included
in the scope of any stack annotation, and the Decompiler will allow only a single variable to exist
at the stack address. A stack annotation can be a formal parameter to the function, but otherwise the
Decompiler does not expect to see a value that exists before the start of the function.


The Decompiler will continue to perform *copy propagation* and other transforms on
stack locations associated with a variable annotation. In particular, within Decompiler output,
if the value is simply copied to another location,
a specific write operation to a stack address may not show up as an explicit assignment to its variable.


#### Register


A variable annotation can refer to a specific *register* for the processor associated
with the Program. In general, such an annotation will be for a variable local to a particular function.
Within a *Listing* window, this annotation is displayed as part of the function header, with
syntax like:


> int EAX:4 iVar1


The *Variable Location* field displays the name of the particular register attached to
the annotation, and the value after the colon indicates the number of bytes in the register.


For local variable annotations with a register storage location, there is an expectation that the
register may be reused for different variables at different points of execution within the function.
There may be more than one annotation, for different variables, that share the same register
storage location.
An annotation is associated with a *first use point* that describes where
the register first holds a value for the particular variable (see the discussion - [Varnodes in the Decompiler](DecompilerConcepts.md#varnodes-in-the-decompiler)).
The entire scope of the annotation is limited to the address regions between the first use point
and any points where the value is read. The Decompiler may extend the scope as part of its
*merging* process, but the full extent is not stored in the annotation.


#### Temporary Register


Variable annotations can have a *temporary register* as a storage location.
A temporary register is not specific to a processor but is produced at various stages of
the decompilation process. See the discussion of the **unique**
space in [Address Space](DecompilerConcepts.md#address-space). These registers do not have a meaningful name, and
the specific storage address may change on successive decompilations. So, within a
*Listing* window, this annotation is displayed as part of the function header
with syntax like:


> int HASH:5f96367122:4 iVar2


The *Variable Location* field displays the internal hash used to uniquely
identify the temporary register within the data flow of the function.


A temporary register annotation must be for a local variable, and as with an ordinary register,
the annotation is associated with a *first use point* that describes
where the temporary register first holds a value for the variable.


## Function Prototypes


Every formal Function in Ghidra is associated with a set of variable annotations and other properties that
make up the **function prototype**. Due to the nature of reverse engineering,
the function prototype may include only partial information and may be built up over time. Individual
elements include:


> Input Parameters Each formal input to the function can have a Variable Annotation that describes its name, data-type,
and storage location. The storage location applies at the moment control flow enters the function.
If annotations exist, they are shown
in a Listing window as part of the Function header, and they usually correspond directly with symbols in the function declaration produced by the Decompiler. Return Value The value returned by a function can have a special Variable Annotation that describes its data-type
and storage location. The storage location applies at the moment control flow exits the function. If it exists, the annotation is shown
in a Listing window as part of the Function header with the name <RETURN> , and it usually
corresponds directly with the return value in the function declaration produced by
the Decompiler. Auto-Parameters Specific prototypes may require auto-parameters like this or __return_storage_ptr__ .  These are special input parameters
that compilers may use to implement specific high-level language concepts. See the discussion
in Auto-Parameters . Within Ghidra, auto-parameters are automatically created by the Function Editor Dialog if the desired prototype requires them.
Within a Listing window, auto-parameters look like other parameter annotations, but the storage field shows the
string (auto) .  Decompiler output will generally display auto-parameters as explicit variables
rather than hiding them. Calling Convention The calling convention used by the function is specified as part of the function prototype. The convention
is specified by name, referring to the formal Prototype Model that describes how storage
locations are selected for individual parameters along with other information about how the compiler treats
the function. Available models are determined by the processor and compiler, but may be extended by the user
(see Specification Extensions ). In the absence of input parameter and return value annotations, the Decompiler will use the prototype model as
part of its analysis to discover the input parameters and the return value of the function. The name unknown is reserved to indicate that nothing is known about the calling convention.  If
set to unknown , depending on context, the Decompiler may assign the calling convention based on
the Prototype Evaluation option (see Prototype Evaluation ), or it
may use the default calling convention for the architecture. Variable Arguments Functions have a boolean property called variable arguments , which can be turned on
if the function is capable of being passed a variable number of inputs.  This property informs the Decompiler that
the function may take additional parameters beyond any with an explicit variable annotation.
This affects decompilation of any function which calls the variable arguments function, allowing
the Decompiler to discover unlisted parameters at a given call site. No Return A function can be marked with the no return property, meaning that once
a call is made to the function, execution will never return to the caller. The Decompiler uses this to
compute the correct control flow in any calling functions. In-Line If the in-line property is turned on for a particular function,
it directs the Decompiler to inline the effects of the function into the decompilation of any of its calling functions.
The function will no longer appear as a direct function call in the decompilation, but all of its data flow
will be incorporated into the calling function. This is useful for bookkeeping functions, where it is important for the Decompiler to see its effects on the calling function.  Functions that set up the stack frame for a caller or
functions that look up or dispatch a switch destination are typical examples that should be marked in-line . Call-fixup This property is similar in spirit to marking a function as in-line .
A call-fixup directs the Decompiler to replace any call to the function with a specific
chunk of raw p-code.  The decompilation of any calling function no longer shows the function call, but the chunk
of p-code incorporates the called function's effects. Call-fixups are more flexible than just inlining a function.  The call-fixup chunk can be tailored to incorporate all of,
just a part of, or something different to the behavior of the function. Call-fixups are specified by name.  The name and associated p-code chunk are typically defined in the compiler specification for the Program. Users can extend the available set
of call-fixups (see Specification Extensions ).


### Signature Source


Ghidra records a **Signature Source** for every function,
indicating the origin of its prototype information.  This is
similar to the *Symbol Source* attached to Ghidra's symbol annotations
(see the documentation for
[Filtering](../SymbolTablePlugin/symbol_table.md#filtering)
in the Symbol Table).  The possible types are:


> DEFAULT - for basic or no information AI - for information that is produced with AI assistance ANALYSIS - for information derived by an Analyzer IMPORTED - for information imported from an external source USER_DEFINED - for information set by the user


Upon import of the Program, if there are debugging symbols available, Ghidra will build
annotations of the function's parameters and set the Symbol Source type to *IMPORTED*.
Otherwise, it will generally be set to *DEFAULT*.


However, Ghidra adjusts the Signature Source for a function if there is any change to the
prototype.  In particular, if the user adds, removes, or edits variable annotations
for the function's parameters or return value, Ghidra automatically converts the Signature
Source to be *USER_DEFINED*.


If the Signature Source is set to anything other than *DEFAULT*, the
function's prototype information is forcing on the Decompiler (see the discussion
in [Forcing Data-types](DecompilerAnnotations.md#forcing-data-types)).


### Discovering Parameters


The input parameter and return value annotations of the function prototype, like
any variable annotations, can be forcing on the Decompiler
(see the complete discussion in [Forcing Data-types](DecompilerAnnotations.md#forcing-data-types)).
But keep in mind:


> **Warning:** The input parameters and return value are all forced on the Decompiler as a unit based on the Signature Source . They are all forced if the type is set to anything
other than DEFAULT ; otherwise none of them are forced.


If the function prototype's annotations are not forcing, the Decompiler will attempt to discover the parameters
and return value using the calling convention.  The prototype model underlying the calling convention
dictates which storage locations can be considered as parameters and their formal ordering.


### Custom Storage


If there are parameter or return value annotations that do not agree with the calling convention that
has been set, the function prototype is said to be using **custom storage**.
Using the [Function Editor Dialog](../FunctionPlugin/Variables.md#edit-function)
for instance, any storage location can be specified as a parameter, and a completely custom prototype
can be built for the function.


The Decompiler will disregard the calling convention's rules in this situation and use the custom storage
locations for parameters and the return value.  Other aspects of the calling convention, like the
*unaffected* list, will still be used.


## Data Mutability


**Mutability** is a description of how values in a specific memory region,
either a single variable or a larger block, can change during Program execution based either on
properties or established rules.  Ghidra recognizes the mutability settings:


> Normal Constant - (read-only) Volatile


Mutability affects Decompiler analysis and can have a large impact on the output.


Most memory has **normal** mutability;
the value at the memory location may change over the course of executing the Program, but for a given
section of code, the value will not change unless an instruction explicitly writes to it.


Mutability can be set on an entire block of memory in the Program, typically from the
[Memory Map](../MemoryMapPlugin/Memory_Map.md#memory-map).
It can also be set as part of a single Variable Annotation.  From a Listing window, for instance,
use the [Settings](../DataPlugin/Data.md#data-settings) dialog.


### Read-only


The **constant** mutability setting indicates that values within
the memory region are read-only and don't change during Program execution.  If a read-only variable is
accessed in a function being analyzed by the Decompiler, its constant value, if present in the
Program's *load image*, replaces the variable within data flow for the
function.  The Decompiler may propagate the constant and fold it in to other operations, which
can have a substantial impact on the final output.


### Volatile


The **volatile** mutability setting indicates that values within
the memory region may change unexpectedly, even if the code currently executing does not directly
write to it.  Accessing a variable within a volatile region, either reading or writing, can have other
side-effects on the machine state, and it cannot in general be treated as normal variable.
If a volatile variable is accessed in a function being analyzed by the Decompiler,
each access is expressed as a copy statement on its own line, separated from other expressions,
so that the its position within the code and any sequence of accesses is clearly indicated.
Any access, either read or write, will always be displayed, even if the value is not directly
used by the function. The token representing the variable will be displayed using the
**Special** color, highlighting that the access is volatile
(See [Color for <token>](DecompilerOptions.md#displaytokencolor)).


```

	  X = SREG;              // Reading volatile SREG
	  DAT_mem_002b = 0x20;   // Writing volatile DAT

```


## Constant Annotations


Ghidra provides numerous actions to control how a specific constant is formatted or displayed.
An annotation can be applied directly to a constant in a Decompiler window, which always affects
Decompiler output. Or, an annotation can be applied to the constant operand of a specific machine
instruction displayed in a Listing window.  In this case, to the extent possible, the Decompiler
attempts to track the operand and apply the annotation to the matching constant in the Decompiler output.
However, the constant may be transformed from its value in the original machine instruction during the Decompiler's
analysis.  The Decompiler will follow the constant through one of the following simple transformations, but
otherwise the annotation will not be applied.


> Signed or zero extension Bitwise negation Integer negation - Two's complement Add or subtract 1


### Equates


Ghidra can create an association between a name and a constant, called an **equate**.
An equate is a descriptive string that is intended to replace the numeric form of the constant, and equates
across the entire Program can be viewed from the
[Equates Table](../EquatePlugin/Equates.md#view-equates).


An equate can be applied to a machine instruction with a constant
operand by using the [Set Equate](../EquatePlugin/Equates.md#set-equate)
menu from a Listing window. If the Decompiler successfully follows the operand to a matching constant,
the equate's name is displayed as part of the Decompiler's output as well as in any Listing window.
A transformed operand is displayed as an expression, where the transforming operation is applied to
the equate symbol representing the original constant.


Alternatively, an equate can be applied directly to a constant from a Decompiler window using its
[Set Equate...](DecompilerWindow.md#set-equate) menu.  The constant may or may not have a corresponding instruction
operand but will be displayed in Decompiler output using the descriptive string.


### Format Conversions


Ghidra can apply a **format conversion** to any integer constant that is displayed
in Decompiler output.


A conversion can be applied to the machine instruction containing the constant
as an operand using the [Convert](../EquatePlugin/Equates.md#convert) menu option
from a Listing window. If the Decompiler successfully traces the operand to a matching constant,
the format conversion is applied in the Decompiler output as well as in the Listing window.


Alternately, a conversion can be applied directly to an integer constant in a
Decompiler window using its [Convert](DecompilerWindow.md#convert) menu option. The constant may or may not
have a corresponding instruction operand but is displayed in Decompiler output using the conversion.


Conversions applied by the Decompiler are currently limited to:


> Binary - 0b01100001 Decimal - 97 Hexadecimal - 0x61 Octal - 0141 Char - 'a'


If necessary, a header matching the format is prepended to the representation string, either "0b", "0x" or just
"0".  A conversion will not switch the signedness of the constant; the signed or unsigned data-type associated
with the constant, as determined by analysis, is preserved.  If the constant is negative, with a signed data-type,
the representation string will always start with a '-' character.


## Register Values


A **register value** in this context is a region of code in the Program
where a specific register holds a known constant value.  Ghidra maintains an explicit list of these values for
the Program (see the documentation for [Register Values](../RegisterPlugin/Registers.md)),
which the Decompiler can use when analyzing a function.
A register value benefits Decompiler analysis, especially if the original compiler was aware
of the constant value, as the Decompiler can recover address references calculated as offsets relative to the register
and otherwise propagate the constant.


A *register value* is set by highlighting the region of code in a Listing window and then invoking the
[Set Register Values...](../RegisterPlugin/Registers.md#setting-register-values-over-address-ranges) command
from the pop-up menu.  The beginning and end of a region is indicated in a Listing window with
`assume` directives, and regions can be generally viewed from the
[Register Manager](../RegisterPlugin/Registers.md#register-manager) window.


In order for a particular register value to affect decompilation, the region of code associated with the
value must contain the entry point of the function, and of course the function must read from the register.
Only the initial reads of the register are replaced with the constant value.
The Decompiler will continue to respect later instructions that write to the register, even if the
instruction is inside the register value's region.
If a register value's region starts in the middle of a function, decompilation is *not*
affected at all.


### Context Registers


There is a special class of registers called **context registers** whose
values have a different affect on analysis and decompilation than described above.


> **Tip:** Context registers are inputs to the disassembly decoding process and directly affect which
machine instructions are created.


The value in a context register is examined when Ghidra decodes machine instructions from the underlying
bytes in the Program. A specific value generally corresponds to a specific *execution mode*
of the processor. The ARM processor *T bit*, for instance, which selects whether the
processor is executing ARM or THUMB instructions, is modeled as a context register in Ghidra.
The same set of bytes in the Program can be decoded to machine instructions in more than one way,
depending on context register values.


Bytes are typically decoded once using context register values
established at the time of disassembly. From Ghidra's more static view of execution, a context register holds
only a single value at any point in the code, but the same context register can hold different values for
different regions of code. Setting a new value on a region of the Program will affect any subsequent disassembly
of code within that region.


If a context register value is changed for a region that has already been disassembled, in order to see
the affect of the change, the machine instructions in the region need to be cleared, and disassembly needs
to be triggered again (see the documentation on the
[Clear Plugin](../ClearPlugin/Clear.md#clear)).


Values for a context register are set in the same way as for any other register, using the
[Set Register Values...](../RegisterPlugin/Registers.md#setting-register-values-over-address-ranges) command
described above.  Within the
[Register Manager](../RegisterPlugin/Registers.md#register-manager) window,
context registers are generally grouped together under the *contextreg* pseudo-register heading.
For details about how context registers are used in processor modeling, see
the document "SLEIGH: A Language for Rapid Processor Specification."


Because context registers affect machine instructions, they also affect the underlying p-code and
have a substantial impact on decompilation.  Although details vary by processor, context register
values are typically established during the initial import and analysis of a Program and aren't changed
frequently.


---

[← Previous: Constant Annotations](DecompilerAnnotations.md) | [Next: Decompiler Options →](DecompilerOptions.md)
