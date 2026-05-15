[Home](../index.md) > [DebuggerTimeOverviewPlugin](index.md) > Time Overview Sidebar

# Debugger: Time Overview


Patterned on the Program Overview, this plugin provides a pair of sidebars for the Dynamic
Listing that indicate the history of the current trace, similar to those in the [Time](../DebuggerTimePlugin/DebuggerTimePlugin.md) and [Memview](../DebuggerMemviewPlugin/DebuggerMemviewPlugin.md) plugins. The Trace
Overview bar gives a compressed view of various events (thread creation/destruction, module
loads/unloads, et cetera). Events are added in time snap order *without* spaces between
consecutive events, as in the Memview display. The Trace Selection sidebar allows the user to
click & drag over a section of either sidebar and zooms in on that time span. In the zoomed
version, events are in snap order *with* intervening space to indicate the actual time
delays (although these are dictated, in part, by the numbering schema for events).


## Navigation


### Zoom ![In](../icons/zoom_in.png)


Clicking and dragging over a region of the Trace Overview causes that span to be displayed
uncompressed in the Trace Selection. The same action can also be applied to the Trace Selection
itself, resulting in a more detailed zoom.


### Move ![In](../icons/zoom_in.png)


Shift click & drag on the Trace Selection allows the user to move forward and backward
in the view without rescaling.


---

[← Previous: Memview Plot](../DebuggerMemviewPlugin/DebuggerMemviewPlugin.md) | [Next: P-code Stepper →](../DebuggerPcodeStepperPlugin/DebuggerPcodeStepperPlugin.md)
