# CaRT File Format


Compressed and ARC4 Transport (CaRT) neutering format is a file format that is used to
neuter files for distribution. This is often used to neutralize malware in the malware
analyst community, but could be used for non-malware as well. Using Ghidra's file system
support the binary stored in the CaRT may be safely extracted and processed as normal
without ever needing to store the original binary to disk.


## About CaRT


The CaRT format was developed by the Canadian government within their
*Canadian Centre for Cyber Security*. The documentation and
repository can be found on the *CaRT GitHub* page.


The official *CaRT python library* is usually used
to create CaRT files via its command-line interface or within other python applications or
libraries.


## Supported CaRT Format Versions


Currently CaRT only has a single format version, namely version 1
. If/when new versions are released this file system will be updated to support them.


## Decryption Keys


The CaRT format uses ARC4 encryption and supports two modes of keys: default and private.


- **Default** - In this mode a default key (the first 8 digits of PI, twice) will be used
without any further interaction from the user. Binary data is safely neutered without the need
to share and transmit passwords.
- **Private** - This mode is appropriate when the key for the encrypted data should be
transmitted and stored separately from the CaRT file itself. The key may be provided to
Ghidra in two ways, attempted in the following order:
  1. *INI Configuration* - If the default CaRT configuration file exists (
${USER_HOME}/.cart/cart.cfg) the key stored there, if
any, will be attempted first. See the
*CaRT GitHub* for more
documentation on this configuration file.
  2. *User Prompt* - If the key is not found through the configuration file then the
user will be prompted to input the key manually. The key may be entered as plaintext
or in base-64 format (thus supporting arbitrary binary keys). The user will be
repeatedly prompted until either the correct key is provided or they click 'Cancel'.


See the *CaRT GitHub* page for more
documentation on keys, requirements, and formats.


## Metadata (and Hashes)


The CaRT format supports a number of metadata fields including MD5, SHA-1, and SHA-256
hashes, and additional user-specified metadata. These hashes will be verified when Ghidra
imports the binary for analysis. Warnings will be displayed if any of these hashes are missing
and processing will be halted if any of them are present but do not match the binary contents.
Additional metadata fields are visible via the "Get Info" context menu option.
