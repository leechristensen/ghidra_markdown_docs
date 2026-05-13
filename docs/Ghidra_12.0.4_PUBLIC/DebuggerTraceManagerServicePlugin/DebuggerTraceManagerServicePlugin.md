[Home](../index.md) > [DebuggerTraceManagerServicePlugin](index.md) > Trace Management

# Debugger: Trace Management


This service plugin manages the collection of open traces, and it is controlled primarily
via the [Listing](../DebuggerListingPlugin/DebuggerListingPlugin.md)
window's tab panel. It maintains a list of open traces, the active trace coordinates (trace,
time, object), and permits saving, opening, and closing traces. To some extent, it also tracks
which traces have live targets.


## Actions


The plugin provides the following actions and toggles:


### Open Trace


This action is always available. It prompts for a trace in the current project and opens
that trace in the Debugger tool.


### Save Trace


This action is available whenever at least one trace is open and active. It saves the
current trace. If the current trace is not in any project, it saves it under "New Traces" of
the current project.


### Close Trace


This action is available whenever at least one trace is open and active. It closes the
current trace.


### Close All Traces


This action is available whenever at least one trace is open. It closes all traces in this
tool.


### Close Other Traces


This action is available whenever there is an open trace other than the active one. It
closes all traces in this tool, except the active trace.


### Close Dead Traces


This action is available whenever at least one trace is open. It closes all dead traces in
this tool.


### Save by Default


This toggle is always available. If the tool is closed with this toggle enabled, all open
traces are immediately saved. Note that if Ghidra is abruptly terminated (a rare occurrence
under normal use), traces may not be saved. When the tool is re-opened, the open traces are
also restored.


### Close Traces on Termination


This toggle is always available. If a target terminates with this toggle enabled, and it was
being recorded into a trace, that trace is automatically closed. If Save by Default is active,
the trace is saved.


---

[← Previous: Threads](../DebuggerThreadsPlugin/DebuggerThreadsPlugin.md) | [Next: Emulation →](../DebuggerEmulationServicePlugin/DebuggerEmulationServicePlugin.md)
