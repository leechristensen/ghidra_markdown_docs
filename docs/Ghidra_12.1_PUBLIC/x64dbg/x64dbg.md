[Home](../index.md) > [x64dbg](index.md) > Remote via SSH

# Debugger Launchers: x64dbg Debugger


Integration with **`x64dbg`** is achieved using the Python 3
API **`x64dbg-automate-pyclient`** and underlying plugin **`x64dbg-automate`**, kindly provided by Darius Houle
(see https://github.com/dariushoule/x64dbg-automate & x64dbg-automate-pyclient).  The console
debugger launches a full **`x64dbg`** session by default, synchronized with the
Ghidra debugger UI.


Local launchers are included, one for a local process and one for a local pid, and ssh equivalents:


## Local


The plain "`local-x64dbg`" launches the current program as a user-mode process
on the local system. If there is no current program, the user may specify the **Image** option
explicitly or launch x64dbg without a target.


### Setup


Make sure you have installed the executables for **`x64dbg-automate`** (typically the contents
of x64dbg/build[32|64]/Release) in the plugins directory for **`x64dbg`** (release/x[32|64]/plugins).


If you have access to PyPI, setting up your Python 3 environment is done using Pip. (Please
note the version specifier for Protobuf.)


-
  ```

  python3 -m pip install x64bag_automate protobuf

  ```


If you are offline, or would like to use our provided packages, we still use Pip, but with a
more complicated invocation:


-
  ```

  cd C:\path\to\ghidra_
  version\Ghidra\Debug
  python3 -m pip install --no-index -f Debugger-rmi-trace\pypkg\dist -f Debugger-agent-x64dbg\pypkg\dist x64dbg_automate protobuf

  ```


### Options


- **`python` command**: This is the command or path to the Python interpreter. It
must be version 3. Python 2 is not supported.
- **Image**: This is the path to the target binary image (EXE file). Ghidra will try to
fill this in based on information gathered when the current program was imported. If the file
exists and is executable on the local machine, it will be filled in automatically. Otherwise,
it is up to you to locate it. **NOTE:** If you have patched the current program database,
these changes are *not* applied to the target. You can either 1) apply the same
patches to the target once it is running, or 2) export a patched copy of your image and
direct this launcher to run it.
- **Arguments**: These are the command-line arguments to pass into the target process.
- **Dir**: The initial directory for the target process.
- **Path to `x64dbg.exe`**: where the x64dbg executable resides (or the x32dbg executable
for 32-bit programs).


Once running, you are presented with a command-line interface in Ghidra's Terminal. This CLI
accepts your usual x64dbg native commands. You can escape from this CLI and enter a Python 3 REPL
by entering "`.exit`". This is not an actual x64dbg command, but our implementation
understands this to mean exit the x64dbg REPL. From the Python 3 REPL, you can access the
underlying Python-based API `x64dbg_automate`. This is an uncommon need, but may be useful for
diagnostics and/or workarounds. To re-enter the x64dbg REPL, enter "`repl()`".
Alternatively, if you are trying to quit, but typed "`.exit`", just type
"`quit()`" to terminate the session.


## Attach


This launcher allows the user to attach to a local running process. Options are the same as
those for the base x64dbg, except **Process Id** replaces **Image**.


### Options


- **ProcessId**: The pid of the process you wish to attach to.


## Remote via SSH


"`ssh-x64dbg`" is the remote equivalent to "`x64dbg`";
"`ssh-x64dbg-attach`" is the remote equivalent to "`x64dbg-attach`".


### Setup


Instructions are indentical to those above but executed on the remote machine.


- **ssh command**: The ssh command to execute, optionaly with full path.
- **[User@]Host**: This is the host name of the target system, optionally including a
user name. This is passed as is to `ssh`, which may interpret it according to local
configuration.
- **Remote Trace RMI Port**: An available TCP port on the target system, which will
listen for x64dbg's Trace RMI connection and forward it back to Ghidra.
- **Extra `ssh` arguments**: These are extra arguments to pass to `ssh`.
They are inserted immediately after the `ssh` command but before the host name. Beware
that syntax errors may cause strange behavior, and that not all features may be compatible
with this launcher.


---

[← Previous: Local](x64dbg.md) | [Next: Connection Manager →](../TraceRmiConnectionManagerPlugin/TraceRmiConnectionManagerPlugin.md)
