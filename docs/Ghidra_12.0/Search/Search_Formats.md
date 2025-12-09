# Search Formats


The selected format determines how the user input is used to generate a search byte
sequence (and possibly mask byte sequence). They are also used to format bytes back into
"values" to be displayed in the table, if applicable.


## Hex:


The hex format allows the user to specify the search bytes as hex values.


#### Notes:


- The input string is interpreted as a sequence of hex numbers, separated by spaces.
- Wildcard characters can be used to match any single hex digit (i.e. any 4 bit
value).
- Either the '.' or '?' character can be used for the wildcard character.
- Each hex number group (groups are separated by spaces) will produce a sequence of bytes
that may be reversed depending on the byte order. To avoid byte ordering effects, separate
each two digit hex value with a space.
- The byte search pattern is formed by concatenating the bytes from each hex number
group.
- The Hex format generates no "values" in the values table column (it would just be a
repeat of the bytes column).
- As a convenience, if a user enters a single wildcard value within the search text, then
the search string will be interpreted as if 2 consecutive wildcard characters were entered,
meaning to match any byte value.
- Similarly, if the search string contains an odd number of characters, then a 0 is
prepended to the search string, based on the assumption that a single hex digit implies a
leading 0 value.


#### Examples: (Little Endian)


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| 12 | 12 | FF |
| 12 A4 | 12 A4 | FF FF |
| 12A4 | A4 12 | FF FF |
| 12 3456 | 12 56 34 | FF FF FF |
| 5 E12 | 05 12 0E | FF FF FF |
| 5. | 50 | F0 |
| .5 | 05 | 0F |
| 12.4 | 04 12 | 0F FF |


#### Examples: (Big Endian)


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| 12 | 12 | FF |
| 12 A4 | 12 A4 | FF FF |
| 12A4 | 12 A4 | FF FF |
| 12 3456 | 12 34 56 | FF FF FF |
| 5 E12 | 05 0E 12 | FF FF FF |
| 5. | 50 | F0 |
| .5 | 05 | 0F |
| 12.4 | 12 04 | FF 0F |


## Binary:


The Binary format allows the user to specify the search bytes as binary
values.


- The input string is interpreted as a sequence of binary numbers.
- Binary values must always be specified in groups of up to 8 "0" or "1" digits.
- Since a group can have at most 8 characters, a group always represents 1 byte.
- Since a group can be only 1 byte, byte ordering doesn't affect the binary format.
- Wildcard characters can be used to match any single binary digit (i.e. any 1 bit
value).
- Either the '.' or '?' character can be used for the wildcard character.
- The byte search pattern is formed by concatenating the bytes from each binary number
group.
- The binary format generates no "values" in the values table column
- As a convenience, if a user enters less than 8 binary digits, it is assumed that the
leading bits are 0.


#### Examples:


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| 10000001 | 81 | FF |
| 11 | 03 | FF |
| 0 1 0 | 00 01 00 | FF FF FF |
| 0 10 | 00 02 | FF FF |
| 111.00.0 | E0 | ED |
| 1 . 0 | 01 00 00 | FF 00 FF |


## String:


The String format allows the user to search to specify the search bytes as a string.


