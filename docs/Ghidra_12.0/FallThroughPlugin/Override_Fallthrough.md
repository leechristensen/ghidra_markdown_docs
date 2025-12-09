[Home](../index.md) > [FallThroughPlugin](index.md) > Set Fallthrough Address

# Fallthrough Address


The fallthrough address on an instruction is the address of the *next* instruction that
will be executed. You can change the fallthrough address by using the *Set Fallthrough
Address* dialog, as shown below. By default, an instruction's fallthrough address (or lack
thereof) is determined by the language processor. For example, a "return" or a "jump"
instruction does not have a fallthrough address.


| ![](images/SetFallThrough.png) |
| --- |


### Set a Fallthrough Address


The dialog shows the default fallthrough address of the instruction. The radio buttons
below the *Fallthrough Address* field indicate whether the address is the default
fallthrough or user defined. When the **Default** button is selected, the *Fallthrough
Address* field is disabled. If an instruction has no default fallthrough (e.g., "jump"),
the Fallthrough Address field is empty. Choose the **User** button to enter a new
fallthrough address. When the **User** button is selected, the *Fallthrough*
*Address* field is updated as you move the cursor in the Code Browser.


Select the Home button to navigate the Code Browser back to this address. The home panel
shows the address and the instruction when you selected the **Set** option.


To change the fallthrough address,


1. Position the cursor on an instruction.
2. Right mouse click and select **Fallthrough** → **Set...** to display the dialog.
3. Select the **User** radio button.
4. Enter an address
(or [Address Expression](../Misc/AddressExpressions.md)), or click in
the Code Browser at the address of the new fallthrough.
5. Select the **Apply** button to change the fallthrough and leave the dialog intact;
select the OK button to change the fallthrough and dismiss the dialog.


You can see the effects of setting the fallthrough address by selecting the [limited flows from option](../Selection/Selecting.md#select-limited-flows-from); the
instructions that are skipped over via setting the fallthrough address are not included in
the selection.


> **Tip:** Just below the overridden address will be a comment indicating the override, containing
the text Fallthrough Override , along with the updated fallthrough address.


To clear a fallthrough address using this dialog, select the **None** button, then
**Apply** or **OK**.


### Auto Override


The "auto override" feature skips over data following an instruction, finds the next
instruction following the data and sets this address as the fallthrough address. You can
automatically override the fallthrough address for a single instruction or override the
fallthrough addresses over a [selection](../Selection/Selecting.md).


To auto override,


1. [Make a selection](../Selection/Selecting.md) in the Code Browser
or position the cursor at an instruction.
2. Right mouse click and select **Fallthrough** → **Auto override**


> **Note:** The Auto Override option is disabled
for a single instruction if the instruction's fallthrough was already overridden.


### Clear Overrides


To clear overridden fallthroughs,


1. [Make a selection](../Selection/Selecting.md) in the Code Browser
or position the cursor at an instruction whose fallthrough address was overridden.
2. Right mouse click and select **Fallthrough** → **Clear Overrides**


> **Note:** The Clear Overrides option is disabled
for a single instruction if the instruction's fallthrough address was not overridden.


*Provided by: *FallthroughPlugin**


**Related Topics:**


- [Selections](../Selection/Selecting.md)
- [Code
Browser](../CodeBrowserPlugin/CodeBrowser.md)
- [Languages](../LanguageProviderPlugin/Languages.md)


---

[← Previous: View Properties](../PropertyManagerPlugin/Property_Viewer.md) | [Next: Navigation →](../Navigation/Navigation.md)
