[Home](../index.md) > [BSimFeatureVisualizerPlugin](index.md) > BSim Feature Visualizer

# BSim Feature Visualizer Plugin


The **BSim Feature Visualizer Plugin** is used to visualize the
[BSim Features](../BSim/FeatureWeight.md#features-of-software-functions) of the function at the current address.



## The BSim Feature Table


The features are displayed in the **BSim Feature Table**. In order to
explain the columns of the table, we first briefly discuss BSim feature types.


### DATA_FLOW features


These features describe data flow into a single "base" varnode.  A neighborhood of the data
flow graph consisting of the base varnode and all vertices reachable by traversing edges
against the direction of flow (through at most 3 pcode ops) is hashed to produce these
features.



### CONTROL_FLOW features


These features describe small neighborhoods of the control flow graph. Each neighborhood
is defined by a "base" block.


### COMBINED features


These features are generated from a neighborhood in the control flow graph and data flow
information into the first "root" pcode op in the block, which must be either a CALL, CALLIND,
CALLOTHER, STORE, CBRANCH, BRANCHIND, or RETURN op.


### DUAL_FLOW features


These features are formed from two adjacent "root" ops (as defined above) in a single basic
block.


### COPY_SIG features


These features are formed from the "standalone copies" within a basic block.  An example of
a standalone copy is an assignment of a constant to a global variable with no further dataflow
within the function.


### Table Columns


We now list the columns of the BSim feature table.  Note that some columns only apply to
some BSim feature types. If a column does not apply to a given feature it will be blank the in
corresponding row.


- **Sequence Number**:
(See [here](../DecompilePlugin/DecompilerConcepts.md#p-code-operations)
for details on sequence numbers).For DATA_FLOW and COMBINED features,
this column contains
the sequence number of the pcode op associated with the feature.  For DUAL_FLOW features it
contains the sequence number of the main pcode op (which is the second op in address order).
For CONTROL_FLOW features it contains an artificial sequence number corresponding to the
beginning of the associated basic block.
- **Address**: This column is hidden by default. It contains the address corresponding to
the sequence number defined above.
- **Base Varnode**: For DATA_FLOW features, this column shows the corresponding base
varnode.  For other feature types it is blank.
- **Basic Block Start**: For CONTROL_FLOW and COMBINED features this is the start address
of the basic block corresponding to the feature.  For DATA_FLOW and DUAL_FLOW features it is
the start address of the basic block containing the relevant pcode op(s).
- **Block Index**: This is the block index of the basic block defined above.
- **Feature**: This is the 32-bit hash corresponding to the feature.
- **Feature Type**: The feature type of the feature.
- **Pcode Op Name**: For DATA_FLOW features this is the name of the pcode op defining the
base varnode.  For COMBINED features it is the root pcode op, and for DUAL_FLOW features it is
the main pcode op.
- **Previous Op Info**: For DUAL_FLOW features, this is the Mnemonic and Sequence number
of the previous pcode op.


## Visualizing BSim Features


To visualize a BSim feature, right-click on a row in the BSim Feature Table and select
"Highlight and Graph". This action creates a graph showing the regions of the control flow and
data flow graphs which correspond to the feature.  Most (but not all) of the data that goes
into the hash is depicted in the graph.  The action also highlights some tokens in the
decompiler associated with the feature.  Note that if the "Highlight by Row" option is
selected then the decompiler highlight is applied automatically whenever the selected
row changes.



### The Graph


Hovering over a vertex or edge in the graph will display a popup listing its attributes.
Vertices corresponding to basic blocks are displayed as rectangle whereas vertices
corresponding to varnodes and pcode ops are generally drawn as circles (function inputs and
constants are drawn as triangles).  Certain COPY, MULTIEQUAL, and INDIRECT ops are colored
differently to indicate that they are collapsed during feature generation.  Note that the graph
can be used to navigate and make selections.



### Decompiler Highlights


Certain tokens in the decompiler corresponding to the feature are highlighted in the
decompiler.  In general, the highlight show less information than the graph.  For instance,
for DATA_FLOW features, only the base varnode, its defining op, and the line containing them
are highlighted.  Note that sometimes there will not be a token to highlight, which can result
from features of temporary varnodes that are not associated with a C language token. Also note
that the decompiler performs additional transformations when producing C code which can
complicate token highlighting.



### Removing Decompiler Highlights


Click the ![error.png](../icons/error.png) in the upper right corner of the table to clear any
decompiler highlights added by this plugin.  Other decompiler highlights are unaffected.


## Options


This plugin has several options which can be set in the Tool Options menu.


### Database Configuration File


This file is a BSim database configuration template.  An "index tuning" parameter is
read from this file and passed to the decompiler when generating BSim features. See
[here](../BSim/DatabaseConfiguration.md#creating-a-database)
for details.


### Reuse Graph


If checked, the same graph window will be used to display all BSim feature graphs.  Only
one feature graph is displayed at a time (the previous feature graph will be cleared).  If
unchecked, each feature graph will be drawn in a separate window. Note that in either case only
one feature at a time will be highlighted in the decompiler.


### Decompiler Timeout


This parameter controls the maximum amount of time (in seconds) the decompiler will spend
trying to decompile a function before quitting.


### Highlight by Row


If selected, the decompiler highlights will be applied whenever the selected row in the
BSim Feature Table changes.


---

[← Previous: Comparing Feature Vectors](../BSim/FeatureWeight.md) | [Next: Command-Line Utility Reference →](../BSim/CommandLineReference.md)
