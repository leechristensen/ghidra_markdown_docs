[Home](../index.md) > [EclipseIntegration](index.md) > Eclipse Integration

# Eclipse Integration


Ghidra is capable of integrating with an existing Eclipse installation that has the
GhidraDev Eclipse plugin installed.  The GhidraDev Eclipse plugin listens for socket connections
from Ghidra on configurable ports.  Ghidra does not have to know the installation location of
Eclipse for this communication to succeed.  However, in order for Ghidra to launch Eclipse if
it has not been opened already, Ghidra must know the installation location of Eclipse.


The Eclipse installation location and communication ports can be configured in the Front End
tool's ***Eclipse Integration*** options.  If an attempt is made to launch Eclipse from
Ghidra and these things are not configured correctly, the user will be taken to Eclipse
Integration options automatically.


## Eclipse Integration Tool Options


| Tool Options |  |
| --- | --- |
| **Option** | **Description** |
| Automatically install GhidraDev | Automatically install the GhidraDev plugin into the            "dropins" directory of the specified Eclipse if it has not yet been installed.  If this            option is not set, you will be prompted to perform the installation when launching an            Eclipse that does not have GhidraDev installed. |
| Eclipse Installation Directory | Path to an Eclipse installation directory.  This is only           necessary if you want to launch Eclipse from Ghidra.  Ghidra will still be capable of           communicating with an open Eclipse as long as the GhidraDev plugin is installed and the           communication ports are configured correctly on both ends. |
| Eclipse Workspace Directory (optional) | Optional path to an Eclipse workspace directory.  If defined           and the directory does not exist, Eclipse will create it.  If undefined, Eclipse will be            responsible for selecting the workspace directory. |
| Script Editor Port | The port number used to communicate with Eclipse for            script editing.  It must match the port number set in the Eclipse GhidraDev plugin            preference page in order for them to communicate. |
| Symbol Lookup Port | The port number used to communicate with Eclipse for            symbol lookup.  It must match the port number set in the Eclipse GhidraDev plugin            preference page in order for them to communicate. |


## GhidraDev Eclipse Plugin


For more information on installing and using the GhidraDev Eclipse plugin, see
***Extensions/Eclipse/GhidraDev/GhidraDev_README.html***


---

[← Previous: Pop-up Menu and Keyboard Actions](../DecompilePlugin/DecompilerWindow.md) | [Next: Entropy Overview →](../OverviewPlugin/Overview.md)
