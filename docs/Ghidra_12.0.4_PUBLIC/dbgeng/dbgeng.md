[Home](../index.md) > [dbgeng](index.md) > Windows Kernel

# Debugger Launchers: Windows Debugger (WinDbg, dbgeng.dll)


Integration with WinDbg is achieved by implementing a console debugger in Python 3 based on
`dbgeng.dll` (via pybag). This DLL represents the Microsoft Windows Debugger engine, and
so is best suited for debugging Windows user-space targets. This DLL also backs WinDbg and
several other debuggers on Windows. By default, the launcher will search for this DLL in an
installation of the Windows Debugging Kits version 10. If it does not find it there, it will
probably crash with a message in the Terminal.


The following launchers based on Microsoft's `dbgeng.dll` are included out of the
box:


## Local


The plain "`dbgeng`" defaults to launching the current program as a user-mode process
on the local system. If there is no current program, this launcher cannot be used. Clearing the
**Image** option will cause this launcher to fail.


Please note on some system configurations, one of the debugger's dependencies
`dbghelp.dll` may get loaded from the system directory instead of from the WinDbg
installation, usually because a security product has pre-loaded it into the Python process. You
might work around this by copying the affected DLLs from your WinDbg installation into your
Python installation.


### Setup


Installing WinDbg is highly recommended. If you wish to forego installing WinDbg, you can
use the DLL provided with Windows, which is substantially less capable, by manually pointing
this connector to `C:\Windows\system32`. If you do this, some commands, e.g.
`.server`, will not be available.


If you have access to PyPI, setting up your Python 3 environment is done using Pip. Please
note the version specifier for Protobuf.


-
  ```

  python3 -m pip install pybag protobuf==3.20.3

  ```


If you are offline, or would like to use our provided packages, we still use Pip, but with a
more complicated invocation:


-
  ```

  cd C:\path\to\ghidra_
  version\Ghidra\Debug
  python3 -m pip install --no-index -f Debugger-rmi-trace\pypkg\dist -f Debugger-agent-dbgeng\pypkg\dist pybag protobuf

  ```


If you get an import error regarding `distutils`, it is due to a transitive
dependency on a buggy version of `capstone`. Work around it by installing
`setuptools`.


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
These are passed as is into WinDbg's "`CreateProcess`" function.
- **Use `dbgmodel`**: If `dbgmodel.dll` is available on the system, this
launcher will use it to populate the trace's object model. Without that DLL, the launcher
will invent its own model, roughly approximating the same, using just the information
available from `dbgeng.dll`. Disabling this option will prevent the launcher from
using `dbgmodel.dll`, even when it is available.
- **Path to `dbgeng.dll` directory**: By default, the launcher allows the
underlying `pybag` package to locate the Windows Debugger DLLs. This is typically
found by examining the registry for a Windows Kits 10 installation. Otherwise, it may check
its typical installation directory. This will *not* search the Windows system
directory, but you can configure it manually here. This option allows you to override this
search. For example, if you have installed WinDbg Preview or later from the Microsoft Store
and wish to use its DLLs, you will need to fill in this option.


Once running, you are presented with a command-line interface in Ghidra's Terminal. This CLI
accepts your usual WinDbg (kd) commands. You can escape from this CLI and enter a Python 3 REPL
by entering "`.exit`". This is not an actual kd command, but our implementation
understands this to mean exit the kd REPL. From the Python 3 REPL, you can access the
underlying Python-based API `pybag`. This is an uncommon need, but may be useful for
diagnostics and/or workarounds. To re-enter the kd REPL, enter "`repl()`".
Alternatively, if you are trying to quit, but typed "`.exit`", just type
"`quit()`" to terminate the session.


## Extended Local


