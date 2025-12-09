[Home](../index.md) > [Tool](index.md) > Undo/Redo

# Undo/Redo


*Undo* is a generalized capability for returning a program back to a state
prior to the last edit operation.  *Redo* is the opposite of *Undo* and it
effectively re-applies the last edit operation.  *Undo* can be applied repeatedly to
erase the effects of  a sequence of edit operations up to a current limit of 20.
After performing a sequence of *Undo* operations, the same number of *Redo*
operations are available. However, the instant a new edit is performed, the *Redo* list is
cleared.


- To *undo* an edit operation, select **Edit → Undo** from the main menu or press the ![Undo](../icons/edit-undo.png)
button on the tool bar.
- To *redo* an edit operation, select **Edit → Redo** from the main menu or press the ![Redo](../icons/edit-redo.png)
button on the tool bar.


> **Tip:** Hovering the mouse over the button will display the name of the edit operation that would be "undone".  Similarly,
hovering the mouse over the button will display the name of the edit
operation that would be "redone".


> **Tip:** Also, pressing the drop-down arrow will show a list
of all the undo/redo's that are available. Clicking on one of those will undo/redo that
item and all the ones above it.


---

[← Previous: Keyboard Navigation](../KeyboardNavigation/KeyboardNavigation.md) | [Next: Glossary →](../Glossary/glossary.md)
