# Visual Studio Code Integration


Ghidra is capable of integrating with an existing Visual Studio Code installation to aid
in the development of Ghidra scripts and modules.

## Visual Studio Code Integration Tool Options


The following Front-End tool options (Edit -&gt; Tool Options) may need to be configured for
Ghidra to successfully launch Visual Studio Code on your platform.


| Tool Options |  |
| --- | --- |
| **Option** | **Description** |
| Visual Studio Code Executable Path | Path to a Visual Studio Code executable file. It defaults           to the most commonly used location on your specific platform. |


## Create Visual Studio Code Module Project


This action creates a new Visual Studio Code project folder which can be used as a convenient
starting point to develop a new Ghidra module. The new project will be linked against the
version of Ghidra that was used to create the project. Once the project is created, the
associated Ghidra version cannot change. This behavior may become more flexible in the
future.


Visual Studio Code launchers are provided which will allow you to debug your module's code.
Also, a Gradle task named *ghidra/distributeExtension* is provided that will allow you to
build a distributable Ghidra extension.
