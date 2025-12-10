[Home](../index.md) > [FunctionGraphPlugin](index.md) > Zooming

# Function Graph Plugin


| ![](images/FunctionGraphWindow.png) |
| --- |


The Function Graph Plugin is a simple graph display that shows the code blocks of the
function containing the cursor in the [Listing](../CodeBrowserPlugin/CodeBrowser.md).


The display consists of the [Primary View](#primary-view) and the [Satellite View](../VisualGraph/Visual_Graph.md#satellite-view). There is also a group of [actions](#graph-actions) that apply to the entire graph.


<a name="toggle-listing-and-function-graph"></a>


> **Tip:** Ctrl-Space will toggle
between the full Listing view and the Function Graph view.  The Toggle Listing and
Function Graph action's key binding can be changed in the tool options.


## Primary View


The Primary View displays the [Vertices (or Blocks)](#vertices-blocks) and [Edges (or Control Flow)](#edges) of the graph. From this view you can interact with
blocks, both for editing and arrangement.


The graph rendered in the Primary View may represent an undefined function, such as a
subroutine. If this is the case, then the background of the Primary View will be a gray
color, such in the following image:


| ![](images/FunctionGraph_Provider_Undefined.png) |
| --- |


<a name="stale-graph"></a> By default, as changes to the program are detected, the graph
will **not** relayout to account for these changes. The image below shows the bottom of
the Primary View when the graph has detected changes and is considered **stale**


| ![](images/FunctionGraph_Stale_Graph.png) |
| --- |


Once a graph is stale, you can press the refresh button at any time to have the graph
re-create itself **without performing a relayout**. The green box in the image above
contains the refresh button. Alternatively, you can press the [relayout action](#graph-actions) to refresh the stale graph **and**
perform a relayout, which we reposition the vertices of the graph to their preferred
locations.


If you would like to change the default behavior on program changes to perform a full
graph update, then you can change this value via the tool options. You can access these
options by right-clicking in graph and selecting the **Properties** action. Alternatively,
you can click on the tool's menu bar **Edit-&gt;Tool Options...** to launch
the options.   From there you can find the option at **Function Graph-&gt;
Automatic Graph Relayout**


## Vertices (Blocks)


Each vertex in the displayed graph represents a code block within the graphed function.
The term **block** is used synonymously with the term vertex. The block display consists
of a header and a code listing. The fields contained in the listing are a subset of the
available fields. You may change the fields displayed from the [Edit Code Block Fields](#graph-actions) action.


The header contains the name of the block, as defined by the label at that location, or
that address if no label exists. The header also contains buttons that allow you to perform
some common operations on the block.


As long as you are within the [interaction threshold](#interaction-threshold),
you may interact with the block's listing just as you would with Ghidra's primary [Listing](../CodeBrowserPlugin/CodeBrowser.md).


The following actions are available from the primary view.


### Selecting Blocks


Left-clicking a block will select that block. To select multiple blocks, hold down the
**`Ctrl`** key (or the equivalent for your OS) while clicking. To deselect a
block, hold the `Ctrl` key while clicking the block. To clear all selected blocks,
click in an empty area of the primary view. When selected, a block is adorned with a
halo.


You may also select multiple blocks in one action by holding the `Ctrl` key while
performing a drag operation. Press the `Ctrl` key and start the drag in an empty
area of the primary view (not over a code block). This will create a bounding rectangle on
the screen that will select any blocks contained therein when the action is finished.


### Navigating Blocks


If you double-click a block header, then the [Zoom Level](#zooming) of the
Primary View will change. If the block is not at full zoom (1:1), then the zoom level will
be changed to full zoom. Otherwise, the zoom level will be changed to fully zoomed out. If
you are zoomed past the [interaction threshold](#interaction-threshold), then
you can double-click anywhere in the block to trigger a full zoom.


Assuming you are **not** zoomed past the interaction threshold, then double-clicking
a field inside the block's listing will perform a navigation [as determined by that
listing](../CodeBrowserPlugin/CodeBrowser.md#navigation). If you **are** zoomed past the interaction threshold, then double-clicking
anywhere in the block will trigger navigation in the same way as double-clicking the block
header.


### Block Information


You can hover over a block to get descriptive information. Depending upon the [Zoom Level](#zooming) of the primary view, you will get different hovers. When zoomed past
the interaction threshold, the hover action will trigger a popup window showing a preview
of the block. At full zoom, you will only receive popup windows [as determined by the listing](../CodeBrowserPlugin/CodeBrowser.md#mouse-hover)
inside of the block. You may disable [popups](#popups) as desired.


### Vertex Actions


| ![](images/FunctionGraph_Vertex_Header.png) |
| --- |


<a name="vertex-action-color"></a>The ![](images/FunctionGraph_Vertex_Action_Color.png) button
allows you to set the background color for the vertex. You may press the button to choose
the color currently displayed in the icon, or you may use the drop-down menu to pick a
previously used color. Additionally, from the drop-down menu you can clear the color or
choose a new color to set.


![Note](../shared/note.yellow.png) By default, colors
applied to a vertex are also applied to the primary disassembly Listing.


<a name="vertex-action-group"></a>The ![shape_handles.png](../icons/shape_handles.png)
button will [group](#vertex-grouping) all selected vertices.


### Popup Menu Vertex Actions


<a name="vertex-action-label"></a>The ![](images/FunctionGraph_Vertex_Action_Label.png)
button allows you to set the label for the code block (this will also change the block
header).


<a name="vertex-action-full-view"></a>The ![fullscreen_view.png](../icons/fullscreen_view.png)
toggle button allows you to quickly view the contents of the block in a full window
view, which uses the same format as Ghidra's primary [Listing](../CodeBrowserPlugin/CodeBrowser.md). To restore the graph view
from the full window view, click this action again, which will then have this icon:
![](images/FunctionGraph_Vertex_Action_Full_View_Alt.png).


<a name="vertex-action-xrefs"></a>The ![](images/FunctionGraph_Vertex_Action_XRefs.png)
button will show a table of xrefs to the entry point of the currently graphed
function.


> **Note:** This action will also
appear in the vertex containing the function entry point, for convenience.


### Grouped Vertex Actions


| ![](images/FunctionGraph_Grouped_Vertex_Header.png) |
| --- |


> **Note:** This section describes vertex
grouping, which is covered later in this document .


<a name="group-vertex-action-color"></a>The ![](images/FunctionGraph_Vertex_Action_Color.png) button
allows you to set the background color for the vertex. You may press the button to choose
the color currently displayed in the icon, or you may use the drop-down menu to pick a
previously used color. Additionally, from the drop-down menu you can clear the color or
choose a new color to set.


#### Group Vertex Coloring Algorithm


This group color feature allows you to easily color large numbers of vertices after
you have grouped them and to keep already set user-defined colors as you are grouping
vertices.


The Function Graph will automatically color your group vertex, depending on the color
state of the vertices being grouped:


- If none, or some but not all, of the vertices being grouped have a user-defined
color, then the group vertex will be made the default color (which you can change from
the options).
- If all of the vertices being grouped have a user-defined color, but that color is
not the same, then the group vertex will be made the default color.
- If all of the vertices being grouped have **the same** user-defined color, then
the new group vertex **will be made the color of the vertices**.


When a group vertex has a user-defined color, then all vertices grouped therein will
take on that color.


> **Tip:** Via the options you can
disable this feature.


<a name="group-vertex-action-label"></a>The ![](images/FunctionGraph_Vertex_Action_Label.png) button
allows you to set the text displayed in the group vertex. Unlike the action when used in a
non-grouped vertex, this action will not edit the label at the start address of the
vertex.


<a name="vertex-action-ungroup"></a>The ![shape_ungroup.png](../icons/shape_ungroup.png) button will [ungroup](#the-ungrouping-process) the
given vertex.


<a name="group-vertex-action-group"></a>The ![shape_handles.png](../icons/shape_handles.png) button will [group](#vertex-grouping) all selected
vertices.


<a name="vertex-action-group-add"></a>The ![shape_square_add.png](../icons/shape_square_add.png) button will add to the given group vertex all other selected
vertices.


The difference between **group** and **add to group** is somewhat subtle. The
**group** action creates a *new* group vertex with each selected vertex as a
child, contained inside of the new grouped vertex. Alternatively, the **add to group**
action adds to the *existing* group node chosen all other selected vertices.


<a name="vertex-action-regroup"></a>The regroup ![edit-redo.png](../icons/edit-redo.png) button is included in the header of any **uncollapsed** vertex,
which is a vertex that is the member of a group, where that group has been [ungrouped](#the-ungrouping-process). This action will **regroup** (or collapse) all
vertices in the same group as the vertex containing the action. To regroup is to convert
all members of a given group back into a single grouped vertex.


> **Tip:** To remove an uncollapsed vertex
from group membership, right-click on that vertex and select Ungroup Selected
Vertices .


## Edges


The Edges of the vertices represent a flow from one code block to another. One end of each
edge has an arrowhead that represents the direction of the flow. Furthermore, the color of
the edge provides a visual indication as to the type of the flow. The default flow colors
are:


|  | Fallthrough - the negative case of a conditional check |
| --- | --- |
|  | Conditional - the positive case of a conditional check |
|  | Unconditional - An unconditional flow |


The following actions are available from the primary view.


### Selecting Edges


You may select an edge by left-clicking it. To select multiple edges, hold down the
**`Ctrl`** (or the equivalent for your OS) while clicking. To deselect an edge,
hold the `Ctrl` key while clicking the edge. To clear all selected edges, click in an
empty area of the primary view.


### Navigating Edges


Double-clicking an edge will navigate to the one of the incident blocks. The navigation
will first take you to the destination block if it is not already selected. Otherwise, the
navigation will take you to the source block.


### Edge Information


You can hover over an edge to get descriptive information. When you hover over an edge you
will be presented with a popup window showing a preview for the source and destination blocks
for the hovered edge. You may disable [popups](#popups) as desired.


### Articulated Edges


Some graph layouts create articulated edges, which are edges that contain bends in them to
route around vertices. As you drag vertices around the graph the bends in the articulations
in the dragged edge may disappear if the articulation causes the edge to contain awkward
angles.


## Vertex Grouping


| ![](images/FunctionGraph_Pre_Group.png) Selected Vertices - Before Grouping |
| --- |


| ![](images/FunctionGraph_Post_Group.png) Grouped Vertices |
| --- |


You may select 2 or more vertices to be turned into a single grouped vertex. This allows
you to organize vertices to reduce the amount of information displayed in the graph. As an
example, you may wish to place all branches of a switch statement into a single grouped
vertex.


> **Tip:** You can select a single vertex
to group. This allows you to annotate a given vertex with text, without editing the label
at the vertex address, which is the default behavior of the edit label action . In addition to setting the text for the
grouped vertex, it will remove the disassembly. In this regard, grouping a single vertex is
a form of information hiding.


Before a group vertex is created you are prompted to enter text that will be displayed in
the body of the group vertex. By default, the titles of each grouped vertex will be listed as
the text of the grouped vertex.


| ![](images/FunctionGraph_Group_Text_Dialog.png) Grouped Vertex Text Input Dialog |
| --- |


*The default contents of the group vertex text entry dialog are generated from the
titles of each vertex being grouped. When grouping a vertex which is itself a group, the
text of that group vertex will be used in the text entry dialog in addition to its
title.*


> **Tip:** Grouped vertices may contain other
grouped vertices.


> **Warning:** As you group vertices, the
graph may perform a relayout of the vertices, depending upon the Function Graph Options, as
described below .


### The Ungrouping Process


Ungrouping a grouped vertex will restore to the graph all vertices contained in the
grouped vertex. The layout behavior of the graph after performing an ungroup operation is
dependent upon the graph options; specifically, the **Automatic Graph Relayout** option.
The default setting for automatic relayout is **Vertex Grouping Changes Only**. This
means that as you group and ungroup vertices, the graph will relayout its vertices, which
may be a drastic layout change. To prevent the graph from performing a relayout during
grouping or ungrouping, set the option listed above to be **Block Mode Changes Only** or
**Never**.


> **Tip:** You can access the Function
Graph Options by right-clicking in an empty area of the graph and clicking the Properties menu item.


You can ungroup all group vertices in the graph via the right-click popup menu by
selecting [Ungroup All Vertices](#grouping). Warning:
this will ungroup all groups, which is an operation that cannot be undone.


> **Tip:** Ungrouped vertices can be
regrouped by executing the regroup action . This
action is executed from an individual vertex, but will apply to all vertices in its
group.


## Graph Actions


The following actions are buttons in the Function Graph Plugin header.


| ![](images/FunctionGraph_Provider_Header.png) |
| --- |


<a name="function-graph-action-copy"></a>The ![page_white_copy.png](../icons/page_white_copy.png) button will perform a copy action in one or more vertex
listings. See the [Clipboard](../ClipboardPlugin/Clipboard.md) help
for more information on using copy in the Listing and Listing-based views.


<a name="function-graph-action-paste"></a>The ![page_paste.png](../icons/page_paste.png) button will perform a paste action in one or more
vertex listings. See the [Clipboard](../ClipboardPlugin/Clipboard.md)
help for more information on using paste in the Listing and Listing-based views.


<a name="function-graph-action-home"></a>The ![house.png](../icons/house.png) button will
navigate to and select the entry point block.


<a name="function-graph-reload-graph"></a>The ![Refresh](../icons/reload3.png) button clear all **position and grouping** changes made to the graph and
then perform a reload and relayout of the graph.


<a name="function-graph-action-layout"></a>The ![](images/FunctionGraph_Action_Layout.png) button allows
you to both change the layout used to arrange the graph and to perform a relayout of the
graph using the current layout. Simply pressing the button will trigger a relayout, whereas
clicking on the drop-down arrow will allow you to choose a new layout.


> **Tip:** This action allows you to
perform a graph relayout without losing grouping information


<a name="function-graph-action-format"></a>The ![field.header.png](../icons/field.header.png) button allows
you to change the fields of the blocks' listing.


By default, the format configuration of the vertices is greatly condensed. This is
done to fit as many vertices on the screen as is possible. You can make the vertices
larger or smaller as you see fit. Form more information about adding and removing fields,
as well as adjusting the size of the fields in the vertex listing display, see the [Listing Panel's format
help](../CodeBrowserPlugin/Browser_Field_Formatter.md).


<a name="function-graph-action-snapshot"></a>The ![camera-photo.png](../icons/camera-photo.png) button will create a [Snapshot](../Snapshots/Snapshots.md) of the current graph.


## Path Highlight Actions


The focus and hover path highlighting modes are designed to help show the flow of
execution through the code blocks in a function, as well as illustrate some of the
structure. Hover highlights are triggered when you move the mouse over a block. Focus
highlights are triggered by selecting a block and only work from one selected block, not
with multiple selected blocks.


The **focus highlight** paints the edges between certain code blocks with a bold
stroke, thicker than the regular edges. The **hover highlight** paints a dashed,
thicker stroke that also moves in the direction of flow for a limited period of time.


The path highlighting modes (described in the table below) are available for both
focus and hover, except in special cases, as noted.


| Icon | Name | Description |
| --- | --- | --- |
| <a name="scoped-flow-from-block"></a> ![](images/FunctionGraph_Action_Show_Scoped_Flow_From_Block.png) | Show Scoped Flow From Block | Highlights control flow to code blocks that are only reachable if the current               code block is executed. This is useful to see a local neighborhood of blocks that               follow the current block. |
| <a name="scoped-flow-to-block"></a> ![](images/FunctionGraph_Action_Show_Scoped_Flow_To_Block.png) | Show Scoped Flow To Block | Highlights control flow from code blocks that must eventually reach the current               code block. This is useful to see a local neighborhood of blocks that precede the               current block. |
| <a name="paths-to-from-block"></a> ![](images/FunctionGraph_Action_Show_Paths_To_From_Block.png) | Show Paths To/From Block | Highlights control flow from codes blocks that can reach the current code block,               as well as control flow to code blocks that can be reached from the current block.               This is useful to show all possible flows before and after the current block. |
| <a name="paths-from-block"></a> ![](images/FunctionGraph_Action_Show_Paths_From_Block.png) | Show Paths From Block | Highlights control flow to code blocks that can be reached from the current code block.               This is useful to show all possible flows after the current block. |
| <a name="paths-to-block"></a> ![](images/FunctionGraph_Action_Show_Paths_To_Block.png) | Show Paths To Block | Highlights control flow from codes blocks that can reach the current code block.                This is useful to show all possible flows before the current block. |
| <a name="loops-containing-block"></a> ![](images/FunctionGraph_Action_Show_Loops_Containing_Block.png) | Show Loops Containing Block | Highlights the control flow between all possible looped blocks (cycles) that pass               through the current block. If a function has multiple non-intersecting loops, this               helps resolve the loops from each other in the case that the graph layout has placed               them too close to differentiate. |
| <a name="paths-from-focus-to-hover"></a> ![](images/FunctionGraph_Action_Show_Paths_From_Focus_To_Hover.png) | Show Paths From Focus to Hover (hover mode only) | Highlights the control flow from the currently focused code block to the               currently hovered code block. If there are no paths possible, no edges will be               highlighted. This is useful to see reachability between two sections of the               function. |
| <a name="all-loops-in-function"></a> ![](images/FunctionGraph_Action_Show_All_Loops_In_Function.png) | Show All Loops In Function (focus mode only) | Highlights the control flow between all possible looped blocks (cycles) in the               current function. This mode doesn't actually depend on a focused code block; instead,               selecting it highlights all loops immediately. |


## Function Graph Options


The <a name="auto-relayout"></a>**Automatic Graph Relayout** option describes when the
graph will perform an automatic relayout of the vertices as the graph changes. The available
values are:


- **Always** - always perform a graph relayout anytime the code blocks change or when
graph groups change
- **Block Mode Changes Only** - only performs a relayout when the code blocks of the
graph change (e.g., from an external edit)
- **Vertex Grouping Changes Only** - only performs a relayout when the state of the
graph groups changes (during a group or ungroup operation)
- **Never** - never perform a relayout of the graph automatically


The **Navigation History** option determines how the navigation history
will be updated when using the Function Graph.  The values are:


- **Navigation Events** - save a history entry when a navigation takes place
(e.g., double-click or Go To event).  This setting will record less history.  Further,
this setting works the same as the Tool's general history saving mechanism.  This
setting should be preferred if you wish to use the navigation actions to go back
to previously visited **functions** more than individual addresses.
- **Vertex Changes** - save a history entry each time a new vertex is selected.  This
setting allows users to move throughout the graph view while using the navigation actions
to go back to previously visited vertices.  This setting will create a much larger
and more detailed history list.


The **Scroll Wheel Pans** option signals to move the graph vertical when scrolling the
mouse scroll wheel. Disabling this option restores the original function graph scroll wheel
behavior of zooming when scrolled.


The **Update Vertex Colors When Grouping** option signals to the graph to make the
color of the grouped vertex be that of the vertices being grouped.


The **Use Animation** option signals to the graph whether to animate mutative graph
operations and navigations.


<a name="layout-compressing"></a>The **Use Condensed Layout** option signals to the
graph to bring vertices as close together as possible when laying out the graph. Using this
option to fit as many vertices on the screen as possible. Disable this option to make the
overall layout of the graph more aesthetic.


The **Use Full-size Tooltip**When toggled off, the tooltip for a vertex will be
the same size and layout of the vertices in the graph.  When toggled on, the tooltip
for a vertex will be larger, using the layout of the Listing.   The larger size is
more informative, but also takes up more space.


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


## Creating Program Selections


### From Paths


<a name="path-selection"></a> You may create Program Selections from the **current path
highlights** by clicking **Program Selection →  From Hovered Edges** and **From Focused Edges** from the popup menu of a block.
If not paths are highlighted, then these actions will be disabled.


### From Code Blocks


<a name="code-unit-selection"></a> You may select all Code Units in a Code Block by
clicking **Program Selection →  Select All
Code Units** from the popup menu (or by using the default keybinding, **Ctrl-A**). This
action will select all Code Units in all selected Code Blocks in the graph. **If no Code
Blocks are selected, then a Program Selection will be created for all Code Units in all Code
Blocks in the graph.**


### Clearing Selections


You may clear the current Program Selection by clicking **Program Selection →  Clear Selection** from the popup menu.


## Popups


The primary view provides various popup windows to provide information as you hover over
the blocks and edges in the graph. To enable and disable popups in the primary view,
right-click anywhere in the primary view and select the **Display Popup Windows** toggle
button from the popup menu.


## Grouping


The following popup menu items provide additional [grouping](#vertex-grouping)
functionality.


- <a name="vertex-grouping-group-selected-popup"></a> **Group Selected Vertices** -
Groups all selected vertices
- <a name="vertex-grouping-add-selected-vertices-to-group"></a> **Group Selected
Vertices - Add to Group** - Adds the selected vertices to group vertex in the selection.
This action will not be enabled if there is not one, and only one, group vertex in the
selection.
- <a name="vertex-grouping-remove-from-group"></a> **Remove From Group** - Removes the
[uncollapsed vertex](#group-vertex-coloring-algorithm) from its group.
- <a name="vertex-grouping-ungroup-all-popup"></a> **Ungroup All Vertices** - Ungroups
**all** vertices in the graph, not just those selected or visible. This operation cannot
be undone!
- <a name="vertex-grouping-ungroup-selected-popup"></a> **Ungroup Selected Vertices**
          - Ungroups the selected group vertices


## Zooming


At **full zoom**, or **block level zoom**, each block is rendered at its natural
size, which is the same scale as Ghidra's primary [Listing](../CodeBrowserPlugin/CodeBrowser.md). From that point, which is a 1:1
zoom level, you can zoom out in order to fit more of the graph into the display. See
[Visual Graph Zooming](../VisualGraph/Visual_Graph.md#zooming) for
more information on graph zooming.


### Vertex Quick Zoom


If you double-click a block header, then the [Zoom Level](#zooming) of the
Primary View will change. If the block is not at full zoom (1:1), then the zoom level will
be changed to full zoom. Otherwise, the zoom level will be changed to fully zoomed out. If
you are zoomed past the [interaction threshold](#interaction-threshold), then
you can double-click anywhere in the block to trigger a full zoom.


### Interaction Threshold


## Saving View Information


The *Function Graph Plugin* will automatically save your changes to the graph,
specifically, coloring nodes, grouping nodes, zooming and panning.   This happens as your
change the function displayed in the graph and when you close the graph window.


![Note](../shared/note.yellow.png)Changes made to
[Snapshots](#graph-actions) will not be saved.  This is
done to avoid conflict between
changes made to the connected view and any of the snapshots


## Standard Graph Features and Actions


The function graph is a type of Ghidra Visual Graph and has some standard concepts, features
and actions.



- [Satellite View](../VisualGraph/Visual_Graph.md#satellite-view)
- [Panning](../VisualGraph/Visual_Graph.md#panning)
- [Zooming](../VisualGraph/Visual_Graph.md#zooming)
- [Interaction Threshold](../VisualGraph/Visual_Graph.md#interaction-threshold)


*Provided by: *Function Graph Plugin**


**Related Topics:**


- [Code Browser](../CodeBrowserPlugin/CodeBrowser.md)
- [Snapshots](../Snapshots/Snapshots.md)


---

[← Previous: Popups](Function_Graph.md) | [Next: Layouts →](Function_Graph_Layouts.md)
