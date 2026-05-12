# Listing Background


You can change the background colors of the Listing via context actions or
programmatically by using the *ColorizingService*. Changing specific address range
background colors can be useful for many reasons, such as marking areas of interest. Further,
coloring can be performed from a script, which allows you to color disassembly during
automated processing.


> **Note:** Unlike program selections and
highlights, the background colors you set will be saved with the program.


## Changing Colors


### Actions


**Set Color** - Available from the listing right-click context menu under the
**Colors** pull-right. This action will show a color chooser dialog that allows you to
pick a color to be applied over the current selection or the current address if no
selection exists.


**Clear Color** - Available from the listing right-click context menu under the
**Colors** pull-right. This action allows you to clear the color that has been
previously set for the current selection or the current address if no selection
exists.


**Clear All Colors** - Available from the listing right-click context menu under
the **Colors** pull-right. This action will clear all colors applied **to the entire
program**. exists.


> **Note:** Any of these actions can be undone
using the undo action .


### Service


From a script, using the `GhidraScript` API:


| public void run() throws Exception {                 setBackgroundColor(anotherAddress, Color.YELLOW);                                                   // OR, using a range of addresses                                  // create an address set with values you want to change                 AddressSet addresses = new AddressSet(currentProgram.getAddressFactory());                                      addresses.add(currentAddress.add(10));                 addresses.add(currentAddress.add(11));                 addresses.add(currentAddress.add(12));                  setBackgroundColor(addresses, new Color(100, 100, 200));         } |
| --- |


From a script, using the service directly:


| public void run() throws Exception {                 ColorizingService service = state.getTool().getService(ColorizingService.class);                 if (service == null) {                         println("Can't find ColorizingService service--ColorizingPlugin not installed");                                return;                 }                  service.setBackgroundColor(currentAddress, currentAddress, new Color(255, 200, 200));         } |
| --- |


## Navigating Colors


### Actions


**Next Color Range** - Available from the menu bar at **Navigation  →  Next Color Range** This action will
navigate to the next color range at an address larger than the current address. Depending
upon the range navigation options, either the bottom of the current range, or the top of
next range will be chosen.


**Previous Color Range** - Available from the menu bar at **Navigation  → Previous Color Range** This action will
navigate to the next color range at an address larger than the current address. Depending
upon the range navigation options, either the bottom of the previous range, or the top of
the previous range will be chosen.


> **Note:** You can change range navigation
behavior by editing the Navigation Range Navigation tool
options .


### Markers


You can also navigate to color ranges via the Listing's [navigation
markers](CodeBrowser.md#navigation-marker).


*Provided by: *Colorizing* plugin*


**Related Topics:**


- [Listing](CodeBrowser.md)
