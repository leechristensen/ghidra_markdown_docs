[Home](../index.md) > [DecompilePlugin](index.md) > SLEIGH Specification Files

# Decompiler Concepts


## P-code


P-code is Ghidra's Intermediate Representation (IR) language. When analyzing a function,
the Decompiler translates every machine instruction into p-code first and performs its
analysis directly on the operators and variables of the language. Output of the Decompiler
is also best understood in terms of p-code. This section presents the key concepts of
p-code. For a more detailed discussion see the document "P-Code Reference Manual."


### Address Space


P-code defines all data in terms of an address space. An **address space**
is defined simply as an indexed sequence of bytes that can be read and written by p-code operations.
For a specific byte, the unique index that labels it is called the byte's **address**.
Each address space has a:


> name - a formal name for the space size - the maximum number of bytes that can be addressed endianness - how groups of bytes are interpreted as integers


For a p-code model of a specific processor, all elements of the processor state (including RAM, registers,
flags, etc.) must be contained in some address space. The model will define multiple address spaces
to accomplish this, and beyond the raw translation of machine instructions to p-code, the Decompiler
can add additional spaces. Address space definitions that are common across many different processors include:


> ram A space that models memory accessible via the processor's main data bus. Depending on
the architecture, different spaces might be substituted for ram ,
such as separate code and data spaces. register A space that models the processor's general purpose registers.  Ghidra still uses
the standard names to refer to registers for the processor, but internally each register maps to a
specific address in this space. unique A space dedicated to temporary registers.
It is used to hold intermediate values when modeling instruction behavior, and the Decompiler
uses it to allocate space for variables that don't directly correspond to the low level
processor state.  The name unique is reserved for this purpose and
is present in all processor models. stack A space that represents bytes explicitly indexed through a stack pointer .
This is an example of an address space added by the Decompiler beyond what the raw processor
model defines.  The stack space is a logical construction representing the set of bytes a
single function might access through its stack pointer.  Each stack address represents
the offset of a byte in some underlying space (usually ram ) relative
to the initial value of the stack pointer upon entry to the function. The stack space is
always referenced in the context of a single function, and in this sense, each function
can be viewed as having its own distinct stack space. constant A special space for encoding constants in p-code.
For complete generality, even constants that the processor might manipulate are
assigned to their own address space.  For an address in the constant
space, the index itself represents the constant.


### Varnodes


A **varnode** is defined as a sequence of bytes in
an address space.  It represents the storage for a single value (variable) being
acted on by the processor.
All manipulation of data by p-code operations occurs on varnodes.
A varnode can always be represented as the formal triple:


> (address space,offset,size)


Both *offset* and *size* are integer values
specified in terms of bytes.
The first two elements, address space and offset, taken together represent the
*address* of the varnode.


Varnodes by themselves do not necessarily have a data-type associated with them.
The Decompiler ultimately assigns a formal data-type, but at the lowest level of p-code,
varnodes inherit one the building block data-types from the p-code operations that
act on them:


> Integer Boolean Floating Point


The integer data-type assumes a two's complement encoding in the endianness of the
address space containing the varnode.  Similarly, the floating point data-type assumes
an IEEE 754 standard encoding.  The precision of the integer or floating point value is
determined by the varnode's size.  A boolean data-type assumes the varnode has a size
of 1 byte and takes either a value of 0, for *false*, or a value of
1 for *true*.


### P-code Operations


A **p-code operation** is defined as a formal operator,
labeled by its *opcode*, acting on 1 or more varnodes as input and
storing a result in at most 1 varnode. Each p-code operation is associated with an
address, which is usually the address of the machine instruction from which the p-code
operation was translated. As most instructions require more than one p-code operation
to fully model it, a separate 1-up counter is used to distinguish p-code operations
associated with the same address. Together the address and the counter are referred
to as the operation's **sequence number**.


The formal opcodes break up into categories similar to many programming languages.


