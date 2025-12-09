[Home](../index.md) > [DataGraphPlugin](index.md) > Layout

# Data Graph


| ![](images/DataGraph.png) |
| --- |


The data graph is a graph display that shows data objects in memory. Each data vertex
displays a scrollable view of a data object and its contents.


Initially, a data graph is generated from a specific data program location. The graph
will be populated with one data vertex showing the data for that location. From this original
source vertex, the references to and from this vertex can be explored to add additional
vertices to the graph. In the data vertex display, any data elements that have an outgoing
reference will have an ![Right](../icons/right.png) icon that can be clicked
to quickly explore that reference.


If a reference leads from/to code, a simple code vertex is generated
that simply shows the function and offset of the reference from the function's entry point.
For the purposes of the data graph, code vertices are end points and cannot be explored
further.


The display consists of the [Primary View](#primary-view) and an optional [Satellite View](../VisualGraph/Visual_Graph.md#satellite-view).


## Primary View


The primary view shows an initial data object that was used to create the graph. This
data vertex can be used to explore references and pointers. As you explore, new vertices
will be added to the graph. All vertices in the graph can trace a reference relationship
back to the original source data object.


> **Tip:** The original source data vertex
has a icon in its header to indicate it is the original source vertex.


## Vertices


### Data Vertices


Data vertices show information about the data and values they contain. If the vertex
datatype is a primitive, such as an int, the vertex contains only one row that shows its name
and value. If the data is more complex such as a structure or array, the vertex will display
multiple rows showing the name and value of each field in the structure. If the structure
contains other structures or arrays of data, those data items can be expanded in a tree/table
structure showing the names and values of that internal data.


Any elements that are pointers (or have attached outgoing references) will display a
![Right](../icons/right.png) icon that can be clicked to explore those
references to add new vertices.


Data vertices can be resized by dragging the bottom right corner. Also, the interior column
sizes can be adjusted by hovering the mouse on a column boundary and dragging left or
right.


The header of a vertex contains the name of the label and/or address of the data object.
The header also contains buttons that allow you to perform some common operations on the
vertex.


As long as you are within the [interaction threshold](../VisualGraph/Visual_Graph.md#interaction-threshold),
you may interact with the vertex to expand/collapse sub-data elements and to click on any
pointer references to add vertices to the graph.


### Code Vertices


Generally vertices in the graph show data objects, but a vertex can also represent a
reference from or to code. In the data graph, code vertices are terminal vertices, simply
showing the function name and offset into or out of that function.


| ![](images/CodeVertex.png) |
| --- |


In the image above, the graph is showing two references to the same string.


### Vertex Layout


The data graph uses a special layout to attempt to maintain a logical structure as
more vertices are added to the graph. This layout uses the exploration order
to layout the vertices.


Starting with the original data vertex. All vertices that were
added to the graph by following outgoing references are displayed in a column to the right of
the vertex. Within this column, the vertices are ordered by the order they are first referenced
from the source vertex.


Similarly, vertices added to the graph by following incoming references are shown in a
column to the left of the source vertex. Within this column, the vertices are ordered by
address.


Additional layers of vertices can be added by further exploring the child vertices and their
descendants. These additional vertices are ordered in the same way relative to their immediate
source vertex.


Whenever a vertex is removed from the graph, all vertices that were discovered by exploring
from that vertex are also removed.


### Vertex Actions


The following toolbar actions are available on a data vertex.


- ![Expand All](../icons/expand_all.png) **Expand All** -
Expands all expandable sub-data elements recursively contained in the data object. Note
that this action is not available if the data has no sub-data elements.
- ![Collapse All](../icons/collapse_all.png) **Collapse All**
- Collapses all expanded sub-data elements. Note that this action is not available if the
data has no sub-data elements.
- [Close] **Delete Vertex** - Removes this vertex and all vertices
that descend from this vertex.
- ![Refresh](../icons/reload3.png) **Restore Location** - Moves the vertex
to its preferred location (only shows up if the vertex was manually moved).


The following popup actions are are available depending on where the
mouse is positioned when the popup is triggered.


- **Add All Outgoing References** - All outgoing references
from this data element or its sub-elements will generate a new vertex in the graph, if
not already present.
- **Add All Incoming References** - The program will be
searched for any references to this data element or its sub-elents and a new vertex be
created each discovered reference, if not already present.
- **Expand Fully** - If the mouse is over an
expandable row in data vertex, the vertex and all it's child elements will be fully
expanded.
- **Set Original Source** - Makes this the original source
root vertex. All other vertices are reorganized and laid out as if they were discovered
by following references from this vertex.See [Vertex
Layout.](#layout)
- **Delete Selected Vertices** - Deletes the selected
vertices and any descendants vertices (vertices that were discovered via exploring from
that vertex.)
- **Show Popups** - If selected, hovering over data rows in a data
vertex will show additional information for the data in that row.


### Selecting Vertices


Left-clicking a vertex will select that vertex. To select multiple vertices, hold down
the **`Ctrl`** key while clicking. To deselect
a block, hold the `Ctrl` key while clicking the block. To clear all selected
blocks, click in an empty area of the primary view. When selected, a block is adorned
with a halo.


You may also select multiple vertices in one action by holding the **`Ctrl`** key
while performing a drag operation. Press the **`Ctrl`** key and start the drag in an
empty area of the primary view (not over a vertex). This will create a bounding rectangle
on the screen that will select any vertices contained therein when the action is
finished.


### Navigating Vertices


By default the data graph can be used to navigate the main views of the tool. Clicking
on a vertex or a row within a vertex will generate a goto event for that address, causing
the main tool to navigate to that location. See the actions below to turn off this
behavior.


Also, the data graph can listen for tool location changes and select the appropriate
vertex in the graph if any vertices contain the tool location address. This behavior is
off by default, but can be turn on via a popup action.


## Data Graph Actions


### Toolbar Actions


- ![Reset](../icons/reload3.png) **Refresh Layout** - All manually positioned
vertices will be reset and the graph will relayout to its automated locations.
- ![Home](../icons/go-home.png) **Go To Source Vertex** - The original source vertex will be selected
and centered in the graph.
- ![Navigate On Incoming Event](../icons/locationIn.gif) **Navigate In** - If selected, the graph will
listen for tool location events and select the vertex that contains the location address,
is one exists.
- ![Navigate On Outgoing Event](../icons/locationOut.gif) **Navigate Out** - If selected, the graph will
generate tool location events when vertices are selected or rows within a vertex are
selected.
- ![Format](../icons/view_detailed_16.png) **Expanded Format** - If selected,
vertices will show more information for each row in the display. In compact mode, a data
row will generally show the field name and its value. In expanded mode, a data row will
generally show the datatype, field name, and its value.


Standard Graph Features and Actions


The data graph is a type of Ghidra Visual Graph and has some standard concepts, features
and actions.



- [Satellite View](../VisualGraph/Visual_Graph.md#satellite-view)
- [Panning](../VisualGraph/Visual_Graph.md#pan)
- [Zooming](../VisualGraph/Visual_Graph.md#zoom)
- [Interaction Threshold](../VisualGraph/Visual_Graph.md#interaction-threshold)


*Provided by: *Data Graph Plugin**


---

[← Previous: Popups](Data_Graph.md) | [Next: Function Call Graph →](../FunctionCallGraphPlugin/Function_Call_Graph.md)
