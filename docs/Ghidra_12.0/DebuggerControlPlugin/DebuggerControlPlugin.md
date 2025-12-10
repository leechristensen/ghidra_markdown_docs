[Home](../index.md) > [DebuggerControlPlugin](index.md) > Control and Machine State

# Debugger: Control and Machine State


This plugin presents actions for controlling targets and modifying machine state. It
provides a drop-down action in the main toolbar for choosing what to control for the current
target: The live target, the integrated emulator, or the recorded trace. Only those control
actions suitable for the selection are displayed. Machine-state edits and breakpoint commands
throughout the UI are directed accordingly.


## Actions


The plugin provides several actions, but only certain ones are displayed, depending on the
current mode.


### Control Mode


This action changes the mode for the active trace and, if applicable, its associated live
target. It is always displayed, but only available when a trace is active. The possible modes
are:


- ![Target](../icons/record.png) **Control Target w/Edits
Disabled:** The default, this presents actions for controlling the live target but rejects
all machine-state edits. Breakpoint commands are directed to the live target. When active,
the UI automatically follows the latest snapshot recorded, and navigating back in time is not
permitted. If the target is terminated and the trace remains open, the mode is automatically
switched to **Control Trace**.
- ![Target](../icons/write-target.png) **Control Target:** This
presents actions for controlling the live target and directs edits to the live target.
Breakpoint commands are directed to the live target. When active, the UI automatically
follows the latest snapshot recorded, an navigating back in time is not permitted. If the
target is terminated and the trace remains open, the mode is automatically switched to
**Control Emulator**.
- ![Trace](../icons/video-x-generic16.png) **Control Trace w/Edits
Disabled:** This presents actions for navigating trace snapshots but rejects all
machine-state edits. Breakpoint commands are directed to the emulator.
- ![Trace](../icons/write-trace.png) **Control Trace:** This
presents actions for navigating trace snapshots. It directs all edits to the trace database.
Edits are generally always accepted, and they are applied directly to the trace. Breakpoint
commands are directed to the emulator.
- ![Emulator](../icons/write-emulator.png) **Control Emulator:** This
presents actions for controlling the integrated emulator. Breakpoint commands are directed to
the emulator. This can be used for interpolating and extrapolating execution from the current
snapshot, without affecting the live target. It directs edits to the integrated emulator by
generating patch steps and appending them to the emulation schedule. See the [Go To Time](../DebuggerTimePlugin/DebuggerTimePlugin.md#go-to-time) action.
Essentially, the change is applied in the trace's scratch space, leaving the original
recording in tact. Due to implementation details, a thread must be selected, even if edits
only affect memory. Additionally, the disassembly context register cannot be modified.


## Target Control Actions


These actions are visible when a **Control Target** mode is selected. They are available
only when the current trace has an associated live target. Commands are directed to the focused
object or a suitable substitute.


### Resume ![Resume](../icons/resume.png)


Allow the current target to resume execution. Other debuggers may call this "continue" or
"go." If successful, the target enters the "running" state until it is interrupted or
terminated. This is available when the target is currently stopped.


### Interrupt ![Interrupt](../icons/interrupt.png)


Interrupt the current target's execution. Other debuggers may call this "break," "suspend,"
or "stop." If successful, the target enters the "stopped" state. This is available when the
target is currently running.


### Kill ![Kill](../icons/kill.png)


Kill the current target. Other debuggers may call this "terminate" or "stop." This may
consequently close the current trace. If successful, the target enters the "terminated" state.
This is always available for a live target.


### Disconnect ![Disconnect](../icons/disconnect.png)


Disconnect from the current target's debugger. This usually causes the connected debugger to
terminate and likely kill its targets. This may consequently close the current trace (and
perhaps others). This is always available for a live target.


### Step Into ![Into](../icons/stepinto.png)


Step the current target to the next instruction. This is available when the target is
currently stopped. If successful the target may briefly enter the "running" state.


### Step Over ![Over](../icons/stepover.png)


Step the current target to the next instruction in the current subroutine. This is available
when the target is currently stopped. If successful the target may briefly enter the "running"
state.


### Step Out ![Finish](../icons/stepout.png)


Allow the current target to finish the current subroutine, pausing after. This is available
when the target is currently stopped. If successful the target may briefly enter the "running"
state.


### Step Extended (Repeat Last) ![Last](../icons/steplast.png)


Perform a target-defined step, perhaps the last (possibly custom) step. This is available
when the target is currently stopped. If successful the target may briefly enter the "running"
state.


## Trace Navigation Actions


These actions are visible when a **Control Trace** mode is selected. They are available
when there is an active trace.


### Snapshot Backward ![Backward](../icons/2leftarrow.png)


This activates the previous snapshot. All windows displaying machine state will show that
recorded in the activated snapshot. This is available only when there exists a snapshot
previous to the current.


### Snapshot Forward ![Forward](../icons/2rightarrow.png)


This activates the next snapshot. All windows displaying machine state will show that
recorded in the activated snapshot. This is available only when there exists a snapshot after
the current.


## Emulation Actions


These actions are visible when the **Control Emulator** mode is selected. They are
available when there is an active trace. Commands are directed to the integrated emulator for
the current trace.


### Resume ![Resume](../icons/resume.png)


Allow the emulator to resume execution. This is available when no other integrated emulator
is running. A monitor dialog is presented during execution, but the GUI remains responsive.
Only one emulator can be run from the GUI at a time. If the current snapshot represents the
live target, the emulator may read additional machine state from the live target. For
non-contrived programs, the emulator will likely be interrupted, since some instructions and
system calls are not yet supported. It could also start executing from unmapped memory or enter
an infinite loop. If it seems to carry on too long, interrupt it and examine.


### Interrupt ![Interrupt](../icons/interrupt.png)


Interrupt the currently-running emulator. This is available when any integrated emulator is
running. In most cases, this is the emulator for the current trace, but it may not be.
Canceling the dialog for an emulation task will also interrupt the emulator. Upon interruption,
the emulation schedule is noted and the snapshot displayed in the GUI.


### Step Back ![Back](../icons/stepback.png)


Steps the emulator to the previous instruction, by flow. This is available when the current
snapshot includes emulated steps. This operates by repeating the current emulation schedule
with one less step. Thus, it effectively steps backward, heeding the proper control flow. While
not common, if emulation to the current snapshot took a good bit of time, then stepping
backward will likely take about the same amount of time.


### Step Into ![Into](../icons/stepinto.png)


Steps the emulator to the next instruction, by flow. This is available when there is an
active thread. At worst, this operates by repeating the current emulation schedule with one
more step of the current thread. In most cases, this can use the cached emulator for the
current snapshot and advance it a single step. Note that "Step Over" is not currently supported
by the emulator.


### Skip Over ![Over](../icons/skipover.png)


Skips the emulator over the current instruction, ignoring flow. This is available when there
is an active thread. At worst, this operates by repeating the current emulation schedule with
an added skip for the current thread. In most cases, this can use the cached emulator for the
current snapshot and advance it by skipping once. Note that this *skips* the
instruction. Thus, when used on a "call" instruction, all effects and side-effects of the
subroutine are averted. This is not the same as "*Step* Over," which is not currently
supported by the emulator.


## Recommendations


The default mode is **Control Target w/Edits Disabled**, because in most cases, this is
the desired behavior. When the target dies, the mode becomes **Control Trace w/Edits
Disabled**. For the most part, modifying the recorded trace itself is discouraged. There are
few reasons to edit a trace, perhaps including 1) Hand-generating an experimental trace; 2)
Generating a trace from a script, e.g., importing an event log, recording an emulated target;
3) Patching in state missed by the original recording. Be wary of **Control Trace** mode,
especially after emulating, since you could accidentally edit scratch space in the trace. It is
allowed but can produce non-intuitive and erroneous results, since the emulator caches its
snapshots in scratch space.


To modify state in a live target, use the **Control Target** mode. **NOTE:** Some UI
components will also require you to toggle a write protector. This also affects scripts that
use the state editing service. However, disabling edits cannot prevent a script from directly
accessing Ghidra's Target API to modify a target. Nor can it prevent edits via the connected
debugger's command-line interpreter. The following components all use the service: [Dynamic Listing](../DebuggerListingPlugin/DebuggerListingPlugin.md), [Memory (Dynamic
Bytes)](../DebuggerMemoryBytesPlugin/DebuggerMemoryBytesPlugin.md), [Registers](../DebuggerRegistersPlugin/DebuggerRegistersPlugin.md), and [Watches](../DebuggerWatchesPlugin/DebuggerWatchesPlugin.md).


---

[← Previous: Variable Hovers](../VariableValueHoverPlugin/VariableValueHoverPlugin.md) | [Next: Memview Plot →](../DebuggerMemviewPlugin/DebuggerMemviewPlugin.md)
