# Show Instruction Info


Displays information about an instruction.


## **Raw Instruction Display**


Displays the raw instruction under the current cursor location.  The instruction is
displayed as it was disassembled without any operands replaced by label references or other
adornments.


To see the raw instruction


Set the current program location to an instruction code unit (i.e., using the mouse,
left click on an instruction within the code viewer).  The raw instruction is
displayed in the lower right hand corner of the code browser tool.


![](images/RawInstructionDisplay.png)


## **Processor Manual**


Displays the micro-processor manual page for the instruction at the current cursor
location. If there is no instruction at the selected location then the manual will be shown
opened to the first page of the document.


1. Position the cursor over the instruction
2. right-mouse-click, select **Processor Manual**


Not all Ghidra language
modules support this functionality.


Implementation Note:

Ghidra uses a local web server in order to pass processor manual content to client web
browsers. Ghidra will attempt to launch the client web browser, but cannot always determine
the proper application to launch. If Ghidra cannot successfully launch a default application
to show the processor manual, then Ghidra will show a warning message that provides the file
URL and path that Ghidra is trying to open. From this dialog you can edit the settings Ghidra
uses to open manuals. You may also copy the file information from text fields, if so desired
by selecting the text and pressing *Ctrl-C*. Below is the warning dialog.


![](images/UnableToLaunch.png)


If you choose to edit the settings you will be taken to the options dialog shown
below.


<a name="processor-manual-options"></a> ![](images/ProcessorManualOptions.png)


| Options Name | Description |
| --- | --- |
| Command String | The name of a process to launch on your system. For example, if you have the             Firefox web browser installed on your system and it is in your system path, then you             can simply enter the value `firefox` . You may also enter the full path to an             application for Ghidra to launch. |
| Command Arguments | A space separated list of arguments that Ghidra will pass to the process listed             above. If you need to include spaces as part of one of the arguments, then enclose the             argument in double quotes (e.g., "arg with space"). |
| File Format | Ghidra will pass, by default, a URL to the given process. You may change this value             to signal to Ghidra that it should pass a filename instead. |


## **Instruction Info Window**


The *Instruction Info* window displays internal information about an
instruction.  It is very useful for debugging problems with instructions.


The left-most text display column provides general information about the instruction
(Mnemonic, Number of Operands, Address, Flow Type, Delay Slot Depth, Prototype Hash, Input
Objects, Result Objects, Constructor line numbers, Instruction Bytes, etc.).


The Operand columns (*Op0*, *Op1*, etc.) display information about a particular
operand.  Each operand has a number of rows.  At the end of the row is a
descriptive name for the information displayed on that row.


| Operand | Raw instruction operand representation |
| --- | --- |
| Labeled | Default operand markup (e.g., referenced symbol name,               etc.)   |
| Type | Type of operand (ADDR, DATA, SCAL, REG, etc.) |
| Scalar | Result of getScalar() for the operand |
| Address | Result of getAddress() for the operand |
| Register | Result of getRegister() for the operand |
| Op-Objects   | Result of getOpOpbjetecs() for the operand which               reflects all varnodes referenced by pcode produced by operand subconstructor.   |
| Operand Mask   | Identifies which bits within instructions bytes are               responsible for the operand value (i.e., register, scalar, etc.)   |
| Masked Value   | Identifies the specific bit values within the               instruction bytes which are responsible to the operand value (i.e., specific               register, scalar value, etc.)   |


![](images/ShowInstructionInfo.png)


The ![In](../icons/locationIn.gif) *Dynamic Update* toggle indicates whether the
window should update when you change the location in the Code Browser.  By default, the
toggle is selected. As you change your
[location](../CodeBrowserPlugin/CodeBrowser.md#cursor) in the Code
Browser, the window will be updated to show the info for the new location.  If you turn
off the toggle, the window does not update; the next time you choose *Instruction
Info*, a new tab is displayed in the *Instruction Info* window.


*Provided by: *Show Instruction Info* Plugin*


**Related Topics:**


- [Code
Browser](../CodeBrowserPlugin/CodeBrowser.md)
