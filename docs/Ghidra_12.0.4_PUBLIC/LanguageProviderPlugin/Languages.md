[Home](../index.md) > [LanguageProviderPlugin](index.md) > Languages

# Processor Languages


All processors have an associated language that defines the mapping
between
user readable assembly language instructions (e.g. MOV, ADD,
etc.)  and their
corresponding byte values.  In order to disassemble a binary image
for a
specific processor, Ghidra requires a *language module* for that
processor.
A language module is the software that implements the language
translation.
Ghidra has a set of language modules for the most commonly-used
processor
languages. New languages can be added to Ghidra by writing new language
modules.


Ghidra uses a processor modeling language called Sleigh to define the binary
parsing and instruction symantics associated with each language.
The semantic information allows for
more
advanced analysis and enables features such as the decompiler.


The list of available languages can be found in the **Ghidra Release Notes**.





## Setting a Program's Language


All programs are initially assigned a Processor Language when they
are first imported into a project.  The processor language can be
changed, but only to a closely related language.
Any stored register values will
be transferred if there is a register with the same name in the new
language.  If a matching register can't be found those values will
be removed.


> **Note:** If your program has been added to version control in a shared
project , you must first have an exclusive
check out on the file before you can set the language.
In addition, the program file may not be open in a tool when changing
the assigned processor language.


To change the processor language, right-click on the prorgam file
within the Project Window
data tree, and setlect Set Language...
from the popup menu.  Since setting the language is such a major
change, the following warning will appear.


![](images/Warning.png)


Alternatively, if your file is versioned, you
should check-in any recent changes prior to performing this
operation.  If you press the "OK" button, the Select Language
dialog will be displayed:


![](images/Languages.png)


Select the language from the list and press "OK" to
change the processor language for the current program.  If the
selected language is
sufficiently similar to the existing language, the change will be
made.  Otherwise, an error dialog will appear and the change will
not be allowed.
*By default, a filter will automatically be applied that displays the
most
compatible languages. It is recommended to only use one of these
languages.*


> **Note:** Once the operation completes successfully the only way to
revert to the previous language (aside from attempting another Set
Language) is to undo your checkout if it is versioned.  Otherwise,
you must rely on a backup copy which you hopefully made prior to the
operation.


> **Note:** Set Language will fail if any old address
space can not be mapped to the same size or larger address spaces
within the new language.  This allows migration to larger
processor implementations (e.g., 32-bit to 64-bit), but not the reverse.


## PCode


The semantic information provided by the SLED and SLEIGH-based
languages is called PCode (a form of generic microcode).  Each
assembly language instruction can be
broken down into one or more PCode instructions.  The more
advanced automatic analysis features in Ghidra require PCode in order
to operate.


To see PCode, add the PCode field in the Instruction/Data tab of the
[Browser Field](../CodeBrowserPlugin/Browser_Field_Formatter.md).
The figure
below shows a CodeBrowser with the PCode field added.


![](images/PCodeDisplay.png)


**Related Topics:**


- [Analysis](../AutoAnalysisPlugin/AutoAnalysis.md)
- [Disassembly](../DisassemblerPlugin/Disassembly.md)


---

[← Previous: Block Models](../BlockModel/Block_Model.md)
