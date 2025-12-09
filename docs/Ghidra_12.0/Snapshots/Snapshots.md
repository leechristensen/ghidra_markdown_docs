# Snapshot Views


In previous versions of Ghidra, there were basically two types of
component views: main views
and subordinate
views.  Main views are the primary working
views such as the Listing
view and the Bytes
view.  Subordinate views,
such as the Symbol Table and Data Type Mangager, show more
specific information and are complimentary to the information displayed
in the main views.  The main views are connected to each other - cursor
location
changes in one view cause the other views to follow along.


Ghidra main views now have corresponding Snapshot views  A snapshot
view is similar to its related main view,
but it is disconnected.  It does not respond to movements in
other views and navigating within a snapshot view does not cause other
views to move.  The main view
can then navigate to other programs and locations, but the snapshot
view will remain at its same location unless the user navigates within
the
snapshot view. Most actions that work on a connected view also
work in its corresponding snapshot view.  Each snapshot view has
its own [navigation
history](../Navigation/Navigation.md#navigation-history), while the connected views all share a single navigation
history.


## Creating a Snapshot View


Snapshot views are created by first
viewing the desired information in the connected view.  Views that
support snapshots will have the Create
Snapshot action (![camera-photo.png](../icons/camera-photo.png)) on the local toolbar.
Pressing this icon will create a snapshot view of the same type (a Code Viewer will create a Code Viewer snapshot, a Decompiler will create a Decompiler snapshot, etc.)
configured exactly the same as the creating view.  The main view
can then navigate to other programs and locations, but the snapshot
will remain at its same location unless the user navigates within the
snapshot view.


## Snapshot Views, Windows, and Actions


Snapshot views can be docked with normal views or they can live in
their own windows.  Global menu and toolbar actions have been
changed to accommodate snapshot views.  Global actions now operate
on whatever component has focus (the component whose header bar is
colored blue).  For example, if you have the connected Listing View and a snapshot Listing View, both docked in the
same window, global actions such as Go
to Next Instruction will navigate the normal view if it has
focus or the snapshot view if it has focus.  If neither has focus,
the action will be disabled.

Note this is different from previous versions of Ghidra.
Previously, the Go to Next Instruction
action would always navigate the (one and only)

Listing View, even if, for
example, the Symbol Tree has
focus.  Now, if the Symbol Tree
has focus, the Go to Next Instruction
action is disabled.


Since global actions now work on the active component (the
component that has focus) within its window, many global actions can
appear in multiple windows.  For example, the undo/redo actions will appear in any
window containing a Listing View,
a Decompiler View, or a Bytes View.
