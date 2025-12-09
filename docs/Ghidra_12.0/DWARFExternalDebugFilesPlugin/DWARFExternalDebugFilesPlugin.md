[Home](../index.md) > [DWARFExternalDebugFilesPlugin](index.md) > DWARF External Debug Files

# DWARF External Debug Files


These files contain DWARF debug information that has been stripped from the original binary and
placed into a separate file (typically to save space).  These external files can be found using
information embedded in the original binary's ".gnu_debuglink" section (a filename and crc32) and/or
".note.gnu.build-id" section (a hash value).


Use the ExtractELFDebugFilesScript to pull external debug files from pre-packaged install
files, typically provided by Linux / BSD distributions, for later consumption by Ghidra.


## Menu Actions


### DWARF External Debug Config


Allows the user to pick a directory where Ghidra will search for DWARF external debug files.


Ghidra will search for external debug files under the selected directory
as ".build-id/NN/hexhash.debug" if build-id information is available, falling back to trying
the debuglink filename in any subdirectory, and lastly in the original binary's import location.


*Provided by: *DWARF External Debug Files Plugin**


---

[← Previous: Search for Code and Functions](../RandomForestFunctionFinderPlugin/RandomForestFunctionFinderPlugin.md) | [Next: PDB →](../Pdb/PDB.md)
