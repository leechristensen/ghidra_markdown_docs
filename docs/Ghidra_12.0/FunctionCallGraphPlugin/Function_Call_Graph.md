[Home](../index.md) > [FunctionCallGraphPlugin](index.md) > Function Call Graph

# Function Call Graph Plugin


| ![](images/FunctionCallGraphProvider.png) |
| --- |


The Function Call Graph Plugin is a simple graph display that shows incoming and
outgoing calls (as edges) for the function containing the current address, also known as
the *Source Function*, in the
Listing.  This display provides some context for how a function is used within the
program.   The functions are organized by [Level](#level).


To show the Function Call Graph provider window,
select the **Window** →
**Function Call Graph** option on the tool menu.


The graph of function calls related to the source function being displayed can be
explored by [adding existing function calls](#showhide-edges-action)
to the initial graph display.


> **Tip:** The graph updates itself as you navigate within
the tool.  To prevent losing graph state (e.g., expanded functions, node locations,
etc), a small number of graphs will be cached.   For example, if you navigate
away from a function and then immediately return, the graph will be restored to
its previous state.


## Terms


- **Source Function**: the function that contains the current address in
the Listing.   This function is considered the center of the graph, with all
other callers/callees added to the graph at a new level.
- **Level**: Each function node in the graph belongs to a
level.   The source function is at level 1; the source function's incoming
calls are at level 2; the source function's outgoing calls are also at level 2.
Organizing functions by level allows the user to quickly see how many hops, or
calls, a given function is from the source function.
New levels of calls can be added to the graph by the user.
- **Direction**: Each function node, other than the source function, is
considered to be in one of two directions: In or Out.  All function nodes in
a given level share the same direction.  So, all nodes that directly call the
source function node are considered to be the *In* direction; all nodes
directly called by the source function are considered to be the *Out*
direction.
When a given node's level is expanded in the graph, the nodes added are based
upon the selected node's direction:  for *In* nodes, the newly added nodes
will be those nodes that **call** the selected node; for *Out* nodes, the
newly added nodes will be those nodes **called by** the selected node.
- **Direct Edges**: An edge (a call) between two adjacent levels.
- **Indirect Edges**: An edge (a call)
between two	non-adjacent levels or an edge within the same level.   These
edges are rendered with less emphasis than *direct edges*.


## Actions


### Show/Hide Edges Action


Within the *Function Call Graph* you can show and hide function calls
as desired.
Showing additional function calls can be accomplished multiple ways.  From
any function node, you can select the *Expand* icon (
![Expand All](../icons/expand_all.png)


Additionally, these same functionality is provided from the popup menu
actions (i.e., **Show/Hide Incoming Edges** and Show/Hide Outgoing
Edges).


> **Note:** As new vertices are added to the
graph, any indirect edges will be added to the
graph.


Note here how new vertices may appear in odd places when expanding (such as
when they are already in the graph at a previous level).




> **Warning:** It is important to understand
that the graph is only a subset of the entire program graph.  This
graph does not represent all functions and function calls in the
program.


> **Warning:** Sometimes a function
may have too many references to display in the graph.   When this
happens, the function node will be a gray color, with the expand icon
replaced with a warning icon, as so:


### Show/Hide Level Edges Action


All functions that relate to the [Level](#level) of
the selected function will be shown, **not just calls to the selected
function.**


### Navigate on Incoming Location Changes


This action (![Navigate On Incoming Event](../icons/locationIn.gif)


Having this action on is useful if you wish to quickly see the graph of
different functions as you navigate the program.   Alternatively, having this
action off is useful when you wish to explore the program by navigating from
within the graph, say by double-clicking function nodes in the graph.


### Layout Action


This action (![Refresh](../icons/reload3.png)


### Graph '*Function Name*'


This action is available from the popup menu of any node that is not the
currently graphed node.  When pressed, this action will graph the clicked
function.


## Satellite View


The Satellite View provides an overview of the graph. From this view you may also perform
basic adjustment of the overall graph location. In addition to the complete graph, the
satellite view contains a **lens** (the white rectangle) that indicates how much of the
current graph fits into the primary view.


When you single left mouse click in the satellite view the graph is centered around the
corresponding point in the primary view. Alternatively, you may drag the lens of the
satellite view to the desired location by performing a mouse drag operation on the lens.


You may hide the satellite view by right-clicking anywhere in the Primary View and
deselecting the **Display Satellite View** toggle button from the popup menu.


> **Tip:** If the Primary View is painting
sluggishly, then hiding the Satellite View cause the Primary View to be more
responsive.


### Detached Satellite


The Satellite View is attached, or **docked**, to the Primary View by default.
However, you can detach, or undock, the Satellite View, which will put the view into a
Component Provider, which itself can be moved, resized and docked anywhere in the Tool you
wish.


To undock the Satellite View, right-click in the graph and deselect the **Dock
Satellite View** menu item.


To re-dock the Satellite View, right-click in the graph and select the **Dock Satellite
View** menu item.


> **Tip:** To reshow the Satellite View if it is
hidden, whether docked or undocked, you can press the button. This button is in the lower-right
hand corner of the graph and is only visible if the Satellite View is hidden or
undocked.


### Docked Satellite Location


When the Satellite View is attached, or **docked**, to the Primary View, you
can choose which corner to show the satellite view. To change the
corner, right-click in the graph, select **Docked Satellite Position** and then
select the appropriate sub-menu for the desired corner.


## Options


The **Scroll Wheel Pans** option signals to move the graph vertical when scrolling the
mouse scroll wheel. Disabling this option restores the original function graph scroll wheel
behavior of zooming when scrolled.


The **Use Animation** option signals to the graph whether to animate mutative graph
operations and navigations.


The **Use Condensed Layout** option signals to the
graph to bring vertices as close together as possible when laying out the graph. Using this
option to fit as many vertices on the screen as possible. Disable this option to make the
overall layout of the graph more aesthetic.


The **Use Mouse-relative Zoom** option signals zoom the graph to and from the mouse
location when zooming from the middle-mouse. The default for this option is off, which
triggers zoom to work from the center of the graph, regardless of the mouse location.


The **View Settings** option describes how the graph will be zoomed when it is first
loaded.  The values are:


- **Start Fully Zoomed Out** - always start fully zoomed out so that the entire
graph can be seen.
- **Start Fully Zoomed In** - always start fully zoomed in on the vertex containing
the current location.
- **Remember User Settings** - keep the zoom level where the user previously left
it.


There are various edge color and highlight color options available to change. The
highlight colors are those to be used when the flow animations take place.


*Provided by: *Function Call Graph Plugin**


**Related Topics:**


- [Graphs](../Graph/GraphIntro.md)


---

[← Previous: Layout](../DataGraphPlugin/Data_Graph.md) | [Next: Function Graph →](../FunctionGraphPlugin/Function_Graph.md)
