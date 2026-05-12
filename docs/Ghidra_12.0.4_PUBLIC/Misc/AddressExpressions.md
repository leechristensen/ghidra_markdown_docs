[Home](../index.md) > [Misc](index.md) > Address Expressions

# Address Expressions


An address expression is an arithmetic expression that is entered into an address input
field and can include symbol names or memory block names that when evaluated results in a
program address.


## Operands


Operands can be either a number or a name that evaluates to an address.


### Names


If the operand is a name, then an attempt will be made to find a unique label or
function name in the current program for that name. If that fails, then memory blocks
will be searched looking for a memory block with that name. In either case, the associated
address for that label, function, or memory block will be used in evaluating the
expression.


Generally, symbols (addresses) must be the left operand for a binary operator and will
generate a address as the result (maintaining the address space). The one exception is
you can subtract two addresses and the result is a number.


### Numbers


Numeric operands will be evaluated as either a hex number or decimal number, depending
on the **Hex/Decimal Mode** of the input field.


When in hex mode, undecorated numbers will be interpreted as if they are hex values.
(so "100" would evaluate to the number 256). If in decimal mode, hex numbers can still be
entered by prefixing them with "0x".


For fields that support either mode, the current mode will be displayed as "hint text"
in the lower right corner of the field. The mode can be toggled between decimal and hex
by pressing `<CTRL>` M.


When in hex mode, there is no corresponding prefix to use to specify a number as being
decimal. So if you want to have a mixed mode expression, use decimal mode and use the
"0x" prefix for any hex numbers in the expression.


## Operators


Most standard operators are supported, but not all operators are supported for all
operands. Also order of operands is important when mixing numbers and addresses. For
example,a number can be added to an address, but an address can't be added to a number.


Operator precedence is the standard precedence defined by the "C" programming
language.


### Math Operators


Supported math operators are "+ - * /". These operators generate either a number or
address result depending on the operands.


### Logical and Relational Operators


Supported logical operators are "&lt; &gt; &lt;= &gt;= == != || && and !".
These operators generator a numeric value of 0 or 1.


### Bit Operators


Supported bit operators are &lt;&lt;, &gt;&gt;, &, |, ^, and ~. These operators
generate either a number or address result depending on the operands.


### Groups Operators


Parenthesis can be used to group sub-expressions to control the order of
operations


## Result


The result of the expression is always an address or a number. If the result is a
number, it is converted to an address using the selected address space (in the case where
there are multiple possible address spaces, a combo is shown for choosing the desired
address space, otherwise the default address space is used)


## Examples


| Expression   | Result   |
| --- | --- |
| **ENTRY+10** | Address 0x10 higher than the symbol "ENTRY" |
| **10+ENTRY** | Error (Can't add an address to a number) |
| **100000+30** | Address 0x100030 (hex mode) |
| **0x100000+30** | Address 0x100030 (hex mode) |
| **0x100000+30** | Address 0x10001e (decimal mode) |
| **0x100000+(2*10)** | Address 0x100020 |
| **ENTRY + 1&lt;&lt;4** | Address that is 16 higher than the symbol "ENTRY" |
| **X - (X &gt; 100) * 100** | If symbol "X" address &gt; 100, Result is 100 less than X; Otherwise X |
| **ENTRY \| FF** | Address that is the symbol "ENTRY" with its last 8 bits set to FF |


---

[← Previous: Program Annotation](../ProgramManagerPlugin/Program_Annotation.md) | [Next: Auto Analysis →](../AutoAnalysisPlugin/AutoAnalysis.md)
