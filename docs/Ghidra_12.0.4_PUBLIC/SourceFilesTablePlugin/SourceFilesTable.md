# Source Files Table Plugin


This plugin shows the source file information (described [below](#source-file-information)) associated with the current program and allows the user
to manage source file path [transforms](#source-path-transformations).


## Source Files Table


Each row in this table corresponds to a Source File added to the program's source file
manager. The columns show the source file, path, transformed path, and number of source map
entries for a source file. If the *Transformed Path* column is empty for a given source
file, then no transformation applies to that file. Note that there are optional columns,
hidden by default, to show the SourceFileIdType and identifier of each source file.


### Reload Model


This action reloads the Source File Table. Note that this can be an expensive operation
since the number of source map entries must be computed for each source file. For this
reason, the action is only enabled after program events which might change the data shown in
the table.


### Show Source Map Entries


This action brings up a table which displays all of the source map entries for the
selected source file.


### View Source Files


This action opens a source file (at line 1) in the configured viewer. Options for
configuring the viewer are described [below](#plugin-options).


### Transform File


This action allows you to create a file transform for the selected source file.


### Transform Directory


This action allows you to create a directory transform whose source is a user-selected
parent directory of the corresponding source file.


## Transforms Table


This table shows all of the source file transformations defined for a program.


### Remove Transform


This action removes the selected transform from the list of transforms.


### Edit Transform


This action allows you to change the destination of a transform (but not the source).


## Listing Actions


### View Source


This Listing action is enabled if there is source map information for an address. It will
open the corresponding source file at the appropriate line in a source code viewer (currently
Eclipse and VS Code are supported). Options for configuring the viewer are described [below](#plugin-options). If there are multiple source map entries
defined for an address, the user will be prompted to select which one to send to the viewer.
Performing this action on a particular line of the Source Map Listing field will open the
corresponding file in the viewer even if there are multiple entries defined at the current
address.


## Plugin Options


These options can be changed from the Code Browser via Edit-&gt;-Tool Options-&gt;Source
Files and Transforms.


### Use Existing As Default


If enabled, the SourcePathTransformer will just return a SourceFile's path if no transform
applies to the file.


### Viewer for Source Files


Selects the viewer to use for source files. The supported viewers are Eclipse and Visual
Studio Code. Your viewer of choice must be configured via the appropriate option in the
Front-End tool (aka Ghidra Project Window).


# Source File Information


Ghidra can store information about the source files for a program, including their locations
in the build environment and the correspondence between lines of source code and addresses in a
program. A common source of this information is debug data, such as DWARF or PDB.


A major use case of this information is to synchronize Ghidra with an IDE, such as
Eclipse.


## Source Files


A source file record in Ghidra consists of three pieces of information:


1. A path, which must be an absolute, normalized path using forward slashes. E.g.,
"/usr/src/main/file.c", "/C:/Users/Ghidra/sourceFile.cc".
2. A *SourceFileIdType*, which can be NONE, UNKNOWN, TIMESTAMP_64, MD5, SHA1, SHA256,
or SHA512.
3. An identifier, which is the value of the identifier as a byte array.


## Source Map Entries


A *Source Map Entry* associates a source file and a line number to an address or
address range in a program. It consists of:


1. A source file.
2. A line number.
3. A base address.
4. A length. If the length is non-zero, the entry defines an address range, otherwise it
defines an address.


Source map entries are constrained as follows:


- An address in a program may not have duplicate (same source file, line number, base
address, and length) source file entries.
- Given two source map entries with non-zero lengths, their associated address ranges
must be either identical or distinct (i.e., no partial overlaps). Multiple source maps
entries based at the same address are allowed as long as they obey this restriction. Length
zero entries may occur anywhere, including within ranges corresponding to entries of
non-zero lengths.


## Source File Manager


Source files and source map entries are managed by a program's source file manager. A source
file must be added to a program before it can used in a source map entry. The DWARF, PDB, and
Go analyzers add source files and source map entries to a program by default. There are no GUI
actions to add source files or source map entries to a program, but such information can be
added to a program via a Ghidra Script. There are example scripts in the "SourceMapping" script
category.


> **Note:** Note that adding source files,
removing source files, or changing the source map requires an exclusive checkout if the
program is in a shared Ghidra repository. Reading the source file list or source map does not
require an exclusive checkout.


## Source Path Transformations


Source file path information can be sent to an external tool, such as an IDE. However, there
is no guarantee that a path recorded for a source file exists on the machine running Ghidra.
For instance, you could use Ghidra running under Linux to analyze a Windows program with source
file information. An additional complication is that the program may be in a shared Ghidra
repository where users have different operating systems or local file systems. We solve this
issue by allowing users to modify source file paths. The modifications are stored locally for
each user and are not checked in to a shared repository.


A note on terminology: to avoid overuse of the word "map", we use "map" when discussing the
association of a source file and a line number to an address and length in a program (the
"source file map"). We use the word "transform" when discussing user-determined modifications
of a source file's path.


There are two type of source path transforms:


1. *File Transforms*, which entirely replace a source file's path with another file
path.
2. *Directory Transforms*, which replace a parent directory of a source file's path
with another directory. For example, the directory transform "/src/ -&gt;
"/usr/test/files/" would transform the path "/src/dir1/file.c" to
"/usr/test/files/dir1/file.c".


Given a source file, the transformed path is determined as follows. If there is a file
transform for that particular file, the file transform is applied. Otherwise, the most specific
directory transform (i.e., the one replacing the longest initial segment of the path) is
applied. If no transform is applied, the user may opt to use the untransformed path.


Source file path transformations are managed using a *SourcePathTransformer*. Path
transformations can be managed using the actions on the [Source
Files Table](#source-files-table). In a script, you can get the path transformer for a program via the static
method *UserDataPathTransformer.getPathTransformer(Program)*. Note that modifications to
the path transformer are not affected by undo or redo actions in Ghidra.


**Related Topics:**


- [Source
Map Field](../CodeBrowserPlugin/CodeBrowserOptions.md#source-map-field)
- [Eclipse
Integration](../EclipseIntegration/EclipseIntegration.md)
- [Visual Studio Code
Integration](../VSCodeIntegration/VSCodeIntegration.md)
