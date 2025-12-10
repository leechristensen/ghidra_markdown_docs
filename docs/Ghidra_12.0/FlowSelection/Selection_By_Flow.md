[Home](../index.md) > [FlowSelection](index.md) > Selection by Flow

# Selecting Scoped Flow


Scoped [Flow](../Glossary/glossary.md#flow) is the potential flow
through a function, removing any flow that is not in the selected scope.
This is useful for determining how to reach a set of instructions.


## Forward and Reverse Scoped Flow


*Forward scoped flow* is the set of addresses that can only be reached by
passing through the [Basic Block](../Glossary/glossary.md#basic-block) containing the current address.


*Reverse scoped flow* is the set of addresses that must pass through the
[Basic Block](../Glossary/glossary.md#basic-block) containing
the current address.


To create forward or reverse scoped
[selections](../Selection/Selecting.md), use one of the
following two actions, respectively:


- From the menu bar choose **Select****→
Scoped Flow → *Forward Scoped Flow***
- From the menu bar choose **Select****→
Scoped Flow → *Reverse Scoped Flow***


*Provided by: *Select By Scoped Flow* Plugin*


**Related Topics:**


- [Selecting in Ghidra](../Selection/Selecting.md)
- [Highlighting](../SetHighlightPlugin/Highlighting.md)


---

[← Previous: Selection](../Selection/Selecting.md) | [Next: Selection Highlighting →](../SetHighlightPlugin/Highlighting.md)
