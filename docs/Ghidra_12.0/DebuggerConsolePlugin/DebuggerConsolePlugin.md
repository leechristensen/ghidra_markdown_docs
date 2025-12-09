[Home](../index.md) > [DebuggerConsolePlugin](index.md) > Debug Console

# Debugger: Console


![](images/DebuggerConsolePlugin.png)


The console logs messages from Ghidra related to the debugger. This no longer includes
messages sent to the application log, but only messages that plug-ins deliberately deliver to
this console. Some log messages include an action context, allowing plug-ins to offer actions
on that message. These are said to be "actionable" messages. A noteworthy example is when
navigating to a module that could not be automatically mapped from the current project. Instead
of displaying a prompt, it will log a message and suggest actions to resolve the issue. A
successful resolution typically removes the message from the log. Note that additional actions
may be available from the context menu. Some messages communicate progress of a background
task. These may have a progress bar, and the associated message may change over time. These
entries may offer a cancel action.


By default, the log is sorted so that actionable messages appear at the top. Then, it is
sorted by descending date, so that the most recent messages appear at the top. Like any other
Ghidra table, it can customized and filtered. Note that the filter box is at the top, because
we anticipate a command-line input in the future, which we would like to place at the
bottom.


## Table Columns


The table has the following columns:


- Icon - an icon to identify the type, topic, or source of a message.
- Message - the message itself.
- Actions - if actionable, a row of buttons for available actions.
- Time - the time the message was generated in 24-hour HH:mm:ss.SSS format.


## Actions


Not considering actions for "actionable" messages, the console provides the following:


### Clear


Removes all messages, including actionable messages, from the log.


### Select None


Resets the selection, usually so table scrolling can be restored to "normal."


### Cancel


For a tasks displaying a progress message in the console, this action will cancel the
task.


---

[← Previous: Troubleshooting](../Debugger/Troubleshooting.md) | [Next: Copy Actions →](../DebuggerCopyActionsPlugin/DebuggerCopyActionsPlugin.md)
