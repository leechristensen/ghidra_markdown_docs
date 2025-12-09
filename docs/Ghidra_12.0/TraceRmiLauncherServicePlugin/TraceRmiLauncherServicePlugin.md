[Home](../index.md) > [TraceRmiLauncherServicePlugin](index.md) > Launchers

# Debugger: Launchers


The Debugger has an updated and simplified launcher system. A nice collection of basic
launchers for our supported platforms are provided out of the box. For Linux, we provide a
suite of GDB-based launchers. For macOS, we provide a suite of LLDB-based launchers (though,
these work on Linux, too). For Windows, we provide a launcher based on the Windows Debugger
(`dbgeng.dll` and `dbgmodel.dll`). Help is available for each in its respective
sub-topic.


Each launcher automates the creation of a Trace RMI [acceptor](../TraceRmiConnectionManagerPlugin/TraceRmiConnectionManagerPlugin.md#connect-accept),
executes the back-end shell script in a Terminal, then waits for the resulting target trace. In
contrast to the previous system, the Terminal is the first and most basic interface presented.
Even if just about everything else goes wrong, the terminal should still be faithfully
operational:


![](images/GdbTerminal.png)


The Terminal is fully integrated into Ghidra's UI and so can be docked or undocked just like
the rest of Ghidra's windows. It provides fairly robust VT-100 emulation. Thus, the user
experience from the Terminal is nearly identical to using the same debugger outside of Ghidra.
This terminal-first approach also ensures that you interact with the target application's
standard I/O. This was not possible in the previous system, as we re-implemented the CLI using
the back end's `execute` method. The debugger's (and so also the target's) actual I/O
streams were hidden away within a GDB/MI wrapper.


Each launcher script sets up a — usually Python — environment, launches the
actual debugger, and provides a sequence of commands for it to load the Trace RMI plugin,
connect back to Ghidra, launch the actual target process, and start the target trace. At this
point, the plugin generally takes over, reacting to user and target events, accepting front-end
requests, and generally keeping Ghidra and the back end synchronized.


The list of launchers can be accessed in either of two places:
1) In the **Debugger → Configure and Launch ...** menu or more conveniently from the
**Launch** button in the main toolbar. This is the blue bug ![Debugger](../icons/debugger.png)
button near the top center. The **Configure and Launch ...** menu lists all available
launchers. Selecting one will prompt for its options then launch. To re-launch quickly, use the
**Launch** button. Clicking it will re-launch using the most recent launcher and
configuration for the current program. If this is the first launch of the given program, the
button will instead activate its drop-down menu. The drop-down is also accessible by clicking
the down arrow next to the **Launch** button. The drop-down lists all launchers that have
been previously configured for the current program. Clicking one will immediately launch the
program without prompting. The **Configure and Launch ...** sub-menu of the drop-down
functions exactly like in the **Debugger** menu.


The Terminal provides some fairly standard actions. Other keyboard control sequences,
notably **CTRL-C**, are interpreted by the terminal, rather than Ghidra's action system, to
achieve their expected behavior, e.g., interrupt.


### Copy


This is accessed using the toolbar button or the key sequence **CTRL-SHIFT-C**. As
expected, it copies the current selection to the system clipboard.


### Paste


This is accessed using the toolbar button or the key sequence **CTRL-SHIFT-V**. As
expected, it pastes the text contents of the system clipboard into the terminal, as if
typed.


### Find


This is accessed using the local drop-down menu or the key sequence **CTRL-SHIFT-F**. It
displays a dialog for searching the terminal's scrollback buffer.


### Find Next/Previous


These actions are accessed using the local drop-down menu or the key sequence
**CTRL-SHIFT-H** or **CTRL-SHIFT-G**, respectively. They repeat the last search in the
forward or backward direction.


### Select All


This is accessed using the local drop-down menu or the key sequence **CTRL-SHIFT-A**. It
selects all text in the terminal, including its scrollback buffer. If all the text is already
selected, then this selects nothing, so that pressing the keystroke twice is effectively
"Select None."


### Increase Font Size


This is accessed using the local drop-down menu or the key sequence **CTRL-SHIFT-PLUS**.
It increases the font size for this terminal.


### Decrease Font Size


This is accessed using the local drop-down menu or the key sequence **CTRL-MINUS**. It
decreases the font size for this terminal.


### Reset Font Size


This is accessed using the local drop-down menu or the key sequence **CTRL-0**. It resets
the font size for this terminal according to the theme's configuration'.


### Terminate


This action is accessed using the local drop-down menu. It will terminate the Terminal's
current session. Exactly what that means is determined by the Terminal's creator. In general,
it means to destroy the full debugging session associated with the Terminal. That may cause
related terminals, e.g., a secondary terminal for target I/O and associated target traces, to
be terminated as well. **NOTE:** This action is *not* implied by closing the Terminal
window. Closing the window with an active session merely hides it. It can be recalled using the
**Window → Terminals** menu. If the session has already been terminated (indicated by
an orange border) then closing the window will, in fact, destroy the Terminal.


## Development and Diagnostic Launchers


We currently provide a launcher for Trace RMI API exploration and
development: The "`raw python`" launcher runs Python in a Terminal window, connects a
Trace RMI client back to Ghidra, then starts a blank trace. Once running, it presents the
Python interpreter, with the `ghidratrace` and `ghidratrace.client` packages
imported into the local namespace. Thus, a developer can explore the API, invoke methods, and
observer how Ghidra reacts.


### Setup


If you have access to PyPI, setting up your Python 3 environment is done using Pip. Please
note the version specifier for Protobuf.


-
  ```

  python3 -m pip install protobuf==3.20.3

  ```


If you are offline, or would like to use our provided packages, we still use Pip, but with a
more complicated invocation:


-
  ```

  cd /path/to/ghidra_
  version/Ghidra/Debug
  python3 -m pip install --no-index -f Debugger-rmi-trace/pypkg/dist protobuf

  ```


### Options


- **`python` command**: This is the command or path to `python` version 3.
Python 2 is not supported.
- **Ghidra Language**: The LanguageID for the blank trace.
- **Ghidra Compiler**: The CompilerSpecID for the blank trace.


---

[← Previous: Launching a Target](../Debugger/GettingStarted.md) | [Next: GDB Integration →](../gdb/gdb.md)
