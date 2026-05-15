[Home](../index.md) > [Debugger](index.md) > Troubleshooting

# Debugger: Troubleshooting


Often, it's a good idea to troubleshoot by using the target platform's recommended debugger
without connecting it to Ghidra. If it doesn't work there, it's not likely to work in Ghidra,
since it relies on that debugger. For Linux, use gdb; for macOS, use LLDB; for Windows, use
WinDbg.


## Terminal


The first place to look when you're having trouble is the debugger's terminal. If you do not
see one, check the **Window → Terminals** menu. If there is not one there, then there
is no back-end debugger running — unless, perhaps, you are trying to use a Recorder-based
target. See [Plugin Configuration](#plugin-configuration) if you suspect this is the
case.


If you already have the correct set of TraceRmi-based plugins enabled, but there is still no
terminal after attempting to launch, then the launcher is sorely mis-configured, or your system
or installation is broken. Use **Debugger → Configure and Launch ...** in the menus to
examine and modify your configuration and try again. This menu is also avaible in the drop-down
next to the **Launch** ![Debugger](../icons/debugger.png) button.


If you do have a terminal, then examine it, starting at the very top, for errors and
warnings.


## Error Console


The next place to look is the [Debug Console](../DebuggerConsolePlugin/DebuggerConsolePlugin.md). Launchers and
plugins for the Debugger often direct their diagnostic messages to this console, and sometimes
offer remedies.


## Application Log


The next place to look is Ghidra's application log. From the main project window (not the
Debugger tool window), select **Help → Show Log** in the menus. This is Ghidra's full
application log, so you may need to sift through it for debugger-related entries. Usually
searching for "debugger", "launch", "tracermi", or the name of your platform's debugger, etc.,
will help. If you're running from Eclipse, you can check its "Console" window.


## Plugin Configuration


It is possible you have an old Debugger tool still configured for Recorder-based targets.
Recorder-based targets are being replaced by TraceRmi-based targets. Try re-importing the
default Debugger tool.


Alternatively, use **File → Configure** then click the plug ![Configure](../icons/plugin.png) icon near the top right to check your tool configuration. The
following should be enabled:


- TraceRmiPlugin
- TraceRmiLauncherServicePlugin
- TraceRmiConnectionManagerPlugin
- DebuggerModelPlugin


The following should be disabled:


- DebuggerModelServicePlugin
- DebuggerModelServiceProxyPlugin
- DebuggerInterpretersPlugin
- DebuggerObjectsPlugin
- DebuggerTargetsPlugin


It is possible to leave both sets of plugins enabled, but this is by all means *NOT*
recommended.


## Tutorial


Additional troubleshooting recommendations are given in the Debugger course materials.


---

[← Previous: Connection Manager](../TraceRmiConnectionManagerPlugin/TraceRmiConnectionManagerPlugin.md) | [Next: Debug Console →](../DebuggerConsolePlugin/DebuggerConsolePlugin.md)
