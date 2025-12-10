[Home](../index.md) > [Glossary](index.md) > Glossary

# Ghidra Glossary


[A](#a)  [B](#b)  [C](#c)  [D](#d)  [E](#e)  [F](#f)  [G](#g)  [H](#h)  [I](#i)  J  [K](#k)  [L](#l)  [M](#m)  [N](#n)  [O](#o)  [P](#p)  Q  [R](#r)  [S](#s)  [T](#t)  [U](#u)  [V](#v)  [W](#w)  [X](#x)  Y  Z


**A**


## Action


An operation the user can perform in Ghidra. All menu items, keybindings, and toolbar
buttons are actions.


## Address


A number that identifies a specific location in memory.


## Address Range


A sequential set of addresses within a single Address Space identified by a minimum and
maximum address.


## Address Set


A collection of Addresses.


## Address Space


The set of all legal addresses in memory for a given processor.  The nature of each
address space is defined by the processor and language implementation.


## Address Table


Two or more consecutive addresses in memory.


## Analyzer


A software module that examines and annotates the code in a program to help reveal the
behavior of that program. Examples are disassembly, function generation, and stack
analysis.


## Archive


See [Data Archive](#dynamic-data-type).


See [Project Archive](#project-archive).


## Assembly Language


Programming language closely associated with an individual processor.


## Auto Analysis


Automated way to run all the analyzers in the appropriate order (Example: function
creation before stack analysis).


## B


## Back Reference


Another name for the [Source Address](#source-address) in a reference.


## Background Task


Any action that runs in the background allowing the user to perform other tasks.


## Base Address


An address from which other addresses are derived using offsets.


## Basic Block


A sequence of instructions that has no flow into or out of the sequence except for the
top and bottom (i.e., no branching).


## Basic Block Model


A [Block Model](../BlockModel/Block_Model.md) which partitions code
into small runs of instructions based on points where instruction flow changes.  Jump,
Call, and Branch instructions will cause the execution flow to change.  Arithmetic and
store/load instructions do not break a Basic Block because they do not change the
execution.  A label will also end one block and begin another.


## Binary Data


Bytes that make up a program.


## Big Endian


Byte order for storage such that the high-order byte is at the starting address, as
shown in the figure below, where increasing memory addresses are going from left to
right.


| ![](images/BigEndian.png) |
| --- |


## Block Model


A model which partitions the code into address ranges based on some set of rules.
The most obvious model partitions the code into subroutines.


## Bookmark


Marker used to designate frequently-visited or important locations.


## Bookmark Type


Attaches meaning to a bookmark to indicate its use. Example: Note, Info, Analysis,
etc.


## Browser Field


Individual program elements displayed by the Code Browser's listing window.


## Byte Viewer


A Ghidra component used to display and edit the bytes in a program.


**C**


## Call Block Model


See [Subroutine Model](#subroutine-model).


## Call Graph


Graph displaying the relationships between "function calls" in a program.


## Calling Convention


Determines how a function receives arguments and returns results. The available calling
conventions are currently determined by the program's language specification.


## Check-In


The process of contributing and merging changes from a "checked-out" program to the
globally shared version of the program.


## Check-Out


The process of retrieving the latest version of a shared program for the purpose of
making changes.


## Classpath


Path to search for Ghidra java code.


## Clear


Process of removing information from a program (Example: symbols, comments, everything,
etc).


## **Code Browser**


A [Default
Ghidra tool](#default-ghidra-tool) for displaying and working with program listings.


## Code Block


See [Basic Block](#basic-block)


## Code Unit


An [Instruction](#instruction) or [Data Item](#data-item) in the
listing.


## Computed Call


Call instruction whose destination is dynamically computed.


## Conditional Call


A call instruction that is executed conditionally.


## Conditional Jump


A jump instruction that is executed conditionally.


## Connecting Tools


Process of coordinating two or more [Tools](#tool) with respect to navigation and selection.


## Context Sensitive Menu


Menu that changes depending on cursor location.  In other words, only actions which
are appropriate for the type of information on which the cursor resides are available from
the menu.


## Contrib Plugins


Term used to indicate user-contributed plugins.


## Core Plugins


Term applied to plugins that are supported by the Ghidra team.


## Cycle Group


A sequence of data types applied using the same action repeatedly (i.e.
byte-&gt;word-&gt;dword-&gt;qword).


**D**


## Data (item)


Bytes in the program's memory that are not interpreted as instructions.


## Data Type Archive


File used to store user-defined data types independent of a specific program.


## Data Component


A data item inside a structure or array.


## Data Type


A generalization of data which uniquely defines its specific attributes such as size,
structure and  format. Example: byte, float, double.


## Dead Code


Unreachable code.


## Decompiler


Ghidra module for translating assembly language to C.


## Default Ghidra Tool


1    A pre-configured
CodeBrowser [Tool](#tool) that is ready to use when Ghidra is installed.


2    The tool that has been designated to run when you double click on a
program in the Project Window.


## Destination Address


The "To" address in a reference "From-To" address pair.  An address that is
referred "To" by an instruction operand or pointer.


## Diff


See [Program Diff](#program-diff).


## Direct References


Locations in memory where the bytes make up the address of the current location in the
browser.  See [Search for
Direct References](../Search/Search_for_DirectReferences.md).


## Disassemble


The process of interpreting program bytes as assembly instructions.


## Disassemble, Restricted


The Ghidra disassembly mode where disassembly is restricted to the current
selection.


## Disassemble, Static


The Ghidra disassembly mode where code flows are not followed and only bytes at the
current location or selection are disassembled.


## DLL


Abbreviation for Dynamic Link Library.  A shared library on a Windows platform.


## Docking Window Component


Ghidra user interface component that can be positioned and sized by the user.


## DWord


A 4-byte integer data type.


## Dynamic Data Type


Data types whose structure varies depending on the data bytes on which they are
applied.


**E**


## ELF


Abbreviation for Executable Linking Format.  File format used by Unix and Linux
operating systems for storing executable programs.


## End of Line (EOL) Comment


Comments that are displayed to the right of the instruction.


## Endian


Byte ordering.  See [Big Endian](#big-endian), [Little Endian](#little-endian).


## Entry Point


Location in a program where execution begins.


## Enum Data Type


Ghidra data type for modeling C-type enums.


## Equate


A string substitution for numeric values appearing in instruction operands.


## Exporter


Ghidra module for storing program information in various file formats (XML, HTML, ASCII,
etc).


## External Reference


A reference from a location in one program to a location in another program.


**F**


## Fall Through Address


The address of the next sequential instruction to be executed.


## Favorite Data Type


Ghidra data types that can be accessed via the popup-menu.


## Flow


A.K.A. Instruction Flow or Control Flow.  This the sequence of instructions that
are executed as a program runs, including branching and fall-through.


## Flow Graph


Graph that shows basic instruction flow.


## Forward Refs


Another name for the [Destination Address](#destination-address) in a
reference.


## Fragment


A set of addresses used by the [Program Tree](#program-tree) to organize
code.


## Front End


See [Ghidra Project Window](#ghidra-project-window).


## Function


A program element that is referenced via a call instruction.  A [function](../FunctionPlugin/Functions.md) has an entry point, a body of
instructions, a return data type, and optionally parameters, local variables, and local
register variables.


## Function Signature


The name, return type, and parameters of a function.


**G**


## Ghidra


Ghidra is a java-based framework for reverse engineering.  It provides built-in
capabilities for reverse engineering along with support for user-provided
plugins.


## Ghidra File


Any file that is part of a [Ghidra Project](#ghidra-project).


## Ghidra Program File


Ghidra files containing information about a program.


## Ghidra Project


Ghidra organizes work into projects. All work is performed in the context of a
project.


## Ghidra Project Window


The main Ghidra interface for managing [program files](#program).


## Global Namespace


Symbols that are not in any specific namespace are said to be in the "global" namespace.
The global namespace is the default namespace.


## gzf


File extension given to Ghidra program database files that have been "zipped up".


**H**


## Hex Short


A display format in the [Byte Viewer](#byte-viewer) used to display short
values in hex.


## Hex Integer


A display format in the [Byte Viewer](#byte-viewer) used to display integer
values in hex.


## Hex Long


A display format in the [Byte Viewer](#byte-viewer) used to display long
values in hex.


## Hex Long Long


A display format in the [Byte Viewer](#byte-viewer) used to display longlong
values in hex.


## Hijacked File


A local program file in a project that is "hiding" a shared program with the same name.
Users cannot access the shared program until the local file is removed.


## Highlight


A more permanent type of selection.


## History


List of changes made to labels or comments.


**I**


## IDA Pro


A commercially available reverse engineering
tool.


## Importer


Reads a file (.xml, .dll, .so, etc), and converts its contents into a Ghidra
program.  Ghidra contains multiple importers (corresponding to a specific set of
formats).  Additional importers can easily be added.


## Initialized Block


Memory block whose byte values exist as opposed to uninitialized blocks whose byte
values are unknown.


## Instance Settings, Data Type


Display options for *individual* data items in Ghidra. For example one byte can be
displayed as decimal while another is displayed as hex.  Also see [Data Type Default Settings](../DataPlugin/Data.md#default-settings).


## Instruction


An assembly level command such as MOV, JMP, etc.


## Intel Hex


Binary file format specified by Intel generally used for ROM images.


## Isolated Entry Model


A block model defining subroutines.  A subroutine block must have only one entry
point, but may share code with another subroutine.  The subroutine body will stop if
another is called or a source entry point is encountered.


**K**


## Key Binding


Keyboard shortcut for invoking Ghidra functionality.


**L**


## Label


Symbol name associated with an address in memory.


## Language


The set of instructions associated with a computer processor.


## Little Endian


Byte order for storage such that the low-order byte is at the starting address, as shown
in the figure below, where the increasing memory addresses are going from right to
left.


| ![](images/LittleEndian.png) |
| --- |


## Listing


The display of the assembly language along with comments and other markup
information.


## Local Menu


A menu that is associated with a specific Ghidra docking window.


## Local Symbol


A symbol that is local to a particular function.


**M**


## Marker


Used to indicate a significant location in a program (ex: bookmarks, search results,
analysis problems, etc).


## Memory


The component of a program that contains the raw bytes and the addresses where those
bytes are located in the program's address space.


## Memory Block


A contiguous set of bytes anchored at an address.  Memory consists of one or more
Memory Blocks.


## Memory Map


Ghidra GUI that allows the user to view and
edit the Memory Blocks of a program.


## Memory Reference


A reference from a mnemonic or operand to another address in the same program.


## Merge


1. The process of resolving the differences between a checked out version with the
globally shared version of a program.
2. The process of retrieving changes made by others to the globally shared version of
the program and incorporating those changes into your program **without** introducing
your changes into the shared version (i.e. doing a check-in).


## Microcode


Low-level instructions used to implement a machine instruction.


## Mnemonic


The name of an instruction as it appears in the assembly listing. (i.e. mov, add, jmp,
etc.)


## Modal


Dialogs that prevent user interaction with any other Ghidra component until the dialog
is dismissed.


## Motorola Hex


Binary file format specified by Motorola generally used for ROM images.


## Multiple Entry Model


A block model defining subroutines.  A subroutine block may have multiple entry
points and may not overlap code from other subroutines.


## Multi-User


Term used when multiple users are working together using shared projects and
programs.


**N**


## Name Space


Defines a scope such that all symbol names within that scope are unique.


## NE


Abbreviation for New Executable.  File format used by Windows 3.1.x  operating
systems for storing executable programs.


**O**


## Offcut


A reference into the middle of some instruction or data item.


## Offline


A situation when a shared Ghidra project cannot connect to the server repository.


## Operand


The arguments of an assembly instruction.


## Overlapped Code Model


A block model defining subroutines.  A subroutine block is all code accessible from
a single entry point and terminates at returns.  Code may be shared with other
subroutines.  Each subroutine is defined to include the overlapping code as part of
its body.


## Overlay


A memory block which corresponds to a physical memory space address within a corresponding
overlay address space identified by the block name.  This allows multiple memory blocks to be defined which correspond
to the same physical address region.  While the use of overlay blocks are useful to
represent a memory range its' use has significant limitations for the decompiler and
analysis which may be unable to determine when an overlay should be referenced.


**P**


## Partitioned Code Model


A block model defining subroutines.  There is exactly one entry point which may be
a call or any other flow instruction.  Each instruction belongs to exactly one
subroutine (code is not shared).


## PCode


A form of microcode used by Ghidra to model the semantics of machine- or assembly-level instructions.


## PE


Abbreviation for Portable Executable.  File format used by Microsoft for storing
executable programs.


## PKI Authentication


One of the ways a Ghidra client can use to identify itself to the Ghidra server.


## Plate Comment


Comments that are displayed as a block header above the instruction.  Plate
comments are automatically surrounded by '*'s.


## Plugin


Software bundles that can optionally be added to Ghidra to add additional
functionality.


## Plugin Dependency


The required presence of additional plugins before a particular plugin can be
loaded.


## Plugin Table


A table view of available Plugins that can be added to a tool, as shown in the
*Configure* tool dialog.


## Plugin Tree


A graphical view of available Plugins that can be added to a tool, as shown in the
*Configure* tool dialog.  The Plugins are grouped by functionality and displayed
in a tree-like format.


## Popup menu


A [context-sensitive menu](#context-sensitive-menu) that appears when you press
the right mouse button.


## Post Comment


Comments that are displayed below the instruction.


## Pre Comment


Comments that are displayed above the instruction.


## Project Archive


Project compressed into a single file for archival or transfer purposes.


## Program


Ghidra's representation of an executable binary, its analysis and annotations.


## Program Diff


Abbreviation for **Program Diff**erence.  It is
the process of comparing and contrasting programs in order to determine their similarities
and differences.


## Primary Label


The most important label at a location. It is the label that will appear by default in
all references to that location.


## Processor Language


The assembly language for a processor.


## Program Context


The set of register values at any location in a program.


## Program Tree


The Ghidra GUI module that allows the user to organize the memory of a program
hierarchically.


## Project


A collection of files (programs, etc) and user configuration information.


## Project Repository


A directory on a server that is used by Ghidra's Multi-User module to store shared
programs.


## Property


A storage mechanism used by plugins to store information in a program at specific
addresses.


**R**


## Read-Only Project


A project that can be opened for viewing but cannot be changed (i.e. someone else owns
this project).


## Redo


The process of repeating the last change that was "undone".


## Reference


A link from the mnemonic or operand of an instruction to a destination.  The
destination is an address, stack variable, or external address in another program.


## Register


A special-purpose storage location in a processor.


## Regular Expression


A character sequence used to match patterns in strings. See
[Regular Expression](../Search/Regular_Expressions.md#regular-expression-syntax)
for examples.


## Relocation Table


Relocations are address locations that need to be updated to reflect where the program
is loaded into memory.


## Running Tools


An area on the [Ghidra Project Window](#ghidra-project-window) that displays a
list of icons which represent [Tools](#tool) currently in use.


**S**


## Scalar


A numeric value in a program.


## Scope


The set of addresses for which a variable is defined.


## Screen Element


The individual listing items that are displayed by the code browser (i.e. address,
mnemonic, operand, comment, etc.)


## Select Limited Flow


A Ghidra process that involves following a [program](#program)’s logic
but excluding all branches (conditional and unconditional).  Select Limited Flow often
reveals the high-level algorithm associated with a program. Select Limited Flow is an
option in the [Code Browser](#code-browser).


## Selection


A set of addresses that have been chosen by the user in order to perform some
operation.


## Shared Project


A project that is associated with a Ghidra Server.  The files in a shared project
are accessible by other users.


## Shared Program


A program that can be modified by multiple users. Shared programs reside in project
repositories on a server rather than in local  projects on the user's workstation.


## Simple Block Model


See [Basic Block Model](#basic-block-model)


## SLED


Table-based mechanism for specifying the syntax and semantics for a processor
language.


## SLEIGH


Improved version of SLED. Allows language-writers to more accurately represent all
features of a language.


## Source Address


The "From" address in a reference "From-To" address pair.  An address of an
instruction or pointer that refers to another address.


## Stack Reference


A reference from a mnemonic or operand to a stack variable.


## Stack Variable


A parameter or local variable definition on the stack frame defined by a function.


## Static Disassembly


A version of disassembly where jump and call instructions are not followed.


## Status Window


Area at the bottom of a Ghidra tool used to display messages to the user.


## Subroutine Model


A [Block Model](../BlockModel/Block_Model.md) which partitions code
into address ranges based upon a set of rules defined by a specific model.  Subroutine
models generally define blocks whose entry point(s) correspond to called locations.


## Symbol


A label that associates a name with an address.


## Symbol Table


A component of [program](#program) containing
all the label information.


## Symbol Tree


Ghidra GUI module used to display symbols in a tree structure.


**T**


## Tabbed Window


A window containing two or more sub-windows that can be selected using tabs.


## Terminator


Any assembly instruction that has no flow (ex: Halt).


## Text Highlighting


The mode in the Code Browser where all the uses of a given word are highlighted in
yellow.


## Thunk


Thunks are functions, called by other functions, usually to perform an indirect or
external function call.


## Tool Chest


An area on the [Ghidra Project](#ghidra-project-window) window that displays
icons for the configured and saved [Tools](#tool) which are available to a
user.


## Tool


A collection of [Plugins](#plugin) that work together to produce a useful GUI for performing some user
level task.


## Tool Tip


A popup description that appears when the mouse is hovered over a GUI item.


## Toolbar (local and global)


An icon bar used to invoke Ghidra functionality.


**U**


## Unconditional Call


A call instruction that always executes.


## Unconditional Jump


A jump instruction that always executes.


## Undefined Data


Bytes in the program that have yet to be defined as instructions or data.  By
default, all bytes in a program begin as Undefined Data.


## Undo


The process of removing the last change made to a program.


## Undocked Window


A Ghidra window that has its own frame and can be positioned and sized independently
from other Ghidra windows.


## Unresolved External Reference


An external reference that has not been linked to any program in the project.


## User Access List


The list of users that have access to a particular shared repository on a Ghidra
server.  The list contains usernames and permissions.


## User Authentication


The process of verifying the identity of a client user to the server.


**V**


## Version Control


The process of maintaining multiple versions of a program as changes are made.


## Version History


A dialog displaying the history of changes made to a program.  Any previous version
of the program can be selected for viewing from the **View History** dialog.


## Versioned Program


A program that has been placed under version control in a Ghidra project in order to
maintain a history of all the changes made to that program.


## Viewed Project


A project that has been open as read-only.  Projects that you do not own can only
be opened as a Viewed Project.


**W**


## Workspace


A virtual Ghidra desktop for a set of [running tools](#running-tools).


**X**


## XREF


Abbreviation for cross reference.  CodeBrowser's
display of [Source Addresses](#source-address).


---

[← Previous: Undo/Redo](../Tool/Undo_Redo.md) | [Next: What's New →](../docs/WhatsNew.md)
