[Home](../index.md) > [DebuggerCopyActionsPlugin](index.md) > Copy Actions

# Debugger: Copy Actions


In the course of debugging, the user may want to capture certain state and annotations from
the dynamic context into the static. This might include the contents of the stack, the heap, or
example data stored in uninitialized memory. The copy actions allow for the easy movement of
data and annotations from traces into programs. The actions are all accessed via the
**Debugger** menu.


## Actions


### Copy Into Current Program


This action requires a selection of memory in a dynamic view. It copies selected contents
from the current trace (at the current time) into the current program. The [Copy Dialog](#copy-dialog) is presented with the current program set as the destination.


### Copy Into New Program


This action requires a selection of memory in a dynamic view. It copies selected contents
from the current trace (at the current time) into a new program. The [Copy
Dialog](#copy-dialog) is presented with **`<New Program>`** set as the destination.


### Export Trace View


This action is available whenever a trace is open. The [Export Dialog](../ExporterPlugin/exporter.md#export-dialog) is presented for
the current trace at the current time. This provides a mechanism for capturing a particular
point in time from a trace to a file. The exported image can be analyzed in Ghidra or another
tool.


## Copy Dialog


The **Copy Into...** actions both present the same dialog: (The **Export Trace View**
action uses a different dialog.)


![](images/DebuggerCopyIntoProgramDialog.png)


The dialog consists of several options, followed by a table that displays the proposed
ranges to copy. For selected ranges not contained in the destination program's memory, new
blocks are proposed. The source selection is always broken apart by regions defined in the
trace's memory manager.


### Options


- The **Destination** drop down allows the choice of an alternative destination. All
open programs, **`<New Program>`**, and **`<Temporary Program>`** are available
for selection. Modifying this option will reset the proposal. Choosing **&lt;New
Program&gt;** will prompt for a new destination program upon a successful copy. Choosing
**`<Temporary Program>`** will create a temporary, read-only program. The temporary
program can still be saved later.
- The **Read live** checkbox includes the [Read Memory](../DebuggerListingPlugin/DebuggerListingPlugin.md#read-memory)
action in the copy process. This is only available when the trace is live and at the present.
This assures that bytes copied into the destination program are actually the bytes from the
live target, not just a stale cache or default zeros. **Note:** The copy operation will
proceed even if the read-live-memory step fails, or only partially succeeds. Include [State](#options) if you need to know which bytes are up to date in the destination
program.
- The **Relocate** checkbox enables the use of [Static
Mappings](../DebuggerStaticMappingPlugin/DebuggerStaticMappingPlugin.md) when determining the destination addresses. This is only available for existing
programs, and will only operate on portions of the source trace that are mapped to the
destination program. Modifying this option will reset the proposal.
- The **<a name="use-overlays"></a>Use overlays** checkbox causes the dialog to propose
overlay blocks for destination ranges that already exist in the program's memory. When
unchecked, ranges are broken apart so that portions already in the destination memory map
will not modify the map. Portions not already in the memory map will generate new blocks.
When checked, destination ranges are not broken apart. If any portion already exists in the
destination memory map, the entire range will generate an overlay block. Modifying this
option will reset the proposal.
- The **Include** checkboxes determine which contents are transferred from the current
trace view into the destination. The **Select All** and **Select None** buttons do as
they say. **Note:** Even if no items are selected, the destination blocks will be created,
if the dialog is confirmed.
  - **Bookmarks** copies bookmarks contained in the selection.
  - **Breakpoints** copies breakpoints contained in the selection. **Note:** Since
programs do not support breakpoints, bookmarks are used instead. They are the same type
and category as those used by the [Breakpoints](../DebuggerBreakpointsPlugin/DebuggerBreakpointsPlugin.md)
window.
  - **Bytes** copies the actual memory contents of the selection. **Note:** When
copying into an uninitialized block, the entire block becomes initialized, i.e., all
`??`s become `00`s; however, only the selected ranges are actually
copied in.
  - **Comments** copies all comments contained in the selection.
  - **Data** copies all (non-dynamic) data annotations contained in the selection. It
is only available when the source and destination agree on data organization.
  - **Dynamic Data** copies all data annotations for dynamic data types. This item
requires **Bytes** to also be copied, since the properties (particularly length) of
each unit may depend on the memory contents. It is only available when the source and
destination agree on data organization.
  - **Instructions** copies all disassembled instructions in the selection. This item
requires **Bytes** to also be copied, since instructions depend on the memory
contents. It is only available when the source and destination have identical
languages.
  - **Labels** copies all labels contained in the selection.
  - **References** copies all memory references where both the "from" and "to"
addresses are contained in the selection.
  - **<a name="state"></a>State** copies the memory states (stale, error, known) of
the selection. **Note:** Since programs do not support memory state, the program's
color map is used instead.


### Table Columns


The table displays the proposal and allows for some adjustments. It has the following
columns:


- Remove - a button to remove the selected range from the proposal. If applicable, the
destination block will no longer be created.
- Region - the name of the source memory region of the trace.
- Modules - the names of modules that touch the source range.
- Sections - the names of sections that touch the source range.
- SrcMin - the minimum address in the source range.
- SrcMax - the maximum address in the source range.
- Block - the name of the destination memory block of the program. If the block already
exists, the name is displayed with an asterisk. The block will not be created, but contents
will still be copied into it. If the block does not already exist, the name can be changed by
editing this cell.
- Overlay - indicates whether or not a created block will be an overlay block. This cannot
be modified. See [Use overlays](#options) above.
- DstMin - the minimum address in the destination range.
- DstMax - the maximum address in the destination range.


The **Copy** button confirms the dialog and copies *all proposed ranges* in the
table. If successful, the dialog is closed. The **Cancel** button dismisses the dialog
without performing any operation. The **Reset** button resets the proposal, in case entries
were accidentally removed or modified.


---

[← Previous: Debug Console](../DebuggerConsolePlugin/DebuggerConsolePlugin.md) | [Next: Model →](../DebuggerModelPlugin/DebuggerModelPlugin.md)