> Category Operations Data Moving COPY, LOAD, STORE Integer Arithmetic INT_ADD, INT_SUB,
INT_2COMP, INT_MULT, INT_DIV, INT_SDIV, INT_REM, INT_SREM Integer Shifts INT_LEFT, INT_RIGHT, INT_SRIGHT Integer Comparison INT_EQUAL, INT_NOTEQUAL, INT_SLESS, INT_SLESSEQUAL, INT_LESS, INT_LESSEQUAL Logical INT_NEGATE, INT_XOR, INT_AND, INT_OR, POPCOUNT Boolean BOOL_NEGATE, BOOL_XOR, BOOL_AND, BOOL_OR Floating Point Arithmetic FLOAT_ADD, FLOAT_SUB, FLOAT_MULT, FLOAT_DIV, FLOAT_NEG,
FLOAT_ABS, FLOAT_SQRT Floating Point Comparison FLOAT_EQUAL, FLOAT_NOTEQUAL, FLOAT_LESS, FLOAT_LESSEQUAL Floating Point Conversion INT2FLOAT, FLOAT2FLOAT, TRUNC, CEIL, FLOOR, ROUND Branching BRANCH, CBRANCH, BRANCHIND, CALL, CALLIND, RETURN Extension/Truncation INT_ZEXT, INT_SEXT, PIECE, SUBPIECE Overflow Tests INT_CARRY, INT_SCARRY, INT_SBORROW, FLOAT_NAN Managed Code CPOOLREF, NEW


#### Operator Tokens


Most opcodes naturally correspond to a particular C operator token,
and in Decompiler output, many of the operator tokens displayed correspond
directly to a p-code operation present in the Decompiler's internal
representation.  The biggest exception are the *Branching*
operations; the Decompiler uses standard high-level language control-flow
structures, like *if/else*, *switch*, and
*do/while* blocks, instead of the
low-level branching operations. But even here, there is some correspondence
between operations and keywords in the high-level language.


Operations in the *Extension/Truncation* and
*Floating Point Conversion* categories tend to be
represented as *cast* operations in the high-level language,
and so don't have an explicit operator token representing them.  Many p-code
operations share the same operator token, such as the integer and floating-point
addition operations **INT_ADD** and
**FLOAT_ADD**. The high-level language distinguishes
between them via the underlying data-type of the variables.


> Name Operator Token Description COPY = Copy one varnode into another. LOAD * or -> Dereference a pointer, or load a value from memory. STORE * or -> Store a value to memory, through a pointer. BRANCH goto Branch execution to a specific address. CBRANCH if (...) goto Branch execution to an address if the condition is true. BRANCHIND switch(...) Branch execution to a computed address. CALL funcname(...) Branch to a function, as a call. CALLIND (*funcptr)(...) Branch through a pointer to a function, as a call. RETURN return Return execution to the calling function. PIECE CONCAT Concatenate two varnodes. SUBPIECE SUB Extract a subset of bytes. POPCOUNT POPCOUNT Count the 1 bits. INT_EQUAL == True if input varnodes are equal. INT_NOTEQUAL != True if input varnodes are not equal. INT_LESS < or > True if one varnode is less than the other as unsigned integers. INT_SLESS < or > True if one varnode is less than the other as signed integers. INT_LESSEQUAL <= or >= True if one varnode is less than or equal to the other as unsigned integers. INT_SLESSEQUAL <= or >= True if one varnode is less than or equal to the other as signed integers. INT_ZEXT ZEXT Zero extension. INT_SEXT SEXT Signed extension. INT_ADD + Add as integers. INT_SUB - Subtract as integers. INT_CARRY CARRY True if adding produces an unsigned carry. INT_SCARRY SCARRY True if adding produces a signed carry. INT_SBORROW SBORROW True if subtracting produces a signed borrow. INT_2COMP - Two's complement. INT_NEGATE ~ Bitwise negation. INT_XOR ^ Bitwise exclusive-or. INT_AND & Bitwise logical-and. INT_OR | Bitwise logical-or. INT_LEFT << Left shift. INT_RIGHT >> Unsigned (logical) right shift. INT_SRIGHT >> Signed (arithmetic) right shift. INT_MULT * Integer multiplication. INT_DIV / Unsigned integer division. INT_REM % Unsigned remainder. INT_SDIV / Signed division. INT_SREM % Signed remainder. BOOL_NEGATE ! Boolean negation. BOOL_XOR ^^ Boolean exclusive-or. BOOL_AND && Boolean logical-and. BOOL_OR || Boolean logical-or. FLOAT_EQUAL == True if inputs are equal as floating-point numbers. FLOAT_NOTEQUAL != True if inputs are not equal as floating-point numbers. FLOAT_LESS < or > True if one input is less than the other as floating-point numbers. FLOAT_LESSEQUAL <= or >= True if one input is less than or equal to the other as floating-point numbers. FLOAT_ADD + Add as floating-point numbers. FLOAT_SUB - Subtract as floating-point numbers. FLOAT_MULT * Multiply as floating-point numbers. FLOAT_DIV / Divide as floating-point numbers. FLOAT_NEG - Negate a floating-point number. FLOAT_ABS ABS Absolute value of a floating-point number. FLOAT_SQRT SQRT Square root of a floating-point number. FLOAT_CEIL CEIL Ceiling function. FLOAT_FLOOR FLOOR Floor function. FLOAT_ROUND ROUND Nearest integral value. FLOAT_NAN NAN True if input is not a valid floating-point number (NaN). INT2FLOAT <na> Convert integer to floating-point. FLOAT2FLOAT <na> Convert between different floating-point precisions. TRUNC <na> Convert floating-point to integer. CPOOLREF <na> Obtain constant pool value. NEW new Allocate an object or an array of objects. MULTIEQUAL <na> Compiler phi-node: merge values from multiple control-flow paths. INDIRECT <na> Indirect effect on a varnode. CAST <na> Copy a value, changing its data-type. PTRADD + Add an offset to a pointer. PTRSUB . or -> Dereference a subfield from a pointer. INSERT <na> Insert a bit-range. EXTRACT <na> Extract a bit-range.


