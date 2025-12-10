[Home](../index.md) > [DebuggerModulesPlugin](index.md) > Modules and Sections

# Debugger: Modules and Sections


![](images/DebuggerModulesPlugin.png)


The concept of a module may vary from platform to platform, but in most cases, it refers to
a binary image which is loaded or mapped into memory comprising some portion of the target's
executable code. Likely, these are the same files that Ghidra can import for static analysis.
Similarly, the concept of a section may vary, but in most cases, it refers to a portion of a
module, possibly backed by its binary image. This window displays information about modules,
and sometimes their sections, known to the back-end debugger. Information in this window
reflects what has been recorded into the current trace, which in turn comes from a target. The
top table displays module information, while the bottom table displays section information.


## Table Columns


The top table, which lists modules, has the following columns:


- Base - if available, the minimum address where the module is mapped in the target's
memory. Double-clicking this field navigates to the address.
- Max - if available, the maximum address where the module is mapped in the target's
memory. Double-clicking this field navigates to the address.
- Name - a short name for the module, typically its file name.
- Mapping - if mapped to a Ghidra program database, the name of that program. An asterisk
is appended if the mapping only covers the module partially. If multiple mappings cover the
module, they are all listed.
- Length - the length from base address to max address, inclusive. Note that not every page
in the range is necessarily mapped.
- Path - the path of the module object in the target's model. This is hidden by default.
See the [Model](../DebuggerModelPlugin/DebuggerModelPlugin.md)
window.


The bottom table, which lists sections, has the following columns:


- Start - the minimum memory address of the section. Double-clicking this field navigates
to the address.
- End - the maximum memory address of the section. Double-clicking this field navigates to
the address.
- Name - the name of the section given by the debugger, usually the name given in the
module binary's header.
- Module Name - the name of the module containing this section.
- Length - the number of bytes in the section.
- Path - the path of the section object in the target's model. This is hidden by default.
See the [Model](../DebuggerModelPlugin/DebuggerModelPlugin.md)
window.


## Actions


This window provides several actions, some of which are only accessible via pop-up
menus.


### Import From File System


This action is available from a module's or section's pop-up menu. It prompts the user to
import the module from the local file system into Ghidra as a static image.


### Auto-Map


This action is always available. It automatically maps trace memory to static images, using
Module, Section, or Region information. See the [Map Modules](#map-modules), [Map Sections](#map-sections), and [Map Regions](../DebuggerRegionsPlugin/DebuggerRegionsPlugin.md#map-regions)
actions for more information. When enabled, this action will automatically perform the
corresponding action whenever the relevant table is updated. By default, it automatically maps
using Modules.


### Map Identically


This action is available when both a trace and a program are opened. It maps the current
trace to the current program using identical addresses. This action ignores the module list. It
is a suitable mapping when the current program is loaded in the trace *without
relocation*. It is also a fallback worth trying in the absence of a module list.


### Map Manually


This action is always available. It simply displays the [Static Mappings](../DebuggerStaticMappingPlugin/DebuggerStaticMappingPlugin.md)
window. From there, it is possible to construct the map from trace memory to static images
entirely by hand.


### Map Modules


This action is available from the modules' or sections' pop-up menu. It searches the tool's
open programs for the selected modules and proposes new mappings. The user can examine and
tweak the proposal before confirming or canceling it. Typically, this is done automatically by
the [Auto-Map](#auto-map) action. By selecting "Memorize" and confirming the dialog,
the user can cause the mapper to re-use the memorized mapping in future sessions. The memorized
module name is saved to the program database.


![](images/DebuggerModuleMapProposalDialog.png)


### Map Module to Current Program


This action is available from a single module's pop-up menu, when there is an open program.
It behaves like Map Modules, except that it will propose the selected module be mapped to the
current program. This action with the "Memorize" toggle is a good way to override or specify a
module mapping once and for all.


### Map Sections


This action is analogous to the Map Modules action. It searches the tool's open programs for
blocks matching the selected sections and proposes new mappings. Users who prefer this to Map
Modules should also consider setting [Auto-Map](#auto-map) to use Sections.


![](images/DebuggerSectionMapProposalDialog.png)


### Map Sections to Current Program


This action is available from the pop-up menu, when the current selection indicates a single
module and there is an open program. It behaves like Map Sections, except that it will attempt
to map sections from the indicated module to blocks in the current program.


### Map Section to Current Block


This action is available from a single section's pop-up menu, when there is an open program.
It behaves like Map Sections, except that it will propose the selected section be mapped to the
block containing the cursor in the static listing.


### Import Missing Module


This action is offered to resolve a "missing module" console message. Such a message is
reported in the [Debug
Console](../DebuggerConsolePlugin/DebuggerConsolePlugin.md) when the cursor in the [Dynamic Listing](../DebuggerListingPlugin/DebuggerListingPlugin.md) cannot be
synchronized to the static listing for lack of a module mapping. This action is equivalent to
[Import From File System](#import-from-file-system) on the missing module.


### Map Missing Module


This action is offered to resolve a "missing module" console message. Such a message is
reported in the [Debug
Console](../DebuggerConsolePlugin/DebuggerConsolePlugin.md) when the cursor in the [Dynamic Listing](../DebuggerListingPlugin/DebuggerListingPlugin.md) cannot be
synchronized to the static listing for lack of a module mapping. This action is equivalent to
[Map Module To](#map-module-to-current-program) on the missing module.


### Retry Map Missing Program


This action is offered to resolve a "missing program" console message. Such a message is
reported in the [Debug
Console](../DebuggerConsolePlugin/DebuggerConsolePlugin.md) when the launcher fails to map the current program database to the launched trace.
This action is equivalent to [Map Modules](#map-modules), but considering only the
missing program and launched trace.


### Map Missing Program to Current Module


This action is offered to resolve a "missing program" console message. Such a message is
reported in the [Debug
Console](../DebuggerConsolePlugin/DebuggerConsolePlugin.md) when the launcher fails to map the current program database to the launched trace.
This action is only available when the current trace is the launched trace. It finds the module
containing the cursor in the [Dynamic Listing](../DebuggerListingPlugin/DebuggerListingPlugin.md) and proposes
to map it to the missing program.


### Map Missing Program Identically


This action is offered to resolve a "missing program" console message. Such a message is
reported in the [Debug
Console](../DebuggerConsolePlugin/DebuggerConsolePlugin.md) when the launcher fails to map the current program database to the launched trace.
This action is equivalent to [Map Identically](#map-identically), but for the
missing program and launched trace.


### Show Sections Table


This actions is always available. By default the sections table (bottom) is showing. Some
debuggers do not offer section information, and even for those that do, it can be expensive to
retrieve it. The visibility of the section table is controlled by toggling this action.


### Filter Sections by Module


This action is always available. By default the bottom table displays all sections in the
current trace. When this toggle is enabled, and at least one module is selected, the bottom
table will only include sections contained by a selected module.


### Select Addresses


This action is available when at least one module or section is selected. It selects all
addresses in the [Dynamic
Listing](../DebuggerListingPlugin/DebuggerListingPlugin.md) contained by the selected modules or sections.


### Select Rows


This action is available when the [Dynamic Listing](../DebuggerListingPlugin/DebuggerListingPlugin.md)'s cursor is
at a valid location. It selects the module and section, if applicable, containing that cursor.
If the dynamic listing has a selection, it selects all modules and sections intersecting that
selection.


---

[← Previous: Time](../DebuggerTimePlugin/DebuggerTimePlugin.md) | [Next: Static Mappings →](../DebuggerStaticMappingPlugin/DebuggerStaticMappingPlugin.md)
