[Home](../index.md) > [BlockModel](index.md) > Block Models

# Block Model


A *Block Model* partitions the code into address
ranges based on some set of rules.  The most obvious partitioning is by subroutine.
There are four Subroutine Models (i.e., Call Block Models).  Each subroutine model defines
a subroutine slightly differently.  The primary differences are based on number of entry
points and whether overlapping code between subroutines is allowed.  It is important to
note that all of these subroutine models will all produce the same result for an M-Model
subroutine which contains a single entry point.


**Subroutine Block Models:**


| Model Name | Model | Entry Point | Overlapping Code? | Entry Point Type |
| --- | --- | --- | --- | --- |
| Isolated Entry* | S | 1 | Yes | only call |
| Multiple Entry | M | 1 or more | --- | only call |
| Overlapped Code* | O | 1 or more | Yes | only call |
| Partitioned Code* | P | 1 | No | any |


- ***Isolated Entry Model**** - A subroutine
must have only one entry point but may share code with another subroutine.  The
subroutine body will stop if another called or source entry point is encountered.
- ***Multiple Entry Model*** - A subroutine may
have multiple entry points and may not overlap code from other subroutines.
- ***Overlapped Code Model**** - A subroutine
is all code accessible from a single entry point and terminates at returns.  Code may be
shared with other subroutines.  Each subroutine is defined to include the overlapping
code as part of its body.
- ***Partitioned Code Model**** - There is
exactly one entry point which may have any type of source flow.  Each instruction
belongs to exactly one subroutine (code is not shared).


*The default
subroutine model for the tool can be specified from **Edit*****→*****Tool Options** dialog on
**[Tool](../Tool/ToolOptions_Dialog.md)** panel.  The default
subroutine model is generally used by those plugins and actions which do not provide a
subroutine model choice (e.g., subroutine selection, call graph, symbol table, etc.).*


There is a more primitive *Block Model* called a
Basic (or Simple) Block Model.  Such blocks generally consist of small runs of
instructions partitioned based on change in instruction flow.  Jump and Branch
instructions will cause the execution flow to change, creating a new block.
Arithmetic and store/load instructions do not break a Basic Block because they do not change
the execution flow.  A label will also end one block and begin another.


In the
example below each color change represents a different basic block.


![](images/BasicBlockCode.png)


Provided By:  *Block Model Service* Plugin


**Related Topics:**


- [Create
Function](../FunctionPlugin/Functions.md)
- [Select
Subroutines](../Selection/Selecting.md)


---

[← Previous: Appendix](../Misc/Appendix.md) | [Next: Languages →](../LanguageProviderPlugin/Languages.md)
