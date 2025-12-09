[Home](../index.md) > [DebuggerBreakpointMarkerPlugin](index.md) > In the Listings

# Debugger: Breakpoints in the Listings


![](images/DebuggerBreakpointMarkerPlugin.png)


For a description of how breakpoints are managed logically in Ghidra, please read about the
[Breakpoints](../DebuggerBreakpointsPlugin/DebuggerBreakpointsPlugin.md)
window. Each individual breakpoint location is placed in its respective listing. Breakpoints
are best controlled using the static program listing, where they are stored as bookmarks. When
this plugin is active, additional actions are available for managing breakpoints and their
locations on target. The actions in the static listing manipulate the logical breakpoint as a
whole; whereas, the actions in the dynamic listing tend to manipulate just the locations for
the current target. **NOTE:** Depending on the connected debugger, locations resulting from
a common specification may not be independently manipulated.


By default, enabled breakpoints are colored a desaturated blue, ineffective breakpoints are
colored grey, and disabled breakpoints have no background at all.


## In the Function Graph


![](images/DebuggerFunctionGraphBreakpointMargin.png)


When active in the Debugger, the [Function Graph](../FunctionGraphPlugin/Function_Graph.md) will display
breakpoints using background colors and markers in each vertex's margin. The margin behaves
exactly as it would in the static listing. A marker is displayed at each address with a
breakpoint indicating its state. Multiple breakpoints at an address may result in display of a
mixed state. Double clicking in the margin will set or toggle a breakpoint at that address.


## In the Decompiler


![](images/DebuggerDecompilerBreakpointMargin.png)


When active in the Debugger, the [Decompiler](../DecompilePlugin/DecompilerIntro.md) will display breakpoints in
its margin. Keep in mind, the relationship between machine instructions and the decompiled code
is not always so simple. One line may correspond to a single address, many addresses, or no
addresses at all. If there is a breakpoint at any address for a given line, then that line will
have a marker indicating the breakpoint's state. If there are multiple, then that state may be
mixed. In most cases, [Setting](#set-breakpoint) a breakpoint in the decompiler will
suggest a Software Execution breakpoint at the minimum address of the current line. If the
current token is a static variable, then it will suggest a Read/Write breakpoint at the
variable's address. (Note that Read/Write breakpoints are not indicated in the Decompiler's
margin.) The other actions affect all breakpoints on the current line.


## Actions


The following actions are added to all disassembly listings by the breakpoint marker plugin.
They allow the placement and toggling of breakpoints by address, kind, and length. **NOTE:**
These actions may also appear in other address-based contexts, but not all of those contexts
include visual breakpoint indicators. The [Model](../DebuggerModelPlugin/DebuggerModelPlugin.md) pane may provide actions
to set breakpoints in other ways.


### Toggle Breakpoint (K)


This action is always available, and it is suitable for almost all cases. If there is a
breakpoint at the cursor, this simply toggles its state. If there is no breakpoint at the
cursor, this will behave like **Set Breakpoint**, giving a reasonable set of default
parameters based on the context at the cursor. At an instruction, it will prefer to set a
Software Execution breakpoint. At defined data, it will prefer to set a Read/Write breakpoint
of the size of data. At undefined data, or if the target does not support the suggested
default, the default kind is left unselected. Please use one of the **Set Breakpoint**
actions to force specific commands. **NOTE:** The default parameters are not guaranteed to
be accepted by the connected debugger.


### Set
Breakpoint


This menu is available on the dynamic listing when the target supports at least one
breakpoint kind. This menu is always available on the static listing. It displays set
breakpoint actions for each reasonable combination of kinds supported by the target. In the
static listing, all reasonable combinations are available, regardless of target support;
however, only those kinds supported by the target will be included in the resulting command.
Selecting one of the actions will display a prompt allowing adjustments to the parameters
before issuing the command.


![](images/DebuggerPlaceBreakpointDialog.png)


- Address - the address of the breakpoint. It defaults to the address of the instruction or
data at the cursor.
- Length - the length in bytes of the breakpoint. For execution breakpoints, this defaults
to 1 — often the required value. For access breakpoints, this defaults to the size of
the data at the cursor.
- Kinds - the kind(s) of breakpoint. Only the reasonable combinations are presented, but
the user may type any desired combination. A connected debugger may not support the desired
combination.
- Name - the user-defined name of the breakpoint. The name is set on the bookmark at its
static location, if applicable.


### Enable
Breakpoint


This action is available when there is at least one disabled breakpoint at the cursor. It
enables those logical breakpoints.


### Disable Breakpoint


This action is available when there is at least one enabled breakpoint at the cursor. It
disables those logical breakpoints.


### Clear
(Delete) Breakpoint


This action is available when there is at least one breakpoint (in any state) at the cursor.
It deletes those logical breakpoints.


---

[← Previous: Breakpoints](../DebuggerBreakpointsPlugin/DebuggerBreakpointsPlugin.md) | [Next: Memory Regions →](../DebuggerRegionsPlugin/DebuggerRegionsPlugin.md)
