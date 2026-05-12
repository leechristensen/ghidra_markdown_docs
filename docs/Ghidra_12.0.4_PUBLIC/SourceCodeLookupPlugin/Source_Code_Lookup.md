# Source Code Lookup Plugin


*Source Code Lookup* attempts to look up a symbol contained within a Ghidra program,
in the source of a C/C++ Eclipse project.


> **Note:** This plugin requires that Eclipse,
the Eclipse GhidraDev plugin, and the Eclipse CDT plugin are installed on your system.


## Setting up Eclipse


1. Install Eclipse.  The *Minimum Requirements* section of
***Extensions/Eclipse/GhidraDev/GhidraDev_README.html*** describes what versions
of Eclipse are supported.  Note that Eclipse is not provided by Ghidra...it must obtained
independently.
2. Install the Eclipse GhidraDev plugin into Eclipse. See
***Extensions/Eclipse/GhidraDev/GhidraDev_README.html***
for information on how to install the GhidraDev plugin into Eclipse.  Your Ghidra
distribution provides the most up-to-date version of the GhidraDev plugin at the time of
that distribution's release.
3. Install the Eclipse CDT plugin into Eclipse.  The *Minimum Requirements* section
of ***Extensions/Eclipse/GhidraDev/GhidraDev_README.html*** describes what
versions of the CDT are supported.  Note that the CDT is not provided by Ghidra...it must
be obtained independently.
4. Create a new C/C++ project (**File → New → Project...**) and give it a
name. The other options do not matter for this plugin.
5. Drag any source code for the binary into the Eclipse project
6. Change the Eclipse indexer settings if necessary (Right click on your project and
select **Properties → C/C++ General → Indexer**). Options such as "Index
source files not included in the build" and "Index unused headers" will make sure that
all of the files in the project get indexed if you have partial source code
7. Edit the GhidraDev Eclipse preferences to point to the project you want to search
(**Eclipse** or **Window → Preferences... → GhidraDev → Symbol
Lookup → Project Name**). The name used here must match the name of the C++ project
created in above.


## Using Source Code Lookup


To use the source code lookup feature, place the [Listing](../CodeBrowserPlugin/CodeBrowser.md) cursor on the symbol you want
to lookup and choose from the menu **Navigation → Go To Symbol Source**.


You can also execute this action when your cursor is in the [Decompiler](../DecompilePlugin/DecompilerIntro.md).


## Troubleshooting


- The port numbers may not match between Ghidra and Eclipse
  - Check that the Ghidra port (Ghidra Front End GUI: **Edit → Tool Options...
→ Eclipse Integration → Symbol Lookup Port**) matches the Eclipse port
(**Preferences → GhidraDev → Symbol Lookup → Port**)
- The Eclipse plugin may be using the wrong project
  - Select the C/C++ project to be used by the Eclipse plugin (**Preferences →
GhidraDev → Symbol Lookup → Project Name**)


*Provided by: *Source Code Lookup Plugin**


**Related Topics:**


- [Code Browser](../CodeBrowserPlugin/CodeBrowser.md)
