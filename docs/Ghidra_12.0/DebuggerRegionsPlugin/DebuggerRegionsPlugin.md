[Home](../index.md) > [DebuggerRegionsPlugin](index.md) > Memory Regions

# Debugger: Memory Regions


![](images/DebuggerRegionsPlugin.png)


Regions refer to ranges of allocated or reserved memory reported by the target, i.e., the
target's memory map. The precise meaning of these regions may vary depending on the nature of
the target. For user-mode applications, this is generally pages of memory allocated for image
sections, the stack, the heap, etc. The regions manager allows the user to rename pages and
modify the recorded permissions. Note that such modifications *do not* affect the
target; but only the recorded trace.


## Table Columns


The table has the following columns:


- Name - the name given to the region by the target. This field is user modifiable.
- Start - the minimum address of the region. Double-clicking this field navigates to the
address.
- End - the maximum address of the region. Double-clicking this field navigates to the
address.
- Length - the length of the region in bytes.
- Read, Write, Execute - various flags of the region. These flags only affect Ghidra's
analysis. Toggling these *do not* affect the target.
- Key, Path - descriptions the region object in the target's model. These are hidden by
default. See the [Model](../DebuggerModelPlugin/DebuggerModelPlugin.md)
window.


## Actions


The Regions window provides the following actions:


### Map Regions


This action is analogous to the Map Modules and Map Sections actions from the [Modules window](../DebuggerModulesPlugin/DebuggerModulesPlugin.md). It searches
the tool's open programs for blocks matching the selected regions and proposes new mappings.
Users who prefer this should also consider setting the [Auto-Map](../DebuggerModulesPlugin/DebuggerModulesPlugin.md#auto-map) action to
use Regions. For the best result, the selection regions should comprise a complete module. In
particular, it should include the region containing the module's image base, because the offset
from this base is used in scoring the best-matched blocks. Additionally, the region names must
include the module's file name, otherwise the matcher has no means to identify a corresponding
program.


![](images/DebuggerRegionMapProposalDialog.png)


### Map Regions to Current Program


This action is available from the pop-up menu, when there is a selection of regions and
there is an open program. It behaves like Map Regions, except that it will attempt to map the
selected regions to blocks in the current program only. This is useful if the regions are not
named according to the module filename. The selected regions should still comprise a complete
module for best results.


### Map Region to Current Block


This action is available from a single region's pop-up menu, when there is an open program.
It behaves like Map Regions, except that it will propose the selected region be mapped to the
block containing the cursor in the static listing.


### Select
Addresses


This action is available when at least one region is selected. It selects all addresses in
the dynamic listing contained by the selected regions.


### Select Rows


This action is available when the dynamic listing's cursor is at a valid location. It
selects the region containing that cursor. If the dynamic listing has a selection, it selects
all regions intersecting that selection.


### Add Region


This action is available when a trace is active. It adds a new region to the memory map. It
should only be used for emulation or to correct a recorded trace.


### Delete Regions


This action is available when at least one region is selected. It deletes those regions. Use
this with caution, since recovering those regions could be difficult. In general, this should
only be used to remove regions that were manually added.


### Force Full View


This action is available when a trace is active. It forces all physical address spaces into
the view. By default, only those addresses in the memory map — as recorded in the trace
at the current snapshot — are displayed in the listing and memory windows. When this
toggle is on, regions are ignored. Instead, all physical addresses are displayed. ("Physical"
includes all Sleigh memory spaces except `OTHER`.) This toggle applies only to the
current trace.


---

[← Previous: In the Listings](../DebuggerBreakpointMarkerPlugin/DebuggerBreakpointMarkerPlugin.md) | [Next: Time →](../DebuggerTimePlugin/DebuggerTimePlugin.md)
