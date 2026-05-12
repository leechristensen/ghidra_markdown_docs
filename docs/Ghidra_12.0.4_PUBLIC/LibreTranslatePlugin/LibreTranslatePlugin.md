[Home](../index.md) > [LibreTranslatePlugin](index.md) > LibreTranslate

# LibreTranslate Plugin


This plugin adds a string translation service that will appear in the **Translate**
menu of a string data instance.  The **Translate** menu will appear in the right-click
context menu of data items that are strings.


LibreTranslate (currently hosted at libretranslate.com) is an independant project that
provides an open source translation package that can be self-hosted.


This plugin queries a LibreTranslate server via HTTP to translate each specified string into
a target language.  The results of that translation will be determined by the LibreTranslate
server.


A LibreTranslate server can be installed locally by following the instructions provided
on LibreTranslate's website, and then this plugin can connect to it via a URL such as
**http://localhost:5000/** (when configured with suggested defaults).


It is also possible to use someone else's LibreTranslate server, and typically they
will issue an API key that will authorize the user to connect.


When a string has been translated, the translated value will be shown in place of
the original value, bracketed with **»chevrons«**


## Configuration


See
**Edit  →
Tool Options  →
Strings | LibreTranslate**


- **URL** - required.  Example: **http://localhost:5000/**
(if self hosted and following suggested values)
- **API Key** - a unique key that authorizes you to connect to the LibreTranslate
server.  Can be blank if api keys are not required.
- **Source Language** - either "auto" or "prompt"
- **Target Language** - the language code (as defined by LibreTranslate) that
strings should be translated into.  This defaults to "en" (English).
- **Batch Size** - the maximum number of strings to include in a single request
to the LibreTranslate server.
- **HTTP Timeout** - the maximum number of milliseconds to wait for the
LibreTranslate HTTP server to respond to a request.
- **HTTP Timeout [per string]** - an additional number of milliseconds,
per string in each request, to wait for the LibreTranslate HTTP server to
respond.


*Provided by: *LibreTranslate Plugin**


**Related Topics:**


- [Code Browser](../CodeBrowserPlugin/CodeBrowser.md)
- [View Defined Strings](../ViewStringsPlugin/ViewStringsPlugin.md)
- [Translate Strings Plugin](../TranslateStringsPlugin/TranslateStringsPlugin.md)
- [Search For Encoded Strings](../Search/Search_for_Strings.md#search-for-encoded-strings)


---

[← Previous: Translate Strings](../TranslateStringsPlugin/TranslateStringsPlugin.md) | [Next: Save Image →](../ResourceActionsPlugin/ResourceActions.md)
