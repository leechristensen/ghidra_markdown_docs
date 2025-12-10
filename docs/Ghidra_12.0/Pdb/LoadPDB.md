[Home](../index.md) > [Pdb](index.md) > Load PDB File

# Load PDB


## Symbol Servers and Symbol Storage


In an effort to manage large collections of symbol files, Microsoft specified a scheme to organize
symbol files into directory structures.


Ghidra can search Microsoft-style symbol servers (web-based HTTP/HTTPS) or local file system symbol
storage directories as well as unorganized, non-MS symbol storage directories for the PE executable's
matching PDB symbol file.


- Microsoft symbol servers / symbol storage directories:
  - Organize symbol files (typically PDB files) into a directory hierarchy using information
from the symbol file being stored.
  - <a name="onelevel-symboldirectory"></a>In a single-level symbol server directory hierarchy, a symbol file named `myprogram.pdb` might be stored
as:
    - `myprogram.pdb/012345670123012301230123456789AB1/myprogram.pdb`.
    - `myprogram.pdb` is the name of the file and the name of the initial subdirectory off the root of the server.
    - `012345670123012301230123456789AB` is the 32 character hexadecimal value (made up for this example) of the GUID
"01234567-0123-0123-0123-0123456789AB" of the PDB file.
      - This value might instead be a 8 character hexadecimal value of the ID of the symbol file if it was created by an older version of the tool chain.
    - `1` is the hexadecimal value of the 'age' (build number) of the PDB file. Note: most PDB files will have an age value of 1.
  - <a name="twolevel-symboldirectory"></a>In a two-level symbol server directory hierarchy, the same symbol file would be stored
as: `my/myprogram.pdb/012345670123012301230123456789AB1/myprogram.pdb`, where the
first two letters of the symbol file's name are used to create a bucketing directory called "my" where all symbol files starting with
"my" are stored.
    - A two-level symbol server directory hierarchy is indicated by the presence of a file called `index2.txt` in the root directory of
the hierarchy.
  - Symbol storage directories are expected to have a `pingme.txt` file and a special directory called `000admin`.
  - Compressed symbol files (`*.pd_`):
    - Microsoft symbol server tools can compress symbol files to save space.  The compressed file is stored in place of the original file, renamed
to have a trailing underscore ("_") character in the file extension.
    - Before use, Ghidra will decompress the file into the **Local Symbol Storage** directory, using whatever organization scheme
that directory is configured with to store the uncompressed version of the file.
  - Remote symbol files hosted on a HTTP server will be copied to and stored in the configured **Local Symbol Storage** directory before they
can be used.
- <a name="unorganized-symboldirectory"></a>Unorganized directories:
  - Symbol files are matched by their filename and the GUID / ID / age values extracted from
the information inside the PDB symbol file.


## Menu Actions


### Load PDB File


Allows the user to pick a PDB file or search for a PDB file and apply it to the currently open program in the CodeBrowser.


Use this action instead of the **PDB Analyzer** if the PDB file can't be found automatically with the currently configured
symbol server search locations, if you need to force load a non-exact PDB file, or you need to use other PDB options.


#### Steps:


- Invoke **File → Load PDB File...**
![](images/LoadPdb_Initial_Screenshot.png)
- The **PDB Location** field will either have the path of an existing matching PDB file, or
it will prompt the user to use the browse button to select a file or use the
**Advanced** screen to search for the file.
  - A `PDB.XML` file can be selected using the browse button.  This will limit the selected parser to be the MSDIA parser.
