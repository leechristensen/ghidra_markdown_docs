[Home](../index.md) > [DynamicStaticSynchronizationPlugin](index.md) > Static Synchronization

# Debugger: Static Synchronization


This plugin ensures the static and dynamic listings, byte viewers, etc., all remain
synchronized.


## Actions


The plugin places a few actions in the **Debugger → Synchronization** menu to toggle
synchronization, and to transfer locations and selections on demand.


### Synchronize Static and Dynamic Locations


This action is always available. When selected, navigation in either listing —
including automatic navigation — automatically navigates to the corresponding location,
if applicable, in the other. In general, "corresponding location" is computed using information
about loaded modules reported by the debugger. For the finer details, see the [Static Mappings](../DebuggerStaticMappingPlugin/DebuggerStaticMappingPlugin.md)
window. When you navigate to a location contained by a module, but there is no corresponding
static location, a "missing module" appears in the console, offering either to import the
module or map it to an existing program. If the cursor cannot be mapped, the other listing's
location is left unchanged. If this does not seem correct. Check your module list and static
mappings.


### Synchronize Static and Dynamic Selections


This action is always available. When selected, selection in either listing automatically
selects the corresponding ranges, if applicable, in the other. In general, "corresponding
ranges" are computed using information about loaded modules reported by the debugger. For the
finer details, see the [Static Mappings](../DebuggerStaticMappingPlugin/DebuggerStaticMappingPlugin.md)
window. Portions of the selection which cannot be mapped are omitted.


### Transfer Dynamic Selection to
Static


This action is available when the dynamic listing has a selection. It maps the current
dynamic selection to corresponding static ranges and selects those in the static listing. In
general, "corresponding ranges" are computed using information about loaded modules reported by
the debugger. For the finer details, see the [Static Mappings](../DebuggerStaticMappingPlugin/DebuggerStaticMappingPlugin.md)
window. Portions of the selection which cannot be mapped are omitted. If no part of the
selection is mappable, an error is displayed in the status bar. This can happen if the module
list is missing, or Ghidra could not find the program for the current module.


### Transfer Static Selection to
Dynamic


This action is available when the static listing has a selection. It maps the current static
selection to corresponding dynamic ranges and selects those in the dynamic listing. In general,
"corresponding ranges" are computed using information about loaded modules reported by the
debugger. For the finer details, see the [Static Mappings](../DebuggerStaticMappingPlugin/DebuggerStaticMappingPlugin.md)
window. Portions of the selection which cannot be mapped are omitted. If no part of the
selection is mappable, an error is displayed in the status bar. This can happen if the module
list is missing, or Ghidra could not find the program for the current module.


### Open Program


This action is offered as a resolution whenever a module cannot be automatically opened.
This typically happens when the module's program database has crash data that can be recovered
and/or needs a version upgrade. It will attempt to open the program, allowing Ghidra to prompt
you about the situation.


---

[← Previous: Static Mappings](../DebuggerStaticMappingPlugin/DebuggerStaticMappingPlugin.md) | [Next: Watches →](../DebuggerWatchesPlugin/DebuggerWatchesPlugin.md)
