[Home](../index.md) > [RandomForestFunctionFinderPlugin](index.md) > Search for Code and Functions

# Random Forest Function Finder Plugin


This plugin trains models used to find function starts within a program.  Essentially,
the training set consists of addresses in a program where Ghidra's analysis was able to
find functions.  The models are then applied to the rest of the program.
Models can also be applied to other programs.


In the motivating use case, you either don't know the toolchain which produced a program
or do not have a large number of sample programs to train other types of models.


Note: in general, this plugin ensures that addresses used for training, testing, or
searching for function starts are aligned relative to the processor's instruction alignment.
Defined data within an executable block is an exception - all such bytes are added to
the test set as examples of non-starts.


## Basic Suggested Workflow


1. To begin, select *Search-&gt;For Code And Functions...* from the Code Browser.
2. Click the *Train* button to train models using the default parameters.
3. Choose the model with the fewest false positives (which will be apparent from
the *Model Statistics* table).
4. Right-click on that model's row and select *DEBUG - Show test set errors*.
5. Examine the resulting table to determine if there is a good cutoff for
the probabilities.  Note that some of the "errors" might not actually be
errors of the model: see the discussion in
[Debug Model Table](#debugmodeltable).
6. If you're satisified with the performance of the model, right-click on the
row and select *Apply Model*.  If you aren't, you can try changing the parameters
and training again.  You can also try the *Include Bit Features* training option.
7. In the resulting table, select all addresses with an *Undefined* interpretation whose
probability is above your threshold, right-click, and select *Disassemble*.  This will
start disassembly (and follow-on analysis) at each selected address.
8. Now, select all addresses whose interpretation is *Block Start* and whose probability
of being a function is above your threshold, right-click, and select *Create Function(s)*.
It's also probably worth filtering out any addresses which are the targets of
conditional references (which can be seen in the *Conditional Flow Refs* column).


The script *FindFunctionsRFExampleScript.java* shows how to access the functionality of
this plugin programmatically.


## Model Training Table


This table is the main interface for training and applying models.


### Data Gathering Parameters


The values in this panel control the number of models trained and the data used to train them.
The first three fields: [Number of Pre-Bytes (CSV)](#numberofprebytes),
[Number of Initial Bytes (CSV)](#numberofinitialbytes), and
[Start to Non-start Sampling Factors (CSV)](#starttononstartfactors) accept
CSVs of positive integers as input (a single integer with no comma is allowed).  Models
corresponding to all possible choices of the three values will be trained and evaluated.
That is, if you enter two values for the *Pre-bytes* field, three values for the
*Initial Bytes* field, and four values for the *Sampling Factors* field, a total
of 2*3*4 = 24 models will be trained and evaluated.


#### Number of Pre-bytes (CSV)


Values in this list control how many bytes before an address are used to construct its
feature vector.


#### Number of Initial Bytes (CSV)


Values in this list control how many bytes are used to construct the feature vector
of an address, starting at the address.


#### Start to Non-start Sampling Factors (CSV)


Values in this list control how many non-starts (i.e., addresses in the interiors
of functions) are added to the training set for each function start in the training set.


#### Maximum Number Of Starts


This field controls the maximum number of function starts that are added to the training
set.


#### Context Registers and Values (CSV)


This field allows you to specify values of context registers.  Addresses will only
be added to the training/test sets if they agree with these values, and the disassembly
action on the [Potential Functions Table](#functionstarttable) will apply the
context register values first.  This field accepts CSVs of the form "creg1=x,creg2=y,...".
For example, to restrict Thumb mode in an ARM program, you would enter "TMode=1" in this field.


#### Include Preceding and Following


If this is selected, for every function entry in the training set, the code units immediately
before it and after it are added to the training set as negative examples (and similarly for the
test set).


#### Include Bit Features


If this is selected, a binary feature is added to the feature vector for each bit in the
recorded bytes.


#### Minimum Function Size


This value is the minimum size a function must be for its entry and interior to be included
in the training and test sets.


### Function Information


This panel displays information about the functions in the program.


#### Functions Meeting Size Bound


This field displays the number of functions meeting the size bound in the
[Minimum Function Size](#minimumfunctionsize) field.  You can use
this to ensure that the value in [Maximum Number
of Starts](#maximumnumberofstarts) field doesn't cause all starts to be used for training (leaving
none for testing).


#### Minimum Undefined Range Size


This value is the minimum size of an undefined address range that will be considered when
applying the model to a program. Defaults to the value stored in the plugin options, see
[Minimum Length of Undefined Ranges to Search](#minlengthundefinedrange).


#### Restrict Search to Aligned Addresses


If this is checked, only addresses which are zero modulo the value in the
[Alignment Modulus](#alignmentmodulus) combo box are searched for function starts.
This does not affect training or testing, but can be a useful optimization when applying
models, for instance when the [Function Alignment Table](#functionalignmenttable)
shows that all (known) functions in the program are aligned on 16-byte boundaries.


#### Alignment Modulus


The value in this combo box determines the modulus used when computing the values in
the [Function Alignment Table](#functionalignmenttable).


#### Function Alignment Table


The rows in this table display the number of (known) functions in the program
whose address has the given remainder modulo the alignment modulus.


### Model Statistics


This panel displays the statistics about the trained models as rows in a table.
Actions on these rows allow you to apply the models or see the test set failures.


#### Apply Model Action


This action will apply the model to the program used to train it. The addresses
searched consist of all addresses which are loaded, initialized, marked as executable,
and not already in a function body (this set can be modified by the user via the
[Restrict Search to Aligned Addresses](#restrictsearchtoalignedaddresses)
and [Minimum Length of Undefined Ranges to Search](#minlengthundefinedrange)
options).  The results are displayed in a
[Function Start Table](#functionstarttable).


#### Apply Model To Other Program... Action


This action will open a dialog to select another program in the current project and
then apply the model to it.  Note that the only check that the model is compatible with
the selected program is that any context registers specified when training must be
present in the selected program.


#### Apply Model To Selection Action


This action will apply the model to the current selection in the program used to train it.


#### Debug Model Action


This action will display a [Debug Model Table](#debugmodeltable), which shows
all of the errors encountered when applying the model to its test set.


## Potential Functions Table


This table displays all addresses in the search set which the model thinks are function starts
with probability at least .5. The table also shows the current "Interpretation" (e.g., undefined,
instruction at start of basic block, etc) of the address along with the numbers of certain types
of references to the address.


The following actions are defined on this table:


### Disassemble Action


This action is enabled when at least one of the selected rows corresponds to an address
with an interpretation of "Undefined".  It begins disassembly at each "Undefined" address
corresponding to a row in the selection.


### Disassemble and Apply Context Action


This action is similar to the [Disassemble Action](#disassembleaction), except
it sets the context register values specified before training the model at the addresses
and then disassembles.


### Create Functions Action


This action is enabled whenever the selection contains at least one row whose corresponding
address is the start of a basic block.  This action creates functions at all such addresses.


### Show Similar Function Starts Action


This action is enabled when the selection contains exactly one row.  It displays
a [table](#similarstartstable) of the function starts in the training set
which are most similar to the bytes at the address of the row.


## Similar Function Starts Table


This table displays the function starts in the training set which are most similar
to a potential function start "from the model's point of view".  Formally, similarity
is measured using **random forest proximity**.  Given a potential start *p* and
a known start *s*, the similarity of *p* and *s* is the proportion of trees
which end up in the same leaf node when processing *p* and *s*.


For convenience, the potential start is displayed in a table with a single row directly
above the similar starts table.


## Debug Model Table


This table has the same format as the [Potential Functions Table](#functionstarttable)
but does not have the disassembly or function-creating actions (it does have the action to
display similar function starts).  It displays all addresses in the test set where the classifier
made an error.  Note that some in some cases, it might be the classifier which is correct and the
original analysis which was wrong.  A common example is a tail call which
was optimized to a jump during compilation.  If there is only one jump to this address, then analysis
may (reasonably) think that the function is just part of the function containing the jump even though
the classifier thinks the jump target is a function start.


## Options


This plugin has the following options. They can be set in the Tool Options menu.


### Maximum Test Set Size


This option controls the maximum size of the test sets (the test set of function
starts and the test set of known non-starts which together form the model's "test set").
Each set that is larger than the maximum will be replaced with a random subset of the maximum size.


### Minimum Length of Undefined Ranges to Search


This option controls the minimum length a run of undefined bytes must be in order to
be searched for function starts.  This is an optimization which allows you to skip the
(often quite numerous) small runs of undefined bytes between adjacent functions.  Note
that this option has no effect on model training or evaluation.


*Provided By: *RandomForestFunctionFinderPlugin**


---

[← Previous: Query Results Window](../Search/Query_Results_Dialog.md) | [Next: DWARF External Debug Files →](../DWARFExternalDebugFilesPlugin/DWARFExternalDebugFilesPlugin.md)
