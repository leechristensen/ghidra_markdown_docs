[Home](../index.md) > [DebuggerWatchesPlugin](index.md) > Watches

# Debugger: Watches


![](images/DebuggerWatchesPlugin.png)


Watches refer to expressions which are evaluated each pause in order to monitor the value of
variables in the target machine state. The watch variables are expressed in Sleigh and
evaluated in the current thread's context at the current point in time. If the current trace is
live and at the present, then the necessary target state is retrieved and recorded. The watch
can be assigned a data type so that the raw data is rendered in a meaningful way. When
applicable, that data type can optionally be applied to the trace database. Some metadata about
the watch is also given, e.g., the address of the value.


The watch window uses colors to hint about changes in and freshness of displayed values. By
default, changed values are displayed in red, and stale values are displayed in dark grey. A
*stale* value is one which depends on any register or memory whose contents are not
known. The value displayed is that computed from the last recorded contents, defaulting to 0
when never recorded. A *changed* watch is one whose value has just changed. For example,
if a value changes as result of stepping, then that watch is changed. However, given the
possibility of rewinding, changing thread focus, etc., "changed" is actually subtly more
flexible. The watch remembers the evaluation from the user's last coordinates (time, thread,
frame, etc.) as well as the current coordinates. So, "changed" more precisely refers to a watch
whose value differs between those two coordinates. This permits the user to switch focus
between different coordinates and quickly identify what is different.


## Examples


For those less familiar with Sleigh, here are some example expressions:


- `RSP`: Display the value of register RSP.
- `*:4 0x7fff0004:8`: Display 4 bytes starting at ram:7fff0004, e.g., to read
the `int` at address 7fff0004. The extraneous but required size specifier on the
constant 0x7fff0004 is a known issue. Just use the target's pointer size in bytes — 8
in the example.
- `*:4 my_global`: Display 4 bytes starting at the label "my_global", e.g., to
read the `int` value there. The label may be in the trace or in a program mapped
to the trace. Ambiguities are resolved arbitrarily.
- `*:8 RSP`: Display 8 bytes of [ram] starting at the offset given by register
RSP, e.g., to read a `long` on the stack.
- `*:4 (RSP+8)`: Display 4 bytes of [ram] starting 8 bytes after the offset
given by register RSP, e.g., to read a `int` on the stack.
- `*:4 ((*:8 RSP)+4)`: Display 4 bytes of [ram] starting 4 bytes after the
offset given by reading 8 bytes of [ram] starting at the offset given by register RSP. This
might be used to read the second `int` of an array whose base pointer is on the
stack.


## Table Columns


The table displays and allows modification of each watch. It has the following columns:


- Expression - the user-modifiable Sleigh expression defining this watch.
- Address - when evaluation succeeds, the address of the watch's value. This field is
really only meaningful when the outermost operator of the expression is a memory dereference.
Double-clicking this cell will navigate the primary dynamic listing to this address, if
possible.
- Symbol - the symbol best representing the address, if applicable. When the watch has an
address in memory, this will search the trace for a symbol at that address, preferring the
primary. If no such symbol exists, it will search in the mapped static program, if there is
one, again preferring the primary symbol. Finally, it will search for a containing function
in the mapped program.
- Value - the raw bytes of the watched buffer. If the expression is a register, then this
is its hexadecimal value. This field is user modifiable when the **Enable Edits** toggle
is on, and the variable is modifiable. Edits may be directed toward a live target, the trace,
or the emulator. If the value has changed since the last navigation event, this cell is
rendered in red.
- Type - the user-modifiable type of the watch. Note the type is not marked up in the
trace. Clicking the [Apply Data Type](#apply-data-type) action will apply it to
the current trace, if possible.
- Representation - the value of the watch as interpreted by the selected data type. If the
value is an address, i.e., Type is a pointer, then double-clicking this cell will navigate
the primary dynamic listing, if possible. This field is user-modifiable whenever the Value
column is modifiable and the selected data type provides an encoder.
- Error - if an error occurs during compilation or evaluation of the expression, that error
is rendered here. Double-clicking the row will display the stack trace. Note that errors
during evaluation can be a very common occurrence, especially as contexts change, and should
not necessarily cause alarm. An expression devised for one context may not have meaning under
another, even if it evaluates without error. E.g., `RIP` will disappear when
switching to a 32-bit trace, or `*:8 (*:8 (RSP+8))` may cause an invalid
dereference when the stack pointer moves.


## Actions


The watches window provides the following actions:


### Apply Data to Listing


This action is available when there's an active trace, and at least one watch with an
address and data type is selected. If so, it applies that data type to the value in the
listing. That is, it attempts to apply the selected data type to the evaluated address, sizing
it to the value's size.


### Watch Type Settings


This action is available on the context menu when there is a single watch selected with a
data type assigned. It permits the adjustment of that data type's settings, e.g., to display
decimal vs. hexadecimal.


### Select Range


This action is available when there's an active trace, and at least one watch with memory
addresses is selected. It selects the memory range comprising the resulting value. This only
works when the outermost operator of the expression is a memory dereference. It selects the
range at the address of that dereference having the size of the dereference. For example, the
expression `*:8 RSP` would cause 8 bytes of memory, starting at the offset given by
RSP, to be selected in the dynamic listing.


### Select Reads


This action is available when there's an active trace, and at least one watch with memory
reads is selected. It selects all memory ranges dereferenced in the course of expression
evaluation. This can be useful when examining a watch whose value seems unusual. For example,
the expression `*:8 RSP` would cause 8 bytes of memory, starting at the offset given
by RSP, to be selected in the dynamic listing -- the same result as Select Range. However, the
expression `*:4 (*:8 RSP)` would cause two ranges to be selected: 8 bytes starting
at RSP and 4 bytes starting at the offset given by `*:8 RSP`.


### Add


This action is always available. It adds a blank watch to the table. Modify the expression
to make the entry useful.


### Watch


This action is available in context menus for addresses, selections, or registers. It adds
the selected item(s) to the watch table. If the context is derived from a static view, it first
attempts to map it to the current trace. For selections, it adds a typeless watch for each
range. For single-address locations derived from a listing, it adds a typed watch on the
current code unit. For other single-address locations, it adds a 1-byte typeless watch on the
address. For registers, it adds a watch on that register. Note that `contextreg` and
its children cannot be watched, due to a limitation in Sleigh.


### Remove


This action is available when at least one watch is selected. It removes those watches.


### Enable Edits


This toggle is a write protector for machine state. To modify a watch's value, this toggle
must be enabled. Edits are directed according the to [Control and Machine State
Plugin](../DebuggerControlPlugin/DebuggerControlPlugin.md).


---

[← Previous: Static Synchronization](../DynamicStaticSynchronizationPlugin/DynamicStaticSynchronizationPlugin.md) | [Next: Variable Hovers →](../VariableValueHoverPlugin/VariableValueHoverPlugin.md)
