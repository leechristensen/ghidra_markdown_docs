[Home](../index.md) > [AssemblerPlugin](index.md) > Assembler

# Assembler


![](images/Assembler.png)


Assembly Editor


The Assembler plugin provides actions for modifying program bytes by inputing mnemonic
assembly and data values.


## Actions


There are two actions: One for instructions and one for data.


### Patch Instruction


This action is available at any initialized memory address. It allows you to edit the
current assembly instruction in the listing. The first time you use the action, it may take a
moment to prepare the assembler for the current program's processor language. You can then edit
the text of the instruction, optionally replacing it altogether. As you edit, a content assist
will provide completion suggestions. When the text comprises a valid instruction, it will also
display assembled byte sequences. Activating a suggestion will input that text at your cursor.
Activating a byte sequence will finish the action, replacing the instruction at the current
address. Pressing ESC or clicking outside of the assembly editor will cancel the action.


At times, the assembler will generate undefined bits. Typically, these bits are actually
reserved, and so by default, the assembler fills them with 0s. The toggle below the content
assist will cause the assembler to fill them will all possible patterns of 1s and 0s. This
toggle should be used with care, since some languages may generate many undefined bits, and
each bit grows the list by a factor of 2.


Ghidra's assembler is based on the same SLEIGH modeling that powers the disassembler. This
offers some nice benefits:


- There is no need for an external tool chain.
- The assembler and disassembler share the same mnemonic syntax.
- Most Ghidra-supported processors are also supported by the assembler.
- Processors added to Ghidra automatically get an assembler (most of the time).


Keep in mind, the above list is in an ideal world. The assembler essentially "solves" the
disassembly routine for its input given a desired output. While the process works well in
general, some languages require special attention. Thus, we periodically test our processor
languages for assembly support and assign each a performance rating. The possible ratings
are:


1. **Platinum:** Our automated tests did not find any errors. This offers the best
possible user experience.
2. **Gold:** Our automated tests found a couple of small errors. You should rarely
encounter issues.
3. **Silver:** Our automated tests found a handful of errors, or perhaps one large class
of errors. You will likely encounter one, but still find the assembler useful.
4. **Bronze:** Our automated tests found many errors, or perhaps a few large classes of
errors. You are very likely to encounter them, but still may find the assembler useful, if
not just a bit frustrating.
5. **Poor:** Our automated tests found many severe errors, and/or several large classes
of errors, or the tests could not complete. You will likely encounter an error the first time
you try using it. A few instructions may assemble correctly, but it'll be more frustrating
than useful.
6. **Unrated:** The processor is not tested. Your experience will depend on the
complexity of the processor language. In general, the more SLEIGH context operations,
especially those preceding the main instruction table, the more issues that may arise.


If the current processor scored anything less than **Platinum** you will receive a
friendly warning reminding you what to expect.


### Patch Data


This action is available at initialized memory addresses having a data unit with a type that
provides an encoder. It allows you to edit the current data unit by typing its string
representation. There is (currently) no content assist, and generally only primitive types and
strings are supported. **NOTE:** Strings must be enclosed in double quotes, since that is
how they are displayed in the listing. Pressing ENTER attempts to encode the data and place it
at the current address. If this fails, the error is displayed in Ghidra's status bar, and the
input fields remain on screen.


*Provided by: *Assembler* plugin*


**Related Topics:**


- [Listing View](../CodeBrowserPlugin/CodeBrowser.md#code-browser)


---

[← Previous: Ghidra Functionality](../Intro/GhidraFunctionality.md) | [Next: BSim →](../BSim/BSimOverview.md)
