[Home](../index.md) > [Debugger](index.md) > Debugger

# Ghidra Debugger


The Debugger is a collection of plugins comprising Ghidra's Dynamic Analysis Framework. This
includes a platform for connecting to and controlling debuggers. Ghidra is not a debugger in
itself, but rather, it relies on existing 3rd-party ("back end") debuggers, their APIs, wire
protocols, and/or command-line interfaces. Such back ends are pluggable, allowing Ghidra to be
extended and integrated with additional debuggers.


Once a target is launched in the back end, the debugger can record that target into a Ghidra
Trace database, and the UI will display the target state. The user can command the debugger
using it's command-line interface (CLI) or the actions provided in Ghidra's Debugger UI. The
trace logs all the observations made by the framework or the user. The user can rewind this
recording during or after a session, and the UI will recall those observations, displaying the
recorded machine state instead of the present machine state. These traces can also be saved,
loaded, and analyzed after a target has terminated or been disconnected. Furthermore, they can
be committed to a Ghidra Server for sharing and revision control; however, conflicting changes
*cannot* be merged.


A system of mappings, which is usually populated automatically, tracks the relationship of
imported Ghidra Program databases to modules recorded in a trace. By default, Ghidra will
synchronize the cursor in the dynamic listing with that in the static listing, and encourage
the user to import missing modules. In this way, existing static analysis is readily at hand
during a dynamic analysis session, and the user can further populate program databases during a
debugging session. However, target memories contain more spaces than program images, e.g.,
stack and heap space, and some of those spaces are modified at runtime, e.g., .bss or .data.
This information, if observed, is dutifully recorded into the trace for immediate or offline
analysis.


A variety of plugins allow the user to interact with the target, view and manipulate machine
state, set breakpoints, view recordings, etc. See the table of contents for a comprehensive
list of current plugins. Plugins generally fall into one of these categories:


1. Target manipulation - those used for managing connections and interacting with
targets.
2. Trace manipulation - those used for viewing and manipulating the trace database,
including machine state inspection. Most of these behave differently when the view is "at the
present," i.e., corresponds to a live target machine state. They may directly command and/or
request additional information from the target.
3. Global manipulation - those which aggregate information from several targets or traces,
presenting a comprehensive picture. Modifications in these views may be directed to any
target or affect any trace, depending on the context of the user action.
4. Services - those which do not present their own windows, but manage information and/or
add actions and options to other windows.


This package is already enabled in the default "Debugger" tool. You may need to import the
tool using the Tools → Import Default Tools menu from Ghidra's
project window. You may also add the package to an existing tool using the File → Configure menu from your tool window and selecting "Debugger."


---

[← Previous: Program Differences](../Diff/Diff.md) | [Next: Getting Started →](GettingStarted.md)
