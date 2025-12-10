[Home](../index.md) > [DecompilePlugin](index.md) > Specification Extensions

# Decompiler Options


This page lists configuration options that explicitly affect the behavior of the Decompiler or
its output, independent of the code that is being decompiled. The bulk of these options are
accessible by selecting the Code Browser menu


> Edit -> Tool Options...


and then picking the *Decompiler* folder. The options are associated
with the particular Code Browser or other tool being used and will apply to decompilation of any Program
being analyzed by that tool. There are three categories of options, which are listed by clicking either on the
*Decompiler* folder or one of its two subsections.


> Decompiler - lists General Options that affect the engine behavior. Analysis - lists Analysis Options that affect the Decompiler's transformation process. Display - lists Display Options that affect the final presentation of Decompiler output.


Options that are specific to the particular Program being analyzed are accessed by
selecting the Code Browser menu


> Edit -> Options for <program>... .


Picking the *Decompiler* section shows [Program Options](DecompilerOptions.md#program-options)
that only affect the Decompiler.  Picking the [Specification Extensions](DecompilerOptions.md#specification-extensions) section
shows a table of the available prototype models, call-fixups, and callother-fixups. These
affect more than just the Decompiler but are also documented here.


## General Options


These options govern what resources are available to the Plug-in and the Decompiler engine but do
not affect how analysis is performed or results are displayed.


<a name="generalcachesize"></a>**Cache Size (Functions)**


Producing decompilation results for a single function can be computationally intensive.
This option specifies the number of functions whose decompilation results
can be cached simultaneously. When navigating to a function that
has been recently cached, as when navigating back and forth between a few functions,
a new decompilation is not triggered.


<a name="generalmaxpayload"></a>**Decompiler Max-Payload (MBytes)**


This option limits the number of bytes that can be produced by the Decompiler process as output
when decompiling a single function. A payload includes the actual characters to be displayed in
the window, additional token markup, symbol information, and other details of the underlying
syntax tree. The limit is specified in megabytes of data. If the limit is exceeded for a single
function, decompilation is aborted for that function, and an error message
"Decompiler results exceeded payload limit ..." is displayed.


<a name="generaltimeout"></a>**Decompiler Timeout (seconds)**


This option sets an upper limit on the number of seconds the Decompiler spends attempting
to analyze one function before aborting.
It is currently **not** enforced for a Decompiler
window.  Instead it applies to the DecompilerSwitchAnalyzer, the `analyzeHeadless` command, scripts, and other
plug-ins that make use of the Decompiler service.


<a name="generalmaxinstruction"></a>**Max Instructions per Function**


This option sets a maximum number of machine instructions that the Decompiler will attempt
to analyze for a single function, as a safeguard against analyzing a long sequence
of zeroes or other constant data. The Decompiler will quickly throw an exception if it
traces control flow into more than the indicated number of instructions.


<a name="generalmaxjumptable"></a>**Max Entries per Jumptable**


This option sets the maximum number of entries (addresses) that the Decompiler can
recover from analyzing a single jumptable. This serves as a sanity check that the recovered
dimensions of a jumptable are reasonable and places an upper limit on the sheer number
of addresses the Decompiler is willing to trace from a single indirect jump.


## Analysis Options


These options directly affect how the Decompiler performs its analysis, either by
toggling specific analysis passes or changing how it treats various annotations.


<a name="analysisaliasblocking"></a>**Alias Blocking**


When deciding if an individual stack location has become dead, the Decompiler
must consider *aliases*, pointers onto the stack that could
be used to modify the location within a called function.  One strong heuristic the Decompiler
uses is: if the user has explicitly created a variable on the stack between the
base location referenced by the pointer and the individual stack location, then
the Decompiler can assume that the pointer is not an alias of the stack location.
The alias is *blocked* by the explicit variable.
However, if the user's explicit variable is labeling something that isn't
really an explicit variable, like a field within a larger structure, for instance,
the Decompiler may incorrectly consider the stack location as dead and start removing
live code.


In order to support the exploratory labeling of stack locations, the user can use this
setting to specify what data-types should be considered blocking. The four options are:


> None - No data-type is considered blocking Structures - Only structures are blocking Structures and Arrays - Only structures and arrays are blocking All Data-types - All data-types are blocking


Selecting *None* is the equivalent of turning off the heuristic. Selecting anything
except *All Data-types* allows users to safely label small variables without
knowing immediately if the stack location is part of a larger structure or array.


<a name="analysisunreachable"></a>**Eliminate unreachable code**


When toggled *on*, the Decompiler eliminates code that it
considers unreachable.  This usually happens when, due to constant propagation and other
analysis, the Decompiler decides that a boolean value controlling a conditional branch can
only take one possible value and removes the branch corresponding to the other value. Toggling
this to *off* lets the user see the dead code, which is typically demarcated
by the control-flow structure:


> if (false) { ... }


<a name="analysisignoreunimplemented"></a>**Ignore unimplemented instructions**


When toggled *on*, the Decompiler treats instructions whose semantics
have been formally marked **unimplemented** as if they do
nothing (no operation). Crucially, control flow falls through to the next instruction.
In this case, the Decompiler inserts the warning "Control flow ignored unimplemented
instructions" as a comment in the function header, but the exact point at which
instruction was ignored may not be clear.
If this option is toggled *off*, the Decompiler inserts the built-in
function `halt_unimplemented()` at the point of the unimplemented instruction, and
control flow does not fall through.


<a name="analysisinferconstants"></a>**Infer constant pointers**


When toggled *on*, the Decompiler infers a data-type for constants
it determines are likely pointers. In the basic heuristic,
each constant is considered as an address, and if that address starts a known data or function element
in the program, the constant is assumed to be a pointer.  The constants are treated like
any other source of data-type information, and the inferred data-types are freely propagated by
the Decompiler to other parts of the function.


<a name="analysisnanignore"></a>**NaN operations**


This option determines how the Decompiler treats floating-point **NaN**
(Not a Number) operations.  Many processors automatically perform NaN checks on the operands of
floating-point instructions, and unless specifically configured, these show up in Decompiler output
as `NAN()` functional tokens.  Common floating-point source code operations, like
`<`, `>`, and `==` can generate `NAN` tokens as a
side effect, even if the original source code was not designed to handle NaN values, and the
tokens can clutter the output.


The user can optionally configure some or all of the NaN operations to be ignored, meaning that
inputs to the NaN operation are *assumed* to be valid floating-point values and the
`NAN` function is removed, replacing it with the value: **false**.
The possible settings are:


> Ignore none - No NaN operations are removed Ignore with comparisons - NaN operations associated with comparisons are removed Ignore all - All NaN operations are removed


The Decompiler considers a NaN operation to be associated with a floating-point comparison if they both
can be considered boolean clauses of the same **if** condition.


<a name="analysisforloops"></a>**Recover -for- loops**


When toggled *on*, the Decompiler attempts to pinpoint
variables that control the iteration over specific loops in the function body.
When these *loop* variables are discovered, the loop is
rendered using a standard **for** loop header
that contains an initializer statement, condition, and iterating statement.


> for (iVar2 = 10; iVar2 < len; iVar2 = iVar2 + 1) { ...


When toggled *off*, the loop is displayed using
**while** syntax, with any initializer and
iterating statements mixed in with the loop body or preceding basic blocks.


<a name="analysisreadonly"></a>**Respect read-only flags**


When toggled *on*, the Decompiler treats any values in memory
marked *read-only* as constant. If a read-only memory location is explicitly
referenced by the function being decompiled, it is considered to be unchanging, and the initial
value present in the Program is pulled into the data flow of the function as a constant.
Due to *Constant Propagation* and other transformations, read-only memory
can have a large effect on Decompiler output.


Typically, as part of the import process, Ghidra marks memory blocks as read-only if they
are tagged as such by a section header or other meta-data in the original binary.
Users can actively set whether specific memory regions are considered read-only through the
*Memory Manager*, and individual data elements can be marked
as *constant* via the **Mutability** setting
(see [Data Mutability](DecompilerAnnotations.md#data-mutability)).


<a name="analysisextendedprecision"></a>**Simplify extended integer operations**


This toggles whether the Decompiler attempts to simplify double precision arithmetic operations,
where a single logical operation is split into two parts, calculating the high and low pieces
of the result in separate instructions.  Decompiler support for this kind of transform is currently
limited, and only certain constructions are simplified.


<a name="analysispredicate"></a>**Simplify predication**


When this option is active, the Decompiler simplifies code sequences containing
*predicated* instructions. A predicated instruction is executed
conditionally based on a boolean value, the **predicate**,
and a sequence of instructions can share the same predicate. The Decompiler merges the
resulting `if/else` blocks that share the same predicate so that the condition is only
printed once.


<a name="analysissplitstruct"></a>**Split combined structure fields**


When this option is active, the Decompiler attempts to identify places in the code where multiple
fields of a structure data-type are being moved simultaneously with a single operation. Then it splits the
operation into multiple pieces so that the logical fields can be seen individually.
When this option isn't active, the Decompiler creates an artificial token to
represent the combined fields being written to or read from.


```

	      struct1._20_4_ = 0xff00ff00;  // Auto-generated name for assigning multiple fields at once
	        ...
	      struct1.a = 0xff00;           // The same assignment, after splitting
	      struct1.b = 0xff00;

```


<a name="analysissplitarray"></a>**Split combined array elements**


When this option is active, the Decompiler attempts to identify places in the code where multiple
elements of an array are being moved simultaneously with a single operation. Then it splits the
operation into multiple pieces so each element of the array can be seen individually.
When this option isn't active, the Decompiler creates an artificial token to
represent the combined elements being written to or read from.


```

	      text._20_2_ = 0x4241;        // Auto-generated name for assigning multiple elements at once
	        ...
	      text[20] = 'A';              // The same assignment, after splitting
	      test[21] = 'B';

```


<a name="analysissplitpointers"></a>**Split pointers to combined elements**


This options affects when the Decompiler's splitting actions are applied. See
the discussion above about
[Splitting Structure Accesses](DecompilerOptions.md#analysis-options) and
[Splitting Array Accesses](DecompilerOptions.md#analysis-options).
If this option is on, a split is performed whenever combined elements or combined
fields are copied.  In particular, either the read access, or the write access, or both,
can be through a pointer.
If this option is off, splitting is limited to copies between structures or arrays at fixed
locations, either at a global address, or on the local stack.


<a name="analysisinplace"></a>**Use in-place assignment operators**


When toggled *on*, the Decompiler employs in-place assignment operators,
such as `+=` and `<<=`, in its output syntax.


## Display Options


These options do not change the Decompiler's analysis but only affect how the results are presented.


<a name="displaybackgroundcolor"></a>**Background Color**


Assign the background color for the Decompiler window.


<a name="displaybraceformatting"></a>**Brace Format for &lt;kind-of&gt; blocks**


Choose how braces are placed after function declarations, or other kinds of code blocks in Decompiler output.
Formatting can be controlled for:


> function blocks - the main function bodies if/else blocks - blocks delineated by the if and else keywords loop blocks - blocks delineated by the for , do , and while keywords switch blocks - blocks delineated by the switch keyword


The different formatting options primarily control how the opening brace is displayed relative to the line containing
the declaration or keyword starting the block.  The formatting options are:


> Same line - opening brace placed on same line Next line - opening brace placed on the next line Skip one line - opening brace placed on line after a blank line


The "Same line" option is consistent with K & R code formatting style.  The "Next line" option is consistent with
the Allman formatting style.


<a name="displaycolordefault"></a>**Color Default**


Assign the color to any characters emitted by the Decompiler that do not fall into one of token types
listed below. This includes delimiter characters like commas and parentheses as well as various *operator*
characters.


<a name="displaytokencolor"></a>**Color for `<token>`**


Assign colors to the different types of language tokens emitted by the Decompiler.
These include:


> Comments Constants - including integer, floating-point, character, and string Functions names Globals - names of variables with global scope Keywords - reserved names in the language being emitted Parameters - names of function input variables Types - names of data-types in variable declarations and casts Variables - names of local variables Special - volatile variables and other special symbols


<a name="displaycurrenthighlight"></a>**Color for Current Variable Highlight**


Assign the background color used to highlight the token currently under the cursor in a Decompiler window.


<a name="displayfindhighlight"></a>**Color for Highlighting Find Matches**


Assign the background color used to highlight characters matching the current *Find* pattern
(see [Find...](DecompilerWindow.md#find)).


<a name="middlemousecolor"></a>**Color for Highlighting Middle-mouse Matches**


Assign the background color used to highlight characters when highlighting using the middle-mouse button.


<a name="displaycommentindent"></a>**Comment line indent level**


Set the number of characters that comment lines are indented within Decompiler output. This applies only
to comments within the body of the function being displayed.  Comments at the head of the function
are not indented.


<a name="displaycommentstyle"></a>**Comment style**


Set the language syntax used to delimit comments emitted as part of Decompiler output. For C and Java,
the choices are `/* C style comments */` and `// C++ style comments`.


<a name="displaydisablecasts"></a>**Disable printing of type casts**


Set whether the syntax for *type casts* is emitted in Decompiler output.
If this is toggled on, type cast syntax is never displayed, even when rules of the language
require it. So individual statements may no longer be formally accurate.


<a name="commentoptions"></a>**Display &lt;kind-of&gt; Comments**


Set whether a specific type of comment should be incorporated into Decompiler output.
Each type has its own toggle and can be individually included or excluded from Decompiler output.


> EOL PLATE - Whether plate comments within the body of the function are displayed POST PRE


A comment's type indicates how it is placed within a Listing window, not how it is placed in
a Decompiler window.  All comments within the body of the function are displayed in the same way
by the decompiler, regardless of their type (see the discussion in [Comments](DecompilerAnnotations.md#comments)).


<a name="displayheadercomment"></a>**Display Header comment**


Toggle whether the Decompiler emits comments at the head (before the beginning) of a function.
The header is built from Plate comments placed at the *entry point* of the
function (see the discussion in [Comments](DecompilerAnnotations.md#comments)).
The inclusion of other Plate comments is controlled by the **Display PLATE comments** toggle, described above.


<a name="displaylinenumbers"></a>**Display Line Numbers**


Toggle whether line numbers are displayed in any Decompiler window.  If toggled
on, each Decompiler window reserves space to display a numbers down the left
side of the window, labeling each line of output produced by the Decompiler.
Line numbers are associated with the window itself and are not formally part of
the Decompiler's output.


<a name="displaynamespaces"></a>**Display Namespaces**


Control how the Decompiler displays namespace information associated
with function and variable symbols. The possible settings are:


> Minimally - Display the minimal path that distinguishes the symbol Always - Always display the entire namespace path Never - Never display the namespace path


The **Minimally** setting, which is the default, will only emit the portion
of the namespace path necessary to distinguish the symbol from other symbols with the same base name used
by the function, or if a portion of the path is completely outside the function's scope.


The **Never** setting never displays any of the namespace path under any
circumstances and may produce output that is ambiguous and doesn't formally parse.


<a name="displaywarningcomments"></a>**Display Warning comments**


Toggle whether Decompiler generated *WARNING* comments are displayed as part
of the output. The Decompiler generates these comments, independent of those laid down by users, to
indicate unusual conditions or possible errors (see [Warning Comments](DecompilerAnnotations.md#warning-comments)).


<a name="displayfont"></a>**Font**


Set the typeface used to render characters in any Decompiler window. Indentation is generally clearer
using a monospaced (fixed-width) font, but any font available to Ghidra can be used.  The size of
the font can also be controlled from this option.


<a name="displayintegerformat"></a>**Integer format**


Set how integer constants are formatted in the Decompiler output.
The possible settings are:


> Force Hexadecimal - Always use a hexadecimal representation Force Decimal - Always use a decimal representation Best Fit - Select the most natural representation


For **Best Fit**, a representation is selected based on how
close it is to either a *round* decimal value (10, 100, 1000, etc.) or
a round hexadecimal value (0x10, 0x100, 0x1000, etc.)


<a name="displaymaxchar"></a>**Maximum characters in a code line**


Set the maximum number of characters in a line of code emitted by the Decompiler before a line break
is forced.  The Decompiler will not split an individual token across lines. So line breaks frequently
will come before the maximum number of characters is reached, and technically a single token can
extend the line beyond the maximum.


<a name="displayindentlevel"></a>**Number of characters per indent level**


Set the amount of indenting used to print statements within a nested scope in the
Decompiler output.  Each level of nesting (function bodies,
loop bodies, **if/else** bodies, etc.)
adds this number characters.


<a name="displaynull"></a>**Print 'NULL' for null pointers**


Set how null pointers are displayed in Decompiler output.  If this is toggled
on, the Decompiler will print a constant pointer value of zero (a **null** pointer)
using the special token `NULL`.  Otherwise the pointer value is represented with the '0' character,
which is then cast to a pointer.


<a name="displayconvention"></a>**Print calling convention name**


Set whether the *calling convention* is printed as part of the function
declaration in Decompiler output. If this option is turned on, the name of the calling convention
is printed just prior to the return value data-type within the function declaration.  All functions
in Ghidra have an associated calling convention (or prototype model) that is used during
Decompiler analysis (see the discussion in [Prototype Model](DecompilerConcepts.md#prototype-model)).


## Program Options


Changes to these options affect only the Decompiler and only for
the current Program being analyzed.


<a name="optionprotoeval"></a>**Prototype Evaluation**


Sets the calling convention (prototype model) used when decompiling a function where
the convention is not known; i.e., marked as **unknown**.  Many architectures have multiple
calling conventions, **__stdcall**, **__thiscall**, etc.
(see the discussion in [Prototype Model](DecompilerConcepts.md#prototype-model)).


## Specification Extensions


This entry displays elements from the Program's *compiler specification* and
*processor specification* and allows the user to add or remove
**extensions**, including prototype models, call-fixups, and
callother-fixups.


Every program has a *core* set of specification elements,
loaded from the [SLEIGH Specification Files](DecompilerConcepts.md#sleigh-specification-files), that cannot
be modified or removed. Extensions, however, can be added to this core specification. Any extension
imported from this dialog is directly associated with the active Program and is stored permanently
with it.


Users can change or reimport an extension if new information points to a better definition.
Users have full control over an extension, and unlike a core element, can tailor it specifically
to the Program.


This options entry presents a table of all specification elements.
Each element, whether core or an extension, is displayed on a separate row with three columns:


> Extension Type - indicating the type of element Name - showing the formal name of the element Status - indicating whether the element is core or an extension


The core elements of the specification have a blank Status column, and any extension
is labeled either as **extension** or **override**.


### Extension Types


Each of the element types described here represents an XML tag of the same name, which, if
present in the table, must either be in the *compiler specification* file,
the *processor specification* file, or provided to Ghidra as an
import document.


**prototype**


This element is a named [Prototype Model](DecompilerConcepts.md#prototype-model) that holds a specific set
of parameter-passing details. It
can be applied to individual functions by name, typically via the **Calling Convention** menu
in the [Function Editor Dialog](../FunctionPlugin/Variables.md#edit-function).
See the documentation on [Function Prototypes](DecompilerAnnotations.md#function-prototypes) for how they affect decompilation.


The XML `<prototype>` tag always has a **name** attribute
that defines the formal name of the prototype model, which must be unique across all models.


```

<prototype name="__stdcall" extrapop="unknown" stackshift="4">
  <input>
    <pentry minsize="1" maxsize="500" align="4">
      <addr offset="4" space="stack"/>
    </pentry>
  </input>
  <output>
  ...

```


**callfixup**


This element is a Call-fixup, which can be used to substitute a specific p-code
sequence for CALL instructions during decompilation, as described in
[Function Prototypes](DecompilerAnnotations.md#function-prototypes).


The `<callfixup>` tag has a **name**
attribute listing the formal name, which must be unique across all call-fixups.


```

<callfixup name="EH_prolog3">
  <pcode>
    <body><![CDATA<
      EBP = ESP + 4;
      tmp = * EBP;
      ESP = ESP - tmp;
      ESP = ESP - 24;
    ]]></body>
  </pcode>
</callfixup>

```


**callotherfixup**


This element is a Callother-fixup, which can be used to substitute a specific p-code
sequence for CALLOTHER p-code operations.  A CALLOTHER
is a black-box, or unspecified p-code operation (see [User-defined P-code Operations - CALLOTHER](DecompilerConcepts.md#user-defined-p-code-operations-callother)).


The `<callotherfixup>` tag has a
**targetop** attribute which lists the
name of the particular CALLOTHER operation it substitutes for.


```

<callotherfixup targetop="dynamicPush">
  <pcode>
    <input name="amount"/>
    <body><![CDATA[
      RSP = RSP + amount;
    ]]></body>
  </pcode>
</callotherfixup>

```


### Status


The Status column labels an element as either a core specification
or an extension; it also gives an indication of whether the element
is about to be installed or removed.


With no changes pending, the column will show one of the three main values:


*`<blank>`*


A blank Status column indicates that the element is a core part of the
specification, originating from one of the *specification files*.
These elements cannot be changed or removed.


**extension**


Indicates that the element is a program-specific extension that has been
added to the specification.


**override**


Indicates that the element, which must be a **callotherfixup**,
is an extension that overrides a core element with the same target.  The extension
effectively replaces the p-code injection of the core element with a user-supplied one.
If this type of extension is later removed, the core element becomes active again.


If the user has either imported additional extensions or selected an extension for removal but
has not yet clicked the *Apply* button in the Options dialog, the Status column
may show one of the following values, indicating a pending change:


**install**


Indicates a new extension that will be installed.


**remove**


Indicates an extension that is about to be removed.


**replace**


Indicates a new extension that will replace a current
extension with the same name.


**override pending**


Indicates a new extension that will override a core element when
it is installed.


### Importing a New Extension


The *Import* button at the bottom of the
**Specification Extensions** pane allows the user to import one of the
three element types, **prototype**,
**callfixup**, or **callotherfixup**,
into the program as a new extension.
The user must supply a properly formed XML document, as a file, that fully describes the new
extension.  Clicking the *Import* button brings up a File Chooser dialog,
from which the user must select their prepared XML file.  Once *Ok* is
clicked, the file is read in and validated.  If there are any problems with the validation, or if
the new extension's name collides with a core element, the import does not succeed and
an error message will be displayed. Otherwise, the import is accepted, and the table is updated
to indicate the pending change.


The final change to the program, installing the new extension, will not happen until the
*Apply* button, at the bottom of the Options dialog, is clicked.


The XML file describing the extension *must* have one of the tags,
`<prototype>`, `<callfixup>`, or `<callotherfixup>`,
as its single root element. Users can find numerous examples within the compiler
and processor specification files that come as part of Ghidra's installation
(see [SLEIGH Specification Files](DecompilerConcepts.md#sleigh-specification-files)).


In the case of **prototype** and **callfixup**
elements, extensions cannot replace existing core elements, so the new extension *must not*
have a name that matches an existing core element.  If a new **callotherfixup**
extension has a targetop that matches a core element, the extension is automatically treated as an override.


Existing extensions can be replaced simply by importing a new extension with the same name or targetop.


### Removing an Extension


The *Remove* button at the bottom of the **Specification Extensions** pane allows
the user to remove a previously installed extension.  A row from the table is selected first, which
must have a Status of **extension** or **override**.
Core elements of the specification cannot be removed.
Clicking the *Remove* button brings up a confirmation dialog, and if
*Ok* is clicked, the selected extension is marked for removal.  The Status of the row
changes to **remove**, reflecting this.


The final change to the program, removing the extension, will not happen until the
*Apply* button, at the bottom of the Options dialog, is clicked.


If a **prototype** or **callfixup** is removed,
all functions are checked to see if they have the matching calling convention or call-fixup set.
A function with matching calling convention is changed to have the *default* convention, which is always a core element.
A function with matching call-fixup is changed to have no call-fixup.


---

[← Previous: Program Options](DecompilerOptions.md) | [Next: Decompiler Window →](DecompilerWindow.md)
