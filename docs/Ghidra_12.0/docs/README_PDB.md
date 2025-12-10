# PDB Parser Application


GHIDRA includes a bundled application *pdb.exe* for use within Microsoft Windows environments.
This application is used to parse program debug information provided in the form of PDB files which are associated
with specific executable programs and libraries.  PDB files are produced during the compilation and linking
process and may be made available by the software vendor for debugging purposes.


## Prerequisites


The native PDB parser application has been built with Microsoft Visual Studio 2017 using the 8.1 SDK to allow for possible use
under Windows 7, 8.x, 10 and 11.  For this application to execute properly the following prerequisites must be properly installed:


- [Microsoft Visual C++ Redistributable for Visual Studio 2017](https://go.microsoft.com/fwlink/?LinkId=746572) with its'
prerequisite updates, and
- [DIA SDK runtime support.](#DIASDK)


## PDB File Processing


Execution of the native PDB parser for a specified PDB file produces an XML output which is subsequently parsed by GHIDRA
during PDB Analysis.  If running under windows the native PDB parser may be invoked directly if the appropriate
PDB file can be located locally, while on other platforms only the XML file form produced by the PDB parser
is supported.  Batch conversion of PDB files to XML is facilitated by the *support/createPdbXmlFiles.bat*
script.  In the near future GHIDRA will adopt a pure Java implementation which will eliminate the Microsoft Windows
native execution issue and the use of an intermediate XML format.


## Microsoft Symbol Server


Although GHIDRA has been primarily designed to utilize locally stored PDB files during analysis,
the ability to interactively download individual PDB files from a web-based Microsoft Symbol Server
is also provided.  This capability is accessed via the GUI while a program is open via the
***File → Load PDB File...*** action.


## DIA SDK Dependency


In order for the native PDB parser to work on your Microsoft Windows machine, you must:


1. Ensure you have *msdia140.dll* on your computer, and
2. Register *msdia140.dll* in the Windows registry.


**NOTES:**


- The following instructions assume you have a 64-bit operating system.  If you have rebuilt
pdb.exe with a newer version of the DIA SDK you will need to register the corresponding
version of the 64-bit DLL.  The DIA SDK 14.0 corresponds to Visual Studio 2017.
- The PDB format is known to change over time and may be incompatible with the current *pdb.exe*
parser contained within Ghidra.  A Microsoft Visual Studio project is provided within the
*Ghidra/Features/PDB/src/pdb* directory which will allow you to rebuild it with a newer version
of Visual Studio and DIA SDK.


### Ensure you have *msdia140.dll* on your computer


First, check to see if you already have the *msdia140.dll* library installed on your system.
It is generally installed with Microsoft Visual Studio 2017 when C/C++ development support
is included ( may be Community, Professional, or other VS 2017 distribution package name).


```

        C:\Program Files (x86)\Microsoft Visual Studio\2017\\DIA SDK\bin\amd64\msdia140.dll

```


This file is commonly located here, although it may be installed in other locations as well.  Any 64-bit
copy may be registered provided it is the correct version.  There is no need to register more than
one.


### Register 'msdia140.dll' in the Windows registry


Please register 64-bit *msdia140.dll* even if you already had a copy of it on your computer
since it is not registered by the Visual Studio installation process.  You will need administrative
rights/privileges in order to register the DLL in the Windows registry.


1. Start a command prompt as an administrator:
  - Click Windows Start menu, enter CMD in the search box to locate CMD program.
  - Right-click on CMD program and then click Run as administrator.
  - If the User Account Control dialog box appears, confirm that the action it displays is
what you want, and then click Yes to continue.  You may be prompted for an
Admin password to elevate permissions.
2. At the prompt within the displayed CMD window, navigate to the parent folder that
contains the 64-bit version of *msdia140.dll* or specify the full path of the DLL to
regsvr32 command below.
3. Enter the following command to register the DLL:


```

	   regsvr32 msdia140.dll

```


When the registration has completed you should see a popup that indicates that "DllRegisterServer in *msdia140.dll*
succeeded".
