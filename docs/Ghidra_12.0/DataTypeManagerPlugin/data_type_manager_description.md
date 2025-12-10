[Home](../index.md) > [DataTypeManagerPlugin](index.md) > Data Types

# Data Type Manager


The *Data Type Manager* allows users to locate, organize, and apply data types to a
program. Allowing the user to build libraries of data types and to share them between programs,
projects, and different users is a long term goal for Ghidra.


## Topics


- [Basic Concepts](#basic-concepts)
- [Data Type Manager Window](data_type_manager_window.md)
- [Working With Data Type Archives](#working-with-data-type-archives)
- [Working With Categories](#working-with-categories)
- [Working With Data Types](#working-with-data-types)
- [Managing Archives](data_type_manager_archives.md)


## Basic Concepts


### Data Types


Ghidra supports three kinds of data types: "Built-in", user defined, and derived.


| **Built-in** | The built-in data types are implemented directly in Java and are used for the               basic standard types such as byte, word, string, etc. They can't be changed, renamed,               or moved within an archive. |
| --- | --- |
| **User Defined** | There are four user defined data types: Structures, Unions, Enums, and               Typedefs. They can be created, modified, and renamed as needed. |
| **Derived** | There are two derivative data types: Pointers and Arrays. Pointers and arrays can               be created and deleted as needed, but they take on a name derived from their base               type. |


### Data Type Archives


Data type archives are used to bundle and share data types between programs, projects, and
users. There are two different types of user created archives: File data type archives and
Project data type archives. Data type archives can be accessed within the
*Data Type Manager* window. When a data type archive is open, it
is displayed as a node in the *Data Type Manager*
tree. Archives can be opened by the user or automatically when a program is opened which
references that archive. Data type archives can be [open for
modification](#opening-a-file-data-type-archive-for-editing) or as read-only. Within the *Data Type Manager* window there are
actions for opening, closing, renaming, and making archives modifiable.


### Built-In Data Type Archive ![closedBookBrown.png](../icons/closedBookBrown.png)


The "Built-in" archive is a special archive that is always available in the
*Data Type Manager* window. It provides access to all of Ghidra's
"Built-in" data types. "Built-in" types are discovered by searching through Ghidra's class
path.


> **Note:** In the unlikely event that new data type class files
or jar files are added while Ghidra is running, there is a refresh action which will find and
add the new data types to the "built-in" archive.


### File Data Type Archive ![closedBookGreen.png](../icons/closedBookGreen.png)


File data type archives (or simply: file archives) store data types in files and have
".gdt" filename extensions. They can be located anywhere in the filesystem. File archives can
be open by more than one user at the same time (assuming it is located on a shared
filesystem), but only one of those users can have it open for modification.


### Project Data Type Archive ![closedBookBlue.png](../icons/closedBookBlue.png)


Project data type archives (or simply: project archives) store data types in Ghidra
project database directories, along with the programs for that project. The [Ghidra Project Window](../FrontEndPlugin/Ghidra_Front_end.md) will display project
archives in the same tree structure used to show the programs in the project. Project
archives can be versioned and shared in a multi-user environment just like programs. They use
the same "check-in/checkout" semantics for updating and sharing changes.


### Data Types in a Program ![closedBookRed.png](../icons/closedBookRed.png)


Besides being stored in archives, data types are also stored inside programs.


> **Note:** Any data type used in a program must be stored in
that program even if it originally came from an archive.


Because of this, the "same" data types can live in more than one archive or program and
can be modified in different ways in each place where it lives. Prior to Ghidra 4.3, keeping
data types consistent between archives and programs was a problem because there was no way to
maintain an association, except by location and name, which was difficult due to potential
conflicts. Now additional information such as source archive, unique ID and various change
times are maintained to facilitate keeping data types consistent across archives and
programs.


### Categories ![closedFolder.png](../icons/closedFolder.png)


Within a program or data type archive, data types can be organized using categories.
Categories are like folders in a filesystem and allow data types to be organized into a
hierarchical structure. Categories are ignored for purposes of [data
type synchronization](#updating-an-archive-from-a-source-archive). In other words, the same data type might be in a category named
"aaa" in an archive and be in a category named "bbb" in the program. As far as Ghidra is
concerned, the different category does not constitute a data type difference.


### Data Type Manager Tree


The *Data Type Manager* window organizes data types
using a tree structure. At the first level below the tree root, a node will exist for each
open archive and the "Built-in" archive. If a program is open, a node will also exist at this
level representing the program. In many ways, an open program behaves like a data type
archive.


### Applying Data Types


The primary purpose of a data type is to apply it to various elements in a program. Data
types can be applied to memory locations to provide interpretations of the bytes at those
locations. They can also be used to describe function parameters and local variables.


One way to apply data types is to drag them from an archive and drop them on an element in
the program [Listing](../CodeBrowserPlugin/CodeBrowser.md#listing-view). This
action will cause a copy of the data type to be added to the program and then a reference to
the copy will be used to annotate the program element. There are other ways of applying data
types to a program and they are described in more detail [later](#applying-data-types-to-a-program).


### Resolving Data Types


When a data type from an archive is applied to a program, a copy of that data type is
created in the program. The process of making that copy is called *resolving*. This is a
complicated process because data types can contain or reference other data types, possibly in
a circular fashion (via pointers). These referred data types may or may not already exist in
the program and the resolving process must account for this. Sometimes, a data type might
already exist with the same name as the *resolving* data type. Even if the conflicting
data type is equivalent, Ghidra may not be able to determine if the existing data type is
really meant to be the same as the *resolving* data type. Generally, such conflicts are
resolved by renaming the new or moved type by appending ".conflict" to its name. For many of
the data type actions initiated from the Data Type tree window, the specific conflict
resolution is determined by the current [Data Type Conflict Mode](data_type_manager_window.md#data-type-conflict-resolution-mode).
In the end, applying a single data type to a program can cause many new data types to be
added to the program.


### Source Archive


Whenever data types are resolved from an archive to a program or another archive, the
default behavior is to tag the copied data types with information about the archive from
which the data types originated. So each archive or program maintains a list of source
archives from which it has associated data types. Ghidra uses the term *Source Archive*
as a descriptor that identifies a file or project data type archive where a data type
originated. Whenever a program is opened, the *Data Type Manager* gets a list of source
archives from the program and automatically opens the corresponding data type archives if it
can find them. Using information stored in the source archive object along with information
from the actual archive and the change time on a data type, Ghidra can determine if data
types are *out-of-sync* with their corresponding data type in a program or other
archive.


> **Note:** The data type tree will indicate data types that have a source archive association
by displaying the name of the source archive in parenthesis after the data type name.


DataTypeName **(SourceArchiveName)**


### Client Archive


Ghidra uses the term *client* *archive* to
represent the archive that contains a data type taken from a *[source archive](#source-archive)*. This includes normal data type archives **and
the program**.


### Update Source Archive Names


When new releases of Ghidra are installed, old datatype archives may be dropped. In some
cases these old archives may be replaced with a differently named archive. When this
happens, this popup action can be used on a client archive to update the old source archive
references. This popup action is only available when such an archive name change has
occurred. Any programs or other client archives which reference the old archive will have
this popup action available to update the source archive name reference.


### Committing Changes To Source Archive


If changes are made to a data type that has an association with a source archive, those
changes must be applied to the original in the source archive to keep the data types in
sync. Ghidra uses the term *commit* to mean propagating changes from a data type back
to its corresponding data type in the source archive.


### Updating Data Types From Source Archive


If changes are made to a data type in an archive that has associated data types in a
client archive, those changes can be pushed out to those associations. Ghidra uses the term
*update* to mean propagating changes from a data type in a source archive to its
associated copies in a client archive.


### Reverting


If changes are made to a data type that has an association with a source archive, that
data type is now different from its source data type. Ghidra uses the term *revert* to
throw away the changes and put the data type back to the way it is in the source archive.
If changes are made in both the referenced data type and the source data type, the
*revert* action will not be available because the original state is not known. In this
case, you must either [commit](#committing-changes-in-an-archive-to-a-source-archive), which will lose the changes in the
source archive, or [update](#updating-an-archive-from-a-source-archive) losing the changes in the client
archive. Currently, there is no merge capability.

See [Reverting Changes](#reverting-changes) for more information.


### Synchronizing an Archive


When changes are made to data types in either the source archive or client archive, the
archive is said to be *out-of-sync*. Ghidra provides a capability known as
*synchronizing* to find all the data types that need to be [committed](#committing-changes-to-source-archive), [updated](#updating-data-types-from-source-archive), or [reverted](#reverting-changes) and allow the user to make a decision on each data
type.


### File Archive Path


Ghidra maintains a list of directories used to search for file archives. This list is
known as the archive path. Ghidra provides a dialog for adding, removing, and re-ordering
the list of these directories. When Ghidra maintains source archive information for a file
data type archive, it only stores the name of the archive and not the entire file path.
Storing absolute paths would make the file archive references very brittle when the program
is shared or moved to another location. By using archive paths, different users can
maintain copies of the source archives in different locations on their computer and still
be able to find the archives in their shared programs.

See also: [editing archive paths](data_type_manager_archives.md#edit-data-type-archive-paths).


## Working with Data Type Archives


There are two types of Data Type Archives: File and Project.


| **File Data Type                 Archives**   | Files containing data type definitions, which have ".gdt" as their                 file suffix. |
| --- | --- |
| **Project Data Type Archives**   | Special files located within the Ghidra project directory structure,                 which also contain data type definitions. These are available in the [Ghidra Project Window](../FrontEndPlugin/Ghidra_Front_end.md) and can be saved                 as versions in a shared project repository. |


The data types contained in an archive are organized into categories similar to the way
files are organized into directories in a filesystem. Archives are useful for sharing data
types with other users, or making your data types available for use in other projects.
Normally, file archives are opened in a read-only mode, but can optionally be [opened](#opening-a-file-data-type-archive-for-editing) for editing. Project archives are normally opened for
editing, since they support sharing and version control and therefore allow more than one
user to modify them at a time. Only one user at a time can have a file archive opened for
editing.


> **Tip:** You can assign a specific "Architecture" to a Data Type Archive while it is open for editing.  This is recommended when an archive is targeting
a specific processor and compiler specification (see Setting
Data Type Archive Architecture ).


### Opening a File Data Type Archive


From the local menu ![menu16.gif](../icons/menu16.gif) , select ***Open
File Archive...***. A file chooser will appear. Use the file chooser to find and select
the data type archive to open. A new node will appear in the tree for the newly opened
archive. Also, the directory containing the newly opened archive will be added to the
archive path if it is not already there.


### Opening a Project Data Type Archive


From the local menu ![menu16.gif](../icons/menu16.gif) , select ***Open
Project Archive...***. A Ghidra project data type archive chooser will appear. This
chooser will show all the project archives in the current project. Use the chooser to find
and select the project data type archive to open. A new node will appear in the tree for
the newly opened archive.


### Creating a New File Data Type Archive


From the local menu ![menu16.gif](../icons/menu16.gif) , select ***New
File Archive...***. A file chooser will appear. Use the file chooser to select a
directory and enter a name for the new archive. If an archive already exists with that
name, a dialog will appear asking if the existing archive should be over-written. A new
node will appear in the tree for the newly created archive.


### Creating a New Project Data Type Archive


From the local menu ![menu16.gif](../icons/menu16.gif) , select ***New
Project Archive...***. A Ghidra project data type archive chooser will appear. Use the
chooser to select a folder and enter a name for the new archive. A new node will appear in
the tree for the newly created archive.


> **Tip:** You can also create a new Project Data Type
Archive by dragging a File Data Type Archive (.gdt) file onto the Ghidra Project Window . This will create a new
Project Data Type Archive populated with the same data types as the dragged File Data Type
Archive.


### Setting Data Type Archive Architecture


By default, data type archives are not assigned an architecture and adopt a default
*Data Organization* which determines primitive data type sizing (e.g., int, long, pointer, etc.)
as well as alignment and packing behavior.  While data types copied between archives or a program
with disimilar *Data Organizations* will generally resolve correctly, unexpected results
may sometimes arise (e.g., bit-field packing within structures).  In addition, this situation
frequently causes some confusion when viewing and editing data types where the *Data
Organization* differs from the intended target architecture.


With either a file or project data type archive open for editing, a specific architecture
may be assigned to the archive.  This is done by selecting the open archive node from the
data type tree, right-click on it and select the ***Set Architecture...*** action.
This will popup a processor/compiler-specification selection dialog from which a selection
may be made and the **OK** button clicked.  A final confirmation dialog will be displayed
before completing the change from which the **Set Architecture** or **Cancel** button
must be clicked to confirm or cancel the change.  If confirmed, any architecture transition
will resolve all data types to the new data organization.  Details related to custom variable
storage for Function Definitions (not yet implemented) will be preserved if possible but
may be discarded.


At present, the user will be forced to save any unsaved archive changes prior to completing
an architecture setting change to allow for a fallback if neccessary.


### Clearing Data Type Archive Architecture


With either a file or project data type archive open for editing, a currently assigned architecture
may be cleared for a selected archive.  This is done by selecting the open archive node from the
data type tree, right-click on it and select the ***Clear Architecture*** action.
A final confirmation dialog will be displayed
before completing the change from which the **Clear Architecture** or **Cancel** button
must be clicked to confirm or cancel the change.  If confirmed, the archive will revert a default
*Data Organization* and any custom variable storage for Function Definitions
(not yet implemented) will be discarded.



At present, the user will be forced to save any unsaved changes prior to clearing the
architecture setting to allow for a fallback if neccessary.


### Closing a Data Type Archive


Select the data type archive to close, right-click on it and select the ***Close
Archive*** action. The archive will be removed from the tree.


### Opening a File Data Type Archive for Editing


When an archive is first opened, it is not editable. In order to make any changes to
the archive, it must be open for editing. Select the archive to edit, right-click on it
and select the ***Open for Editing*** action. If someone else is currently
editing that archive, this action will fail and a dialog will appear explaining that
someone else is already editing that archive.


### Closing a File Data Type Archive for Editing


When an archive that is [open for editing](#opening-a-file-data-type-archive-for-editing) no longer
needs to be edited, then it should be put back to a read-only mode so that other users
can then modify it. Select the data type archive to close for editing, right-click on it
and select the ***Close for Editing*** action. If the archive has unsaved
changes, a dialog will appear providing an opportunity to save the changes.


### Saving Changes to a Data Type Archive


Whenever a data type archive has been opened for
editing and has unsaved changes, the node will display its name with '*' attached.
For example the archive "MyArchive" will display as "MyArchive *". To save these changes,
right-click on the unsaved archive and select the ***Save Archive*** action. The
changes will be saved and the name will be updated to not show a '*'.


Unimplemented Action
`<H3>`&lt;A name="Save_As"&gt;&lt;/A&gt;Saving a File Data Type Archive to a New File`<BR>`
&lt;/H3&gt;

`<BLOCKQUOTE>`
`<P>`Right-click on the file archive to be saved to a new file, and select the `<I><B>`Save
As...&lt;/B&gt;&lt;/I&gt; action. A file chooser will appear which can be used to choose a location
and filename for the new archive that will be created. The tree will be updated to show
the new name for the archive (the filename). The original archive file is unaffected.&lt;/P&gt;
&lt;/BLOCKQUOTE&gt;


### Undo Unsaved Archive Change


The previous unsaved change made to an archive may be reverted by selecting the **Undo Change:...**
popup menu action while that archive is selected in the data type tree.
Each data type archive which is open for editing maintains a
stack of unsaved changes.  The next change which may be reverted is described by the archive's
Undo Change popup menu item.  If this action is used and a change is reverted it may be re-applied by using the
[Redo Change](#redo-unsaved-archive-change) action.  When the data type archive is
[saved](#saving-changes-to-a-data-type-archive) or [closed for editing](#closing-a-file-data-type-archive-for-editing) the undo/redo stack is
cleared.


### Redo Unsaved Archive Change


The previous [reverted](#undo-unsaved-archive-change) unsaved archive change may be
re-applied by selecting the **Redo Change:...** popup menu action while that archive is selected in
the data type tree.
The next reverted change which may be re-applied is described by the archive's
Redo Change popup menu item.  If this action is used and a change is re-applied it may again be reverted by using the
[Undo Change](#undo-unsaved-archive-change) action.  When the data type archive is
[saved](#saving-changes-to-a-data-type-archive) or [closed for editing](#closing-a-file-data-type-archive-for-editing) the undo/redo stack is
cleared.


### Deleting a Data Type Archive


Deleting an archive will not only remove the archive from the tree, but will
permanently remove it from the filesystem. To delete an archive, right-click on it and
select the ***Delete Archive*** action. An archive file must be open for editing
before this action will appear (see [Opening a Data Type
Archive for Editing](#opening-a-file-data-type-archive-for-editing)).


### Removing an Invalid Data Type Archive


When an archive file fails to open (when Ghidra can't find the file in the archive path
or encounters a permission problem) it will be displayed with the ![closedFolderInvalid.png](../icons/closedFolderInvalid.png) icon. If you wish to permanently remove the file path
from the tool configuration and the current program options, you may right-click on it and
select the ***Remove Invalid Archive*** action.


### Updating an Archive From a Source Archive


Datatypes within an archive that originally came from some other source archive may
need updating if they have been changed in the originating archive. If a an archive has
one or more datatypes that need updating, it will be marked with either the ![smallLeftArrow.png](../icons/smallLeftArrow.png) or the ![doubleArrow.png](../icons/doubleArrow.png)
icon.


To update the datatypes, right-click on the node that needs updating and select
**Update Datatypes From** ***→** **&lt;Source Archive
Name&gt;.*** The Update Data Types dialog will be shown allowing you to select
the datatypes to update.


> **Warning:** Ghidra uses time stamps and flags to
determine if an archive is out-of-sync. This can result in Ghidra indicating the
archive needs updating when actually it does not. For example, if a data type is
changed and then changed back, it will cause Ghidra to think the data type was changed.
In this case, invoking the update action will cause Ghidra to search for updates, but
when it finds none, a message dialog will appear indicating that no changes were
detected and the archive will be considered updated.


### Committing Changes in an Archive To a Source Archive


Datatypes within an archive that originally came from some other source archive may
have been changed and need to be pushed back (committed) to the originating archive. If a
an archive has one or more datatypes that need committing, it will be marked with either
the ![smallRightArrow.png](../icons/smallRightArrow.png) or the ![doubleArrow.png](../icons/doubleArrow.png) icon.


To commit the datatypes, right-click on the node that contains the changed datatypes
and select **Commit Datatypes To** ***→** **&lt;Source Archive
Name&gt;.*** The Commit Data Types dialog will be shown allowing you to select
the datatypes to commit.


> **Warning:** Ghidra uses time stamps and flags to determine
if an archive is out-of-sync. This can result in Ghidra indicating the archive needs
committing when actually it does not. For example, if a data type is changed and then
changed back, it will cause Ghidra to think the data type was changed. In this case,
invoking the commit action will cause Ghidra to search for commits, but when it finds
none, a message dialog will appear indicating that no changes were detected.


> **Note:** The source archive must be editable in order to commit.  File archives must be open for editing and project
archives that are under version control must be checked-out.


> **Note:** Any data type dependencies for a comitted
data type, which do not already have a source archive, will become associated to the same
source archive.


### Reverting Changes in an Archive Back To a Source Archive


Datatypes within an archive that originally came from some other source archive may
have been changed and need to be reverted back to same state as the source archive (i.e.
discard the local changes) If a an archive has one or more datatypes that can be
reverted, it will be marked with either the ![smallRightArrow.png](../icons/smallRightArrow.png)
or the ![doubleArrow.png](../icons/doubleArrow.png) icon.


To revert the datatypes, right-click on the node that contains the changed datatypes
and select **Revert Datatypes To** ***→** **&lt;Source Archive
Name&gt;.*** The Revert Data Types dialog will be shown allowing you to select
the datatypes to revert.


### Disassociating Data Types in an Archive From a Source Archive


Datatypes within an archive that originally came from some other source archive may be
disassociated from their source archive. This will prevent them from being updated or
committed back to the source archive. If a an archive has one or more datatypes that have
source archive relationships, the **Disassociate**
action will be available.


To disassociate datatypes, right-click on the node that contains the datatypes and
select **Disassociate Datatypes From** ***→** **&lt;Source
Archive Name&gt;.*** The Revert Data Types dialog will be shown allowing you to
select the datatypes to revert.


### Refreshing Data Type Sync Indicators in an Archive For a Source Archive


Datatypes that are associated with a source archive may have a commit, update, or
conflict icon indicating they are out of sync with the data type in the source archive,
when the data type actually matches the source datatype. This can happen if a data type
is changed, but changed to match its source. Invoke the **Refresh**
action to refresh all the sync indicators for that
source archive.


To refresh sync indicators for datatypes associated with a particular source archive,
right-click on the node that contains the datatypes and select
**Refresh Sync Indicators For** ***→** **&lt;Source Archive
Name&gt;.*** &lt;


### Version Control / Multi-user Actions on Project Archives


The full set of version control actions from the front-end project window are available
when right-clicking on a project archive. See the [Version Control](../VersionControl/project_repository.md#version-control) section of
the Project Window for more information.


## Working with Categories


[Categories](#categories) are used to organize data types into a hierarchical
structure. Categories can contain data types and other categories. Archive nodes represent
the root or default category for their corresponding archive they represent in addition to
representing the archive itself. In other words, most of the actions that apply to category
nodes can also be applied to archive nodes. The two exceptions are ***Delete*** and
***Rename***. The root category in an archive cannot be deleted and to rename it,
you must use the ***Save As...*** action, since its name is the name of the
archive.


### Creating a New Category


Right-click on the category where the new category is to be created. Select the
***New →  Category*** action and a new
category named "New Category" will be created.


### Renaming a Category


Right-click on the category to be renamed. Select the ***Rename*** action and
then type in the new name in the in-place text edit box.


### Deleting a Category


Right-click on the category to be deleted. Select the ***Delete*** action. A
confirmation dialog will appear since **this action cannot be undone** (unless its in
the program's archive)


### Moving a Category


Categories can only be moved **within the same archive**. Attempts to move
categories across archives are converted to a copy action. When a category is moved,
effectively all categories and data types are contained in that category are moved as
well. There are two ways to move a category:


| 1. **Drag-N-Drop** | Click on the category to be moved and drag it onto                 its new parent category. |
| --- | --- |
| 2. **Cut/Paste** | Right-click on the category to be moved and select                 the *Cut* action. Then right-click on the destination parent category                 and select the *Paste* action. |


### Copying a Category


Categories can be copied within an archive or from one archive to another, but the
behavior of the copy is very different for the two cases. When copying within an archive,
the behavior is more natural. Copies are made of the source category and its children and
placed inside the destination category. However, when copying from one archive to
another, the behavior is somewhat unusual. In this case, the selected categories and
contained data types are copied into the destination category, but if there are
additional data types that are referenced by the copied data types, those are copied into
the destination archive as well. After the copy, the additional data types will appear in
the same relative location as they exist in the source archive.


| 1. **Drag-N-Drop** | Click on the category to be moved and copy drag                 (hold the `<Ctrl>` key while dragging) it onto its new parent category. |
| --- | --- |
| 2. **Copy/Paste** | Right-click on the category to be moved and select                 the *Copy* action. Next, right-click on the destination parent category                 and select the *Paste* action. |


## Working with Data Types


Data types are the actual useful objects within archives. They can be applied to
programs to bring meaning to the data, parameters, local variables and function return
types contained in that program. User defined data types such as structures can be
arbitrarily complex, consisting of other data types which can be built upon other data
types and so on, until finally they are built on the primitive types (the built-in data
types.)


![](../shared/note.yellow.png)Built-in types have several restrictions. They
always live in the root category of an archive and they can't be renamed.


### Applying Data Types to a Program


Data types can be applied in several different ways:


| 1. **Drag-N-Drop** | Data types can be dragged directly onto various                 locations in the [Listing](../CodeBrowserPlugin/CodeBrowser.md#listing-view) view. If dropped                 onto undefined bytes, a new Data object is created. If dropped onto a function, the                 return type can be set, etc. |
| --- | --- |
| 2. **Favorites** | Data types can be set to be a favorite. This                 causes a popup menu action to be generated for that data type whenever the mouse is                 right-clicked over the appropriate location in the [Listing](../CodeBrowserPlugin/CodeBrowser.md#listing-view) view. |
| 3. **Last Used** | Whenever a data type is applied to a program it is                 remembered as the "last used" data type and can be easily applied to other                 locations using a key binding or popup menu actions. |


> **Note:** Applying a data type from an archive will
automatically add that data type to the program's archive. Also, the archive will become
associated with the program and automatically be opened whenever the program is
opened.


### Creating New User Defined Data Types


There are seven types of data types that users can create: Structures, Unions, Enums,
Function Definitions, Typedefs and Pointers.


Structures, unions, enums, and function definitions can be created by right-clicking
on the category where the new type should be located, and then choosing either the
***New →  Structure*, *New →  Union*,** ***New →  Enum*** or ***New →  Function Definition*** action respectively. Each of
these actions will bring up an appropriate editor ([structure
editor](../DataTypeEditors/StructureEditor.md) for structures and unions, the [enum editor](../DataTypeEditors/EnumEditor.md) for enums and the edit function
signature editor for function definitions) for creating the new desired data type.


#### Creating a Typedef


Creating a new **typedef** is even easier. Right-click on the data type to be
typedef'ed and select the ***New →  Typedef on
XYZ*** action. A new typedef will be created on the *XYZ* data type in the
same category as the original data type.


Alternatively, you can click ***New →
Typedef...***, which will show a dialog that allows you to choose a typedef name
and the data type from which the typedef will be created.* This action can
also be executed from any folder instead of directly on another data type.


A Typedef created with a Pointer base type will allow additional Settings to be made
which can influence how such a pointer should be interpreted
(see [Pointer-Typedef Settings](#pointer-typedef-settings)).
If no name is assigned to a new Pointer-Typedef is will be treated as an "auto-typedef"
where a dynamic name will be assigned based upon the underlying pointer and assigned
typedef attribute settings. Examples:


- *char * __((space(ram)))*
- *int * __((offset(0x8)))*
- *pointer __((image-base-relative))*


#### Creating a Pointer


To create a **pointer**, you can click ***New →  Pointer to XYZ***. A new pointer will be created to the *XYZ* data
type in the same category as the original data type.*


> **Note:** * A pointer will always be created
within the same category where the base datatype is defined.  When defining a
pointer or typedef for a selected datatype from the Built-in Data Type Manager it will be created within the root category of the active program's datatype manager.


Structures can also be created directly in the [Listing](../CodeBrowserPlugin/CodeBrowser.md#listing-view) view. See [creating structures in
the Browser](../DataPlugin/Data.md#structure) for details.


### Renaming a Data Type


Right-click on the data type to be renamed. Select the ***Rename*** action and
then type in the new name in the in-place text edit box.


### Editing a Data Type


Only structures, unions, enums and functionDefinitions can be edited. To edit one of
these data types, either double-click on its node or right-click its node and select the
***Edit*** action. For structures and unions, the [structure
editor](../DataTypeEditors/StructureEditor.md) will appear, and for enums the [enum editor](../DataTypeEditors/EnumEditor.md) will appear.


> **Tip:** To edit a data type from anywhere
in the tool, you can activate the global Edit Data Type action from the
keyboard by pressing Ctrl-Shift-D .  This will present you a Data Type Chooser
Dialog that you can use to choose a type to edit.


### Creating a new Enum from a Selection of Enums


Select two or more existing enums. Select the ***Create Enum from Selection***
action. A dialog will appear asking you for the new enum's name. This name must be unique
or you will be prompted to enter a unique name. The resulting enum will contain a
combination of all names and values from the selected enums. NOTE: If more than one of
the same value is contained in the enums, they will all be added to the new enum.
However, only the first one entered will be applied when this enum is used. If more than one
entry with the same name is contained in the selected enums, any extras with the same value will
be ignored and any with different value will be given a new name consisting of original name appended
with as many underscores needed to make it unique. A comment will be added so users know which ones
had names modified to allow the addition of the entry.


### Deleting a Data Type


Right-click on the category to be deleted. Select the ***Delete*** action. A
confirmation dialog will appear since **this action cannot be undone** (unless its in
the program's archive)


### Moving a Data Type


Data types can only be moved within the same archive. Attempts to move data types
across archives are converted to a copy action. There are two ways to move a data
type:


| 1. **Drag-N-Drop** | Click on the data type to be moved and drag it                 onto its new parent category. |
| --- | --- |
| 2. **Cut/Paste** | Right-click on the data type to be moved and                 select the *Cut* action. Next, right-click on the destination parent                 category and select the *Paste* action. |


### Copying a Data Type


Data types can be copied within an archive or from one archive to another, but the
behavior of the copy is very different for the two cases. When copying within an archive,
the behavior is more natural. A copy of the source data type is placed inside the
destination category. However, copying from one archive to another behaves somewhat
unusually. In this case, the destination folder is only relevant as to which archive is
the recipient of the copy. After the copy, the destination archive will contain the
copied data type. However, any data types contained by the copied data type are also
copied to exactly the same relative (to the root category node) category paths as the
source archive. There are two ways to copy a data type:


| 1.Drag-N-Drop | Click on the data type to be moved and copy drag                 (hold the `<Ctrl>` key while dragging) it onto its new parent category. |
| --- | --- |
| 2.Copy/Paste | Right-click on the data type to be moved and                 select the *Copy* action. Then right-click on the destination parent                 category and select the *Paste* action. |


### Committing Changes To Source Archive


If changes are made to a data type that has an association with a source archive, those
changes must be applied (*committed*) to the original
in the source archive as well to keep the data types in sync. Right-click on the data type
to be committed. Select the **Commit To Archive** action
and the changes will be applied back to the source archive.


### Updating Data Types From Source Archive


If changes are made to a data type in a source archive that has associated data types in
a client archive (another archive or the program), the data type in the client archive can
be *updated* from the source archive. Right-click on
the data type to be updated. Select the **Update From
Archive** action and the changes will be applied from the archive.


### Reverting Changes


If changes are made to a data type that has an association with a source archive, that
data type is now different from its source data type. Those changes can be thrown away and
the data type can be *reverted* back to its original
state. Right-click on the data type to be reverted and select the
**Revert** action and the changes will be removed.


### Disassociate a Data Type


To remove a data type association with a source archive, right-click on the data type in
the client archive (another archive or the program) and select the
**Disassociate From Archive** action. The data type will become a
local data type within the client archive and any changes to it will not affect the
original data type in the source archive.


### Associate a Data Type with a Source Archive


Whenever a data type is applied to a program, or dragged to a category under the
program's node in the data type manager tree from a file or project archive, a copy of that
data type is created in the program. Also, an association back to the original data type is
created. That is the normal case and it is designed to be fairly intuitive. Less intuitive
is when a data type is originally created in a program and then is shared by dragging a
copy to an archive. Since programs cannot be the source for a data type, a dialog is
displayed asking the user if they want an association to be created. If the user answers
yes, an association is created, but the archive will become the source and the program's
data type is the one that gets the association. In other words, it appears as if the data
type were created in the archive and copied to the program.


### Replacing a Data Type


A data type can be replaced by another data type. This means that every occurrence of
the original data type in a program is replaced by the new data type and the original
data type is deleted. To replace a data type, right-click on the type to be replaced
and select the ***Replace Data Type...*** action.  This will show a
[dialog](../DataTypeEditors/DataTypeSelectionDialog.md) that allows
you to choose the replacement data type.


### Setting Favorite Data Types


Data types can be marked as *favorites* such that they show up in the **[Data](../DataPlugin/Data.md#favorites)** option menu and the **[Set Data Type](../FunctionPlugin/Variables.md#define-variable-data-type-or-function-return-type)** popup action menu in the
Browser. This is a quick way to apply a data type to the Program. The default Code
Browser has most of the well-known types in the ***BuiltInTypes*** category
marked as a favorite.


To make a favorite, right-click on the data type and select the ***Favorite***
action. Favorite data types are marked with the ![emblem-favorite.png](../icons/emblem-favorite.png) icon.


![](images/FavoriteDts.png)


To remove a favorite, right-click on the data type and deselect the
***Favorite*** action.


> **Note:** The favorites are identified by
name and must be unique, so you cannot have data type "fred" in one "categoryA" marked as
a favorite and "fred" in "categoryB" also marked as a favorite.


> **Tip:** Any data type from any archive
type (Program, BuildInTypes, or archive) can be marked as a favorite and used as such,
however, only those marked in the BuiltInTypes category will be saved as
part of your tool's state when you close the Project or exit Ghidra. Your list of
favorites is restored when you re-open your project or restart Ghidra.


### Pointer-Typedef Settings


On occasion there may be the need to add stipulate additional attributes on a pointer
type to stipulate how the associated pointer should be interpreted or processed during analysis.
Such pointer attributes may only be specified when such a pointer in the form of a Typedef
which enables the datatype to preserve these attributes during type resolution and propagation.
This includes preservation of such Typedef Settings within a data type archive, and through
merge processing, which normal Data Settings do not support.


The Typedef Settings may be modified via the Settings dialog in the same way data type Default Settings
are changed for listing Data (see [Changing Default Settings for Data](../DataPlugin/Data.md#changing-data-settings)).
In addition to this popup action on listing Data, the dialog may be displayed from the *Data Type Manager*
tree by right-clicking on a data type and selecting the **Settings...** action.  Typedef-specific settings
are only supported as default settings for a typedef and may not be overridden at the component or data level.


The following Pointer-Typedef settings are currently supported:


- **Address Space** (case-sensitive string) - Allows a specific address space to be associated with a pointer.
If an unknown name is used it will be silently ignored. Auto name attribute format: __((space(*name*))
- **Component Offset** (signed value) - Allows a base-relative offset to be specified.  When applied
to memory an Offset Reference will be generated.  I addition, type analysis may use the offset to identify
a component relative to the pointer's base-datatype (e.g., structure).  Auto name attribute format: __((offset(*signed_value*))
- **Offset Mask** (64-bit mask) - Allows a bit-mask to be applied to a stored value when computing the
absolute memory offset.  This bit-mask will be applied prior to any applied bit-shift.  Auto name attribute format: __((mask(*hex_mask*))
- **Offset Shift** (-64..0..64) - Allows a bit-shift (left=negative, right=positive) to be applied to a
stored value when computing the absolute memory offset.  Auto name attribute format: __((shift(*bitshift_amount*))
- **Pointer Type** (*default, image-base-relative, relative, file-offset*) - allows the overall interpretation of a
pointer to be specified.  The *relative* pointer type has limited applicability and is only
intended to be applied to pointers stored in memory since their storage location is used in computing
the absolute address that the pointer refers to.


> **Note:** All Typedef Settings must be established on
a Typedef before such a type is applied to Data or referenced by other types.  This is highly recommended
since the side-affects of using such a modified typedef will not be updated to reflect subsequent changes.


> **Note:** Full support for the above Pointer-Typedef
Settings within analysis and decompilation will evolve over time.  We also hope to improve
naming concerns for such typedefs and to replace the use of custom BuiltIn data types which would
be better modeled as a Pointer.


*Provided by: *DataTypeManagerPlugin**


**Related Topics:**


- [Data Types](../DataPlugin/Data.md#data-types)
- [Edit Plugin Path](../FrontEndPlugin/Edit_Plugin_Path.md)
- [Apply Data Types](../DataPlugin/Data.md#applying-data-type)
- [Edit Structure](../DataTypeEditors/StructureEditor.md)


---

[← Previous: Categories](data_type_manager_description.md) | [Next: Managing Archives →](data_type_manager_archives.md)