The "`dbgeng-ext`" launcher extends the base `dbgeng` launcher adding extra
options (a la `IDebugClient`'s `CreateProcess2`).


### Options


- **Dir**: This is the starting directory for the process.
- **Env**: This is a composite string containg Environment Variable entries delineated
by '/0' separators. For example, you could redefine USERNAME and USERPROFILE with the entry
'USERNAME=SomeUser/0USERPROFILE=C:\Users\SomeUser'.
- **CreateFlags**: Flags used when creating the process, typically either
DEBUG_PROCESS(1) or DEBUG_ONLY_THIS_PROCESS(2) if you do not wish to follow spawned
processes. Other possible values are defined by processes.h's
CreateProcessCreationFlags.
- **CreateFlags (Engine)**: Engine-specific flags used when creating the process
(defined in dbgeng.h). Typically, these are set to 0.
- **VerifierFlags (Engine)**: Flags used by the Application Verifier. Typically unused,
but, if desired, CreateEngineFlags must include
DEBUG_ECREATE_PROCESS_USE_VERIFIER_FLAGS(2).


## Attach


This launcher allows the user to attach to a local running process. Options are the same as
those for the base dbgeng, except for ProcessId and AttachFlags


### Options


- **ProcessId**: The pid of the process you wish to attach to.
- **AttachFlags**: Flags used when attaching to the target process, typically
DEBUG_ATTACH_PROCESS(0). Other possible values are defined in dbgeng.h and determine whether
the attach should be invasive or not and the status of the process after attaching.


## Remote


This launcher connects to a remote debugger that has opened a port for remote control.


### Options


- **Connection**: This is the connection string specifying the transport options for
communicating with the remote debugger. A typical example might be
'tcp:port=12345,server=192.168.0.2' for a debugger that has issued the command
  ```
  .server tcp:port=12345
  ```


## Process Server


The "`dbgeng-svrcx`" launcher extends the base dbgeng launcher adding an option for
connecting through a remote process server.


### Options


- **Connection**: This is the connection string specifying the transport options for
communicating with the remote server. A typical example might be
'tcp:port=12345,server=192.168.0.2' for a process server launched on the machine at
192.168.0.2 using:
  ```
          dbgsrv -t tcp:port=12345
  ```


## Windows Kernel


This version of the dbgeng should be used for kernel-debugging of a remote machine. Options
are the same as the base dbgeng, except for the connection-string arguments. For remote
debugging, the target machine should be booted with the appropriate options, set using BCDEDIT
or the equivalent, such as:


-
  ```

  bcdedit /debug ON
  bdcedit /dbgsettings NET HOSTIP:IP PORT:54321 KEY:1.1.1.1

  ```


where IP= the address of the machine runing Ghidra.


### Options


- **Arguments**: This is the connection string specifying the transport options for
communicating with the remote target. A typical example might be
'net:port=54321,key=1.1.1.1'.'


- **Type**: The type of kernel connection, either "Remote", "Local", or "EXDI".
"Remote", the most common type, indicates two-machine debugging over various possible
connection media, e.g. Ethernet, serial, USB, etc. "Local" is used for limited introspection
into the target on which the debugger is running. "EXDI" is arguably the most exotic type -
it essentially simulates the normal "Remote" connection using the gdb Remote Serial Protocol.
It can be used when connecting to gdbstubs in platforms, such as QEMU, VMWare, Trace32,
etc.


### EXDI


Setup for EXDI connections is fairly complicated and difficult to get correct. The argument
string typically should be something like:


-
  ```

  exdi:CLSID={29f9906e-9dbe-4d4b-b0fb-6acf7fb6d014},Kd=Guess,DataBreaks=Exdi

  ```


The CLSID here should match the CLSID in the **exdiConfigData.xml** file in the debugger
architectural directory. If windbg has been run using EXDI at some point, there will also be an
entry in the System Registry for this CLSID. The InprocServer32 subentry for this CLSID in the
Registry should point to a copy of ExdiGdbSrv.dll, typically the one in the same directory.
This DLL must reside somewhere that the debugger has permission to load from, i.e. not in the
WindowsApps directory tree. The **exdiConfigData** file should be configured for the target
you're using. We heavily recommend using **displayCommPackets==yes**, as many of the tasks
take considerable time, and this is the only indicator of progress.


The **Kd=Guess** parameter causes the underlying engine to scan memory for the kernel's
base address, which will probably not be provided by the gdbstub. (**Kd=NtBaseAddr** is also
a valid option, as is eliminating the parameter, but, currently, we have no idea how to point
the configuration at a correct value. Using this option will cause the load to spin
pointlessly.) If you can, we highly recommend breaking the target near the base address, as the
search proceeds down through memory starting at the current program counter. If the difference
between the PC and the base address is large, the loading process will punt before useful
values are detected. If anyone understand how to extend this search (or knows how to set the
base address to sidestep the scan), we would really love some guidance.


## TTD (Time-Travel Debugging)


This is an extension to our launcher for the Windows Debugger to support TTD. WinDbg TTD
uses `event:ticks` to denote its times. This corresponds well to Ghidra's
`snapshot:steps` syntax, when we let snapshot be an event and ticks count the number
of instruction steps. Upon expanding the "Events" node in the Model tree, we create a snapshot
for every TTD event, including thread create/terminate, module load/unload, syscall, and other
asynchronous changes. Then, when Ghidra navigates to a schedule of the form
`snapshot:steps`, we command WinDbg to navigate to the corresponding
`event:ticks` instead of using Ghidra's emulator. Conversely, time navigation from
the WinDbg CLI will correspondingly navigate Ghidra. Thus, the two are synchronized in time. We
also add *reverse* variants of the **Go** and **Step** control commands.


### Options


This launcher has basically the same options as the WinDbg launcher, except that arguments
are not included and the DLL path must contain `TTDReplay.dll` and the scripts that
implement TTD. These are most easily obtained by installing WinDbg Preview or later.


### Setup


Depending on how you acquire WinDbg TTD, you may need to copy the installation to a
directory Ghidra is allowed to access. It's best not to try cherry-picking files. Just
copy/unpack the entire WinDbg installation. Point the launch dialog to the directory containing
`dbgeng.dll` as usual.


**NOTE:** It's possible, especially if you have anti-virus software installed, that
`dbghelp.dll` is forcefully loaded into the Python process before our connector package
tries to load `dbgeng.dll`. This can cause `dbghelp.dll` to be loaded from
`System32`, but `dbgeng.dll` to be loaded from the WinDbg installation, often
leading to DLL compatibility problems. This usually manifests in module load and/or Python
import errors. The only real way to be sure is to use a system utility and inspect the DLLs
loaded by the `python.exe` process. You may be able to work around the issue by copying
`dbghelp.dll` (and any other affected WinDbg DLLs) from the WinDbg installation into
your Python installation, e.g., `C:\Python313\dbghelp.dll`.


---

[← Previous: TTD (Time-Travel Debugging)](dbgeng.md) | [Next: drgn Integration →](../drgn/drgn.md)
