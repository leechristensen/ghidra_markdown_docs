[Home](../index.md) > [SetHighlightPlugin](index.md) > Selection Highlighting

# Highlighting


A highlight is a more permanent variation of a [selection](../Selection/Selecting.md). As you may recall, a selection can be
cleared simply by clicking in the Code Browser. In order to clear a highlight, you must
explicitly select the **Select →  Highlight** →  option.


You would commonly use a highlight when you do not want to lose a selection. For example,
you just used [Search Memory](../Search/Search_Memory.md) to search for
all the occurrences of a particular Ascii string. From the *[Query Results](../Search/Query_Results_Dialog.md)* window, you selected all of
the results. Now you wish to visit each code unit in the selection and perform some operations.
A selection would not be entirely useful, because, if you clicked anywhere in the Code Browser,
the selection would be lost. Converting this selection to a highlight enables you to visit each
code unit and click around in the browser, without losing the highlight for the search
results.


### **To set
a highlight from a selection**


1. Create a selection in the Code Browser
2. From the menu-bar of the Code Browser, select **Select  →  Highlight** **→** **Selection**
OR
From the right mouse popup menu of the Code Browser, select **Highlight**
**→** **Entire
Selection**


### **To clear a
highlight**


1. From the menu-bar of the Code Browser, select **Select  →  Highlight** **→** **Clear**
OR
From the right mouse popup menu of the Code Browser, select **Highlight**
**→** **Clear**


### **To
add a selection to a highlight**


1. From the menu-bar of the Code Browser, select **Select  →  Highlight** **→** **Add Selection**
OR
From the right mouse popup menu of the Code Browser, select **Highlight**
**→**  **Add
Selection**


### **To subtract a selection from a highlight**


1. From the menu-bar of the Code Browser, select **Select  →  Highlight** **→** **Subtract Selection**
OR
From the right mouse popup menu of the Code Browser, select **Highlight**
**→**  **Subtract
Selection**


### **To
create a selection from a highlight**


1. Create a highlight in the Code Browser
2. From the menu-bar of the Code Browser, select **Select  →  From Highlight**
OR
From the right mouse popup menu of the Code Browser, select **Select**
**→** **Entire
Highlight**


*Provided By: *Set Highlight Plugin**


## Navigating over a highlight


A highlight will usually consist of one or more address ranges. The address ranges do not
have to be contiguous. Two methods exist to allow navigation over these ranges:


### Using the Navigation Margin


One or more yellow markers will appear in the [Navigation Margin](../CodeBrowserPlugin/CodeBrowser.md#cbnavigationmargin),
where each yellow marker corresponds to an address range included in the highlight.
Clicking on a yellow marker will cause the Code Browser to navigate to the beginning of the
corresponding address range.


### Using the
Navigation Menu


From the menu-bar of the Code Browser, select either **Navigation  →  Previous Highlighted Range** or **Navigation  →  Next Highlighted Range**.


OR


From the tool-bar of the Code Browser, select either the **Go to previous highlighted
range** (![PreviousHighlightBlock16.gif](../icons/PreviousHighlightBlock16.gif)) and **Go to
next highlighted range** (![NextHighlightBlock16.gif](../icons/NextHighlightBlock16.gif))
buttons.


Clicking on the menu-bar or tool-bar options will cause the Code Browser to navigate to
the beginning of the corresponding address range.


> **Tip:** When the Code Browser is on or before the
first address range in the highlight, the "Previous Highlight Range" menu-bar and tool-bar
options will be disabled. Similarly, when the Code Browser is on or after the last address
range in the highlight, the "Next Highlight Range" menu and toolbar options will be
disabled.


*Provided By: *Next Prev Highlight Range Plugin**


**Related Topics:**


- [Selecting](../Selection/Selecting.md)
- [Code Browser](../CodeBrowserPlugin/CodeBrowser.md)
- [Navigation
Margin](../CodeBrowserPlugin/CodeBrowser.md#cbnavigationmargin)
- [Query Results](../Search/Query_Results_Dialog.md)


---

[← Previous: Selection by Flow](../FlowSelection/Selection_By_Flow.md) | [Next: Program Search →](../Search/Searching.md)
