[Home](../index.md) > [ConsolePlugin](index.md) > Console

# Console


The *Console* is a generic message output component.


Any plugin can use the console service to send messages to the console.  It is
mostly used to display output from scripts.


The *Console* shows two different kinds of output, each in a different
color.


- Standard output (black)
- Standard error (red)


![](images/Console.png)


## Scroll Lock


This action stops the console from automatically scrolling as new output is
appended.


## Clear


This action clears all content in the *Console* component.


## Find


This action shows a dialog that allows you to search for all occurrences
of some text.  The dialog supports
[Regular Expressions](../Search/Regular_Expressions.md#regex-syntax).
While the dialog is open, all matching text is highlighted.  If the cursor is in a match,
then the highlight color for that match will be different than the rest.


## Navigation


If the console contains text that represents a valid symbol or address, then
you can navigate to that symbol or address by double-clicking on it. You will know if the
text is valid, because the mouse cursor will change from the pointer to a hand.


*Provided by: *ConsolePlugin**


**Related Topics:**


- [Table Sorting](../Tables/GhidraTableHeaders.md)
- [Regular Expressions](../Search/Regular_Expressions.md)


---

[← Previous: Add and Remove Script Directories](../GhidraScriptMgrPlugin/GhidraScriptMgrPlugin.md) | [Next: Ghidra Script Development →](../GhidraScriptMgrPlugin/ScriptDevelopment.md)
