[Home](../index.md) > [DebuggerDisassemblerPlugin](index.md) > Disassembly and Assembly

# Debugger: Disassembler and Assembler


The Debugger provides specialized disassemble and assemble ("patch instruction") actions.
These actions operate on a smaller scope of instructions, disassembling linearly from the
cursor or program counter up to and including the next branching instruction. They also allow
the user a selection of languages configured on the current trace.


## Actions:


### Disassemble


This action disassembles from the cursor up to the next branching instruction for the
selected language. One action is presented per language configured at the current location.
Other languages may also be presented if the only thing that varies is the default disassembly
context, e.g., configuring ARM will also allow THUMB disassembly.


### Patch Instruction / Assemble


This action assembles an instruction at the cursor. One action is presented per language
configured at the current location. Other languages may also be presented if the only thing
that varies is the default disassembly context, e.g., configuring ARM will also allow THUMB
assembly.


### Patch Data


This action patches the data unit at the cursor, if its type provides an encoder.


---

[← Previous: Dynamic Listing](../DebuggerListingPlugin/DebuggerListingPlugin.md) | [Next: Stack →](../DebuggerStackPlugin/DebuggerStackPlugin.md)
