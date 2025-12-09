[Home](../index.md) > [DecompilerTaint](index.md) > Decompiler Taint

# Decompiler Taint Operations


Taint-tracking is the ability to capture the flow of data through a program by following transfers
from one variable to another. Often, this involves specifying where the data originates (a source)
and which endpoints are of interest (sinks).  In Ghidra, taint-tracking leverages external engines
which rely on the SSA-nature of Ghidra's PCode to describe varnode-to-varnode flows.


Taint-tracking is a four-step process. First, the PCode underlying the target program must be exported
to a directory for subsequent "indexing". Second, the program is indexed creating an index database.
These are one-time actions and need only be re-executed when you change programs or modify the target
program's PCode in a substantive way. Given a database, any number of queries may be processed using
the index. Step three, making a query generally includes marking sources and sinks, and then executing
the query. Last, the results of the query may be selectively re-applied as markup on the decompilation/disassembly.


The first two steps are activated in the menus under **Tools → Source-Sink**. Their options
are accessible via **Edit → Tool Options** under **Options/Decompiler/Taint**. The third step is controlled by
the pop-up menus (or associated keyboard actions) and the toolbar items within the Decompiler window.
Pop-up menus on the results table control how the results are applied.


## Initialization Actions (Tools → Source-Sink)


### Delete Facts and Index


Deletes any pre-existing data (facts and database) from the directories specified under
Taint Options.


### Export PCode Facts


Run an engine-specific ghidra script to export the PCode for the current program as a set
of ASCII fact files to be consumed by the engine.  (For CTADL, our default engine, this
script is ExportPCodeForCTADL.java.)


### Initialize Program Index


Converts the directory of PCode facts into an indexed database for future queries.


### Re-export Function Facts


Updates the existing fact set for the current function, which may be useful if the
decompilation has been improved during the course of analysis. (Does require re-indexing
the database.)


## Tool Options (Options/Decompiler/Taint)


These options govern the locations for various elements of the taint engine.


### Directories.Engine


Path to the executable responsible for the taint engine logic.


### Directories.Facts


Directory where PCode facts will be written.


### Directories.Output


Directory where database index and queries will be written.


### Query.Current Query


The file containing the most recent query.


### Query.Index


Name of the file that contains the database produced by the "Index" operation.


### Force Direction


May be "forward", "backward", "all", or blank. Forward computes all source-to-sink
slices, backward sink-to-source slices, and all both.  Blank chooses source-to-sink
or sink-to-source based on whether the number of sources or the number of sinks is
greater.


### Highlight Color


The color used for taint highlights in the decompiler.


### Highlight Style


"All", "Labels", or "Default".


### Match on Fields


Use all access paths, including field references, for sink/source variables.


### Output Format


Describes the output set.  Currently default to "sarif+all", which should be appropriate
for most cases.  Other options are "sarif" (output paths only), "sarif+instructions"
(output paths and instructions), and "sarif+graphs" (output paths and graphs).


### Query Engine


The engine to be used for formatting queries (e.g. ctadl, angr).


## Decompiler Pop-up Menu and Keyboard Actions


The following actions appear in the **Taint** sub-menu of the Decompiler's context menu,
accessed by right-clicking a token. The pop-up menu is context sensitive and
the type of token in particular determines what actions are available.
The token clicked provides a local context for the action and may be used to pinpoint the exact
variable or operation affected.


### Source


Mark the selected varnode as a taint source.


### Source (Symbol)


Mark the symbol associated with the selected varnode as a taint source.


### Sink


Mark the selected varnode as a taint sink (i.e. the endpoint).


### Sink (Symbol)


Mark the symbol associated with the selected varnode as a taint sink.


### Gate


Mark the selected varnode as a gate (i.e. taint will not pass through this node).


### Clear


Remove the source, sink, and gate markers, and existing taint.


### Slice Tree


Launch a call-tree style viewer for the slices for the selected token.


## Decompiler Toolbar Actions


These actions apply after the source and sinks have been chosen.


### Run taint query


Uses the defined source, sinks, and gates to compose and execute a query. Input
may include parameters, stack variables, variables associated with registers, or
"dynamic" variables. Queries require an index database generated from PCode.


### Run default taint query


Use pre-defined sources and sinks to execute the engine's default query.
(Ignores the sources and sinks specified by the user and tries to apply whatever
the engine considers the de-facto set of sources/sinks - which may be undefined
for a given target.)


### Run custom taint query


Executes the query referenced in option without rebuilding it based on sources, sinks, etc.
Unedited, this will re-execute the last query, but the file can be modified by hand to reflect
any query you're interested in.


### Load SARIF file


Loads a raw SARIF file into the results table.


### Show label table


Displays the current set of source, sink, and gate markers.


## Results Pop-up Menu


These actions appear in the context menu of the Query Results table and transfer the selected results to the decompiler/disassembly.


### Add To Program


Applies SARIF results to the current progam generically, based on the current set of handlers.


### Apply taint


Highlight the varnodes which have been tainted.


### Clear taint


Clear taint matching the selected rows from the Decompiler listing.


### Make Selection


Create a selection from the selected addresses.


---

[← Previous: Decompiler](../DecompilePlugin/DecompilerIntro.md) | [Next: Decompiler Concepts →](../DecompilePlugin/DecompilerConcepts.md)