- Use the information displayed in the **Program PDB Information** panel to help you decide
which PDB file to choose.
- If needed, click the **Advanced** button:
![](images/LoadPdb_Advanced_NeedsConfig.png)
- The **Local Symbol Storage** location (in the [Symbol Server Config](#symbol-server-config) screen) is required
to enable searching.  If missing, click the **Config...** button.
- Set [search options](#pdb-search-search-options) as needed.
- Click the **Search Local** or **Search All** button to search the configured locations.
- The **Local Symbol Storage** location is searched first, followed by any locations listed in the
**Additional Search Paths** list, in listed order.
- Select one of the found PDB files and click the **Load** button to start the import process.
- Remote symbol files will be downloaded to your **Local Symbol Storage** location before continuing.


### Symbol Server Config


Allows the user to configure the location where PDB symbol files are stored and additional locations to search for
existing PDB files.


#### Steps:


- Invoke **Edit → Symbol Server Config**
![](images/SymbolServerConfig_Screenshot.png)
- The **Local Symbol Storage** location is required to be able to search.  If missing, set it to
a directory where Ghidra can store PDB files.
  - For example, `/home/your_id/Symbols` or `C:\Users\your_name\Symbols`.
  - If the location is a new empty directory, the user will be prompted to initialize the directory as a Microsoft symbol storage directory.
- [Add](#add) additional search locations by clicking the ![Plus2.png](../icons/Plus2.png) button.
- Save any changes to the configuration by clicking the ![disk.png](../icons/disk.png) button.
- Search locations can be disabled by toggling the **enabled** checkbox at the beginning of the row.
- A typical configuration: ![](images/SymbolServerConfig_Configured.png)


#### (Add) ![Plus2.png](../icons/Plus2.png)


Allows the user to add a location to the search path list.  Pick from the offered types of locations, or pick
a predefined location.


![](images/SymbolServerConfig_AddButtonMenu.png)


- **Directory** - allows the user to pick an existing directory that will be searched for symbol files.
See [level 1](#symbol-servers-and-symbol-storage)/[level 2](#symbol-servers-and-symbol-storage) or
[unorganized](#symbol-servers-and-symbol-storage) directory descriptions.
- **URL** - allows the user to enter a HTTP or HTTPS URL to a web-based symbol server.
- **Program's Import Location** - automatically references the directory from
which the program was imported. This option first searches for the 'official'
PDB filename embedded in the program's metadata.  If not found, it searches
for other PDB files that match variations of the program's filename.
- **Import _NT_SYMBOL_PATH** - parses the current value of the `_NT_SYMBOL_PATH` system environment variable to extract
URLs and symbol directory locations to be added to the Ghidra configuration.  If no environment value is present,
the user can paste their own value into the text field.


All items listed after the menu dividing line are automatically added from resource files that have a
`*.pdburl` extension.  The default file included with Ghidra is called `PDB_SYMBOL_SERVER_URLS.pdburl` and
is located in the `Ghidra/Configurations/Public_Release/data` directory under the Ghidra install directory.


#### (Delete) ![error.png](../icons/error.png)


Deletes the currently selected locations from the **Additional Search Paths** table.


#### (Up/Down) ![up.png](../icons/up.png) ![down.png](../icons/down.png)


Moves the currently selected item up or down in the **Additional Search Paths** table.


#### (Refresh) ![reload3.png](../icons/reload3.png)


Updates the status column of the locations listed in the **Additional Search Paths**
table.  Symbol servers or storage locations that are unreachable or misconfigured will show an error status in that column.


#### (Save) ![disk.png](../icons/disk.png)


Saves the currently displayed search and storage locations to the preferences file.  This is shared between all Ghidra tools.


### PDB Search - Search Options


These options control how PDB symbol files are found.


- **Ignore Age** - allows matching symbol files with the correct GUID, but incorrect age value.  Only affects searches of local symbol directories.
- **Ignore GUID/ID** - allows matching symbol files with the correct name, but incorrect GUID or age.  Only affects searches of local symbol directories.


Additionally, there are **override** checkboxes in the **Program PDB Information** panel in the **Advanced** screen. These override values only
change the search criteria, they are not persisted to your program's metadata.


- **PDB Name Checkbox** - this checkbox allows entering a custom value for the desired PDB file name.
- **PDB Unique ID Checkbox** - this checkbox allows entering a custom GUID or ID value.
- **PDB Age Checkbox** - this checkbox allows entering a custom age value.


After changing a search option, you will need to perform another search to use the new options.


### PDB Parser


These options control which PDB parser will be used and any options used during parsing after the **Load** button is pressed.


- **Universal** - Platform-independent PDB analyzer (No PDB.XML support).
- **MSDIA** - Legacy PDB Analyzer.  Requires MS DIA-SDK for raw PDB processing (Windows only), or preprocessed PDB.XML file.


**Control** (Universal only) - Controls how the PDB is applied to the Program


- **Process All**: Applies Data Types and Public, Global, and Module Symbols.
- **Data Types Only**: Applies Data Types and Typedefs found in the Global Symbols.
- **Public Symbols Only**: Applies only Public symbols to the program.  It ignores Global symbols and Module symbols.


## Troubleshooting


- If you are connecting to a Symbol Server that requires user authentication using PKI,
you must first set your PKI Certificate before attempting to download from the server. See
[PKI Certificate](../FrontEndPlugin/Ghidra_Front_end_Menus.md#pki-certificate) for more details.


**Related Topics:**


- [PDB (general)](PDB.md)


---

[← Previous: PDB](PDB.md) | [Next: PDB Parser (README_PDB) →](../docs/README_PDB.md)
