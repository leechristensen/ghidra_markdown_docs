[Home](../index.md) > [PropertyManagerPlugin](index.md) > View Properties

# Property Viewer


The Property Viewer window shows all of the properties in a Program. Properties<a name="property"></a> are assigned to a code unit and can store values at addresses. [Plugins](../Tool/Ghidra_Tool_Administration.md#ghidra-tool-administration) can define their own
properties for storing plugin specific information at an address. The display provides a
convenient way to see all the properties that exist in the Program. When you select a property,
the [navigation
margin](../CodeBrowserPlugin/CodeBrowser.md#navigation-marker) in [Code Browser](../CodeBrowserPlugin/CodeBrowser.md) shows a
pink marker for each location of that property. The window provides a quick way to remove all
properties at once.


| ![](images/PropertyViewer.png) |
| --- |


To display the Property Viewer window, select **Window → Manage Properties...** from the tool menu.


In this example, a plugin has placed several source related properties on code units. Select
the row for "Source File" to see all the locations in the Code Browser where a "Source File"
property is defined, as shown in the image below. The [left margin](../CodeBrowserPlugin/CodeBrowser.md#margin-marker) on the shows
marker for the "Source File" property; the [right margin](../CodeBrowserPlugin/CodeBrowser.md#navigation-marker) shows the
other locations where the Space properties exist; click on the right margin to navigate to that
location.


![](images/Markers.png)


<a name="deleteproperties"></a>To delete all properties in the Program,


1. Select a property to delete.
2. Right mouse-click and select **Delete**.
  - The property will be removed from the list of properties in the dialog.
  - To undo the delete, select the ![Undo](../icons/edit-undo.png)button on the tool.


*Provided by: *PropertyManagerPlugin**


**Related Topics:**


- [Code
Browser](../CodeBrowserPlugin/CodeBrowser.md)
- [Navigation
Margin](../CodeBrowserPlugin/CodeBrowser.md#navigation-marker)
- [Marker Margin](../CodeBrowserPlugin/CodeBrowser.md#margin-marker)


---

[← Previous: Clear](../ClearPlugin/Clear.md) | [Next: Set Fallthrough Address →](../FallThroughPlugin/Override_Fallthrough.md)
