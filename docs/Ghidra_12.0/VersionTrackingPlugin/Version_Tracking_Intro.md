[Home](../index.md) > [VersionTrackingPlugin](index.md) > Version Tracking

# Version Tracking Introduction


Version Tracking refers to the process used by reverse engineers to identify matching code or data
between different software binaries.  One common use case is to version track two
different versions of the same binary.  Alternatively, version tracking techniques
can be used to check for the presence of a particular piece of code within a given
binary of interest.


Perhaps the most common version tracking scenario is when you have a binary file that
you have previously analyzed, identifying important areas of interest and annotating the code with comments
and labels.  Suppose the software developer releases a newer version of the software including bug
fixes and feature modifications.  Since customers may be using the more up-to-date version,
the analyst will probably want to continue evaluation with the newer version as well.
However, it can be very time-consuming to have to initiate the analysis from scratch. In
order to leverage the existing work, version tracking enables the reverse engineer
to port comments and labels into the new context.


Perhaps the second most common version tracking scenario is where you wish to check for
the presence of existing code within a given binary.  As an example, given a small collection
of functions, say from some library of routines or code representing known malware, you
can use version tracking to search for that code in a given binary.


The remainder of this document describes high-level version tracking concepts use by
Ghidra, followed by links to documents that describe how to get started version
tracking in Ghidra.


Version Tracking Concepts:


- [Session](#version-tracking-session)
- [Associations](#version-tracking-associations)
- [Matches](#version-tracking-matches)
- [Markup Items](#version-tracking-markup-items)
- [Correlators](#version-tracking-correlators)
- [How to Start](#how-to-start)


## Version Tracking Session


A *session* is created as a result of running one of Ghidra's matching
algorithms (a.k.a., a [correlator](#version-tracking-correlators)) against two binaries.
The newly created session is stored in the
[Ghidra Project Window](../FrontEndPlugin/Ghidra_Front_end.md#ghidra-project-window).
The session records the history of any work done within that session (e.g., applying
markup).  Furthermore, since changes are saved, you may close and reopen a session to
continue work at a later time.  Sessions can be updated with new data by running
additional matching algorithms at any time.


## Version Tracking Associations


An *association* is any pairing of information between the two versions of the same program, which suggests
that the items correspond with one another in some way.  An association is characterized by a collection
of metadata including the correlating algorithm that determined the association, a memory address reference
locating the items in each version, and the type of the items being associated (data or function).


Sometimes a variable or function in the source program will be associated with several
variables or functions in the destination program.  This happens because the version tracking algorithm has
found enough evidence to support each candidate as a possible correspondence between the two versions.  When
this happens, we say that they are conflicting associations.  It may be that only one of the associations
is exactly right or that the modularity of the program has changed sufficiently and none of the associations
is quite right.  Ultimately, the analyst has to inspect the actual code
to make a determination about which associations represents a valid match.


Once an association is accepted by the user, any other associations which may be conflicting because they include
either the same source or the same destination address will become blocked because the tool only allows one-to-one
mappings.  Blocked and conflicting associations which lead to other inconsistencies can be a useful way of identifying
valid matches between two different versions.


## Version Tracking Matches


A *match* is an association that has been assigned a score.  As a correlator finds an
association it will assign that association a score, thus creating a match.  The
[matches table](providers/VT_Matches_Table.md)
contains all matches discovered by any correlators run within a given session.  Users
can use the score to help determine the accuracy of a given match, as not all matches
created by the correlators are correct.


When the you determine that a match is valid, then you can
[accept](providers/VT_Matches_Table.md#match-table-actions)
the match, which will block conflicting, related matches.  When you apply markup for a
given match, then that match is automatically accepted.  Finally, you cannot apply
markup for a match that has been blocked by another already accepted match.


Ghidra also has the concept of an
[Implied
Match](providers/VT_Implied_Matches_Table.md#version-tracking-implied-match).  If you accept a function match, then Ghidra will generate implied matches for any functions
called by the two functions that make up the function match.


## Version Tracking Markup Items


During analysis of a program, the analyst will develop a greater understanding of the code and will annotate
the disassembly with comments, labels, data type information, and parameter and variable names to document
the code and to make it more readable.  Ghidra refers to all of these annotated details
as markup items.


For any given match we can apply its markup items
and port these annotations in an appropriate manner so that the labels and comments appear in the corresponding
locations in the new binary.  This is the ultimate purpose of version tracking, to retain any progress that
has already been made in understanding the code and be able to proceed despite any changes
to the original binary.


## Version Tracking Correlators


There are many strategies for identifying
how different versions of the a program are related to each other.  Any scheme or algorithm
that determines these relationships is referred to as a correlator.  Correlators may be based
on the underlying bytes in a program, the program flow, or any other aspect of the code upon
which similarities may be observed.  Additional documentation is available for the specific
[correlators used in Ghidra.](VT_Correlators.md)


## How to Start


This list presents a few different useful links for getting started with
version tracking.


- [Workflow](VT_Workflow.md)
- [Version Tracking Tool](VT_Tool.md)
- [Version Tracking Wizard](VT_Wizard.md)


*Provided by: *Version Tracking Plugin**


**Related Topics:**


- [Workflow](VT_Workflow.md)
- [Version Tracking Tool](VT_Tool.md)
- [Version Tracking Wizard](VT_Wizard.md)
[Version Tracking Matches Table](providers/VT_Matches_Table.md)
[Version Markup Items Table](providers/VT_Markup_Table.md)


---

[← Previous: Temporary Symbol Table](../SymbolTablePlugin/symbol_table_transient.md) | [Next: Workflow →](VT_Workflow.md)
