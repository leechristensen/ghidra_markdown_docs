[Home](../index.md) > [DebuggerListingPlugin](index.md) > Dynamic Listing

# Debugger: Dynamic Listing


![](images/DebuggerListingPlugin.png)


The dynamic listing is analogous to Ghidra's listing for static
analysis, but in the dynamic context. It displays annotated memory contents from a target. More
precisely, it displays recorded memory contents in a trace. In most use cases, that trace is
"at the present," meaning it is the most recent memory from a live target. Multiple listings
can be displayed simultaneously, using the same pattern as many other Ghidra windows. The
"primary" listing is always displayed and generally tracks with the rest of the tool. Any
listing can be "snapshotted," i.e., cloned. This is where dynamic listings differ from static
listings. Static clones remain in place; they do not automatically navigate. Dynamic clones can
still be configured to navigate, following the rest of the tool. A common use is to configure a
clone to follow the stack pointer. Still, you can disable a listing's automatic navigation, so
it behaves like a true clone. A current limitation is that you cannot use clones to display
different points in time for the same trace.


Where applicable, the static listing's location is synchronized to the dynamic listing, and
vice versa. The dynamic listing permits most of the same mark-up as the static listing. Any
mark-up added to the dynamic listing is saved to the trace. All mark-up (and nearly all trace
record types, for that matter) have a location in space and time. That is, they occupy an
address range (like mark-up in Ghidra programs), but also a time range (unique to traces). When
mark-up is added to the listing, it exists "from this time on". That is, its time interval is
from the current time to infinity, i.e., it has been created but never destroyed. When mark-up
is removed from the listing, its "destruction time" is set to just before the current time. If
this would cause the mark-up to "never exist," i.e., its destruction time precedes its creation
time, then the record is deleted altogether. This yields a mostly-intuitive mechanism for
marking things up "in time," but the fact that mark-up is bound in time can still be
surprising. For example, disassembling some instructions and then stepping back in time will
cause that disassembly to disappear.


Because not all memory is recorded, some background coloring is used to indicate the state
of attempted memory reads. Regardless of state, the most-recent contents, as recorded in the
trace, are displayed in the listing, defaulting to 00. "Stale" memory, that is ranges of memory
which have not been read at the current time, are displayed with a darker background. Where
that memory is marked "read-only" and has been successfully read previously, that coloring is
subdued, since the contents are not likely to have changed. Where a read was attempted but
failed, the entire failed range is displayed with a pink background. Otherwise, up-to-date
contents are displayed with the default background color.


The dynamic listing supports editing memory. See [Control and Machine State](../DebuggerControlPlugin/DebuggerControlPlugin.md).
Such edits are performed as usual: Via the [Patch](../AssemblerPlugin/Assembler.md) actions, or by pasting byte strings.
These edits may be directed toward a live target, the trace, or the emulator.


## Trace Tabs


The trace tab bar is displayed when at least one trace is open. It displays the name of each
open trace in a tab, where the "current" or "focused" trace is selected. Clicking a tab will
select its trace and focus the tool onto it. A trace associated with a live target has a red
"recording" icon ![Record](../icons/record.png) at its left. If that icon is not
present, or has disappeared, the trace is dead or terminated. A "dead" trace can still be
manipulated and marked up, but it will not record any new target information.


### Close Trace / All / Other / Dead Traces


