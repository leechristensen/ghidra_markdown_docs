[Home](../index.md) > [DebuggerTraceViewDiffPlugin](index.md) > Comparing Times

# Debugger: Comparing Times


![](images/DebuggerTraceViewDiffPlugin.png)


A common strategy in dynamic analysis is to compare machine
state between two points in time. To this end, the "trace diff" plugin extends the [Dynamic Listing](../DebuggerListingPlugin/DebuggerListingPlugin.md) to provide
side-by-side comparison of bytes between points in time. When active, listings for both times
are displayed, and the byte value differences between them are highlighted. **NOTE:** This
does not compare annotations. It only compares raw byte values. Additionally, all stale values
are ignored, i.e., to show as a difference, the memory must be observed at *both* points
in time, and the values must differ.


**NOTE:** This plugin only facilitates the comparison of memory displayed in listings. To
compare registers or expressions, use the respective windows: [Registers](../DebuggerRegistersPlugin/DebuggerRegistersPlugin.md) and [Watches](../DebuggerWatchesPlugin/DebuggerWatchesPlugin.md). By navigating back
and forth between two points in time, using the [Time Window](../DebuggerTimePlugin/DebuggerTimePlugin.md), the differences are
displayed in red.


## Actions


The plugin adds actions to the main Dynamic Listing. When active, additional actions are
present.


### Compare


This action is available whenever a trace is active in the main listing. It prompts for an
alternative point in time:


![](images/DebuggerTimeSelectionDialog.png)


The snapshot table is exactly the same as that in the [Time Window](../DebuggerTimePlugin/DebuggerTimePlugin.md). In most cases, simply
selecting a snapshot suffices.


Perhaps the most common use of this action is to identify where a given variable is stored
in memory. The trace saves a record of observed memory from the debugging session. Comparing
snapshots thus identifies changes over time; however, there is no guarantee that the desired
variable was ever observed. Assuming the general vicinity of the variable is known, e.g.,
"somewhere in the .data section," the [Read Memory](../DebuggerListingPlugin/DebuggerListingPlugin.md#read-memory)
action can ensure its value is recorded. Of course, it can also read "all memory," but that
operation and the follow-on comparison could take time. In general, the procedure to locate a
variable is to capture a baseline, execute the target until the variable has changed, capture
again, then compare:


1. Execute the target up to a baseline, and take note of the variable's value, as displayed
by the target program.
2. Consider naming the current snapshot for later reference, using the [Rename Current
Snapshot](../DebuggerTimePlugin/DebuggerTimePlugin.md#rename-snapshot) action. Ideally, the name should indicate the variable's value.
3. Select the range of memory believed to contain the variable. Consider using the [Modules](../DebuggerModulesPlugin/DebuggerModulesPlugin.md) or [Regions](../DebuggerRegionsPlugin/DebuggerRegionsPlugin.md) window to form the
selection.
4. Use the [Read Memory](../DebuggerListingPlugin/DebuggerListingPlugin.md#read-memory)
action to ensure the variable's value is stored in the trace.
5. Allow the target to execute until the variable has changed. Ideally, execute as little as
necessary, so that few or no other variables change.
6. Execution will cause the trace to advance some number of snapshots. Once suspended, it's
a good idea to rename the current snapshot, again indicating the variable's new value and/or
the cause of its change.
7. Repeat the selection and capture steps to ensure the variable's new value is stored in
the trace.
8. Use this **Compare** action and select the baseline snapshot. It's easy to locate in
the table if named appropriately.


Assuming the variable is actually contained in the captured memory ranges, then it should be
among the differences shown. If too many differences appear, repeat the experiment. Consider
executing less code, establishing a new baseline, taking the intersection of the results, etc.
Remember, the variable's storage should encode its value.


Optionally, the specified time may also include emulation. See the [Go To Time](../DebuggerTimePlugin/DebuggerTimePlugin.md#goto-time) action for
the syntax of the **Time Schedule** expression. For simple schedules, the step buttons
provide convenient forward and backward changes to the emulation schedule. Perhaps the most
common use of this is to see what changes from executing an isolated block of code. Ideally,
the baseline is a relatively complete capture or represents the present in a live session, so
that the emulator does not depend on un-recorded state:


1. Execute the target up to a baseline, probably using a breakpoint at the start of the
interesting block of code.
2. Keeping the target alive, use the [Emulator
Control](../DebuggerControlPlugin/DebuggerControlPlugin.md#emu-actions) and/or [Go To Time](../DebuggerTimePlugin/DebuggerTimePlugin.md#goto-time) actions to
reach the end of the interesting block.
3. Use this **Compare** action and select the baseline snapshot.


Alternatively, if the number of steps to reach the end of the block is already known, just
use the emulation expression in the **Compare** action's dialog. **NOTE:** When used this
way, the baseline snapshot will be in the left pane, and the emulated snapshot in the right,
which is opposite the result from the previous procedure.


In either case, this will highlight any memory that was modified by the emulated code. Of
course, this could also be accomplished by setting a second breakpoint and allowing the target
to execute; however, emulation does not necessarily require large memory captures. It only
observes what it needs, and its internal state contains everything that changed. Furthermore,
if establishing the baseline is difficult, emulation allows the target to remain at that
baseline. Assuming sufficient state is captured, emulation can also be performed offline,
without a live target.


### Previous / Next Difference


These actions are only present when the comparison listing is visible. Each is available
when there exists a previous or next range from the main listing's cursor. Clicking the action
navigates to the nearest address in that range.


---

[← Previous: P-code Stepper](../DebuggerPcodeStepperPlugin/DebuggerPcodeStepperPlugin.md) | [Next: Platform Selection →](../DebuggerPlatformPlugin/DebuggerPlatformPlugin.md)
