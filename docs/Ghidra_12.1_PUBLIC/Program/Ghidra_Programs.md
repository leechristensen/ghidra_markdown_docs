[Home](../index.md) > [Program](index.md) > Programs

# Ghidra Programs


A Ghidra [program](../Glossary/glossary.md#program) is an executable unit of
software or some group of data. It can be viewed and
analyzed within a [Ghidra
tool](../Tool/Ghidra_Tool_Administration.md).
A Ghidra program is
stored in a project folder. An assembly [language](../LanguageProviderPlugin/Languages.md)
is associated with a program at the time it is created. The language is used for
disassembling bytes into [instructions](../Glossary/glossary.md#instruction). Each program
defines its own [address spaces](../Glossary/glossary.md#address-space) and
[memory](../Glossary/glossary.md#memory). Various program elements can be added to the program to further
define it as part of the reverse engineering process. Some of the elements that
can be defined in the program are labels,
references, comments, functions, and data.


A Ghidra program is created by [importing](../ImporterPlugin/importer.md)
a file into a [Ghidra project](../Project/Ghidra_Projects.md).
This can be accomplished from either the [Ghidra
Project Window](../FrontEndPlugin/Ghidra_Front_end.md) or any Ghidra tool.  Once a program is part of a Ghidra
Project, the following actions can be performed:


- [Open](../ProgramManagerPlugin/Opening_Program_Files.md)
- [Close](../ProgramManagerPlugin/Closing_Program_Files.md)
- [Rename](../FrontEndPlugin/Ghidra_Front_end.md#rename)
- [Save](../ProgramManagerPlugin/Saving_Program_Files.md)
- [Delete](../FrontEndPlugin/Ghidra_Front_end.md#delete)
- [Export](../ExporterPlugin/exporter.md)
- [About](../About/About_Program_File.md)


**Related Topics:**


- [Ghidra Projects](../Project/Ghidra_Projects.md)
- [Ghidra Tools](../Tool/Ghidra_Tool_Administration.md)


---

[← Previous: Project Access List](../FrontEndPlugin/Ghidra_Front_end.md) | [Next: Import Program →](../ImporterPlugin/importer.md)
