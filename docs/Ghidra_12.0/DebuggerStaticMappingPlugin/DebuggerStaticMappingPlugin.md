[Home](../index.md) > [DebuggerStaticMappingPlugin](index.md) > Static Mappings

# Debugger: Static Mappings


![](images/DebuggerStaticMappingPlugin.png)


A static mapping refers to a range of addresses in the dynamic listing and its corresponding
range in the static listing. These mappings provide a flexible means of mapping Ghidra program
databases into a trace database. Typically, this table is populated automatically. See the [Auto-Map](../DebuggerModulesPlugin/DebuggerModulesPlugin.md#auto-map)
action. Common mapping schemes are available in user actions, e.g., [Map Modules](../DebuggerModulesPlugin/DebuggerModulesPlugin.md#map-modules).
This under-the-hood static mapping window displays the mappings table, allowing users or
developers to diagnose image mapping issues and manually specify mappings, regardless of
reported modules, sections, regions, etc. For most users, there is no reason to access this
window.


## Table Columns


The table has the following columns:


- Dynamic Address - the minimum address in the dynamic address range.
- Static Program - the Ghidra URL of the program database, i.e., the imported static
image.
- Static Address - the minimum address in the static address range.
- Length - the number of bytes in the mapping.
- Shift - the offset from static address to dynamic address.
- Lifespan - the span of snapshots for which this mapping is applicable.


## Actions


This window provides actions for finding, adding, and removing mappings. **NOTE:** To
"modify" an entry, delete and re-add it.


### Select Rows ![Rows](../icons/table_go.png)


This action is available when the active listing's (dynamic or static) cursor is at a valid
location. It selects the mapping containing that cursor. If the active listing has a selection,
it selects all mappings intersecting that selection.


### Add Mapping ![Add](../icons/add.png)


This action is always available. It presents a dialog to manually add a mapping. When one
primary listing (dynamic or static) has a selection, and the other's cursor is at a valid
location, it will populate the dialog, using the selection's size and minimum address, and the
cursor as the corresponding minimum address. The default lifespan is "from now on out", i.e.,
the current snap to infinity.


### Remove Mapping ![Delete](../icons/delete.png)


This action is available when at least one mapping is selected. It removes those
mappings.


---

[← Previous: Modules and Sections](../DebuggerModulesPlugin/DebuggerModulesPlugin.md) | [Next: Static Synchronization →](../DynamicStaticSynchronizationPlugin/DynamicStaticSynchronizationPlugin.md)