- The input string is converted to bytes using the chosen character encoding.
- If the *Case Sensitive* option is on, the bytes are translated exactly to the
string values and the masks bytes are all 0xFF.
- If the *Case Sensitive* option is off, the bytes are translated to the string values in
upper case and the masks are all 0xEF, meaning matches
will be found regardless of the case of the input string or the bytes in memory.
- If the *Escape Sequences* option is on, values such as "\n" or "\t" are translated to
their single byte equivalent escape value.
- If the *Escape Sequences* option is off, values such as "\n" or "\t" are
translated literally to those characters (e.g. the "\" char followed by the "n" char.
- The String format generates strings for the table's *Match Value* column.
- Wild cards are not supported by the String format.


#### Examples: (Encoding is Ascii, Case Sensitive is on, Escape Sequences is off)


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| Hey0 | 48 65 79 30 | FF FF FF FF |
| Hey\n | 49 65 79 5c 6e | FF FF FF FF FF |


#### Examples: (Encoding is Ascii, Case Sensitive is off, Escape Sequences is off)


DF DF DF FF



| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| Hey0 | 48 45 59 30 |  |
| Hey\n | 49 65 79 5c 6e | DF DF DF DF FF DF |


#### Examples: (Encoding is Ascii, Case Sensitive is on, Escape Sequences is on)


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| Hey0 | 48 65 79 30 | FF FF FF FF |
| Hey\n | 49 65 79 0A | FF FF FF FF |


#### Examples: (Encoding is UTF-16, Case Sensitive is on, Escape Sequences is off, Little Endian)


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| Hey | 48 00 65 00 70 00 79 00 | FF FF FF FF FF FF |
| a\n | 61 00 5c 00 6e 00 | FF FF FF FF FF FF |


#### Examples: (Encoding is UTF-16, Case Sensitive is on, Escape Sequences is off, Big Endian)


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| Hey | 00 48 00 65 00 70 00 79 | FF FF FF FF FF FF |
| a\n | 00 61 00 5c 00 6e | FF FF FF FF FF FF |


## Reg Ex:


The Reg Ex format allows the user to search memory for strings using Java regular
expressions.


- The Reg Ex format treats consecutive bytes in memory as if it was a string and uses the
input string as the specification for the regular expression.
- The Reg Ex format generates no bytes and masks, instead using Java's regular expression
engine to try and find matches.
- The Reg Ex format generates strings for the table's *Match Value* column.
- For more information on supported regular expression syntax, see the page on
[Regular Expressions](Regular_Expressions.md)


## Decimal:


The *Decimal* format allows the user to search for a sequence of decimal values.


- The input string can have one or more decimal values, separated by
spaces.
- Each decimal value in the input text, are converted to a sequence of bytes. The number
of bytes for each value is determined by the size as specified in the decimal options.
If the *Unsigned* option is on, negative number can't be entered.
If the *Unsigned* option is on, input numbers can be as big as the largest
unsigned value that can be represented by the selected byte size. For example, if the
byte size is 1, the largest unsigned value you can enter is 255.
If the *Unsigned* option is off, input numbers can be from the lowest negative
number to the highest positive number for values that can be represented by the selected
byte size. For example, if the byte size is 1, the entered values can be from -128 to 127.
The endian setting affects the order of the bytes generated for decimal values.
The Decimal format does not support wildcards.
The byte search pattern is formed by concatenating the bytes from each decimal
number entered in the input.
The Decimal format displays decimal values in the table's *Match Value* column.


#### Examples: (Size = 1 byte, Signed Values)


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| -1 0 127 | FF 0 7F | FF FF FF |


#### Examples: (Size = 2 byte, Signed Values, Little Endian)


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| -1 0 32767 | FF FF 00 00 FF 7F | FF FF FF FF FF FF |


#### Examples: (Size = 2 byte, Signed Values, Big Endian)


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| -1 0 32767 | FF FF 00 00 7F FF | FF FF FF FF FF FF |


#### Examples: (Size = 4 byte, Signed Values, Little Endian)


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| -1 5 | FF FF FF FF 05 00 00 00 | FF FF FF FF FF FF FF FF |


#### Examples: (Size = 4 byte, Signed Values, Big Endian)


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| -1 5 | FF FF FF FF 00 00 00 05 | FF FF FF FF FF FF |


#### Examples: (Size = 8 byte, Signed Values, Little Endian)


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| -1 | FF FF FF FF FF FF FF FF | FF FF FF FF FF FF FF FF |
| 5 | 05 00 00 00 00 00 00 00 | FF FF FF FF FF FF FF FF |


#### Examples: (Size = 8 byte, Signed Values, Big Endian)


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| -1 | FF FF FF FF FF FF FF FF | FF FF FF FF FF FF FF FF |
| 5 | 00 00 00 00 00 00 00 05 | FF FF FF FF FF FF FF FF |


#### Examples: (Size = 1 byte, Unsigned Values)


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| 0 256 | 0 FF | FF FF |


#### Examples: (Size = 2 byte, Unsigned Values, Little Endian)


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| 5 | 05 00 | FF FF |
| 65535 | FF FF | FF FF |


#### Examples: (Size = 2 byte, Unsigned Values, Big Endian)


| 5 | 0 05 | FF FF |
| --- | --- | --- |
| 65535 | FF FF | FF FF |


#### Examples: (Size = 4 byte, Unsigned Values, Little Endian)


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| 5 | 05 00 00 00 | FF FF FF FF |


#### Examples: (Size = 4 byte, Unsigned Values, Big Endian)


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| 5 | 00 00 00 05 | FF FF FF FF FF |


#### Examples: (Size = 8 byte, Unsigned Values, Little Endian)


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| 5 | 05 00 00 00 00 00 00 00 | FF FF FF FF FF FF FF FF |


#### Examples: (Size = 8 byte, Unsigned Values, Big Endian)


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| 5 | 00 00 00 00 00 00 00 05 | FF FF FF FF FF FF FF FF |


## Float:


The Float format allows the user to enter floating point numbers of size 4 bytes.


- The input string is interpreted as a sequence of floating point numbers.
- Each floating point number is converted to 4 bytes.
- The *Endian* setting affects the order of the bytes.
- Wildcard characters are not supported.
- The byte search pattern is formed by concatenating the bytes from each floating point
number.
- The Float format generates floating point numbers in the values table column


#### Examples: (Little Endian)


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| 3.14 | C3 F5 48 40 | FF FF FF FF |


#### Examples: (Big Endian)


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| 3.14 | 40 48 F5 C3 | FF FF FF FF |


## Double:


The Double format allows the user to enter floating point numbers of size 8 bytes.


- The input string is interpreted as a sequence of floating point numbers.
- Each floating point number is converted to 8 bytes.
- The *Endian* setting affects the order of the bytes.
- Wildcard characters are not supported.
- The byte search pattern is formed by concatenating the bytes from each floating point
number.
- The Double format generates floating point numbers in the values table column


#### Examples: (Little Endian)


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| 3.14 | 1F 85 EB 51 B8 1E 09 40 | FF FF FF FF FF FF FF FF |


#### Examples: (Big Endian)


| **Input String** | **Byte Sequence** | **Mask Bytes** |
| --- | --- | --- |
| 3.14 | 40 09 1E B8 51 EB 85 1F | FF FF FF FF FF FF FF FF |
