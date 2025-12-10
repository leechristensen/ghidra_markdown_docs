[Home](../index.md) > [lldb](index.md) > macOS Kernel

# Debugger Launchers: LLDB


Integration with LLDB is achieved using a plugin for LLDB's Python Scripting Bridge. It is
well-suited for debuging user-space targets on a variety of platforms. It is the *de
facto* debugger for macOS. It can be obtained by installing Xcode from the App Store.
Though it may require a bit more careful configuration, it can also be obtained from other
repositories like `brew`.


The following launchers based on the LLDB Debugger are included out of the box:


## Local


The plain "`lldb`" launch script defaults to launching the current program as a
user-mode process on the local system. If there is no current program, or if you clear the
**Image** option, this launcher will only start `lldb` and get it connected to a
Ghidra trace. You may then manually start or connect to your target. Note that this may also
require manual mapping of your program database(s) to the target memory.


### Setup


You must have LLDB installed on the local system, and it must support Python 3 scripting. If
you have access to PyPI, setting up your Python 3 environment is done using Pip. Please note
the version specifier for Protobuf.


-
  ```

  python3 -m pip install psutil protobuf==3.20.3

  ```


If you're using `lldb` from the Android NDK and do not have Pip, see [Setup for Android NDK](#setup-for-android-ndk)


If you are offline, or would like to use our provided packages, we still use Pip, but with a
more complicated invocation:


-
  ```

  cd /path/to/ghidra_
  version/Ghidra/Debug
  python3 -m pip install --no-index -f Debugger-rmi-trace/pypkg/dist -f Debugger-agent-lldb/pypkg/dist psutil protobuf

  ```


Beware that LLDB may embed a different Python interpreter than your system's default. If you
are still getting import errors, check the version that LLDB embeds:


-
  ```

  (bash)$ lldb
  (lldb) script
  >>> import sys
  >>> sys.version

  ```


Note the version and ensure that you are invoking Pip with that version. Supposing
`sys.version` indicates 3.10, you should invoke Pip using `python3.10 -m
pip`.


### Options


- **Image**: This is the path to the target binary image (executable). Ghidra will try
to fill this in based on information gathered when the current program was imported. If the
file exists and is executable on the local machine, it will be filled in automatically.
Otherwise, it is up to you to locate it. **NOTE:** If you have patched the current program
database, these changes are *not* applied to the target. You can either 1) apply the
same patches to the target once it is running, or 2) export a patched copy of your image and
direct this launcher to run it.
- **Arguments**: These are the command-line arguments to pass into the target. These are
passed as is to LLDB's "`settings set target.run-args ...`" command.
- **`lldb` command**: This is the command or path to LLDB. We recommend version
15 or later.
- **Run command**: This is the LLDB command to actually launch the target. In most cases
this should include "`--stop-at-entry`", since this will assure you an initial break
and a chance to enable your breakpoints.
- **Target TTY**: Depending on your target and/or personal preference, you may opt to
separate the debugger's and the target's I/O. If you check this box, the launcher will use
LLDB's "`setting set target.output-path ...`" command (and similar for the input) to
direct the target's I/O to a second Terminal window.


Once running, you are presented with LLDB's command-line interface in Ghidra's Terminal.
This is the *bona fide* LLDB command-line interface, so it has all the functionality you
would expect. If you command LLDB from this shell, the plugin will keep Ghidra in sync. The
terminal can be used to interact with the target application when it is running. The plugin
provides an additional set of commands for managing the connection to Ghidra, as well as
controlling trace synchronization. These are all in the "`ghidra`" category. You can use
tab completion to enumerate the available commands and LLDB's "`help`" command to
examine their documentation.


## Remote


This launcher can target any TCP-based GDB stub that is compatible with a local copy of
`lldb`. Essentially, it just starts `lldb` and then enters


-
  ```

  gdb-remote [host]:[port]

  ```


into it. It is best to test this command outside of Ghidra to be sure everything is
compatible before using this launcher. This launcher does not require an image, nor does it
create your target. Thus, it can be used without a current program.


### Setup


