# File Format Actions


## Introduction


The file formats plugin adds the following actions to the
[File System
Browser](../FileSystemBrowserPlugin/FileSystemBrowserPlugin.md)


## Right-click Context Menu Actions


### Export Eclipse Project


Given a selected Android application package (APK) file, this will create an Eclipse
project for that APK. It will convert the DEX file into a JAR file, then JAD the entire
file.  Requires Java Decompiler (JAD) to be installed in
Ghidra/Features/FileFormats/os/[your_os]/jad[.exe]


### Load iOS Kernel


Given a selected iOS kernel cache file, this will load the entire kernel into the
project. After the kernel is opened, you should run the
`iOS_AnalyzeAllOpenKextsScript` script.


### Decompile JAR


Given a selected JAR file, this will JAD the entire contents and create the source.
Requires Java Decompiler (JAD) to be installed in
Ghidra/Features/FileFormats/os/[your_os]/jad[.exe]


### Create Crypto Key Template File


Builds a template for the crypto keys.


This is important when viewing iOS firmware. See the
`iPhoneWikiFirmwareKeyParserScript` to read KEYs and IVs directly from the
website pages into this template file.


## Known issues


### Strong Crypto Support


Your Java JVM install may not have support for strong crypto currently installed.


In order to fix this issue, you must install Oracle's "Java Cryptography Extension (JCE)
Unlimited Strength Jurisdiction Policy Files"