#### P-code Control Flow


P-code has natural **control flow**, with the subtlety that flow
happens both within and across machine instructions.  Most p-code operators have
**fall-through** semantics, meaning that flow moves to the
next operator in the sequence associated with the instruction, or, if the operator is the
last in the sequence, flow moves to the first operator in the p-code associated with the next instruction.
The p-code operators with **branching** semantics, such as
CBRANCH and BRANCH, can jump to a target operator which is internal to the current instruction, or they can
jump to the first p-code operator corresponding to a new instruction at a different address.


Ghidra labels a machine instruction with one of the following **Flow Types** that describe
its overall control flow.  The Flow Type is derived directly from the control flow of the p-code for the instruction,
with the basic types corresponding directly with a specific branching p-code operator.


> FALL_THROUGH UNCONDITIONAL_CALL - CALL UNCONDITIONAL_JUMP - BRANCH CONDITIONAL_JUMP - CBRANCH COMPUTED_JUMP - BRANCHIND COMPUTED_CALL - CALLIND TERMINATOR - RETURN


Other Flow Types occur due to a combination of multiple p-code branching operators within the same instruction.


> CONDITIONAL_CALL - CALL with CBRANCH CONDITIONAL_TERMINATOR - RETURN with CBRANCH COMPUTED_CALL_TERMINATOR - CALLIND with RETURN CONDITIONAL_COMPUTED_JUMP - CBRANCH with BRANCHIND CONDITIONAL_COMPUTED_CALL - CBRANCH with CALLIND JUMP_TERMINATOR - BRANCH with RETURN


#### User-defined P-code Operations - CALLOTHER


P-code allows for additional, processor specific, operations referred to
as *user-defined* or CALLOTHER operations.
These may be defined as part of a Ghidra's specification for the processor and
are typically used as placeholders for what is otherwise unmodeled processor behavior.
Each CALLOTHER must have a unique name, and as a p-code operation, it still takes
varnode inputs and may produce a varnode output. But the exact affect of the operation is
not specified.


The Decompiler treats a CALLOTHER operation as a black box. It will keep track of data
flowing into and out of the operation but won't simplify or transform it. In Decompiler
output, a CALLOTHER is usually displayed using its unique name, with functional syntax
showing its inputs and output.


