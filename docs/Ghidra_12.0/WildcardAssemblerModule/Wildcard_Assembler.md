[Home](../index.md) > [WildcardAssemblerModule](index.md) > Wildcard Assembler

# Wildcard Assembler Module


**This feature is currently only available as an API for Ghidra scripts and plugins. For
an example of how to use the API, see the FindInstructionWithWildcard and
WildSleighAssemblerInfo scripts in the Script Manager.**


The *Wildcard Assembler* extends Ghidra's assembler to enable assembling instructions
with specific tokens replaced with wildcards.


This assembler will return metadata for each wildcard in an assembled instruction. This
metadata includes details of which specific bits of an assembled instruction are used to
derive the value of the wildcarded token and the expression used to derive the value.


## Wildcard Syntax


Wildcards in instructions are specified by replacing the to-be-wildcarded token with a
wildcard name surrounded by backticks (e.g. ``Q1`` where Q1 is an arbitrary
wildcard name) and passing the entire instruction to the Wildcard Assembler.


By default, the Wildcard Assembler will return metadata about all possible values that a
wildcarded token could take and all the encodings of all these values. This behavior can be
limited by filtering the wildcard by appending specific syntax after the wildcard name:


- **Numeric Filter:**
- Appending `[..]` e.g., `MOV RAX, `Q1[..]``, will constrain
the wildcarded token to only numeric values (and not registers or other strings).
- Appending `[0x0..0x100]` (where 0x0 and 0x100 are arbitrary hexadecimal
values with the smaller number first) will constrain the wildcarded token to only
numeric values between the two given values. This can be used to ensure that the
returned encodings can hold values of a desired size. Multiple non-contiguous ranges
can be specified by separating them with commas (e.g.
`[0x0..0x5,0x1000..0x4000]`)
- **Regex Filter:**
- Appending `/ABCD` where ABCD is an arbitrary regular expression will
constrain the wildcarded token to only be string tokens matching the given regular
expression. This is most likely used for filtering register names; for example
appending `/(sp)|(lr)` to a wildcard in a register position in ARM assembly
will limit the wildcard results to only encodings using the `sp` or
`lr` registers in that position.


Normally a wildcard will only match a single token. For example, in a x86:LE:32:default
binary:


No wildcard:
`MOVSD.REP ES:EDI,ESI`
Single token:
`MOVSD.REP `Q1`:EDI,ESI`
Single token:
`MOVSD.REP ES:`Q2`,ESI`


To allow a single wildcard to match multiple related tokens: precede the wildcard name
with a `!` character:


Multi-token:
`MOVSD.REP `!Q4`,ESI`
Single token (Does *NOT* assemble):
`MOVSD.REP `Q3`,ESI`


*Provided by: *Wildcard Assembler Module**


---

[← Previous: Implied Matches Table](../VersionTrackingPlugin/providers/VT_Implied_Matches_Table.md) | [Next: Data Type Manager →](../DataTypeManagerPlugin/data_type_manager_description.md)
