[Home](../index.md) > [VersionTrackingPlugin](index.md) > Common Problems

# Version Tracking Workflow


The goal of this document is to help users understand not only the basic process of
Version Tracking, but also how and when to use the myriad of methods for tweaking that process to
produce results tailored to individual user needs. The list below outlines the sections
available in this document:


1. [Preconditions](#preconditions)
2. [Correlators](#correlators)
3. [Example Work Flow](#example-work-flow-match-all-possible-functions-between-two-binaries)
4. [Workflow FAQ](#workflow-faq)
5. [Common Problems](#common-problems)


## Preconditions


One of the first items you run across in the Version Tracking Wizard is the [Precondition
Panel](VT_Wizard.md#preconditions-panel). This panel is described in more detail as part of the [Version Tracking Wizard Help](VT_Wizard.md).
However, it is also mentioned here as an important initial step in the Version
Tracking process. In the past, users trying to match functions and pull relevant [markup](Version_Tracking_Intro.md#version-tracking-markup-items)
such as labels and comments into a new version of a binary, would encounter problems if one
or both of the binaries were not sufficiently analyzed or had major analysis problems.
Users were given no indication that these issues were a direct result of having a poorly
analyzed binary. The **Precondition Panel** is an indication of how well your binaries
have been analyzed and how well their analyses "match" each other. If this panel indicates
problems, it is important to fix them before moving on or there will probably be problems
with the Version Tracking process. Problems that might be encountered are missing matches
and incorrect matches. In general, Version Tracking will work best if the same methods of
cleaning up a binary are used and if similar numbers of functions are created.


## Correlators


Once a binary has passed the precondition checks, a user must decide which correlator
(Ghidra terminology for a matching algorithm) to use, what part of the binary to run each
correlator on, and what to do with the matches once they are generated. Depending on the
ultimate goal of the Version Tracking user, the work flow might be different. Some users
might want to identify all matching functions and pull over all related markup items as
quickly as possible. Others might want to quickly identify what has changed in the new
binary. Others might want to only run Version Tracking on a select number of items they
care about. The goal of this section is to help users learn how to determine which
correlators best suit their individual needs.


### What Correlator Should I Use First?


One new feature of version tracking is the ability to sequentially run more than one
correlator to find matching code and data and view their results simultaneously in the
same Version Tracking Session. This ability to choose brings up the question of which to
choose first. There are benefits to choosing certain correlators before others. In
general, users should first run correlators that will find obvious matches and allow for
automated matching and markup of a good portion of the destination program.


#### Exact Correlators


Some of these "obvious" correlators are ones that find matches that are unique and the
same in both binaries:


- [Exact Data
Match Correlator](VT_Correlators.md#exact-data-match)
- [Exact
Function Bytes Correlator](VT_Correlators.md#exact-function-bytes-match)
- [Exact
Function Instructions Correlator](VT_Correlators.md#exact-function-instructions-match)


These correlators all report back unique and exact matches so it is almost assured that
the matches are correct. Also, since they are identical in some way (bytes and/or
instructions), the markup items, such as labels and comments, are going to line up
correctly, allowing an automated pull of all markup at once. To automatically accept all
of these items as matches and apply all related markup, the user can do a **CTRL-A**
in the match table after making sure only the exact matches are in the table. Then, click
on the **Apply Markup** ![checkmark_green.gif](../icons/checkmark_green.gif) icon to
accept all the matches and apply all related markup. If the two binaries are very
similar, this can do the majority of the matching very quickly. **It is recommended to
run these three exact correlators in this order before running any other
correlators.**


#### Symbol Match Correlator


Another one of the "obvious" correlators is the [Symbol Match
Correlator](VT_Correlators.md#symbol-name-match-correlators). If you have unique matching symbols there is a high likelihood that the
corresponding functions or data will be a match. However, it is not immediately apparent,
without visiting them individually, whether these matches are exactly the same in both
versions of the binary. The markup items such as labels, comments, data types, and
parameters might not match up exactly so the user should use the **Accept** ![flag.png](../icons/flag.png) icon to accept the matches, then if necessary, individually [visually inspect
and apply the markup items](providers/VT_Markup_Table.md). In some cases, the user might not care about the markup.
For example, if there are no user-generated markup items associated with the match, there
is no reason to do anything other than "Accept" the match. Users might wonder why it is
important to even accept a match for these items. One reason to accept matches, even if
no markup needs to take place, is to help other correlators get better results. Some
correlators use known accepted match information to make their decisions more accurate.
Another reason is to save time. If there is an easy, quick way to identify matches, other
correlators can ignore them and not waste time or memory trying to identify them.


> **Note:** NOTE: It is also a good idea to check for wildly differing lengths between
matches in case there is the case where a wrapper function in one program has the same
name as the actual function in the other program. You can either take care of length
issues before running the correlator by making the length large enough to not include
wrapper functions, or use the resulting match table to inspect for different lengths. An
easy way to do this is to add the Length Delta column in the match table and sort
it. A delta of zero means there is no difference in the lengths. A high delta means there
is a big difference in lengths.


#### Duplicate Exact Correlators


Sometimes binaries will have more than one identical match. This often happens if
there are multiple copies of strings or data in a binary. It also happens in functions
that have the exact same instructions but different parameters. There are three
correlators that find duplicate matches. These are:


- [Duplicate
Data Match Correlator](VT_Correlators.md#duplicate-data-match)
- [Duplicate
Function Instructions Correlator](VT_Correlators.md#duplicate-function-instructions-match)
- [Duplicate
Exact Symbol Name Correlator](VT_Correlators.md#duplicate-exact-symbol-name-match)


The user won't know right away which ones match. The [Related
Matches Tables](providers/VT_Related_Associations_Table.md) in the Source and Destination CodeBrowsers are useful for determining
which matches are correct. Once the user determines the correct matches, the markup
should line up correctly and be pulled over all at once with the **Apply Markup** ![checkmark_green.gif](../icons/checkmark_green.gif) icon.


#### Other Correlators


Once you finish determining the obvious matches you can run other correlators to find
the rest of the matches. The availability of these other correlators depend on which
version of Ghidra is available. Please
refer to the individual help for these correlators for instructions on how to use them
and how to incorporate them into a work flow process. In general these other correlators
do not use "exact" methods of matching so it is important to be careful when accepting
matches or applying markup.


## Example Work Flow - Match All Possible Functions Between Two Binaries


1. Open an empty version tracking tool ([more info](../Tool/Ghidra_Tool_Administration.md#run-tool))
2. Enable the [Version
Tracking Accept Match Option](providers/VT_Apply_Options.md#accept-match-options) to **Auto Create Implied Matches**
3. Temporarily set the [Match
Table Filter](providers/VT_Matches_Table.md#match-filters) to remove **Implied Matches**, **Accepted Matches**, and
**Blocked** matches from the Match Table so they are not accidentally selected in the
next few steps
4. **(Optional)** Bring up the [Version Tracking
Functions Table](providers/VT_Functions_Table.md) and either tab it with the [Match Table](providers/VT_Matches_Table.md) or dock
it in its own location. Configure it to [**Show
Only Unaccepted Functions**](providers/VT_Functions_Table.md#show-unmatched-functions). This will allow the user to continually see the list of
functions they need to still match.
5. [Create a new
session](VT_Wizard.md#creating-a-new-session) by specifying your source and destination programs and then running the
precondition checks. This will give you a session that initially has no version tracking
matches. You will then Add to the Existing Session to begin getting matches.
6. [Add
to the existing session](VT_Wizard.md#add-to-an-existing-session), choosing the [Exact
Function Bytes Correlator](VT_Correlators.md#exact-function-bytes-match).
After the correlator is finished, in the matched table:
- Press **CTRL-A** to select all matches currently listed in the table
- **Click the Apply Markup** ![checkmark_green.gif](../icons/checkmark_green.gif)
icon to accept all matches and apply all their markup items.
> **Note:** NOTE: For any of the following runs, there is an option to Exclude Accepted
Matches so that the correlator being run will not report matches that are already made.
It is up to personal preference whether to use this option. In large binaries it will speed
up processing time. However, it is sometimes useful to have duplicate information for
verification of results.
7. [Add
to the existing session](VT_Wizard.md#add-to-an-existing-session), choosing the [Exact
Function Instructions Correlator](VT_Correlators.md#exact-function-instructions-match).
After the correlator is finished, in the matched table:
- Press **CTRL-A** to select all matches currently listed in the table
- **Click the Apply Markup** ![checkmark_green.gif](../icons/checkmark_green.gif)
icon to accept all matches and apply all their markup items.
8. [Add
to the existing session](VT_Wizard.md#add-to-an-existing-session), choosing the [Exact Data Match
Correlator](VT_Correlators.md#exact-data-match) .
After the correlator is finished, in the matched table:
- Press **CTRL-A** to select all matches currently listed in the table
- **Click the Apply Markup** ![checkmark_green.gif](../icons/checkmark_green.gif)
icon to accept all matches and apply all their markup items.
9. [Add
to the existing session](VT_Wizard.md#add-to-an-existing-session), choosing the [Symbol Match
Correlator](VT_Correlators.md#symbol-name-match-correlators) .
After the correlator is finished, in the matched table:
- First use the [Match
Table Filter](providers/VT_Matches_Table.md#match-filters) to only show Imported and Analysis symbol types (this is assuming
these types do not have user generated parameters or comments)
- Press **CTRL-A** to select all matches currently listed in the table
- Choose **Accept** to accept the matches but not pull over any markup - there
probably isn't any user markup and actually it is better to take the newest analysis
markup
- Edit the filter to show all symbol types again
- If desired, inspect to see if there are other symbol matches to individually or
automatically match depending on score/confidence/etc...
10. [Add
to the existing session](VT_Wizard.md#add-to-an-existing-session), choosing the [Duplicate
Function Instruction Match Correlator](VT_Correlators.md#duplicate-function-instructions-match)
- Use the [Related
Matches Tables](providers/VT_Related_Associations_Table.md) to figure out which ones match
- **Use the Apply Markup** ![checkmark_green.gif](../icons/checkmark_green.gif) icon
to accept and apply markup for each match individually.
11. [Add
to the existing session](VT_Wizard.md#add-to-an-existing-session), choosing the [Duplicate
Data Match Correlator](VT_Correlators.md#duplicate-data-match)
- Use the [Related
Matches Tables](providers/VT_Related_Associations_Table.md) to figure out which ones match
- **Use the Apply Markup** ![checkmark_green.gif](../icons/checkmark_green.gif) icon
to accept and apply markup for each match individually.
12. Run any other correlators available but don't do anything with their matches yet.
- Reset the [Match
Table Filter](providers/VT_Matches_Table.md#match-filters) to show **Implied Matches** and **Blocked** matches in the Match
Table.
- Sort the Match Table in various ways to help determine any likely matches. Here is a
list of useful ways to sort the table
- Primary sort by **Score** and secondary sort by **Confidence** - if both
are high it is a good indication of a good match
- By **Votes** - high number of votes means the match has many of the same
Implied Match suggestions
- By **Length Delta** - 0 implies matching length Source and Destination
match
- By **Source Address** to see if more than one algorithm reports the same
match
- To help determine valid matches, use the [Related
Matches Tables](providers/VT_Related_Associations_Table.md) to see all correlated matches for a particular match item.
- Use the **Accept** ![flag.png](../icons/flag.png) icon to individually
accept matches once they are determined.
13. Use the [Version Tracking
Functions Table](providers/VT_Functions_Table.md) to see what is left and manually match them using this table.
14. Use the [Markup_Table](providers/VT_Markup_Table.md) to
inspect and manually accept or apply any leftover interesting markup items in the matched
functions. Use the **Status** column in the Match Table to determine which markup items
are not finished. Users should set the filters on the Match Table so that all matches are
visible again to make sure none are missed.


> **Note:** NOTE: This is only one sample workflow
for matching all possible functions. In general, the exact, one-to-one correlators should be
run first and the rest can be used in any order. Users will come up with their own
preferences for workflow as they get used to the tool.


## Workflow FAQ


### What are Implied Matches?


An Implied Match is a match that is found when a function match is Applied or Accepted
and operand references in the matched functions apparently point to a matching function or
matching data. For example, in the matched function pictured below, it is apparent that
FUN_004011a0 in the Destination program is probably a match to the function addPerson. Also
notice that the string s_Lady_Tottington matches the string s_Lady_Tottington. Notice
that the [Implied Match
Table](providers/VT_Implied_Matches_Table.md) below the matching functions, lists this function and string and several other
references to strings as Possible Implied Matches. Users can use this table to make matches
from Implied Matches. This will cause a match to be placed in the Match table with the type
Implied Match. However, the user still has to accept or apply the match. There is also an
[Version
Tracking Accept Match Option](providers/VT_Apply_Options.md#accept-match-options) to automatically generate Implied Matches whenever a
function match is Applied or Accepted. The user still has to Accept or Apply the matches.
The determination to use the automatic generation of Implied Matches or the Implied Match
Table depends on how likely the match is to be correct and how closely aligned the match
listings are. For matches found with the exact one-to-one correlators, it is relatively
safe to turn on the auto option. For other correlators, it is safer to use the table.


![](images/ImpliedMatchExample.png)


### What do the Scores and Confidence Columns Mean?


The **Score** is an indication of how similar two potential matches are. For example,
if two functions are matched with the Exact Function Bytes Correlator, the score will be
1.0. The **Confidence** is an indication of how likely the two potential matches are
actually a match. For example, if two functions are matched with the Exact Function Bytes
Correlator, the Confidence will be 1.0 because this correlator only reports one-to-one
matches. However, if two functions are matched with the Duplicate Exact Function
Instruction Correlator, the Confidence value will be lower because this correlator reports
two or more matches. Users should look at both of these indicators to help decide whether
to Accept, Apply, Reject, or Ignore a match.


**It is important to note that score and confidence values cannot be reliably compared
between different correlators.** A confidence value of 0.8 for one correlator might be
theoretically higher than a confidence value of 0.9 for another, because each correlator
computes similarity and confidence differently.


### How Do I Know Which Functions Have Not Been Matched Yet?


Bring up the [Window->Version
Tracking Functions Table](providers/VT_Functions_Table.md). By default, two separate lists of functions from both
programs are shown. To see which functions in both programs have no matches generated by
any correlator so far, click on the black triangle and choose **Show Only Unmatched
Functions**. To see which functions in both programs have no matches accepted by the user
(includes functions with and without a correlator generated match) choose **Show Only
Unaccepted Functions**


### Why Do I See The Same Match More Than Once in the Match Table?


If a match is found by more than one correlator, it will show up in the table for each
correlator. This allows the user to gain more confidence in a match. It can clutter up the
table, though, so users can filter the table based on algorithm and many other ways. See
the [Matches
Table](providers/VT_Matches_Table.md) help for more information on how to filter out information from the table.


### What Part of the Binary Should I Run The Correlators On?


This is dependent on what the user is trying to do and which correlator is being run.
Most correlators may be run on a subset of the binary. Others correlators must run on the
entire binary. Those that allow subsets will give the user a choice when that correlator is
chosen. If a user has specific items they are interested in finding matches for, they can
run most correlators on those items only without seeing results for the entire binary.
Other users want to match all possible items. Also, once items have been accepted by a
user, users have the choice to ignore them on subsequent correlator runs. There are pros
and cons to doing this. Pros include saving memory, compute time, and less clutter in the
match table, although it can be filtered to remove the clutter. Cons include losing
information about multiple correlator agreements or disagreements.


## Common Problems


This section lists common problems or things that should be avoided when version tracking
programs.


### Making Program Changes


While version tracking two programs you should not make changes to either of the
programs (aside from applying markup through the version tracking tool). Changing programs,
especially the destination program, can cause the state of version tracking data (e.g.,
matches and their markup) to be incorrect. If you need to make changes to either of the
programs, then we recommend restarting the version tracking process from the beginning
after your changes have been made.


*Provided by: *Version Tracking Plugin**


**Related Topics:**


- [Version Tracking
Introduction](Version_Tracking_Intro.md)
- [Version Tracking Tool](VT_Tool.md)
- [Version Tracking
Wizard](VT_Wizard.md)
- [Version
Tracking Matches Table](providers/VT_Matches_Table.md)
- [Version
Tracking Markup Items Table](providers/VT_Markup_Table.md)


---

[← Previous: Workflow FAQ](VT_Workflow.md) | [Next: Program Correlators →](VT_Correlators.md)
