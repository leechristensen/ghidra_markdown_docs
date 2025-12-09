[Home](../index.md) > [Debugger](index.md) > Launching a Target

# Debugger: Getting Started


The debugger supports debugging native user-mode applications for Linux, macOS, and Windows
on 64-bit x86 and often arm64, e.g., when on "Apple Silicon." While not official, it also
supports a variety of other platforms, so long as Ghidra can connect to a debugger that
supports it. Launching is accomplished by connecting to the respective debugger for the target
platform: GDB on Linux, LLDB on macOS, and the Windows Debugger (`dbgeng.dll`) on
Windows. Several launch configurations are already included, and new launchers are fairly
easily added by writing shell scripts.


## Pay Attention to Errors


Many actions are taken automatically on behalf of the user, e.g., reading registers when a
target is paused. In most cases, errors on automatic actions are dropped to the [Debug Console](../DebuggerConsolePlugin/DebuggerConsolePlugin.md), as displaying
them in a dialog could become a pest. That said, if things still don't seem right, please check
the terminal or Ghidra's application log.


## Launching a Target


Starting up the Ghidra Debugger for user-mode debugging of a local process usually entails
just two steps:


1. Open (or import) your program into the Debugger tool
2. Click the **Launch** ![(bug icon)](../icons/debugger.png) button in the main
toolbar


The first time you launch a given program, you may be asked to select and configure a
specific launcher. To load the default Debugger tool, from the main Ghidra application window
select **Tools → Import Default Tools...** from the menus. Select
"defaultTools/Debugger.tool", and hit **OK**. The Debugger tool will be added to the Tool
Chest.


To launch the tool, you have several options, identical to those you might use to launch the
CodeBrowser tool. You can click the Debugger icon to launch an empty Debugger tool. You can
drag a program that you have already imported from the Active Project window onto the tool icon
in the Tool Chest, or you can right-click on one of the programs in the project and pick
**Open With → Debugger**. If you open an empty Debugger tool, you can add programs to
it later in the usual ways, e.g. via **File → Import File...** or by
dragging-and-dropping programs onto the running tool.


The default tool is pre-configured with a collection of plugins relevant to both dynamic and
static analysis. As always, there is some chance that the tool will launch with some portion of
the plugins not displayed or with a less-than-optimal layout. To verify which plugins you have,
you can select **File → Configure**. "Debugger" should already be selected. Choosing
**Configure All Plugins** ![(the plug icon)](../icons/plugin.png) near
the top right should show the full list of pre-selected plugins. Debugger-related plugins all
begin with "Debugger" or "TraceRmi."


For the **Launch** button to work, you must (a) have the program you wish to run visible
and selected in the static Listing window, and (b) have imported the program from the place it
lives on the local system. In other words, the file path associated with the program should be
the path to the executable for the current file system. You can verify this using the **Help
→ About my_program** menu item in the main tool bar. For example, on a Linux system, if
you've imported "xclock", **Help → About xclock...** should have an entry at the bottom
of the page for "`Executable Location: /usr/bin/xclock`".


When you launch the target by this method, a number of changes should be evident in the GUI.
A Terminal should appear, containing the actual back end debugger, likely including some
initialization messages and diagnostics. A new trace will appears in the [Listing](../DebuggerListingPlugin/DebuggerListingPlugin.md). A new tree
structure will be populated within the [Model](../DebuggerModelPlugin/DebuggerModelPlugin.md) window. The remaining
windows will be populated with current trace information. Please be patient, on some platforms
it may still take some time for things to populate and settle. The [Debug Console](../DebuggerConsolePlugin/DebuggerConsolePlugin.md) should provide
some hints as to ongoing activity.


## Debugger Components


Some of the more commonly accessed components are explained below. They also have their own
help pages.


### Terminal


The terminal window allows a user command-line access to the native debugger. For Linux,
this means the standard GDB command line interface; for macOS, the LLDB command line interface;
and for Windows, the WinDbg/kd command set. While basic tasks may not require using the command
line interface, more complicated debugging scenarios invariably require commands specific to
the target which have not or cannot be implemented generically in the GUI. Additionally, if for
some reason the connection to Ghidra fails, the terminal will still provide command-line access
for diagnostics and/or manual recovery.


### Model


The [Model](../DebuggerModelPlugin/DebuggerModelPlugin.md) window
displays a directory of objects in a 3d-party debugging session using a structure determined by
its back-end plugin. In some cases, e.g., when the back end does not recognize the target's
architecture, other displays may struggle to display meaningful information. Even then, this
window should provide a good overview of the debugger's and its target's current state. It may
also provide some useful commands for diagnostics, but the terminal may be a better choice.


### Listing


The back end uses its connection to Ghidra to create a trace and record target information
into it. The Debugger's various windows all derive their contents from the current trace.
Perhaps the most important of these is the [Listing](../DebuggerListingPlugin/DebuggerListingPlugin.md) window. Analogous to
the static listing, it displays the raw bytes in the target's memory and allows the user to
mark them up, e.g., disassemble, place data types, comment. Unlike the static listing, this
window shows live bytes in all valid memory, including stacks and heaps. When it can, the
Ghidra debugger keeps the cursor locations in the Static and Dynamic Listings synchronized.


### Controls and Miscellany


The main toolbar provides your standard debugging controls, e.g., resume, step, interrupt.
They apply to the current thread or frame as defined by the back end's command set. For
details, see the [Control](../DebuggerControlPlugin/DebuggerControlPlugin.md) plugin. During or
after a session, the user can examine trace history or emulate by changing control mode.


Breakpoints can be set from either the [Breakpoints](../DebuggerBreakpointsPlugin/DebuggerBreakpointsPlugin.md) window
or the [Listing](../DebuggerBreakpointMarkerPlugin/DebuggerBreakpointMarkerPlugin.md).
The [Registers](../DebuggerRegistersPlugin/DebuggerRegistersPlugin.md)
and [Stack](../DebuggerStackPlugin/DebuggerStackPlugin.md) windows
reflect the state of the current thread, which can be selected in the [Threads](../DebuggerThreadsPlugin/DebuggerThreadsPlugin.md) window. Typically,
the thread selected for the trace in the Threads window is kept in sync with the
active/selected/focused thread in the back-end debugger, but not always.


### Console


The [Debug Console](../DebuggerConsolePlugin/DebuggerConsolePlugin.md)
is a central place for reporting activity, errors, and suggesting actions. This and the
Terminal are the first places to look when troubleshooting.


---

[← Previous: Getting Started](GettingStarted.md) | [Next: Launchers →](../TraceRmiLauncherServicePlugin/TraceRmiLauncherServicePlugin.md)
