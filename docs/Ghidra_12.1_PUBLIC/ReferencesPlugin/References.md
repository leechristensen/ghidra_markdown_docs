[Home](../index.md) > [ReferencesPlugin](index.md) > References

# References


Within Ghidra, the term "Reference" covers two very broad areas:


1. *Forward References* from a data or instruction code unit to a memory, external,
stack, or register location
2. *Back References* to a location of interest (e.g., code unit, variable, data-type,
etc.).


## Forward References


*Forward References* can be explicitly defined within the program, on data or
instruction code units. This is accomplished during disassembly, auto-analysis or manually by
the user. In addition, *Forward References* to function parameters and variables may also
be inferred. Both explicit and inferred *Forward References* can affect the code unit
rendering and XRefs (i.e., Back References) displayed within the CodeBrowser listing. The
effect of *Forward References* on the rendering of code unit operands can be somewhat
controlled by means of various Code Browser Options (see [Operands Field
options](../CodeBrowserPlugin/CodeBrowserOptions.md#operands-field)).


Management capabilities for explicit *Forward References* is provided by the
**ReferencesPlugin** and is discussed in detail within the [Forward References help section](References_from.md).


## Back References


*Back References* (also referred to as "*Location References*") include both the
inverse of *Forward References*, and the identification of listing locations where
specific data-types are utilized. The viewing of *Location/Back References* is provided by
the **LocationReferencesPlugin** and discussed in more detail on the [Location References Dialog help
section](../LocationReferencesPlugin/Location_References.md).


---

[← Previous: Displaying Comment History](../CommentsPlugin/Comments.md) | [Next: Forward References →](References_from.md)
