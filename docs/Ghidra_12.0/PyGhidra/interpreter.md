[Home](../index.md) > [PyGhidra](index.md) > PyGhidra Interpreter

# PyGhidra Interpreter


The Ghidra *PyGhidra Interpreter* provides a full general-purpose Python interactive shell
and allows you to interact with your current Ghidra session by exposing Ghidra's powerful Java
API through the magic of Jpype.


## Environment


The Ghidra *PyGhidra Interpreter* is configured to run in a similar context as a Ghidra
script.  Therefore, you immediately have access to variables such as `currentProgram`,
`currentSelection`, `currentAddress`, etc without needing to import them.
These variables exist as Java objects behind the scenes, but Jpype allows you to interact with
them through a Python interface, which is similar to Java in some ways.


As in Java, classes outside of your current package/module need to be explicitly imported.
For example, consider the following code snippet:


```

    # Get a data type from the user
    tool = state.getTool()
    dtm = currentProgram.getDataTypeManager()
    from ghidra.app.util.datatype import DataTypeSelectionDialog
    from ghidra.util.data.DataTypeParser import AllowedDataTypes
    selectionDialog = DataTypeSelectionDialog(tool, dtm, -1, AllowedDataTypes.FIXED_LENGTH)
    tool.showDialog(selectionDialog)
    dataType = selectionDialog.getUserChosenDataType()
    if dataType != None: print("Chosen data type: " + str(dataType))

```


`currentProgram` and `state` are defined within the Ghidra scripting class
hierarchy, so nothing has to be explicitly imported before they can be used.  However, because
the `DataTypeSelectionDialog` class and `AllowedDataType` enum reside in
different packages, they must be explicitly imported. Failure to do so will result in a
Python `NameError`.


## Clear


This command clears the interpreter's display.  Its effect is purely visual.
It does not affect the state of the interpreter in any way.


## Interrupt


This command issues a keyboard interrupt to the interpreter, which can be used to interrupt
long running commands or loops.


## Reset


This command resets the interpreter, which clears the display and resets all state.


## Keybindings


The Ghidra *PyGhidra Interpreter* supports the following hard-coded keybindings:


- **(up):**  Move backward in command stack
- **(down):**  Move forward in command stack
- **TAB:**  Show code completion window


With the code completion window open:


- **TAB:**  Insert currently-selected code completion (if no completion selected, select the first available)
- **ENTER:**  Insert selected completion (if any) and close the completion window
- **(up):**  Select previous code completion
- **(down):**  Select next code completion
- **ESC:**  Hide code completion window


## Copy/Paste


Copy and paste from within the Ghidra *PyGhidra Interpreter* should work as expected for
your given environment:


- **Windows:**  CTRL+C / CTRL+V
- **Linux:**  CTRL+C / CTRL+V
- **OS X:**  COMMAND+C / COMMAND+V


## API Documentation


The built-in `help()` Python function has been altered by the Ghidra *PyGhidra Interpreter*
to add support for displaying Ghidra's Javadoc (where available) for a given Ghidra class, method,
or variable.  For example, to see Ghidra's Javadoc on the `state` variable, simply do:


```

    >>> help(state)
    #####################################################
    class ghidra.app.script.GhidraState
      extends java.lang.Object

     Represents the current state of a Ghidra tool

    #####################################################

    PluginTool getTool()
       Returns the current tool.

      @return ghidra.framework.plugintool.PluginTool: the current tool

    -----------------------------------------------------
     Project getProject()
       Returns the current project.

       @return ghidra.framework.model.Project: the current project

    -----------------------------------------------------
    ...
    ...
    ...

```


Calling help() with no arguments will show the Javadoc for the GhidraScript class.


## Additional Help


For more information on the Jpype environment, such as how to interact with Java objects
through a Python interface, please refer to Jpype's documentation which can be found on the
Internet at ***jpype.readthedocs.io***


*Provided by: *PyGhidraPlugin**


---

[← Previous: Jython Interpreter](../Jython/interpreter.md) | [Next: Symbol Table →](../SymbolTablePlugin/symbol_table.md)
