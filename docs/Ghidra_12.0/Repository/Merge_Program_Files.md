[Home](../index.md) > [Repository](index.md) > Merge Programs

# Merge Program Files


The Ghidra Server provides file access to multiple users enabling a team to collaborate on a
single effort. It provides network storage for [shared project repositories](../VersionControl/project_repository.md#project-repository) while controlling user
access. Together the Ghidra Server and the shared project repository allow multiple users to
concurrently:


- Check out the same version of a program file
- Make changes to the program file
- Check the changed program file back into the shared project repository


*Merging* is necessary to integrate changes made to a single version of a program file
by multiple users. The following steps show a typical merge scenario:


**Check in / Merge Sequence:**


1. A file is added to version control,
creating Version **0**.
2. A user checks out Version **0**, makes
changes, and checks it in to create Version **1**.
3. **User A** checks out Version
**1**.
4. **User B** checks out Version **1**
and makes changes.
5. **User B** checks in his changed file,
creating Version **2** in the project repository. Because no other versions were
created since **User B** originally checked out his file, Version **2** can be
created automatically. This new version will be the changed file created by **User
B** (Step 4). In this case, merging is not involved in the check in process.
6. **User A** completes his changes and
checks in the file.
7. During the check in process, the Ghidra
Server determines that a new version of the program file has been added since **User
A** originally checked out the file (Step 3). The latest version of the file
contained in the repository, Version **2**, is not the same file that **User A**
had checked out, Version **1**. A merge is required since a new version of the file
was added to the repository after User **A** checked out the file.


> **Note:** If a new version of a file has been added since the user checked out the file, a merge is
required at check in. This is the only time a merge is required.


The Ghidra Server starts the merge process
by making a copy of Version **2**. Changes from **User** **A**'s checked in file
are applied to this copy to create the new file, Version **3**. There are two types of
merges - **automatic** and **manual**. If changes made by **User A** and **User
B** do not conflict [automatic](#auto-merge) merging is done. If changes made
by **User A** and **User B** do conflict, then **User A** must manually [resolve the conflicts](#resolving-conflicts). Note that the last user checking in
changes must resolve conflicts. A conflict results when **User A** and **User B**
make the *same type of changes* at a location in the program.


The figure below illustrates this typical scenario where two users check out a file, as
described above. The sequence of events are numbered in parentheses in the diagram, and
correspond with the **Check in/Merge Sequence** above:


![](images/MultiUser.png)


To begin the merge process, select the [Check In](../VersionControl/project_repository.md#check-in) option on the Ghidra Project Window. A progress
bar is displayed while the merge is in progress. The merge begins with a copy of the latest
version of the file from the repository. All changes are applied to this copy. At the
conclusion of the merge, this copy along with the applied changes will be saved in the
repository, and will become the newest version of the file.


The merge processes program elements in the following order:


- [Memory](#memory)
- [Program Trees](#program-trees)
- [Data Types and Categories](#data-types-and-categories)
- [Program Context
Registers](#program-context-registers)
- [Listing](#listing)
  - [Code Units](#code-units)
  - [Externals](#external-functions-and-labels)
  - [Functions](#functions)
  - [Symbols](#symbols)
  - [Equates](#equates)
  - [User Defined
Properties](#user-defined-properties)
  - [References](#references)
  - [Bookmarks](#bookmarks)
  - [Comments](#comments)
- [External Program Names](#external-program-names)
- [Property Lists](#property-lists)


Within each program element an automatic merge is attempted first. If conflicts
arise, the user must manually resolve conflicts before moving on to the next program element.
For example, the Program Tree merge performs the auto merge, and then requests user input to
resolve conflicts, as required. Once the Program Tree has been merged, with all conflicts
resolved, the merge of Data Types and Categories begins.


If you cancel the merge at any time, you are canceling the entire *check
in* process and your file remains checked out. None of the changes that was made as a result
of the merge is applied to the program that you have checked out.


While the auto merge is occurring and conflicts are being determined the merge
status is displayed in the merge tool. The following image shows an example of the merge tool
when the merge process is auto merging code units.


![](images/AutoMergeCodeUnits.png)


At this point the Memory, Program Trees, Data Types and Program
Context phases have already completed as indicated by the Completed icon, ![checkmark_green.gif](../icons/checkmark_green.gif). The Bytes & Code Units sub-phase of the Listing
is currently In Progress, ![right.png](../icons/right.png). The Progress In Current Phase progress bar provides the user with an
idea of how much of the phase has completed. The other sub-phases of Listing, the External
Programs and Property Lists have not been merged yet as indicated by the Pending icon, ![label.png](../icons/label.png). The message below the current phase progress bar gives
additional information about what is currently happening in the phase.


At the bottom of the merge tool is a progress bar and message for
an immediate task. When multiple of these smaller tasks are combined sequentially they perform
the merge of the current phase.


The following sections describe the auto merge process and conflict resolution
process in greater detail.


## Auto Merge


For each program element, the *Auto Merge* is the first of the two merges which is
performed. The following paragraphs describe how Auto Merging applies to each program
element.


### Memory


Program memory is organized in [memory blocks](../Glossary/glossary.md#memory-block). The only changes to a
memory block that can be merged are:


- Name
- Permissions
- Comments


You can make changes to the memory structure (add a block, remove a block,
etc.) only when you have checked out the program with an [exclusive lock](../VersionControl/project_repository.md#check-out). This restriction prevents
drastic changes in memory that could potentially have a major impact on other users.
Typically, all users working on the same program should agree on memory structure changes
and then have one user make them. An exclusive lock prevents anyone else from checking out
the program while the exclusive lock exists. When you check in your changes, merging is not
necessary as no other versions were created while you had the program checked out. Your
program becomes the new version.


Comments on the memory block are *replaced* in the results program
during the merge process. You must resolve all [memory
conflicts](#memory) before the merge process can continue with the next program element, program
trees.


### Program Trees


If you make **any** change to a [program tree](../ProgramTreePlugin/program_tree.md), it is marked as changed
and may be merged. No further inspection of changes is done. If the tree was not changed in
the latest version, then the automatic merge can be done. If the tree was changed in the
latest version, this is considered a [conflict](#program-trees) that you
must resolve before the merge process can continue with the next program elements, data
types and categories.


### Data Types and Categories


[Data
types](../DataTypeManagerPlugin/data_type_manager_description.md) can be created, renamed, edited (contents), or deleted. During merging, newly
created data types are added automatically (if a data type with the same name already
exists in the parent category, then your new data type is created with a ".conflict"
appended to the name). All other changes to data types are merged.


When merging data types, there is only one way that data type conflicts can occur. A
conflict results **only** if in both files the same *type* of change (rename, edit
contents, delete) was made to a particular data type. Other than this, no conflicts can
occur and the data type you changed can be merged automatically. For example, if you
renamed a structure data type and in the latest version the contents of that data type were
edited, this will **not** cause a conflict and your change can be applied automatically
during the merge process.


[Categories](../DataTypeManagerPlugin/data_type_manager_description.md#working-with-categories)
can be renamed, moved, deleted, or restructured (add/remove data types and categories).
Note that moving a data type to a different parent category is considered a category
change, not a data type change.


As with data types, there is only one way that category conflicts can occur. A conflict
results only if, in both files, the same *type* of change (rename, move, delete,
restructure) was made to a particular category. Other than this, no conflicts can occur and
the category you changed can be merged automatically. For example, if you renamed a
category and in the latest version the category was moved to a different parent category,
this will **not** cause a conflict and your change can be applied automatically during
the merge process.


All [conflicts](#data-types-and-categories) must be resolved before the merge process
can continue with the next program element, Program Context Registers.


### Program Context Registers


For any of the registers defined by the program's language you can set a register value
for an address or range of addresses. If you set a register value or remove a register
value at an address, it will automatically change the value during the merge process if the
value wasn't changed at that address in the latest version. If your version and the latest
version change the register to the same value at an address, it will also get merged
automatically.


Automatic merging of all the registers will happen before you are prompted to resolve
any conflicting register values.


You must resolve all [register conflicts](Merge_Program_Files.md#program-context-registers) before the
merge process can continue with the next program element, Listing.


### Listing


Various parts of the program are merged in the Listing merge. These include the bytes,
code units, functions, symbols, equates, user defined properties, references, bookmarks,
and comments. For each of these parts the auto merge will occur followed by a manual merge
of any conflicts.


#### Code Units


If you make any change to the memory bytes or to a code unit, such as creating or
clearing an instruction or defining data, the code unit gets marked as changed and may be
merged. If you change the memory bytes and the latest version doesn't have memory byte or
code unit changes, your byte changes will be merged automatically. If you changed the
code unit and it does not conflict with a change in the latest version, the change to the
code unit will be merged automatically.


If the latest version had any of the following changes, the code unit is in conflict
and must be manually merged:


- The latest version and your version have memory bytes changed to different
values
- The latest version changed memory bytes where you changed the code unit or vice
versa
- The latest version created or cleared instructions or data differently than you
did
- The latest version created, changed, or removed an equate for the code unit you
changed or vice versa


You must resolve all [byte and code
unit conflicts](Merge_Program_Files.md#code-units) before the merge process can continue with the next program element,
Functions.


#### External Functions and Labels


If you make any change to the external locations (external functions or external labels)
defined within the program, such as creating,
updating, or removing an external location, the external location gets marked as changed
and it may be merged.


The following types of changes will get merged automatically:


- Changing the name, external memory address, or data type for an external location as
long as the latest version didn't change the same attribute of the external location.
- Changing from an external label to an external function as long as the latest version
didn't set the data type for the same external label or remove the label.
- Changing from an external function to a label or removing an external function as
long as the latest version didn't change the external function.
- Setting the data type on an external label as long as the latest version didn't
also set the data type or change the label into an external function.
- Changing an external function as long as the latest version also didn't make
changes to the function.
Conflicts could be:
- - another variable at the same offsets on the stack frame
  - another register variable with the same named register and first use
address.


You must resolve all [external location
conflicts](Merge_Program_Files.md#external-functions-and-labels) before the merge process can continue with the next program element,
Functions.


#### Functions


If you make any change to the functions defined within the program, such as creating,
updating, or removing a function, the entry point of the function gets marked as changed
and the function may be merged.


The following types of changes will get merged automatically:


- Adding a function with a body that doesn't overlap any function body in the latest
version.
- Removing a function as long as the latest version did not change this function or
its stack frame.
- Making changes to the function name, return type, parameters, parameter offset,
return type offset, etc. as long as the latest version didn't also change the same part
of the function.
- If a variable name conflicts with a variable or symbol of the same name in the
function's [namespace](../SymbolTreePlugin/SymbolTree.md#display) of the latest
version, that variable will automatically be renamed to a conflict name. This
eliminates the name conflict.
- Making changes to existing parameters such as the name, data type, or description
if the latest version didn't change the same part of the parameter.
- All local variables will be automatically added if they don't conflict with changes
to the latest version.
Conflicts could be:
- - another variable at the same offsets on the stack frame
  - another register variable with the same named register and first use
address.
  - another symbol with the same name in the function's namespace
  - the name, datatype, or comment for a local variable is changed to different
values in your version and the latest version.


You must resolve all [function
conflicts](Merge_Program_Files.md#functions) before the merge process can continue with the next program element,
Symbols.


#### Symbols


Whenever you add, remove, or rename a symbol, the program gets marked as changed. It
also gets marked if you change the primary symbol at an address or if you make an address
an external entry point. The symbol phase of the Listing merge will merge labels,
namespace symbols, class symbols, and external symbols. Symbols associated with
functions, function parameters, and function local variables have already been resolved
by the function phase of the Listing merge.


The following types of changes will get merged automatically:


- Any symbol you removed will automatically be removed if the latest version didn't
change that symbol.
- Any symbol you added will automatically be added if latest version did not create
the same named symbol at that address with a different parent namespace.
- If each program has a symbol named the same within a namespace but at a different
address. These are resolved automatically by merging your symbol using a
**.conflict** name. In other words, your symbol will have a .conflict suffix added
to its name when it is merged. You are notified at the end of the symbol merge phase of
any symbols that were renamed to avoid a conflict.
- Any symbol you renamed will automatically get renamed if the latest version didn't
rename that symbol to a different name.
- If you change which symbol is primary, it will be automatically set to primary
unless the latest version set a different symbol to primary.
- Entry points that you added or removed will be added or removed automatically.


You must resolve all [symbol
conflicts](Merge_Program_Files.md#symbols) before the merge process can continue with the next Listing merge phase,
the Address Based Listing Merge.


#### Address Based Listing Merge


During this phase of the Listing merge each of the address based listing elements (the
equates, user defined properties, references, bookmarks, and comments) will get merged.
First an auto merge will occur for each of these elements. When all of the auto merges
are complete, conflict resolution will proceed in address order for each address that has
a conflict for any of the address based listing elements. At each address with a conflict
you will have to resolve all of the conflicts (equates, user defined properties,
references, bookmarks, and comments) before proceeding to the next address with
conflicts. The following sub-sections describe the auto merge for each of the address
based listing elements.


#### Equates


An equate associates a display name with a scalar operand or sub-operand at a
particular address in the program. Whenever you create, rename, or remove an equate the
program gets marked as changed. An equate conflict can arise between your version and
the latest version. The following types of equate changes will get merged
automatically:


- If an equate was set on a scalar and the latest version didn't set an equate on
that scalar, the equate will be added automatically.
- If an equate name's associated value differs between the two versions then there
is an equate conflict that will be resolved automatically by changing your version's
equate name to a conflict name by appending "_conflict" to your equate name.
- If your version's scalar had its associated equate removed, it will get
automatically removed if the latest version didn't change the named equate for that
scalar.
- If your version's scalar had its associated equate name changed, it will get
automatically renamed if the latest version didn't remove or rename it
differently.


If an equate is changed for a scalar operand or sub-operand differently in the
latest and your versions, then you must resolve the conflict.


The [equate conflicts](Merge_Program_Files.md#equates) will need
to be resolved after all of the address based auto merges complete. After the Equates
auto merge completes, an auto merge will begin for User Defined Properties.


#### User Defined Properties


A user defined property change gets marked in the program whenever the named
property gets added, removed or changed at an address. An example property is the
**Space** property created by the **Format** plugin.


A user defined property change will get merged automatically if the latest version
didn't change the same named property at the same address in the program. If the named
property was changed at an address in your version of the program and in the latest
version then a user defined property conflict exists.


The [user defined
property conflicts](Merge_Program_Files.md#user-defined-properties) will need to be resolved after all of the address based auto
merges complete. After the User Defined Properties auto merge completes, an auto merge
will begin for References.


#### References


References consist of memory references, variable (stack and register) references,
and external references. Changes to these include adding references, changing
references, and removing references. The references in your checked out version and the
latest version are compared for each of the mnemonic and operands at an address to
determine whether a conflict exists or the changes can be automatically merged.


The following types of changes will get merged automatically:


- If you added, changed, or removed a reference for a mnemonic or operand at an
address and the latest version didn't change the references.
- If your version and the latest version only have memory references for the
mnemonic or operand.
- If your reference is a stack variable reference and the latest version has a
stack reference to the same stack frame offset or no references.
- If your reference is a register variable reference and the latest version has a
register reference to the same register or no references.
- If your reference is an external reference and the latest version has the same
external reference or no references.


If your checked out version and the latest version both have changes to the
references for a mnemonic or operand, the references are in conflict whenever your
version and the latest version have references that are different types (for example,
one has memory references and the other has an external reference).


The [reference conflicts](Merge_Program_Files.md#references)
will need to be resolved after all of the address based auto merges complete. After the
References auto merge completes, an auto merge will begin for Bookmarks.


#### Bookmarks


Bookmarks allow you to associate a description with an address in the program. The
bookmark has a type and category associated with it. Bookmarks that the user has
entered via the GUI are **Note** type bookmarks. Ghidra plugins can also add
bookmarks of various other types. For example **Auto Analysis** adds **Analysis**
type bookmarks. Only one bookmark of a particular type and category can exist at an
address. However, only one **Note** type of bookmark can exist at an address
regardless of the category.


Changes to bookmarks include adding a new bookmark, removing a bookmark, changing
the description for a bookmark, and changing the category for a note bookmark.


Any changes to the bookmarks will get automatically merged as long as your changes
and the latest versions changes do not result in one of the following conflict
situations:


- your version and the latest version added or changed a **Note** bookmark
resulting in a different category or description for the two versions.
- your version and the latest version added or changed the same bookmark type and
category resulting in a different description for the two versions.


The [bookmark conflicts](Merge_Program_Files.md#bookmarks) will
need to be resolved after all of the address based auto merges complete. After the
Bookmarks auto merge completes, an auto merge will begin for Comments.


#### Comments


If you make a change to a comment (Plate, Pre, End-of-line, Repeatable, or Post) and
the latest version did not have any changes to that type of comment at the same
address, the change is automatically accepted. Comment changes include adding,
removing, or updating the comment. If the latest version has a change to the same
comment then the conflict will need to be resolved manually.


The [comment conflicts](Merge_Program_Files.md#comments) will
need to be resolved after all of the address based auto merges complete. After the
Comments auto merge completes, the conflict merge will begin for address based listing
elements (the equates, user defined properties, references, bookmarks, and comments) at
each of the addresses with a conflict.


After all address based conflicts are resolved, the auto merge process continues
with the next program element, External Program Names.


### External Program Names


Each external reference has an associated external program name. The external name
provides an association to the external program. Changing an external program name is
marked as a change and may be merged. Changes include adding or removing an external
program name, and changing the Ghidra program associated with an external program name. If
the change doesn't conflict with a change in the latest version then it will be merged
automatically.


A conflict occurs whenever your version removes an external program name and the latest
version changes the associated Ghidra program or vice versa. A conflict can also occur if
the latest version and your version both change the Ghidra program associated with a
particular external program name.


You must resolve all [external program name
conflicts](#external-program-names) before the merge process can continue with the next program element, Property
Lists.


### Property Lists


[Property lists](../ProgramManagerPlugin/Program_Options_Dialog.md#detailed-properties-descriptions)
are lists of options that are saved as part of the program. You can view and edit these
properties through the *[Program Options
Dialog](../ProgramManagerPlugin/Program_Options_Dialog.md)*. A property will be merged automatically if it is a new property or it was
not changed in the latest version. A [conflict](#property-lists) results
when you change a property that was either removed or changed in the latest version.


## Resolving Conflicts


For each program element, the *Conflict Resolution Merge* is the second of the two
merges which is performed. The first time a conflict is encountered, the merge process
displays a Merge Tool. Use this tool to resolve each conflict one at a time. To resolve any
conflict, you must choose a radio button or check box depending on the type of conflict.
Most conflicts require you to select from the following:


- Latest version (changes from the Latest version that is checked into the
repository)
- Checked Out version (your changes)
- Original version (values from the file when you originally checked it out)


However, there may be other conflict options that let you choose to add or rename the type of
item that is in conflict in addition to keeping the one that was checked in the Latest version
in the repository. Some conflicts, such as comment conflicts, allow you to check one or both
check boxes for the comment conflict. This allows you to keep the Latest comment, your comment,
or a combined copy of both the Latest and your (Checked Out) comments.


### Memory


All memory conflicts that remain after the [auto merge](#memory) must be
resolved.


The only conflicts on a memory block will be changes to the name, permissions, or
comments. A conflict occurs when you change the name of a memory block and another user has
changed the name of the same memory block. Similarly, if you changed the permissions or
comments on a memory block, and another user has changed the permissions or comments on the
same memory block you will have to select which changes to keep.


The image below is the panel that is shown when there is a conflict on the block name.
In this sample image, the user who created the latest version had changed the block name to
"LatestText" (radio button for *Latest*). You changed the block name to "MY_Text"
(radio button for *Checked Out*). The block name in the original program (the version
that you had originally checked out) is shown as ".text" (radio button for
*Original*).


![](images/MemoryConflict.png)


To resolve the conflict, you must select a radio button. After you select a radio
button, the **Apply** button becomes enabled. Click on the **Apply** button to
continue the merge process. In this example, there was only one conflict in the Memory
merge, as indicated by the *Current Conflict* area of the panel. The progress bar on
the lower right corner of the Merge Tool indicates progress only for the Memory Block
merge, not the entire merge process.


The merge process continues with Program Trees.


### Program Trees


All program tree conflicts that remain after the [auto
merge](#program-trees) must be resolved.


If you make any change to a [program tree](../ProgramTreePlugin/program_tree.md), it is marked as changed
and may be merged. There is no finer granularity than detecting that the tree changed, so
the merge is going to do "all or nothing" on the program tree. For example, if you change
the tree (add a folder, rename a fragment, etc.) and another user changed the same tree,
you will get a choice to keep your changes, keep the changes from the latest, keep the tree
from the original program that you checked out, or rename your tree to a new name. The last
option to rename your tree allows you to create your tree in the program that results in
the latest version, and not lose anyone else's changes. The image below shows this
scenario:


![](images/ProgramTreeConflict.png)


The conflict resolution panel shows what kind of change it is, name change versus a
structure change; the checkbox indicates the change in *Latest Version* and *Current
Checked Out Version*. In this example, another user changed the name of a program tree
to "Tree3_XXX" (*Latest*). You changed the name of the same program tree to "MY TREE
3" (*Checked Out*). The original name of the tree was "Tree Three" (*Original*).
The *Resolve Tree Name Conflict* area of the panel shows radio buttons for each
option:


- Use name 'Tree3_XXX' (Latest) - select this option to lose your changes and keep what
is in the latest version
- Use name 'MY TREE 3 (Checked Out) - select this option to rename the tree in the
program that will become the latest version; the tree is renamed to 'MY TREE 3'
- Add new tree named 'MY TREE 3' - select this option to create a new tree named 'MY
TREE 3' in the program that will become the latest version; changes by other users are
retained
- Use name 'Tree Three' (Original) - select this option to lose your changes;
'Tree3_XXX' will be renamed to 'Tree Three' which is the name from the program that you
had originally checked out


Select an option to resolve the conflict, then click on **Apply**. In this example,
the next conflict will be displayed that must be resolved. The progress bar on the lower
right corner of the Merge Tool indicates progress only for the Program Tree merge, not the
entire merge process.


After all program tree conflicts are resolved, the merge process continues with data
types and categories.


### Data Types and Categories


All data type or category conflicts that remain after the [auto
merge](#data-types-and-categories) must be resolved.


If you make a change (rename, edit contents, delete) to a data type, and the same
*type* of change was made in the latest version, then a conflict arises that you must
resolve. The merge process for data types and categories handles these conflicts one at a
time. The *Current Conflict* area of the panel shows:


*Conflict # x of n*


where *x* is the current conflict number, and *n* is the total number of data
type and category conflicts that must be resolved. Data type conflicts are resolved
first.


The image below shows the scenario where you:


**renamed** Foo  →  My_Foo

**moved** /MISC  →  /Category1

changed undefined  →  char


In the latest version:


**moved** /MISC  →
/Category1/Category2/Category3

changed undefined  →  byte


The conflict arises because in both versions the file was **moved** and also because
the second component was changed to a different data type. The rename of Foo to My_Foo
doesn't cause a conflict. If you had only **renamed** the data type (without
**moving** it or changing the undefined), there
would not have been a conflict.


![](images/DataTypeConflict.png)


These are the options to resolve the conflict:


- *Latest* - select this option to keep what is in the latest version (lose your
changes)
- *Checked Out* - select this option to apply your changes; (changes in the latest
version are lost)
- *Original* - select this option to apply what was in the program that you had
originally checked out (your changes and those in the latest version are lost)


Select a radio button to resolve the conflict.


> **Note:** In the Merge Tool window above, the title
indicates the project, program and new version number that will result from the merge.
Version 5 of  "helloProgram" in the "SampleProject" will be created by the merge. The
source archive is indicated for each data tpe in the conflict window. The "Foo" data type
was added to "helloProgram" from the "MyTestArchive" data type archive and is still
associated with it in each program version (Latest, Checked Out and Original.)


Category conflicts are resolved after data type conflicts. If you make a category change
(rename, move, delete, restructure) in your version of the file, and the same *type*
of change was made in the latest version of the file, then a conflict arises that you must
resolve.


The image below shows the scenario where you:


**moved** /MISC  →  /Category1/MISC


In the latest version:


**moved** /MISC  →  /Category1/Cateogry2/Category3/MISC


![](images/CategoryConflict.png)


The options to resolve the conflict are:


- *Latest* - select this option to keep what is in the latest
version (lose your changes)
- *Checked Out* - select this option to apply your changes
- *Original* - select this option to apply what was in the program
that you had originally checked out (your changes and those in the latest version are
lost)


Select a radio button to resolve the conflict.


After all data type and category conflicts are resolved, the merge process
continues with Program Context Registers.


<a name="sourcearchiveconflict"></a>For data types a source archive
conflict can occur if the name of an associated source archive changes to a different name
in each of the two programs being merged. In the following, the "helloProgram" in the
"SampleProject" (as indicated by the Merge Tool title) has a data type that originated from
"MyTestArchive". Before you checked in your last changes to the program, the source data
type archive was renamed to "TestArchiveTwo". Before someone checked in the Latest changes
the source archive had been renamed "TestArchiveOne".


![](images/DataTypeSourceConflict.png)


Name: This is the name of the
source archive in that version of the program.

Last Sync Time: This is when the program was last
synchronized with the source archive.

Changed Since Last Sync? yes, means that one of
the program's data types associated with the source archive has been changed since the last
time it was synchronized.


To resolve the conflict, select the radio button associated with the
current name of the archive.


### Program Context Registers


All register value conflicts that remain after the [auto merge](Merge_Program_Files.md#program-context-registers) must be resolved.


[Register](../RegisterPlugin/Registers.md) values can be set on an individual
address or a range of addresses. When a register's value at an address or address range is
changed in both the latest version and your checked out version and the two values are
different, this results in a conflict. For each conflict, the merge tool will display the
address or address ranges where the two versions conflict.


The conflict window will present you with
each register that has value conflicts. For each of these registers you will have to
resolve each of the address ranges that has a conflict. The conflict information area at
the top of the window indicates the register name. It also indicates which address range
you are resolving of all the ranges in conflict for this register.


The following image illustrates a conflict due to the
DIRECTION register's value being changed in the latest version and cleared in your checked
out version of the program. The address range affected by this particular conflict is from
address 01002329 to 0100233b. This is indicated in the conflict resolution area below the
program listings. The affected addresses are also indicated by the gray
background in the program listings.


![](images/RegConflict.png)


> **Tip:** The scrolled listings allow you to
see the code units in the different program versions, which may help determine the correct
register value to choose. The layout of the Merge Program Context window is very similar to
the Merge Listing window.


The options to resolve the conflict are:


- *Latest* - select this option to keep what is in the latest
version (lose your changes)
- *Checked Out* - select this option to apply your changes
(overwrites change in the latest version)
- *Original* - select this option to restore the original register values (your
changes and those in the latest version are lost)


Select a radio button to resolve the conflict and then press the
**Apply** button to continue merging.


After all register conflicts are resolved, the merge process continues with
the Listing.


### Listing


Various parts of the program are merged in the Listing merge phase. These include the
bytes and code units, functions, symbols, equates, user defined properties, references,
bookmarks, and comments. Listing conflicts must be resolved in the order they are presented
before moving to the next conflict and eventually completing the merge process.


#### Listing Conflict Window


<a name="mergelistingwindow"></a>Listing conflicts are presented in a Merge Listing
Window. The Merge Listing Window displays four program listings:


| Result   | The new program version that will result from this merge.   |
| --- | --- |
| Latest   | The latest checked-in version of the program.   |
| Checked Out   | Your checked out version of the program to be merged.   |
| Original   | The version of the program that you originally checked out.   |


The following shows the Merge Listing Window and describes (in red
text) some of the features of the conflict window.


The *![Merge.png](../icons/Merge.png) Merge Listing* on the top left side of the
window indicates that you are in the Listing phase of the merge. The *Resolve Byte / Code
Unit Conflict* area title indicates you are in the Code Unit phase of Listing Merge.
This area provides the following information:


- the addresses for the conflict currently being resolved
- number of conflicts at the indicated address(es)
- current conflict
- how many sets of conflicts there are to resolve in this phase of the Listing
merge


![](images/ListingMergeDescriptions.png)


Each of the listings in the above image displays the associated program (Result, Latest,
etc). This allows you to look at each of the programs involved in the merge whenever you
are trying to resolve a Listing conflict. You can use the ![expand.gif](../icons/expand.gif) expand icon in the Result listing's toolbar to adjust the fields that are displayed in
all of the listings like in the Code Browser. The *GoTo* is also available for
navigating within the listings.


Scroll Locks for the Listings ![lock.gif](../icons/lock.gif) ![unlock.gif](../icons/unlock.gif)


Initially, the four programs scroll together. Each listing has a lock icon ![lock.gif](../icons/lock.gif) associated with it. When the lock icon ![lock.gif](../icons/lock.gif) is displayed for a listing, scrolling that listing or
navigating within that listing will also cause all other locked listings to scroll to the
same address. When a listing is displaying the unlocked icon ![unlock.gif](../icons/unlock.gif) , it will not scroll when the other listings scroll. Likewise, scrolling it will
not cause any of the other listings to scroll.


#### Code Units


The first type of Listing conflict you may encounter is a byte or code unit conflict.
All byte and code unit conflicts that remain after the [auto merge](Merge_Program_Files.md#code-units) must be resolved.


The following types of changes will result in code unit conflicts that need
resolving.


- The same bytes had their values changed to different values in the latest version
and your checked out version.
- A byte was changed in one version where a code unit was changed in the other
version.
- The code units were changed in your version and the latest version but not to the
same new code units.
For example, latest created an instruction and your version created data at an address.
Another example would be that a different structure was applied in your version and the
latest version at the same address.
- An instruction was cleared in one version and an equate was set in the other
version.
- An instruction had a flow override applied in one version and a reference was added
in the other version.


> **Note:** If an instruction change conflicts with a
reference change, the references can be viewed by right clicking on an instruction in
one of the four listings (Result, Latest, Checked Out, Original) and choosing the View Instruction Details... action. This will pop up a dialog indicating any
fallthrough override or flow override and the references for that instruction.


Example : The following image shows a code unit conflict that occurred because
you changed the second component of the *SampleStructure* from a word to an array of
two characters and the word was changed in the latest version to two separate
characters.


![](images/CodeUnit2CharConflict.png)


Notice that the listings allow you to open and close the structure in the
same way that you can in the CodeBrowser by clicking on the + in the listing. The
addresses with the gray background in the listing indicate the code unit(s) that you are
currently trying to resolve.


Note that you will have already resolved all [data type conflicts](#data-types-and-categories) by this time; this conflict is due to
different data types being applied at the same address. You are resolving *which data
type to apply* at the address.


In this case the options to resolve the conflict are:


- *'Latest' version* - select this option to keep the structure
containing two separate characters as in the latest version (lose your changes)
- *'Checked Out' version* - select this option to apply your
structure containing the 2 character array (overwrites change in the latest
version)
- *'Original' version* - select this option to restore the original structure
containing the word (your changes and those in the latest version are lost)


Depending on which option you choose, you may end up with a
"SampleStructure.conflict" as the data type name.


Select a radio button to resolve the conflict and press the **Apply**
button to continue with the merge process.


After all byte and code unit conflicts are resolved, the merge process
continues with any Function conflicts in the Listing.


#### External Functions and Labels


All external location conflicts that remain after the [auto merge](Merge_Program_Files.md#external-functions-and-labels) must be resolved.


The following types of changes to external locations will result in conflicts that need
resolving between your checked out version and the latest version in the repository.


- If you add an external function or label and it appears to be the same external as
one that was added in the latest version. (i.e. It has the same name or is
referenced from the same code.)
- If an existing external function or label is removed in your version and changed
in the latest version in any way or vice versa.
- If you change an external label into an external function and the latest sets the
data type on the external label or vice versa.
- If you change the number of parameters, the parameter storage, or the parameter type
(stack versus register) and the latest also changed parameters in any way, then you must
select to keep all of your parameters or all of the latest version's parameters. The
same is true if the latest version changed the number or type of parameters and you changed
parameters in any way.
- If you change a piece of an external functions information and the latest version
changes the same piece of function information to a different value.
For example, if one changes the function's name and the other changes the return
type, then both changes occur without a conflict. If both change the name, this is a
conflict.
- If you change a piece of stack information and the latest version changes the same
piece of stack information to a different value.
Stack information includes:
  - return address offset
  - parameter offset
  - stack purge size
- If you change a piece of parameter information and the latest version changes the
same piece of parameter information to a different value.
Parameter information includes:
  - name
  - data type
  - comment
  - offset
  - register


Example 1 : The following image illustrates a possible Add conflict. In this case,
an external label was added to the Latest program and an external function was added to
the Checked Out program. Both external locations refer to the same external memory address and
may be intended as the same external.


![](images/ExternalAddConflict.png)


In this case you must select the radio button indicating which external(s) to keep:


- *Keep 'Latest'* will keep the external label.
- *Keep 'Checked Out'* will keep the external function.
- *Keep Both* will keep Both the external label and the
external function. If the label and function had the same name, the function would
get renamed with a new name containing a conflict extension.
- *Merge Together* will merge the external label and
function together. In this case, the result would be an external function,
but after pressing the Apply button, you would be prompted
with an additional name conflict that you would need to resolve.


Select a radio button and press the
**Apply** button to continue with the merge process.


Example 2 : The following image illustrates a conflict due to an external label
having its data type set in the latest version while you changed it into a function.


![](images/ExternalDataTypeConflict.png)


In this case you must select the radio button indicating which change to keep:


- *Keep 'Latest'* will result in the external label with a Float
data type and the change to a function is discarded.
- *Keep 'Checked Out'* will keep the external as a function and the
data type change will be discarded.


Select a radio button and press the **Apply** button to continue with
the merge process.


Example 3 : The following image illustrates a conflict because you created the
same external function as was created in the latest version. However, parameter storage
has been defined differently in each version. You must choose which parameter signature
and its associated storage should be kept.


![](images/ExternalFunctionParametersConflict.png)


In this case the options to resolve the conflict are:


- *Use Latest version.* will use the function parameter storage
as it is in the Latest version.
- *Use Checked Out version* will use the function parameter storage
as it is in your Checked Out version.


Select a radio button and press the **Apply** button to continue with
the merge process.


After all external label and external function conflicts are resolved,
the merge process continues
with any regular Function conflicts in the Listing.


#### Functions


All function conflicts that remain after the [auto merge](Merge_Program_Files.md#functions) must be resolved.


The following types of changes to functions will result in conflicts that need
resolving between your checked out version and the latest version in the repository.


- If you create or change a function causing its body to overlap one or more functions
that are defined in the latest version.
  - Functions with bodies that have addresses in common are said to *overlap*
if their entry points and bodies are not exactly the same.
  - In this case you must choose which version's function(s) to keep.
- If an existing function is removed in your version and changed in the latest
version in any way or vice versa.
- If both versions add a function with the same entry point, but all parts of the
function are not the same.
- If you change the number of parameters or the parameter type (stack versus
register) and the latest also changed parameters in any way, then you must select to
keep all of your parameters or all of the latest version's parameters. The same is true
if the latest version changed the number or type of parameters and you changed
parameters in any way.
- If you change a piece of function information and the latest version changes the same
piece of function information to a different value.
Function information includes:
  - name
  - body
  - return data type
For example, if one changes the function's name and the other changes the return
type, then both changes occur without a conflict. If both change the name, this is a
conflict.
- If you change a piece of stack information and the latest version changes the same
piece of stack information to a different value.
Stack information includes:
  - return address offset
  - parameter offset
  - local size
  - stack purge size
- If you change a piece of parameter information and the latest version changes the
same piece of parameter information to a different value.
Parameter information includes:
  - name
  - data type
  - comment
  - offset
  - register
- If you change a piece of local variable information and the latest version changes
the same piece of local variable information to a different value.
Local variable information includes:
  - name
  - data type
  - comment
  - offset
  - register


Example 1 : The following image illustrates a function parameter with multiple
conflicts. In this case the conflict resolution area below the listings is different than
many of the other listing conflict resolution areas. Each row of the table provides you
with a separate conflict and a choice that must be made.


Notice in the image that the parameter name and the parameter type are each in
conflict. You must choose a radio button on each row to indicate what you want to keep in
the version that will get checked in.


![](images/ParameterMultiConflict.png)


The function FUN_01002b44 has two conflicts for its second parameter.

In this case the options to resolve the conflict are:


- Conflict column - indicates what specific part of the function is in conflict.
- *Latest* column - select the item from this column to keep the
latest version's change (lose your changes).
- *Checked Out* column - select the item from this column to keep
your change (overwrites change in the latest version).


Select a radio button on each row to resolve the conflicts and press the
**Apply** button to continue with the merge process.


Example 2 : The following image illustrates a conflict due to overlapping
function bodies. In this case you created a function at address 01001984 and the latest
version created a function at address 01001979. The two functions don't have the same
entry point, but their bodies overlap. Since function bodies can't overlap, you must
choose which version's functions should be kept. The *Resolve Function Overlap
Conflict* area indicates the address range(s) that are in conflict. This is also
indicated by the gray background in the listings.


![](images/FunctionOverlapConflict.png)


In this case you must select the radio button indicating which version's functions to
keep:


- *Latest* - select the radio button in front of Latest to keep
the latest version's functions for the indicated address ranges (lose your
functions).
- *Checked Out* - select the radio button in front of Checked Out
to keep the your functions for the indicated address ranges (overwrites change in the
latest version).


Select a radio button and press the **Apply** button to continue with
the merge process.


Example 3 : The following image illustrates a conflict because you changed the
return type and the function was deleted in the latest version. You must choose whether
to keep the function or remove it.


![](images/FunctionRemoveVsChangeConflict.png)


In this case the options to resolve the conflict are:


- *Delete function as in 'Latest' version.* - select this option
to remove the function as in the latest version (lose your changes)
- *Keep function 'FUN_010031ee' as in 'Checked Out' version* -
select this option to keep the function and your changes to it (overwrites change in
the latest version)


Select a radio button and press the **Apply** button to continue with
the merge process.


After all function conflicts are resolved, the merge process continues
with any Symbol conflicts in the Listing.


#### Symbols


All symbol conflicts that remain after the [auto merge](Merge_Program_Files.md#symbols) must be resolved.


The symbol phase of the Listing merge will merge labels, [namespace](../SymbolTreePlugin/SymbolTree.md#display) symbols, class
symbols, and external symbols.

The following are the types of symbol conflicts that require manual resolution:


- Removed symbol in one version and changed it in other.
- Symbol was renamed differently in each version.
- Same named symbol at the same address in each version, but in different namespaces
(symbols with different scope).
- Each version set a different symbol to primary at an address.


Example 1 : The following image shows a symbol conflict that occurred because
you changed the label "DDD" from global scope to function scope (in the FUN_01004444
function's namespace) and the latest version removed the symbol.


![](images/SymbolRemoveVsChangeConflict.png)


In the *Resolve Symbol Conflict* area you must choose an option to
resolve the conflict. Each row shows the information for a different version of the
program. The Option column allows you to choose a version change or simply indicates
which version's information follows it in the row. The Symbol column gives the symbol
name. The Scope gives the namespace containing the symbol. The address indicates the
address where the symbol is located. The Type indicates whether the symbol is a label,
namespace, class, etc. Primary indicates whether the symbol is the primary symbol at the
address in that version.


In this case the options to resolve the conflict are:


- *Remove as in 'Latest' version* - select this option to leave
the label DDD removed (lose your changes)
- *Change as in 'Checked Out' version* - select this option to
change the label DDD to be in the function's scope (overwrites change in the latest
version)
- *'Original' version* - this is not selectable, but shows the symbol in the
original version you checked out.


Select a radio button to resolve the conflict and press the **Apply**
button to continue with the merge process.


Example 2 : The following image shows a symbol conflict that occurred because you
changed the label "AAA" to "ME" and changed it to global scope, but the latest version
only renamed the symbol.


![](images/SymbolRenameWithScopeConflict.png)


In this case the options to resolve the conflict are:


- *Rename as in 'Latest' version* - select this option if ME
should be in the function's scope (lose your changes)
- *Rename as in 'Checked Out' version* - select this option if ME
should have global scope (overwrites change in the latest version)
- *'Original' version* - this is not selectable, but shows the symbol in the
original version you checked out.


Select a radio button to resolve the conflict and press the **Apply**
button to continue with the merge process.


Example 3 : The following image shows a symbol conflict that occurred because you
added the label "Bud" to the function scope (in the FUN_01004bc0 function's namespace)
and the latest version added the same named symbol at the same address, but gave it
global scope.


![](images/SymbolAddressConflict.png)


In the *Resolve Symbol Conflict* area you must choose an option to
resolve the conflict. Each of the first two rows shows the information for a different
version of the program. Below these rows are two radio buttons that let you choose to
either discard your symbol or rename it so that its name will not conflict with the one
from the latest version.


In this case the options to resolve the conflict are:


- *'Latest' version* - this is not selectable, but shows the
symbol in the latest version.
- *'Checked Out' version* - this is not selectable, but shows your
symbol.
- *Discard 'Checked Out' symbol* - select this option to not
include your symbol (lose your changes).
- *Rename 'Checked Out' symbol to 'Bud_conflict1'* - select this
option to rename your symbol to avoid the conflict.


Select a radio button to resolve the conflict and press the **Apply** button to
continue with the merge process.


Example 4 : The next image shows a symbol conflict about which symbol to make the
primary symbol at an address. In the following scenario, you added the label "Bar" and
the latest version added the label "Foo" at the same address. Both labels can exist at
the same address since they have different names, but they cannot both be the primary
symbol. So you must choose which label is the primary one.


![](images/SymbolPrimaryConflict.png)


In this case the options to resolve the conflict are:


- *Set 'Latest' to primary* - select this option if Foo should be
the primary symbol.
- *Set 'Checked Out' to primary* - select this option if Bar
should be the primary symbol.
- *'Original' version* - this is not selectable, but shows the symbol in the
original version you checked out. In this case there was no label originally.


Notice that both symbol are kept as shown in the Result program's listing.


Select a radio button to resolve the conflict and press the **Apply** button to
continue with the merge process.


Symbol Merge Information Dialog


At the end of the Symbol merge phase, a *Symbol Merge Information* dialog
will appear if any namespaces could not be removed as expected. You might indicate to
remove a namespace when it is in conflict with another symbol or it may have been
removed by auto merge. However, if another symbol gets placed into that namespace as
a result of resolving a conflict, the namespace must be retained. The dialog is
simply to inform you that this has occurred. The following image illustrates that the
namespace called SecondNamespace was not removed since it contained at least one
other symbol.


![](images/SymbolNamespaceKept.png)


Press the OK button on this dialog to continue with the merge process.


The *Symbol Merge Information* dialog can also have symbol conflict information.
If a symbol must be renamed as part of the merge process, you are notified of the new
symbol names at the end of the Symbol merge phase.


Conflicting symbols are renamed by adding a suffix of "_conflict" and an incremented
number to make the name unique. The following image shows two renamed symbols. The first
is the global symbol ME which was renamed to ME_conflict1. The second is the symbol YOU
in the FUN_01001ae3 namespace which was renamed YOU_conflict1.


![](images/SymbolConflictAutoRenamed.png)


Press the OK button to continue with the merge process.


After all symbol conflicts are resolved, the merge process continues with
any Address Based Listing Merge conflicts.


#### Address Based Listing Merge


All of the address based listing elements (equates, user defined properties,
references, bookmarks, and comments) has already been auto merged before any of their
conflicts are presented for conflict resolution. Conflict resolution will proceed in
address order for each address that has a conflict for any of the address based listing
elements. At each address with a conflict you will have to resolve all of the conflicts
(equates, user defined properties, references, bookmarks, and comments) before proceeding
to the next address with conflicts. The following sub-sections describe conflict merging
for each of the address based listing elements.


#### Equates


All equate conflicts that remain after the [auto merge](Merge_Program_Files.md#equates) must be resolved.


[Equates](../EquatePlugin/Equates.md) associate a name with a
scalar. If your version and the latest version change the equate for a scalar and they
are different as a result of the change, then the equates are in conflict and must be
resolved manually. Changes include adding an equate to a scalar, removing an equate for
a scalar, changing the equate name for a scalar.


If an equate is changed differently in the latest and your versions, then you must
resolve the conflict.


Example : The following illustrates an equate conflict on the scalar 0x1 of
operand 0 at 01001d0b. The scalar originally had an equate of **01**. Each version
changed the equate on 0x1 to a new name.

The image below shows the scenario where you:


**changed** 01  →
PEAR


In the latest version:


**changed** 01  →
ORANGE


![](images/EquateConflict.png)


The options to resolve the conflict are:


- *Keep 'Latest' version* - select this option to keep the
equate for the latest version (lose your changes)


- *Keep 'Checked Out' version* - select this option to keep your
equate
- *'Original' version* - this row simply indicates the original
value at the time you checked out the program


Select the radio button for either the latest or checked out version
and press the **Apply** button to continue with the merge process.


After all equate conflicts are resolved, the merge process continues
with the User Defined Properties.


#### User Defined Properties


All user defined property conflicts that remain after the [auto merge](Merge_Program_Files.md#user-defined-properties) must be
resolved.


User defined properties are individual named properties associated with addresses in
the program. Individual plugins can create one or more property. All of the conflicts
for a named property are presented to you and must be resolved before the next named
property with conflicts is presented.


If the named property was changed at an address in your version of the program and
changed differently in the latest version then a user defined property conflict
exists.


Example : The image below shows the scenario where you:


Added a **Space** property with a value of **4**.


In the latest version:


Added a **Space** property with a value of **3**.


![](images/UserDefinedUseForAllConflict.png)


The options to resolve the conflict are:


- *Keep 'Latest' version* - select this option to keep what is in
the latest version (lose your changes)
- *Keep 'Checked Out' version* - select this option to apply your
changes (overwrites change in the latest version)
- *Keep 'Original' version* - select this option to restore the original value
of the property (your changes and those in the latest version are lost)


Select the radio button for the value of the Space property you want to have in the
checked in version.


You can resolve the remaining conflicts for the same named property by selecting the
checkbox, *Use the selected option for resolving all remaining 'Space' property
conflicts.* The same program version option that you selected will be applied to the
remaining conflicts for the same named property. In the example above, the 'Check Out'
version option would be used for the remaining conflicts for the **Space**
property.


When you **Apply** after selecting the radio button and checkbox as illustrated in
the example above, your changes (the Checked Out version) would be chosen for the
**Space** property at the indicated address and for all remaining addresses that have
the **Space** property in conflict. Because you selected the checkbox, you will no
longer be prompted to resolve conflicts for that property type.


> **Note:** Selecting the Use the selected option for
resolving all ... checkbox for the Space property would not affect the resolving of
conflicts for any other named property. However, the user can select the checkbox for
each different named property with conflicts.


After all user defined property conflicts are resolved, the merge process
continues with the References.


#### References


All reference conflicts that remain after the [auto merge](Merge_Program_Files.md#references) must be resolved.


[References](../ReferencesPlugin/References_from.md) consist of
memory references, stack references, register references and external references. The
references in your checked out version and the latest version are compared for each
mnemonic and operand at an address to determine if a conflict exists.


<a name="referenceconflict"></a>References conflict if the two versions of the
program (your version and the latest version) have a reference at the same address and
operand, but they are different types of references (memory, stack, register,
external). References can also conflict when they are the same type if both versions
changed the reference and one or more parts are now different. The following indicates
the parts of a reference that can conflict with another reference of the same type.


Parts of an ***external*** reference that may conflict:


- external program name
- referenced label
- referenced address
- whether or not it is user defined


Parts of a ***stack*** reference that may conflict:


- stack offset
- referenced variable name
- first-use address


Parts of a ***register*** reference that may conflict:


- the register
- referenced variable name
- first-use address


Parts of a ***memory*** reference that may conflict:


- offset
- label
- reference type (computed call, computed jump, data, read, write, flow, etc.)
- whether or not it is a user reference


The following types of changes will result in reference conflicts:


- Your version and the latest version each added a different *reference type*
(memory, stack, or external).
If your checked out version and the latest version both have changes to the
references for a mnemonic or operand, the references are in conflict whenever your
version and the latest version have references that are different types (for
example, one has memory references and the other has an external reference.)
- You removed a reference and the latest version changed the same reference or vice
versa.
- Your version and the latest version both changed a reference and it now differs
in one of the ways they can conflict as indicated above.
- Your version and the latest version both added the same type of reference with
the same from and to addresses, but differed such that they [conflict](#references).
- Your version and the latest version both set the primary reference, but not to
the same reference.


> **Note:** The first operand of an
instruction is numbered as operand 0.


Example 1 : The following image illustrates an *external
reference conflict*. Your version and the latest version both changed the external
reference at address 01001000 operand 0. The latest version caused it to become user
defined and you changed it to refer to the symbol "bud" instead of "IsTextUnicode".


![](images/ExternalRefConflict.png)


The options to resolve the conflict are:


- *Change as in 'Latest' version* - select this option to keep
what is in the latest version (lose your changes). In this case, keep the reference
to "IsTextUnicode."
- *Change as in 'Checked Out' version* - select this option to
apply your changes (overwrites change in the latest version). In this case keep the
reference to "bud."
- *'Original' version* - This field is not selectable, but is provided to show
the value in the Original version that you checked out.


Select the radio button for whether to keep the reference to 0x10 or
0x14 and select the **Apply** button to continue with the merge process.


Example 2 : The following image illustrates *conflicting reference types*
being added in your version and the latest version. Possible reference types are
memory, stack, register or external. In this case, you added a stack reference and the
latest version has a register reference added at address 010018cd operand 0.


![](images/RefRegStackConflict.png)


Once again, select the radio button for which reference to keep and
select the **Apply** button to continue with the merge process.


Example 3 : The next image illustrates a *memory reference
conflict* where you changed an existing memory reference from a DATA reference to a
WRITE reference and the latest version changed the memory reference to a READ_WRITE
reference.


![](images/MemRefConflict.png)


Select the radio button for which reference to keep and select the
**Apply** button to continue with the merge process.


Example 4 : The following illustrates a *conflict when
different reference types are added* in your version and the latest version. In this
case you added an external reference at address 01002510 operand 0 and the latest
version added multiple memory references.


![](images/RefTypeConflict.png)


The options to resolve the conflict are:


- *Use all in 'Latest' version* - select this option to keep
what is in the latest version (lose your changes). This would keep all of the
memory references and lose the external reference.
- *Use 'Checked Out' version* - select this option to apply your
changes (overwrites change in the latest version). This would keep the external
reference and lose all of the memory references.
- *'Original' version* - This field is not selectable, but is provided to show
the value in the Original version that you checked out. In this case there was no
reference originally.


Select the radio button for which references to keep and press the
**Apply** button to continue with the merge process.


After all reference conflicts are resolved, the merge process continues
with the Bookmarks.


#### Bookmarks


All bookmark conflicts that remain after the [auto merge](Merge_Program_Files.md#bookmarks) must be resolved.


**Note** bookmarks are in conflict when any of the following occur:


- your version and the latest version both add a **Note** bookmark and the
category or description differ.
- your version removes a bookmark and the latest version changes the category or
description or vice versa.
- your version and the latest version change the category and/or description so
that they no longer match.


All other bookmarks are in conflict when any of the following occur:


- your version and the latest version both add a non-**Note** bookmark with the
same category but different description.
- your version removes a non-**Note** bookmark of a specific category and the
latest version changes the description for that bookmark type and category or vice
versa.
You cannot directly change the description
on a non-**Note** bookmark through regular bookmark editing in Ghidra, but a
plugin could change it programmatically.
- your version and the latest version change the description for a bookmark of a
particular type and category so that they no longer match.


Example 1 : The next image illustrates a conflict due to your version and the
latest version both adding different **Note** bookmarks at the same address.


![](images/BmNoteBothAddConflict.png)


When bookmarks are in conflict, you can:


- *Keep 'Latest' version* - select this option to keep the
bookmark change in the latest version (lose your changes)
- *Keep 'Checked Out' version* - select this option to apply
your bookmark changes at the address (overwrites change in the latest version)
- *'Original' version* - This field is not selectable, but is provided to show
the value in the Original version that you checked out


> **Note:** Notice that the above bookmarks
conflict even though they are not in the same category. This is because only one Note bookmark is allowed at an address regardless of its category.


Select either the latest version or your checked out version and then select
**Apply** to continue with the merge.


Example 2 : The next image illustrates an **Analysis** bookmark where another
user changed the comment in the latest version, but you removed the bookmark.


![](images/BmRemoveVsChangeConflict.png)


Select *Keep 'Latest' version* to keep the other user's changes or select
*Remove as in 'Checked Out' version* if you don't want the bookmark in the
resulting program. Then select the **Apply** button to continue merging.


#### Comments


All comment conflicts that remain after the [auto merge](Merge_Program_Files.md#comments) must be resolved at each conflict
address.


Only comments of the same type and at the same address can conflict with each other.
The types of comments are Plate, Pre, End-of-Line, Repeatable, and Post.


If a comment is removed in one version and changed in the other version, you must
choose whether to keep or remove it. This scenario is shown in the image below.


![](images/CommentRemoveVsChangeConflict.png)


If both versions added the same type of comment at an address and the two comments
don't match, then you must decide to keep the latest version's comment, your comment,
or both comments.


Similarly, if a particular comment was changed in both versions and the two comments
no longer match then you must decide to keep the latest version's comment, your
comment, or both comments. This scenario is shown in the image below.


![](images/CommentChangeConflict.png)


> **Note:** If you choose to keep both comments by
placing checkmarks in both boxes, your comment is appended to the latest comment with a
new line separating them. If one of the comments is contained within the other comment,
then the longer comment is kept instead of combining them with a new line
separator.


After all address based listing conflicts are resolved, the merge
process continues with External Program Names.


### External Program Names


All external program name conflicts that remain after the [auto merge](Merge_Program_Files.md#external-program-names) must be resolved.


A conflict occurs if :


- both versions add the same external program name with different paths
- both versions changed the path for an existing name
- one version removes the external program name and the other redefines the Ghidra
program path associated with that name


Example 1 : The following image shows a conflict when the latest and your
versions changed the path for an external program name.


![](images/ExternalProgramChangeConflict.png)


Select the version (Latest or Checked Out) of Ghidra program path to associate with the
external program name and then select the **Apply** button to proceed with the
merge.


Example 2 : The image below shows a conflict due to an external program name being
removed in one version and changed in the other.


![](images/ExternalProgramRemoveConflict.png)


In the above scenario, the external program name "ADVAPI32.DLL" was removed in the
latest version. However, the program path indicating which Ghidra program is associated
with the external program name, was modified in your checked out version.


The options to resolve the conflict are:


- *Remove as in 'Latest' version* - select this option to remove the
External Program Name definition for ADVAPI32.DLL (lose your changes)
- *Keep 'Checked Out' version* - select this option to apply your
changes resulting in a new program path for ADVAPI32.DLL (overwrites change in the
latest version)
- *'Original' version* - This field is not selectable, but is provided to show the
value in the Original version that you checked out


Select the radio button for the desired result and then select the **Apply** button
to proceed with the merge.


> **Note:** When you remove an external program name that is
in conflict, it will get added back later as a result of choosing a reference that refers
to that external program name.


### Property Lists


All property list conflicts that remain after the [auto merge](#property-lists)
must be resolved.


A property list conflict will result when you change a property that was either deleted
or changed in the latest version. The image below shows this scenario:


![](images/ProperyListConflict.png)


Here, in the *Analysis Disassembly* Property Group, another user changed the
*Mark Bad Disassembly* property. You changed the same property. You have following
choices:


- Keep the other user's changes (*Latest*), and lose your change
- Keep your changes (*Checked Out*) and lose the change in latest version
- Keep the values from the original version of the program (*Original*), lose
your changes and lose changes made in the latest version. In this example, if you
choose this option, the property will be deleted.


To resolve the conflict, select a radio button, and then click on the **Apply**
button to go to the next property conflict. In this example, there are three property
list conflicts (noted in the *Current Conflict* area of this window). The progress
bar on the lower right corner of the Merge Tool indicates progress only for the Property
List merge, not the entire merge process.


After you resolve all conflicts, the check in process is complete. The Ghidra Server
will contain a new version of the program file.


**Related Topics:**


- [Shared Project
Repository](../VersionControl/project_repository.md#project-repository)
- [Check in](../VersionControl/project_repository.md#check-in)
- [Memory
Blocks](../Glossary/glossary.md#memory-block)
- [Program
Trees](../ProgramTreePlugin/program_tree.md)
- [Data Types and
Categories](../DataTypeManagerPlugin/data_type_manager_description.md)
- [Program
Options](../ProgramManagerPlugin/Program_Options_Dialog.md#detailed-properties-descriptions)
- [Property
lists](../ProgramManagerPlugin/Program_Options_Dialog.md#detailed-properties-descriptions)
- [Symbols](../SymbolTablePlugin/symbol_table.md)
- [Property Viewer](../PropertyManagerPlugin/Property_Viewer.md)


---

[← Previous: About Program](../About/About_Program_File.md) | [Next: Tools →](../Tool/Ghidra_Tool_Administration.md)