On your local system, follow the steps given in [LLDB Setup](#setup). Your
version of LLDB must be compatible with the stub (e.g., `gdbserver`) on the target
system. There are no additional requirements on the target system.


**NOTE:** The target program image must match that imported in Ghidra, or else things may
not map or synchronize correctly.


### Options


- **Host**: The host name of the target stub.
- **Port**: The TCP port of the target stub.
- **Architecture** (optional): If the stub does not describe its architecture to LLDB,
you must set it before connecting. This is passed as is to "`settings set
target.default-arch ...`" immediately before the "`gdb-remote ...`" command.
- **`lldb` command**: This works the same as in LLDB.


## macOS Kernel


This launcher connects to macOS kernels booted in debug-mode using `lldb`.
Essentially, it just starts `lldb` and then enters


-
  ```

  kdp-remote [host]

  ```


It is best to test this command outside of Ghidra to be sure everything is compatible before
using this launcher. This launcher does not require an image, nor does it create your target.
Thus, it can be used without a current program.


### Setup


On your local system, follow the steps given in [LLDB Setup](#setup). Before
connecting to the target kernel, you must force an NMI on the target to ready the connection.
On actual hardware, this is typically achieved by some button sequence, e.g. **L/R-Options +
Power** or **Command+Option+Control+Shift+Esc**. In a VM, you may have to pause the VM and
modify its state. For example, by cd'ing to the VM's container and issuing the command:


-
  ```

  perl -i -pe 's/(?<=pendingNMI\x00{4})\x00/\x01/' macOS_15-1234567.vmss

  ```


### Options


- **Host**: The host IP of the target kernel.
- **Architecture** (optional): If the kernel does not describe its architecture to LLDB,
you must set it before connecting. This is passed as is to "`settings set
target.default-arch ...`" immediately before the "`kdp-remote ...`" command.
- **`lldb` command**: This works the same as in LLDB.


## Via SSH


This works the same as the [GDB via SSH](../gdb/gdb.md#via-ssh) launcher,
but runs `lldb` on a remote system via `ssh`.


## Android


This has the same options as the [LLDB via SSH](#via-ssh) launcher, which are
necessary for connecting to the Android debugger, but executes via the normal lldb
mechanism.


### Setup for Android NDK


If you're using the copy of `lldb` included with the Android NDK (Native Development
Kit), it may not include `pip`. Notably, this is the case on Windows at the time of
writing. Fortunately, you can retrieve the components to install Pip into the NDK from an
official Python distribution.


1. First, figure out the version of Python that is embedded in the NDK's build of LLDB, and
get its path. (If you know the path to lldb, you probably already know the path to its
Python.) From a Windows Command Prompt or Powershell:
  ```
  PS> C:\path\to\android-ndk\...\lldb
  (lldb) script
  >>> import sys
  >>> sys.version
  [copy down the version indicated]
  >>> sys.path
  [look for the paths ending with Lib and DLLs, and copy them down]
  ```
2. Now, obtain the same version of Python from the official Python website, and install or
unpack it.
3. Locate your new installation of Python. If you don't already know where it landed, this
can be found by examining the Properties of the Python shortcut in your Start Menu.
4. There should be a `Lib\ensurepip` directory in the official Python installation.
Copy this into the same place in the Android NDK's build of Python.
5. There are also three native modules that need to be copied from the official Python's
`DLLs\` directory to the same in the NDK's build. This is to support SSL for
downloading packages from PyPI: (Substitue the ??'s appropriately.)
- `_ssl.pyd`
- `libssl-??.dll`
- `libcrypto-??.dll`
6. We should now have enough to bootstrap the NDK's Python with Pip. Again at the Windows
Command Prompt or Powershell:
  ```
  PS> C:\path\to\android-ndk\...\python -m ensurepip
  PS> C:\path\to\android-ndk\...\python -m pip install ...
  ```
See the [Setup](#setup) section for the arguments to pass to `pip install
...`.


---

[← Previous: Via SSH](lldb.md) | [Next: WinDbg (dbgeng.dll) Integration →](../dbgeng/dbgeng.md)
