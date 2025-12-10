[Home](../index.md) > [VisualGraph](index.md) > Visual Graphs

# Visual Graphs


Visual Graphs are highly integrated graphs that all share common features and
actions. Various Graph component providers are based upon the Visual Graph API.They typically
have both a [Primary View](#primary-view) and
a [Satellite View](#satellite-view)


## Primary View


The primary view is the main way to view and interact with the graph whose vertices
and edges are specialized for the particular visual graph instance.


## Satellite View


The Satellite View provides an overview of the graph. From this view you may also perform
basic adjustment of the overall graph location. In addition to the complete graph, the
satellite view contains a **lens** (the white rectangle) that indicates how much of the
current graph fits into the primary view.


The Satellite View can be in one of three states:  docked, undocked, or not showing. A
docked satellite view will be display in a corner of the primary graph. An undocked view
will be displayed in its own window. If the view is not showing, there will be an
![network-wireless.png](../icons/network-wireless.png)icon in the corner to indicate that
it is available.


When you left-click in the satellite view the graph is centered around the
corresponding point in the primary view. Alternatively, you may drag the lens of the
satellite view to the desired location by performing a mouse drag operation on the lens.


You may show/hide the satellite view by right-clicking anywhere in the Primary View and
selecting or deselecting the **Display Satellite View** toggle button from the popup
menu.


> **Tip:** If the Primary View is painting
sluggishly, then hiding the Satellite View cause the Primary View to be more
responsive.


### Detached Satellite


The Satellite View is docked by default. However, you can choose to instead
undock it and display it in its own window.


To undock the Satellite View, right-click in the graph and deselect the **Dock
Satellite View** menu item.


To re-dock the Satellite View, right-click in the graph and select the **Dock Satellite
View** menu item.


> **Tip:** To show the Satellite View if it is
hidden, whether docked or undocked, you can press the button. This button is in the lower-right
hand corner of the graph and is only visible if the Satellite View is hidden or
undocked.


### Docked Satellite Location


When the Satellite View is attached, or **docked**, to the Primary View, you can
choose which corner to show the satellite view. To change the corner, right-click in the
graph, select **Docked Satellite Position** and then select the appropriate sub-menu for
the desired corner.


## Standar Graph Operations


### Panning


There are various ways to move the graph. To move the graph in any direction you can
drag from the whitespace of the graph.


By default, the scroll wheel zooms the graph. The scroll wheel can also be used
to scroll the graph vertically by holding the `Ctrl` key while
using the scroll wheel. Alternatively, you can move the graph left to right using the
mouse while holding `Ctrl-Alt`.


The satellite viewer may also be used to move the primary graphs view by dragging and
clicking inside of the satellite viewer.


### Zooming


At **full zoom**, or **block level zoom**, each block is rendered at its natural
size. From that point, which is a
1:1 zoom level, you can zoom out in order to fit more of the graph into the display.


To change the zoom you may use the mouse scroll wheel. This works
whether the mouse is over the primary viewer or the satellite viewer.


The [satellite viewer](#satellite-view) is always zoomed out far enough to
fit the entire graph into its window.


### Interaction Threshold


While zooming out (away from the vertices) you will eventually reach a point where you
can no longer interact with the component inside of the block. The blocks provide a subtle
visual indication when they are zoomed past this level, in the form of a drop-shadow. The
image below shows this drop-shadow. The block on the left is not past the interaction
threshold, but the block on the right is, and thus has a drop-shadow. This example is for
illustrative purposes only and during normal usage all blocks will share the save zoom
level. So, if one block is zoomed past the interaction threshold, all other blocks will
be as well.


### Painting Threshold


While zooming out (away from the blocks) you will eventually reach a point where
contents each vertex will not be painted. Instead, each block will be painted by a
rectangle that is painted with the current background color of the vertex.


---

[← Previous: Program Graph](../ProgramGraphPlugin/ProgramGraph.md) | [Next: Graph Services →](../Graph/GraphServicesIntro.md)
