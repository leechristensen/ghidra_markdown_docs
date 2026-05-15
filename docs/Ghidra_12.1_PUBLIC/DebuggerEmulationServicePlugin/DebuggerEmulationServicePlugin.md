[Home](../index.md) > [DebuggerEmulationServicePlugin](index.md) > Emulation

# Debugger: Emulation Service


This service plugin provides emulation to the [Trace
Manager](../DebuggerTraceManagerServicePlugin/DebuggerTraceManagerServicePlugin.md) and provides actions for launching emulated traces from programs, i.e., without
requiring a connected debugger. Please note that "pure emulation" of a target program, while it
doesn't require a platform to execute the target natively, it typically does require
significant state initialization and dependency stubbing, except in limited circumstances.


## Actions


### Emulate Program


This action is available whenever a program is active. It will create a new trace suitable
for "pure emulation" of the current program starting at the current address. More precisely, it
will open a new blank trace, initialize it with the current program's memory map, allocate a
stack, and create a thread whose program counter is initialized to the current address and
whose registers are initialized to the register context at that address. Optionally, any other
initialization can be done by manually modifying the trace in the UI, or using a script. The [emulator
controls](../DebuggerControlPlugin/DebuggerControlPlugin.md#emulation-actions) can then be used.


To control the initial stack allocation, create a `STACK` block in the target
program database before emulating. If the stack is already in the target image's memory map,
create an overlay block named `STACK`. This will initialize the stack pointer
without modifying the emulator's memory map. Note that customizing the stack initialization may
prevent you from adding a second thread.


### Add Emulated Thread


This action is available whenever a "pure emulation" trace is active. It spawns a new thread
in the current trace suitable for emulation starting at the current address. More precisely, it
will allocate another stack and create a new thread whose program counter is initialized to the
current address and whose registers are initialized to the register context at that address.
Optionally, other registers can be initialized via the UI or a script. The new thread is
activated so that control actions will affect it by default.


### Configure Emulator


This action is always available. It lists emulators available for configuration. Selecting
one will set it as the current emulator. The next time emulation is activated, it will use the
selected emulator.


### Invalidate Emulator Cache


This action is available whenever a trace is active. It invalidates all the scratch
snapshots in the current trace, which are used for caching emulated machine states. This is
recommended when you change the emulator configuration, when you change the Sleigh code of an
emulated breakpoint, or when you patch the trace database. If you do not invalidate the cache,
the effects of your change may not appear, since the trace manager may recall a cached snapshot
instead of actually emulating.


---

[← Previous: Trace Management](../DebuggerTraceManagerServicePlugin/DebuggerTraceManagerServicePlugin.md) | [Next: Memory →](../DebuggerMemoryBytesPlugin/DebuggerMemoryBytesPlugin.md)
