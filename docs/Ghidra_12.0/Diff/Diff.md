[Home](../index.md) > [Diff](index.md) > Program Differences

# Program Differences


The Code Browser can be used to view a second program alongside the
tool's program to determine the differences between them. This is
called a Program Diff. The Program Diff highlights code units in the
second program to indicate there is a difference. Highlighted code
units in the second program can then have their differences applied to
the tool's program causing it to change. The ultimate goal is to apply
some or all of the differences from the second program to the tool's
program in order to get another user's changes into your program.


## Opening and Closing the Diff View


The **Open/Close Diff View** icon
![table_relationship.png](../icons/table_relationship.png)
in the Code Browser tool bar is used for both opening and closing
a second program in the Code Browser Diff panel. This is one of two ways to open the Diff
tool. The other is the menu action, Tools
**→
Program Differences...**
which is described later under **Viewing Program Differences**.


**Opening**

When there is only a single program displayed in the Code Browser,
select the Open Diff View icon
![table_relationship.png](../icons/table_relationship.png)
in the tool bar above the program to open a program for Diff.
You will be prompted to select the second program and then prompted
for Diff settings just as when
[viewing program differences](#viewallprogramdifferences)
.


**Closing**

When you are done working with program differences and the second
program, select the
![table_relationship.png](../icons/table_relationship.png)
icon in the tool bar above the second program. The second program
and the associated Diff are closed and the Code Browser returns to
displaying only the tool's program.


**Bring Diff View to Front**

If you navigate away from the current diff session to another program tab, then
clicking the ![table_relationship.png](../icons/table_relationship.png) action will
make the diff session be the active program tab.


## Viewing Program Differences


A Diff can be opened from the menu action, Tools
**→
Program Differences...**. This is one of two ways to open the Diff
tool. The other is the **Open/Close Diff View** icon
![table_relationship.png](../icons/table_relationship.png)
in the Code Browser tool bar which is described above in **Opening and Closing the Diff View**.
The following describes using the menu action to open the Diff tool.


With a program open in the Code Browser tool, do the following to
view a second program's differences.


1. From the Code Browser, select
Tools
**→
Program Differences...**
.
2. The *Select Other Program* dialog is displayed.


![](images/SelectOtherProgram.png)


1. From the *Select Other Program* dialog select the second
program to be viewed and compared with the tool's program.
The second program must have the same address spaces
defined. In other words, they should be the same type of program
(i.e. based on the same program language).
If you wish to Diff against a specific version of a
**versioned program**, a specific version may be selected from the
**Version History** table.  The project file history panel is displayed
when the **History&gt;&gt;** button is clicked.
Select the versioned program from the tree.
Next select the desired version of the program from the **Version History**
table on the right side of the dialog.
![](images/SelectOtherVersionedProgram.png)
If you wish to Diff against another program which is already open in the same tool
you can select a compatible program from the **Open Programs** tab.  Programs
which are not compatible (e.g., different architecture) are not shown in the table.
The **Open Programs** tab is not available if compatible open programs are not
found.  You may return to the project file tree selection panel by clicking the
**Project Files** tab.
![](images/SelectOpenProgram.png)
2. Click the **OK** button.
3. The *Determine Program Differences* dialog is displayed.
This dialog is displayed whenever you are going to determine the
differences between two programs. To get all the differences
between the two programs make sure all the check boxes in the
**Do Differences On** area have checks and the check box in the
**Address Ranges To Diff**should not have a check as shown here.


![](images/DetermineDiffs.png)


The check boxes allow you to limit the types of differences that are
determined and where differences are determined in the program.
To learn more, see
[Determine Program Differences Dialog](#get-differences).


1. Click the OK button to determine the differences.
2. An *In Progress* dialog appears while the differences are
being determined. Upon completion the dialog disappears and the code
unit's in the second program where differences exist will be
highlighted.


> **Note:** The selected program is displayed as the second program in
the browser. Only the portion of the second program that matches the
address set of the current view is displayed. Highlighted code units in
the second program indicate where there are differences.


The following illustrates a Program Diff where differences between
two programs are highlighted.


![](images/Diff.png)


> **Tip:** The tool's program, that will be modified by the Diff, is
displayed on the left-hand-side of the Code Browser.
The second program, where the differences to apply are obtained, is
displayed on the right-hand-side. Markers in the right margin of the
second program give an indication of all the positions in the current
view where there are differences between the two programs. The view of
both programs is still controlled by the program tree for the tool's
program. In other words, the second program's view will only show
addresses that match those viewed for the tool's program. Notice that the difference highlights are light orange above. The selected
difference is green. These are only the default colors. They can be
changed from the tool's Options dialog ( Edit O ptions... , open the Listing Fields folder,
and select Selection Colors , double click on the Difference color).


Blank space is added to each program as necessary to align the
addresses between the two programs. The vertical or horizontal
scrollbar of either program causes both programs to scroll in a
synchronized manner. Also, changing the cursor location in one program,
changes it in the other program.


The Program Diff colors the two programs where they differ. These
differences can then be applied individually from the second program to
the tool's program. Applying a difference changes the tool's program so
it matches the second program where it was different previously. The
ultimate goal is to apply some or all of the differences from the
second program to the tool's program.


Program Diff is most commonly used to compare different users' copies
of the same program. With versioned programs, it can also be used to
determine differences against an older version of the same program.
When working on a project as a team, each person can make changes to
his own copy of a program file. The Program Diff can then be used to
determine where the programs differ. Changes that another team member
has in his program can be merged into yours by applying the difference.


The **toolbar** above the displayed programs provides buttons
for use with a Program Diff. Click on the icon below to go to the help
section that gives details of that feature.


| [![pencil16.png](../icons/pencil16.png)](#Apply_Differences) | Apply the selected differences from the second program to the tool's program. |
| --- | --- |
| [![pencil_arrow16.png](../icons/pencil_arrow16.png)](#Apply_Differences_and_Goto_Next_Difference) | Apply the selected difference and go to the next highlighted difference block.   |
| [![eraser_arrow16.png](../icons/eraser_arrow16.png)](#Ignore_Selection_and_Goto_Next_Difference) | Ignore the selected differences and go to the next highlighted difference block. |
| [![xmag.png](../icons/xmag.png)](#Show_Diff_Location_Details) | Show the details of the differences between the programs at                the current cursor location. |
| [![down.png](../icons/down.png)](#Next_Difference) | Go to the next highlighted difference block. |
| [![up.png](../icons/up.png)](#Previous_Difference) | Go to the previous highlighted difference block. |
| [![settings16.gif](../icons/settings16.gif)](#Show_Diff_Apply_Settings) | Display the Program Difference Settings dialog. |
| [![Diff16.png](../icons/Diff16.png)](#Get_All_Differences) | Determine the differences between the programs. |
| [![table_relationship.png](../icons/table_relationship.png)](#Open_Close_Diff_View) | Open/Close the second program and the Program Diff. |


---


## Determine Program Differences Dialog


Whenever you initiate a Program Diff the *Determine Program
Differences* dialog allows you to control the following settings:


- [Do Differences On](#executediffdialog-dodifferenceson)
: the types of differences to be determined and
highlighted by the Program Diff. The **Select All** button is a
convenience for selecting all of the check boxes for difference types.
Likewise, the **Deselect All** button removes the check marks from
all the difference type check boxes.
- [Address Ranges To Diff](#executediffdialog-addressrangestodiff)
: indicates the addresses to be checked for differences.
- [Limit To Selection](#executediffdialog-limittoselection)
: whether or not the Program Diff should be
limited to the current selection in the tool's program.


![](images/DetermineDiffs.png)


Pressing the **OK** button will check the indicated addresses
for differences. It then highlights the code units in the second
program where differences were found. While the Program Diff is
determining the differences, an *In Progress* dialog is displayed.
Pressing the **Cancel** button will remove the *Determine Program Differences*
dialog without performing the Program Diff.


> **Tip:** If the two programs being compared are large, determining
program differences can be time consuming. If you are not interested in
all of the differences in the program, you can reduce the amount of
time required to determine differences by removing some types of
differences being determined or by determining differences on just a
portion of a program.


### Do Differences On


The **Do Differences On** area specifies the types of
differences that will be determined. Placing a check in a box indicates
that this type of difference should be detected.


**Bytes**- detect any code units that have memory bytes
that differ between the programs being compared.


**Labels** - detect any code units where the labels differ.


Possible label differences are:


- More labels at a code unit in one program than the other
- Labels named differently
- Different labels could be marked as the primary label
- Same named label, but with different scope (parent namespace).
For example, one program's label is local to a function and the
other label is a global label.
- Same named label, but with different source. For example, one
program's label was named by default and the other label
was named by the user.
- One program's code unit with a label could be an entry
point and the other program code unit is not an entry point


**Code Units** - detect any code units where the code unit or
equates differ.


Possible code unit differences are:


- Different instructions.
- Instruction in one program and Data in the other program at
the same address.
- Different equates on the instruction in each program.
- Different data types when data is defined in both programs
at an address.


**References** - detect any code units where the references differ.


Possible reference differences are:


- One program has a reference and the other doesn't.
- References are not to the same address.
- References are not on the same operand or mnemonic.
- References types (Memory, Stack, External) are different.


> **Note:** Program Context - detect any code units where the values
of the program context registers differ. If the two programs contexts don't have the same registers
defined, the program context is disabled and can't be compared between
the programs.


**Comments** - detect any code units where the comments differ.


Possible comment types are:


- End of Line Comment
- Pre-Comment
- Post-Comment
- Plate Comment
- Repeatable Comment


The difference could be that a comment exists in one program
and not the other. It could also be that the text of a particular
comment type is not exactly the same for the two programs.


**Bookmarks** - detect any code units where bookmarks differ.


**Properties** - detect any code units where User Defined
Properties differ.


**Functions**
- detect any code units where the functions differ.


Possible differences are:


- Function in one program and not in the other.
- Function comment differs.
- Addresses that make up the function body differs.
- Function signature differs. (Function name, return type, or
parameters differ.)
- Parameters differ by name, data type, size or offset.
- Local variables differ by name, data type, size, or offset.
- Stack offset differs.
- Stack Frame size differs.
- Whether or not the stack grows in a negative direction.
- Function tags differ.


**Source Map**
- detect any addresses where the source map information is different.


When the *Determine Program Differences* dialog is initially
displayed, all the Differences check boxes are checked. This indicates
that all the types of differences will be detected and displayed.


### Address Ranges To Diff


The **Address Ranges To Diff** area indicates the address
ranges where program differences will be determined. If the two
programs have different address sets, then only the addresses that
the two programs have in common can be compared. The addresses
where differences are determined can also be limited to a set of
addresses that are selected in the tool's program.


#### Limit To Selection


If there is a selection in the tool's program when you determine
differences, the address set where differences are determined can be
limited to the addresses in the selection. Selecting the
**Limit To Selection** box,
limits the differences to the selection's addresses.


---


## Diff and Multiple Program Tabs


Only one Program Diff can be performed at a time. However, you can
view another program using the tabs in the
[Listing View](../CodeBrowserPlugin/CodeBrowser.md)
while a Program Diff is active. This will not terminate the current
Diff. The Diff will reappear when you change back to the tab for the program
that the Program Diff is being performed on.


While a Program Diff is active, the **Diff View**
icon ![table_relationship.png](../icons/table_relationship.png)
is visually pressed down. If the Diff is being performed on a
program that is not being actively displayed (in a tab other than the
current tab), then pressing the **Diff View** icon
![table_relationship.png](../icons/table_relationship.png) will bring the tab
containing the Diff to the front.

If you attempt to start a Diff using **Tools**
→  **Program Differences...**
in the tool menu and a Diff is already being performed, the status bar
will indicate the name of the program that currently has a Diff.


A Program Diff is terminated by any of the following:


- Selecting the **Diff View** icon
![table_relationship.png](../icons/table_relationship.png) from the
Listing toolbar when the Program Diff is actively being displayed.
- Selecting the **Close Window** icon
![](../shared/close16.gif) from the
Listing toolbar when the Program Diff is actively being displayed.
(Normally this will close the current program, but when Diff is active
this closes the Diff.)
- Closing the Diff's program via the Tool's menu, **File**
→ **Close**,
when the Diff is actively displayed. (In this case the Diff is closed
along with the current program.)
- Exiting the Tool or Ghidra will also terminate an active Diff.


> **Note:** Hovering the mouse over the Diff View icon provides a tooltip
indicating whether the current action is Open Diff View , Close Diff View , or Bring Diff View to Front .


---


## Diff Apply Settings


The *Diff Apply Settings* dockable component allows you to
control which types of differences get applied from the second program
to the tool's program, and how each type gets applied.


For each type of difference, you can select one of the
following apply settings:


- **Ignore**- do not change the selected code units in the
tool's program for this type of difference.
- **Replace**- changes the tool's program to match the second
program for this type of difference.
- **Merge**-
(Only available for Labels and Comments) changes the tool's program by
adding this type of difference from the second program to what is
already in the tool's program. For Labels, this will not change which
label is set to primary.
- **Merge & Set Primary**
- (Only available for Labels) merges labels from program 2 into the current
program and sets the primary label as it is in program 2, if possible.


![](images/DiffApplySettings.png)


The following types of differences are controlled by the
*Diff Apply Settings*.


**Bookmarks** - all categories of bookmarks.


**Bytes**


**Code Units** - includes code units
(**instructions** & **data**)
and **equates**.


**Comments** - **Plate, Pre, End-of-line, Repeatable, &
Post** comments.


**Functions** - functions
(includes their associated stack frames).

**& Function Tags**


**Labels** - labels or symbols.


**Program Context** - program context **register** values.


**Properties** - user defined properties that have been added
to the program by plugins.


**References** - **Memory, External, & Stack** references.


The
*Diff Apply Settings* toolbar has a **Save as Default** icon
![disk.png](../icons/disk.png) to save your
current Diff Apply Settings to the tool as your new defaults. When you
select it, the current *Diff Apply Settings* values are set to
the default Diff Apply Settings. Whenever you start a new Diff, the
current *Diff Apply Settings*
will get set to the default settings for that Program Diff. If you determine
the program differences again for an existing Diff using the **Determine
Program Differences** icon ![Diff16.png](../icons/Diff16.png)
, the current *Diff Apply Settings* will not be affected by the
defaults.


The Default Diff Apply Settings can also be set by changing the
[Diff Default Apply Settings tool options](#diffapplysettingstooloptions)
.


The *Diff Apply Settings* toolbar menu
![menu16.gif](../icons/menu16.gif) also has actions for changing
all the apply settings at once. They are:


![](images/DiffApplySettingsPopup.png)


- **Set Ignore For All Apply Settings** - Changes all the settings
to **Ignore**. Before you can apply anything you would need to
individually set at least one difference type's setting to
**Replace** or **Merge.**
- **Set Replace For All Apply Settings** - Changes all the
settings to **Replace**.
- **Set Merge For All Apply Settings** - Changes all the
settings to **Merge** that allow merging and all others are changed
to **Replace**. Labels will be set to **Merge & Set Primary**.


---


## Getting New Differences


There are several reasons to get new program differences.


- Changes were made to the tool's program directly (not by
applying a difference) since you last determined program differences.
- The second program has been changed since you last determined
program differences.
- You want to determine differences for different addresses of
the program than the current Diff used. For example, you initially
determined program differences limited to a selection and now you want
to know differences for the whole program or for a different set of
selected addresses.


When a second program is already displayed in the Code Browser
tool, do the following to determine new program differences between
that program and the tool's program.


1. From the toolbar above the second program, select
the Get Differences ![Diff16.png](../icons/Diff16.png) button.
or
Press the right mouse in the second program area. From the
popup menu, select **Get Differences...**.
2. The *[Determine Program Differences](#get-differences)*
dialog is displayed.
3. From the dialog, select the types of differences to be
determined and the addresses to check for differences.
4. Click the **OK** button.


An *In Progress* dialog appears while the program
differences are being determined. When it is done determining the
differences, the dialog is removed and the differences are highlighted
in the second program.


## Limiting the Diff to the Browser Selection


The **Limit to Selection** box in the *Program Difference
Settings* dialog can be selected whenever a Program Diff is started
while there is a selection in the tool's program in the Code Browser.
When the box is checked the differences will only be determined for
addresses in that selection. This limits the differences being highlighted
and manipulated by the Program Diff to only those that are in a specific
set of code units in the program. To limit the Program Diff select the
target code units in the tool's program in the browser and check the
**Limit to Selection**
check box in the *Program Difference Settings* dialog. Notice
that the **Address Ranges To Diff** area changes as you check or
uncheck the **Limit to Selection** box. It switches between the
addresses in common between the two programs and those in the selection.


> **Note:** Once you press the OK button on the Program
Difference Settings dialog, the Program Diff is performed against
the indicated address ranges (address set). You can make a selection in
the tool's program before initiating the Get Differences to
get differences against a different address set.


## Navigating Differences


When viewing program differences in the CodeBrowser, you can
navigate on difference blocks. A difference block is a contiguous group
of one or more highlighted code units in the second program. A difference
block can be a single code unit where a difference was found if the code unit
before and after it did not have a difference. There can be multiple code units
in a difference block when each of the code units next to each other has a
difference. To move to the next/previous code unit in a highlighted block use
the up and down arrow keys on the keyboard or click the mouse on the desired code unit.


### Next Difference


Selecting the **Next Difference** button
![down.png](../icons/down.png) moves the
current location in the Program Diff to the next difference block.


If only part of the program is in the current view, the next
difference may be outside the current view of the program. If this is
so, then navigating will add the fragment, with the next difference, to
the view.


### Previous Difference


Selecting the **Previous Difference** button
![up.png](../icons/up.png) moves the current location in
the Program Diff to the previous difference block.


If only part of the program is in the current view, the previous
difference may be outside the current view of the program. If this is
so, then navigating will add the fragment, with the previous
difference, to the view.


### Marker Margin


Clicking on a difference marker in the right margin will
navigate to that difference.


> **Tip:** Some of the difference markers may overlap in the right margin.
Therefore, it is best to use the markers for navigation to a
region where there are differences and then use the Next Difference or Previous Difference buttons
to navigate to the next/previous difference block.


## Selecting Differences


### Automatically Selecting a Difference Block


Using the **Next Difference**
![down.png](../icons/down.png) or **Previous Difference**
![up.png](../icons/up.png) to navigate to a highlighted
difference block selects the code units contained in that
difference block. Left mouse clicking on a difference block also causes the entire
difference block to become selected. You can then right mouse click and the
popup menu appears so you can apply the selection.


### Manually Selecting Differences


Differences can be selected within the right-hand Diff listing as follows:


- To select a single difference block, simply left mouse click on the highlighted
difference block. It will become selected, so it can then be applied.
- Left mouse clicking on a code unit that is not highlighted as part of a difference
block will clear the current Diff selection.
- To select individual code units within a highlighted difference
block, drag the cursor in the second program as you normally would in
the Code Browser. If you select code units that are not highlighted as
a difference, they will automatically be removed from the selection
when the mouse button is released. When the cursor is released, the
selection will become restricted to only the
code units with highlighted differences in the selection.
- The Ctrl key along with a left mouse click can be used to add/remove a code unit
from the selection.
- The Shift key along with a left mouse click can
be used to extend the selection.


> **Tip:** When differences are applied from the second program to
the tool's program, only selected code units in the current view will
be applied.


### Select All


Invoking the **Select All Differences** from the second
program's popup menu, selects all the currently highlighted differences
in the second program.


### Setting the Program Diff Selection From the Tool's Program Selection


The selection from the tool's program can be used to select some
of the differences in the second program. While viewing program
differences in the Code Browser, make a selection in the tool's
program. Select the **Set Diff Selection** icon
![DiffSelect16.png](../icons/DiffSelect16.png) in
the tool bar above the tool's program. The selection in the second
program will become any highlighted differences in the second program
that correspond to the selected code units in the tool's program.


For example, you can use this to select all the differences in a
subroutine. First select all the code units in the tool's program
that make up the subroutine. The **Set Diff Selection** icon
![DiffSelect16.png](../icons/DiffSelect16.png) will become
enabled. Select the **Set Diff Selection** icon
![DiffSelect16.png](../icons/DiffSelect16.png). All the
corresponding code units with highlighted differences in the second
program become selected. The selection of differences can then be
[applied](#apply-differences) or
[ignored](#ignore-selection-and-goto-next-difference).


## Applying Differences


Applying a difference, changes the tool's program to match the
second program in the Program Diff for each type of difference being
applied. The Program Diff can control which types of differences get
applied from the second program to the tool's program
(see [Apply](#diff-apply-settings)). It can also control
whether some types of differences replace what is in the tool's program
or whether they are merged into the tool's program. Only the highlighted
code units in the second program, which are currently selected, can have
their differences applied.


### To apply a selection


1. Select Differences in the second program.
2. Make sure the difference types you want to apply have their
boxes checked in the *ProgramDiff Settings* dialog.
3. Click the **Apply Selection** button
![pencil16.png](../icons/pencil16.png) in the toolbar.
or
Press the Apply Selection hot key.
or
Click the right mouse on the highlighted difference and select the
**Apply Selection**button.


Remember all the types of differences that are being **Replaced**or
**Merged**in the [*Diff Apply Settings*](#diff-apply-settings)
dockable component will be applied for the selected code units.


When applying differences, comments and labels can be replaced
with the second program's comments or merged with them. Merging comments
or labels in the Program Diff results in the union of the two programs
comments or labels for each code unit being applied.


### Example:


A code unit in the tool's program does not have any comments or
labels. The code unit in the second program has a pre-comment and a
bookmark. All Apply boxes are checked. Apply a selection containing the
code unit. The pre-comment and bookmark appear in the program in the
Code Browser.


Say the Bookmarks box in the Apply area of the settings dialog was
not checked and the Comments box was checked when the difference was
applied. The pre-comment would appear in the Code Browser's program,
but the bookmark would not.


## Applying Differences and Going To Next


This applies the selected differences and navigates to the next difference
in a single step (see [Apply](#apply-differences) and
[Next](#next-difference)). It can also control whether some
types of differences replace what is in the tool's program or whether they
are merged into the tool's program. Only the highlighted code units in the
second program, which are currently selected, can have their differences applied.


### To apply a selection and go to the next difference


1. Select differences in the second program.
2. Make sure the difference types you want to apply have their
boxes checked in the *Diff Apply Settings* dockable component.
3. Click the **Apply & Go To Next** button
![pencil_arrow16.png](../icons/pencil_arrow16.png) in the toolbar.


All the types of differences that were last selected under Apply
in the *Program Difference Settings* dialog will be applied for
the selected code units. The Diff will then navigate to the next
difference and select it.


## Ignoring Differences


Ignoring a difference indicates you no longer want the current
Program Diff to highlight the code unit. The Diff then navigates to the next difference.


Only selected code units in the second program of the Program Diff
can have their differences ignored. The selection can be made on an
entire highlight block or individual code units in one or more
difference blocks.
(See [Selecting Differences](#selecting-differences)).


Note: All versions of Ghidra before 7.4.*X* did not navigate to the next difference after ignoring.


### To ignore a selection


1. Select Differences in the second program.
2. Click the **Ignore Selection** button
![eraser_arrow16.png](../icons/eraser_arrow16.png) in the toolbar.
or
Press the Ignore Selection hot key.
or
Click the right mouse on the highlighted difference and select the
**Ignore Selection**button.


The selected code units will be ignored. This means they will no
longer be highlighted as a difference. The Diff will then navigate to the next difference and select it.


> **Note:** Once a code unit is
ignored, it will no longer be marked
in the browser with a change bar and will no longer be highlighted. If
you Determine Program Differences, any previously ignored items where
there are still differences will once again be highlighted.


## Viewing Difference Details at a Location


When viewing two programs in the Code Browser, it is possible to
view all the differences at the current program location. The *Diff
Details* dockable component displays details indicating
differences, if any, between the two programs code units at the current
program location.


To view the difference details at a location:


1. Click on the code unit of interest to set the location and
select the **Location Details** button
![xmag.png](../icons/xmag.png) in the tool bar.
or
Press the right mouse button on the code unit of interest and select
the **Location Details** button.
2. The *Diff Details* dockable component is displayed
indicating the detailed differences, if any, at the indicated location.


The following image shows the *Diff Details* dockable component.
In Program 1 of the Diff "MyLabel" is a global label,
whereas in Program 2 "MyLabel" is a local function label.


![](images/DiffDetails.png)


> **Note:** When the Automatically Update Details check box is
selected, the Diff Details will update automatically to show the
differences at the current location whenever the current address
changes. This can be useful when you are navigating through
Differences and need to see details that are not displayed
by the CodeBrowser.


> **Note:** When the Only Show Expected Difference Types check box is
selected, the Diff Details will only show Diff Details for the types
of Differences that you chose to look for when you determined your differences.
If this box is not checked, you will see all types of differences that exist at
the location regardless of whether it was one of the types of differences you were
seeking.


> **Note:** If you modify the program at the current location after the Diff
Details are displayed, press the Refresh button in the local toolbar to update the difference details. This will
recompute the differences and then redisplay them.


### Why view the difference details at a particular program location?


- The code units appear different between the two programs,
but are not highlighted.
- If a particular type of difference was not selected when
differences were determined, then it will not get highlighted.
- If the thing that appears different is due to a difference
elsewhere in the program, then it will not get highlighted. For
example, XREFs are not a difference where they are shown. The code unit
where the reference is from is different, not where the reference is
to. The XREF is displayed on the code unit the reference is to.
- The code units appear the same between the two programs, but
are highlighted. This can happen when there is something different
about the code unit, but that thing is not displayable. For example,
references are not visually displayed, but they are a valid difference
at the code unit the reference is from.
- The location is highlighted, but you want to know exactly
what is different here.


In other words, are there other types of differences here besides
the boxes I checked in the *Program Difference Settings* dialog?
Remember, only the difference types with their Apply boxes checked in
the dialog will be applied if an *Apply Selection*is done.


## Diff Apply Settings Tool Options


The Program Diff adds **Default Apply Settings** options to
the tool. To view or edit the option settings:


- From the tool's menu select **Edit**
→
**Tool Options...** which displays the
[Tool Options Dialog.](../Tool/ToolOptions_Dialog.md)
- Open the *Diff* tree node.
- Click on the *Default Apply Settings* tree node to view its options.


Each time a new Program Diff begins, the *Diff Apply Settings*
will have their values set to the default ones specified by the
*Default Apply Settings Options*.


Each option will have one or more of the following settings available:


| Diff Apply Setting   | Functionality   |
| --- | --- |
| Ignore   | Do not change the selected code units in the                   tool's program for this type of difference.   |
| Replace   | Change the selected code units in the                   tool's program to match the second                   program for this type of difference.   |
| Merge   | (Only available for Labels, Comments and Function Tags.)                   Change the selected code units in the tool's program by adding                   this type of difference from the second program to what is                    already in the tool's program. For Labels, this will not change                    which label is set to primary.   |
| Merge & Set Primary   | (Only available for Labels.) Merges labels from the second                    program into the tool's program for the selected code units                    in the Diff and set the primary labels as in the second                    program, if possible.   |


The *Default Apply Settings Options*
contains the following options:


| Option | Functionality   |
| --- | --- |
| Bookmarks | Controls whether bookmark differences will be applied.                    Can be: *Ignore* or *Replace* .   |
| Bytes   | Controls whether byte differences will be applied.                    Can be: *Ignore* or *Replace* .   |
| Code Units   | Controls whether instruction, data, and equate differences will be applied.                    Can be: *Ignore* or *Replace* .   |
| End Of Line Comments   | Controls whether end of line comment differences will be applied.                    Can be: *Ignore* , *Replace* , or *Merge* .   |
| Functions   | Controls whether function differences will be applied.                    Can be: *Ignore* or *Replace* .   |
| Function Tags   | Controls whether function tag differences will be applied.                    Can be: *Ignore* , *Merge* or *Replace* .   |
| Labels   | Controls whether label differences will be applied and                    which to set as the primary label.                    Can be: *Ignore* , *Replace* , *Merge* , or *Merge & Set Primary* .   |
| Plate Comments   | Controls whether plate comment differences will be applied.                    Can be: *Ignore* , *Replace* , or *Merge* .   |
| Post Comments   | Controls whether post comment differences will be applied.                    Can be: *Ignore* , *Replace* , or *Merge* .   |
| Pre Comments   | Controls whether pre comment differences will be applied.                    Can be: *Ignore* , *Replace* , or *Merge* .   |
| Program Context   | Controls whether program context register value differences will be applied.                    Can be: *Ignore* or *Replace* .   |
| Properties   | Controls whether user defined property differences will be applied.                    Can be: *Ignore* or *Replace* .   |
| References   | Controls whether reference differences will be                   applied. Can be: *Ignore* or *Replace* .   |
| Repeatable Comments   | Controls whether repeatable comment differences will be applied.                    Can be: *Ignore* , *Replace* , or *Merge* .   |
| Source Map   | Controls whether Source Map differences will be applied.                    Can be: *Ignore* (the default) or *Replace* .   |


To change an option, click on the combo box to the right of the
option name and select the desired setting from the list.


## Problems/Limitations


You cannot undo an **Ignore Selection** ![eraser_arrow16.png](../icons/eraser_arrow16.png) action. Undo of an
**Apply Selection** or **Ignore Selection** in a Program Diff currently can't
re-highlight the code units with differences that were ignored. If you want to get
back differences after undo of an **Apply Selection** ![pencil_arrow16.png](../icons/pencil_arrow16.png) or if you want all ignored
differences to no longer be ignored, you must re-Diff the programs by selecting the
**Get Differences** button ![Diff16.png](../icons/Diff16.png).


*Provided by: *Program Diff* Plugin*


**Related Topics:**


- [Code Browser](../CodeBrowserPlugin/CodeBrowser.md)


---

[← Previous: Configuration Options](../CodeBrowserPlugin/CodeBrowserOptions.md) | [Next: Debugger →](../Debugger/Debugger.md)
