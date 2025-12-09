[Home](../index.md) > [VariableValueHoverPlugin](index.md) > Variable Hovers

# Debugger: Variable Hovers


This service plugin provides hovers to the [Static Listing](../CodeBrowserPlugin/CodeBrowser.md), the [Dynamic Listing](../DebuggerListingPlugin/DebuggerListingPlugin.md), and the [Decompiler](../DecompilePlugin/DecompilerIntro.md). Hovering the mouse over
variables or operands in any of those windows will cause the service to display a tip showing
the value of that variable, if it can. For stack and register variables, the service will
attempt to unwind the stack until it finds a call record for the function using the variable.
Thus, it is important to have all the modules imported, analyzed, and open in the Debugger so
that the unwinder can access the static analysis of every function it needs to unwind.


Stack unwinding can be tenuous. It relies heavily on accurate static analysis and expects
functions to follow certain conventions. Thus, it's very easy to break and may frequently be
incorrect. For hovers that include a **Frame** row, the displayed value depends on an
accurately unwound stack. Take the value with a grain of salt, especially if the hover also
includes a **Warnings** row. To diagnose the unwound stack, use the [Unwind Stack](../DebuggerStackPlugin/DebuggerStackPlugin.md#unwind-stack)
action.


## Table Rows


A hover may display any of the following rows:


- **Name:** The name of the variable or operand.
- **Frame:** A description of the frame (call record) unwound to evaluate the variable.
This is omitted for global or static variables and for raw register operands.
- **Storage:** The statically-defined storage of the variable.
- **Type:** The data type of the variable.
- **Instruction:** If the operand refers to code, the instruction at the target
address.
- **Location:** The actual location of the variable on the target.
- **Bytes:** The bytes in the variable, subject to the target's endianness. For long
buffers, the bytes are split into lines of 16 bytes each for at most 16 lines.
- **Integer:** The value displayed as an integer in various formats: decimal,
hexadecimal; unsigned, signed. The alternative formats are only included if they differ from
the formats already presented.
- **Value:** The value as given by its type's default representation. This only applies
if the variable has a type and it was able to interpret the variable's bytes.
- **Status:** If the evaluation is taking significant time, this provides feedback while
evaluation proceeds in the background.
- **Warnings:** Displays any warnings encountered while unwinding the stack, if
applicable.
- **Error:** Displays an exception or error message when there was a problem evaluating
the variable. Other rows may be present, but overall the table is incomplete.


## Examples


![](images/VariableValueHoverPluginListing.png)


A register operand in the Dynamic Listing


When hovering over operands in the Dynamic Listing, that operand is most likely a register.
The register's value is displayed without regard to the stack frame. It will always use the
"innermost frame," meaning it will display the register's current value. In the example, the
user has hovered over register EDX; however, the value of EDX was not recorded, so its integer
value `0` is displayed in gray. Furthermore, the user had not assigned a type to EDX
in the [Registers](../DebuggerRegistersPlugin/DebuggerRegistersPlugin.md)
window, and so the service cannot interpret the value except as an integer. Register values are
never displayed as raw byte arrays.


![](images/VariableValueHoverPluginBrowser.png)


A stack variable in the Static Listing


When hovering over operands in the Static Listing, the service will gather context about the
operand and find a frame for the relevant function. It will take the first appropriate frame it
encounters during unwinding (from innermost out) so long as the frame's level is at least the
current frame level. In the example, the user has hovered over the parameter *n*, which
is a stack variable of the function *fib*. The curent frame is 0, so the service unwinds
the stack, finds that the current frame is a call record for *fib*, and selects it. It
displays the variable's static storage `Stack[0x4]:4` and type `uint`. It
then applies this information to determine the actual run-time location and value. Since the
frame base is `00004fa0`, it adds the stack offset to compute the run-time location
`00004fa4:4`. It reads the bytes `01 00 00 00` from the target and
computes the integer value `1`. It also interprets the value using the assigned data
type, giving `1h`.


![](images/VariableValueHoverPluginDecompiler.png)


A stack variable in the Decompiler


When hovering over variables in the Decompiler, the service behaves similarly to how it does
for operands in the Static Listing. It locates the appropriate frame and attempts to derive the
variable's run-time value. Just as in the Static Listing example above, the user has hovered
over the variable *n*, so the service has again computed the value `1h`.


---

[← Previous: Watches](../DebuggerWatchesPlugin/DebuggerWatchesPlugin.md) | [Next: Control and Machine State →](../DebuggerControlPlugin/DebuggerControlPlugin.md)