In most cases, a trace is ephemeral, but occasionally, interesting behavior is observed that
is difficult to store as static mark-up. When traces are no longer needed, they can be closed.
Several can be closed at once by right-clicking a tab and selecting one of the actions. See [Trace
Management](../DebuggerTraceManagerServicePlugin/DebuggerTraceManagerServicePlugin.md#close-trace) for details of each action.


## Actions


The listing provides a variety of actions, some for managing and configuring listings, and
others for capturing memory from a target.


### New Dynamic Listing


This action is always available in the **Window → Debugger** menu. It creates a new
listing window with the same configuration as the primary dynamic listing. It is equivalent to
cloning the primary dynamic listing.


### Export Trace View


This action is available in the **Debugger** menu whenever there is a trace open in the
listing. It is analogous to "Export Program," but for the current trace at the current time.
This provides a mechanism for capturing a particular point in time from a trace as a static
image. The exported image can be analyzed in Ghidra or another tool.


### Follows Selected Thread


This action is only available on cloned dynamic listings. The primary listing always follows
the tool's current thread. Disabling this toggle causes the clone to remain on its own current
thread rather than following the tool's. The current thread is used when computing a location
to navigate to automatically. It is only applicable when "Track Location" is set to something
other than "Do Not Track."


### Track Location


This action is always available on all dynamic listings. It configures automatic navigation
for the dynamic listing. When location tracking is enabled, the listing is automatically
navigated to an address computed from the trace's or target's machine state. The address is
displayed in the top right of the viewer. That address and its corresponding static address are
also highlighted in green in the listing. If the address cannot be located in the listing, the
address is displayed in red. The computed address is affected by the tool's current
"coordinates," that is the selected thread, frame, and point in time. The options are
pluggable, but currently consist of:


- Do Not Track - disables automatic navigation.
- Track Program Counter - (default) navigates this listing to the current program counter.
If the stack contains a record of the program counter, it is preferred to the recorded
register value. Note that debuggers may vary in how they report the program counter, and its
meaning may vary among platforms. While there may be some nuances to the register value, the
value recorded in the stack should indicate the next instruction to be executed.
- Track Program Counter (by stack) - navigates this listing to the current program counter
as recorded from the debugger's stack trace. This option is not recommended for regular use,
especially for emulation, since the emulator does not provide stack trace records. Its use is
recommended for debugger connection developers to verify the stack records are being properly
interpreted by the GUI.
- Track Program Counter (by register) - navigates this listing to the current program
counter as recorded from the registers. While suitable for regular use, the default "Track
Program Counter" option is recommended, since the stack may record the program counter in
some cases where the registers do not. For example, when unwinding a stack frame, the
debugger may report the frame's program counter without reporting the frame's registers. This
option may be desired if stack frames are recorded incorrectly.
- Track Stack Pointer - navigates this listing to the current stack pointer. Note that
platforms may vary in how they define the stack pointer.
- Track address of watch - navigates this listing to the address of the expression's value.
This option is replicated for each watch in the [Watches](../DebuggerWatchesPlugin/DebuggerWatchesPlugin.md) window.


### Go To (G)


This action is available whenever a trace is active in the listing. It prompts the user for
an address, which can be expressed in simple notation or **Sleigh**, then attempts to
navigate to it. The expression is evaluated in the context of the current thread, frame, and
point in time. If the current trace is live and at the present, the target may be queried to
retrieve any machine state required to evaluate the expression. The expression may be in terms
of labels, registers, and constants. Labels may come from the current trace or a program mapped
into the trace. Ambiguities are resolved arbitrarily.


![](images/DebuggerGoToDialog.png)


Note that a Go-To action can fail for many reasons, e.g., syntax errors, computation
failures. One possible reason is that the address is not part of a memory region known to the
debugger. This failure can be overcome by enabling [Force Full View](../DebuggerRegionsPlugin/DebuggerRegionsPlugin.md).


Some examples:


- `00401234` — A constant address in simple notation
- `0x00401234:8` — A constant address in Sleigh notation
- `main + 10` — 10 bytes past the address of "main"
- `RAX` — The address in RAX
- `RSP + 8` — The address of stack offset 8
- `*:8 (RSP+8)` — The address pointed to by stack offset 8


### Auto-Disassembly


This action is always available. It automatically disassembles starting at the current
program counter. It applies only when a "Track Program Counter" option is selected in the [Track Location](#track-location) action. Disassembly occurs whenever the program
counter is updated, when the memory at the program counter is updated, or when navigating to a
new context. It terminates at the first branch encountered. Disassembly can be performed
manually using the [Disassemble](../DisassemblerPlugin/Disassembly.md#disassembly) command.


### Read Memory


This action is available when the current trace is "at the present" with a live target. It
will instruct the target to read the contents of memory for the selected or visible addresses.
Typically, the visible addresses are automatically read — see the Auto-Read action
— so this action is for refreshing or for reading large selections.


### Auto-Read Memory


This action is always available on all dynamic listings. It configures whether or not the
memory range(s) displayed in the listing are automatically read. Like the Read Memory action,
it is only permitted when the current trace is "at the present" with a live target. It occurs
when the user scrolls the listing, or when the listing is otherwise navigated to a new
location. Note that other components may read memory, regardless of this listing's
configuration. For example, the target typically reads the page of memory pointed to by the
program counter. In other words, this action *cannot* "disable all memory reads." The
options are pluggable, but currently consist of:


- ![Delete](../icons/delete.png) Do Not Read Memory - disables automatic memory
reads *for this listing only*.
- ![Autoread](../icons/autoread.png) Read Visible Memory - automatically
reads stale ranges that enter this listing's view.
- ![Autoread](../icons/autoread.png) Read Visible Memory, RO Once -
(default) behaves like Read Visible Memory, except it will neglect read-only ranges that have
been read previously.


---

[← Previous: Registers](../DebuggerRegistersPlugin/DebuggerRegistersPlugin.md) | [Next: Disassembly and Assembly →](../DebuggerDisassemblerPlugin/DebuggerDisassemblerPlugin.md)