Ghidra or a user can provide the behavior details for a named CALLOTHER operation.  The
details are provided as a sequence of p-code operations, referred to as a
**Callother-Fixup**, which is substituted for the
CALLOTHER operation during decompilation, or by other Analyzers that use p-code.
Callother-Fixups are applied by Ghidra for specific processor or compiler variants,
and a user can choose to apply them to an individual Program (see [Specification Extensions](DecompilerOptions.md#specification-extensions)).


#### Internal Decompiler Functions


Certain p-code operations can show up in Decompiler output that cannot be represented
as either an operator token, a cast operation, or other depiction that is natural to
the language.  The Decompiler generally tries to eliminate these, but this isn't always
possible. The Decompiler resorts to a functional syntax for these kinds
of p-code operations, displaying them as if they were built-in functions for the language.


```

	    SUB42(0xaabbccdd,1) = 0xbbcc

```


## The HighFunction


A **HighFunction** is the collection of specific information
produced by the Decompiler about a function, referring to the root class in the Ghidra
source which holds this information.
The HighFunction is made up of the following explicit objects:


> A control-flow representation of the function
in terms of basic blocks . A data-flow representation of the function
in terms of varnodes and p-code operations . A symbol-table of variables accessed by the function.


The Decompiler's output provides a standalone view of the function which is distinct
from any annotations about the function that are present in the Program database
and displayed in the Listing (although the output may be informed by these annotations).
The terms *HighFunction*, *HighVariable*, and
*HighSymbol* refer to this Decompiler specific view of the function.


### HighSymbol


A **HighSymbol** is one of the explicit symbols recovered by the
Decompiler.  It is made up of a name and data-type and can describe either:


> a formal parameter of the function, a local variable of the function, or a global variable accessed by the function.


An important aspect of HighSymbols is that they are distinct from
the standard Ghidra symbols stored in the Program database and are part of
the Decompiler's separate view of the function. When the Decompiler displays
declarations for symbols in its output for instance, it is displaying
HighSymbols, which may not directly match up with database symbols.
The Decompiler is generally
*informed* by annotations in the database and may
copy specific symbols from the database into its view, but it is
generally free to invent new symbols discovered during its analysis.


Various actions within Ghidra allow the user to *commit*
specific HighSymbols to the database as a permanent annotation, but this
does not happen by default.


### Varnodes in the Decompiler


Varnodes are the central *variable* concept for the Decompiler.
They form the individual nodes in the Decompiler's data-flow representation
of functions and are used during all stages of analysis.  During the initial stages
of analysis, varnodes simply represent specific storage locations that are accessed
in sequence by individual p-code operations. The Decompiler immediately converts
the p-code into a graph-based data-flow representation, called Static Single
Assignment (SSA) form.  In this form, the varnodes take on some additional attributes.


In SSA form, each write of an operation to a storage location defines a new varnode.
Write operations at different points in the code to the same storage location, still
produce different varnodes.  In this context, each varnode has a *lifetime*
or *scope* within the function. The scope starts at:


> The defining p-code operation which has the
varnode as its output. Or The beginning of the function, if the varnode is an input to the function.


The scope extends via control flow to each p-code operation that *reads* the
specific varnode as an operand.  The value of the varnode between the defining p-code operation
and the reading operations does not change. The scope of a varnode can be thought of as a set
of addresses within the function's body connected by control flow.  The address of the defining
p-code operation is referred to as the varnode's **first use point**
or **first use offset**.


In the Decompiler output for a specific high-level language like C or Java,
a varnode still has a *scope* and represents a variable
in the high-level language only across this connected region of the code.
A set of varnodes, with disjoint scopes, provides a complete
description of a high-level variable that can be written to at more than one point
in the function.


### HighVariable


A **HighVariable** is a set varnodes that, taken
together, represent the storage of an entire variable in the high-level language
being output by the Decompiler.  Each varnode describes where the variable's
value is stored across some section of code.


There is generally a one-to-one correspondence between HighVariables and
HighSymbols. HighVariables can be thought of as the detailed storage description
of the high-level variable, while the HighSymbol provides its name and data-type.
However, there are some technical caveats to this correspondence to keep in mind.


A HighVariable always describes *explicit* manipulation of
data by instructions in the function.  In some cases, a HighVariable may only describe part
of the storage for a HighSymbol. Particularly for structured or composite data-types, a
function may operate on different parts of the variable at different points of the code,
so a HighVariable may only encompass one field of the structure.


A symbol may be referenced in a function, but the symbol's value may not be explicitly
manipulated.  Constant pointers may refer to variables either
on the stack or in main memory, but the variable's value is neither read nor written
within the function. In this case, the HighSymbol exists, but there
is no corresponding HighVariable.


#### Merging


**Merging** is the part of the analysis process where
the Decompiler decides what varnodes get grouped together to create the final
HighVariables in the output.  Each varnode's scope (see the discussion in
[Varnodes in the Decompiler](DecompilerConcepts.md#varnodes-in-the-decompiler)) provides the fundamental restriction on this process.
Two varnodes cannot be merged if their scopes intersect.  But this leaves a lot of
leeway in what varnodes *can* be merged.


Certain varnodes must be merged; if they use the same storage but in different
control-flow paths that come together, for instance, or if it is explicitly
known that the varnodes must represent the same variable.  This is referred
to as **forced merging**.


The Decompiler may also merge varnodes that could just as easily exist as separate
variables.  This is called **speculative merging**.
In addition to the intersection condition on varnode scopes, the Decompiler only
speculatively merges variables that share the same data-type. Beyond this, the Decompiler
prioritizes variable pairs that are read and written within the same instruction and
then pairs that are *near* each other in the control flow of the function.
To a limited extent, users are able to control this kind of merging
(see [Split Out As New Variable](DecompilerWindow.md#split-out-as-new-variable)).


### Prototype Model


Functions in high-level languages manipulate symbols like parameters and return values that
are implicitly stored in a way that doesn't collide with other functions and variables.  To
actually map these symbols to physical registers and memory locations, compilers establish a
*calling convention* for the function.
Loosely, this is a set of memory resources, whether it is registers or stack locations,
and a procedure for sequentially assigning resources to parameters based on their properties.
A **prototype model** is the formal object in Ghidra that represents
a calling convention and holds its specific rules and resource details.


Prototype models are architecture-specific, and depending on the compiler, a single Program may make
use of multiple models.  Subsequently, each distinct model has a name like **__stdcall** or
**__thiscall**. The Decompiler makes use of the prototype model, as assigned to the function by the user or
discovered in some other way, when performing its analysis of parameters.
It is possible for users to extend the set of prototype models available to a Program
(see [Specification Extensions](DecompilerOptions.md#specification-extensions)).


A prototype model is typically used as a whole and is assigned by name to individual functions.  But some of
the sub-concepts of the model may be relevant to reverse engineers. Concepts that a prototype
model encapsulates include:


#### Incoming and Outgoing Storage Locations


A formal input parameter is always assigned a specific memory location to hold its value coming into the function.
The storage location can be a register, a stack location, or other memory location.  The storage
location may be reused later by other variables in the function; only the incoming value stored there is guaranteed
to be that of input parameter.


If the parameter
is stored on the stack, the storage location is viewed as a constant offset in the **stack**
space, where the offset is relative to the incoming value of *stack pointer*
(see the discussion in [Address Space](DecompilerConcepts.md#address-space)).


The *return value* for the function, unless it is passed back on the stack, is also stored at a single
memory location.  It is guaranteed to be at that location only at points where the function is exited.  There may be multiple exit
points, but they all share the same return value storage location.  For return values passed back on the stack, compilers
generally implement a special input register to hold the location where the value will be stored.  See the
discussion of [Auto-Parameters](DecompilerConcepts.md#auto-parameters) and the **__return_storage_ptr__** below.


#### Auto-Parameters


Compiled binaries may pass values as parameters between functions that aren't in the formal
list of parameters as defined by the original source code for the program. These are referred to
as **auto-parameters** or sometimes **hidden**
parameters within the documentation. If the prototype model requires it, Ghidra will automatically
create an auto-parameter for a function to honor a user's request for a specific formal signature.
See [Function Editor Dialog](../FunctionPlugin/Variables.md#edit-function).
Because reverse engineers need to see them, the
Decompiler will generally display auto-parameters explicitly in function prototypes as part of its output, even though
they would not be present in the original source.
Ghidra explicitly defines two auto-parameters:


> this Within Object Oriented languages, a function defined as a class method often has a this parameter pointing to an instantiation of the
class' structure data-type.  Within Ghidra, functions with the __thiscall calling convention are automatically assigned a this parameter.
If the function is part of a class namespace and the class has an associated structure, the this parameter will be a pointer to the structure, otherwise
it will be a pointer to the void data-type. __return_storage_ptr__ Most calling conventions allow the value returned by a function, if it is large enough, to be passed back
on the stack instead of in a register. This is usually implemented by having the calling function
pass an additional input parameter that holds a pointer to the location on
the stack where the return value should be stored.  Ghidra labels this special parameter as __return_storage_ptr__ , which will be a pointer to the
data-type of the return value.


#### Unaffected


Prototype models can specify a set of **unaffected** memory locations,
whose value must be *preserved* across the function. I.e. each location
must hold the same value at a function's exit that it held coming into the function.
These encompass a calling convention's *saved registers*, where a calling function
can store values it doesn't want to change unexpectedly, but also may include other registers that are
known not to change, like the stack pointer.
The Decompiler uses the information to determine which locations can be safely propagated across
a called function.


#### Killed by Call


In contrast to *unaffected* memory locations, a prototype model may specify
**killed by call** locations that are guaranteed *not*
to be used to hold a value across the function.


## SLEIGH Specification Files


SLEIGH is Ghidra's specification language for describing processor instructions.
Specification files are read in for a Program, and once configured, Ghidra's SLEIGH engine can:


> Disassemble machine instructions from the underlying bytes and Produce the raw p-code consumed by the Decompiler and other analyzers.


Specification files are selected based on the *Language Id*
assigned to the Program at the time it is imported into Ghidra
(see [Import Program](../ImporterPlugin/importer.md)).


> x86:LE:32:default:windows AARCH64:LE:64:default:v8A:default MIPS:BE:32:micro:default


A **Language Id** is a label with these 5 formal fields, separated
by a ':' character:


> Processor family Endianness Size of the address bus Processor variant Compiler producing the Program


A field with the value **default** indicates either the preferred processor variant or the preferred compiler.


Within the Ghidra installation, specification files are stored based on the overarching
processor family, such as **MIPS** or
**x86**.  For a specific family, files are located under


> <Root>/Ghidra/Processors/<Family>/data/languages


where `<Root>` represents the root directory of the Ghidra installation and
`<Family>` is the processor family.


There are several types of specification files that are distinguishable by their suffix.
These include:


> SLEIGH files - *.slaspec or *.sinc These are the human readable SLEIGH language files. A single specification is
rooted in one of the *.slaspec files, which may recursively include
one or more *.sinc files.  The format of these files is described
in the document "SLEIGH: A Language for Rapid Processor Specification." Compiled SLEIGH files - *.sla This is a compiled form of a single SLEIGH specification.  It is produced
automatically by Ghidra from the corresponding *.slaspec . Compiler specification files - *.cspec These files contain configuration for a specific compiler.  Analysis of Programs whose
executable content was produced using this compiler benefits from this information.
The file is an XML document with tags describing details of data organization and
other conventions used by the compiler.  In particular, the compiler specification
contains tags: <prototype> - describing a specific calling convention <callfixup> - describing a Call-fixup <callotherfixup> - describing a Callother-fixup Processor specification files - *.pspec These files contain configuration information that is specific to a particular
processor variant.


### Modifying Specification Files


Changing any of the specification files described here is not recommended.
To make additions to either the *compiler specification*
or the *processor specification* files, see
[Specification Extensions](DecompilerOptions.md#specification-extensions), which describes a safe and portable way
to add specific elements.


> **Warning:** Making modifications to specification files within a Ghidra installation is possible,
but any analysis results obtained will likely not be portable to other installations.
In particular, saving a Program from a modified Ghidra and then reopening it using
an unmodified installation may corrupt the Program database.


When Ghidra starts, it checks for changes to `*.slaspec`
and `*.sinc` files and will rebuild the corresponding
`*.sla` file automatically.  Also, specification files are read again when
Ghidra restarts. So analysts can and do make changes to these files.
However they need to be prepared to view any results as temporary and
should backup their installation and specific Programs being analyzed.


---

[← Previous: The HighFunction](DecompilerConcepts.md) | [Next: Program Annotations Affecting the Decompiler →](DecompilerAnnotations.md)
