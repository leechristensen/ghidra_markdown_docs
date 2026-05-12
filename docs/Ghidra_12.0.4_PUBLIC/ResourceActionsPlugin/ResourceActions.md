[Home](../index.md) > [ResourceActionsPlugin](index.md) > Save Image

# Saving an Image


These
actions are found in the popup menu in the **Data** → **Save Image** submenu.


## Actions


### Save Image As New Format


Given a selected embedded image object, this will write the image to a specified file
using the format implied by the filename's extension.


For example, saving a image as "myfile.png" will write the image as PNG format,
regardless of the original format of the embedded image.


Known supported formats include:


- PNG
JPG
GIF
BMP


Attempting to save an image that contains transparency to a format that does not support
transparency will fail.


### Save Image Original Bytes


Given a selected embedded image object, this will write the embedded
resource's exact bytes to the specified file.


*Provided by: *Resource Actions Plugin**


**Related Topics:**


- [Listing](../CodeBrowserPlugin/CodeBrowser.md)
- [Data](../DataPlugin/Data.md)


---

[← Previous: LibreTranslate](../LibreTranslatePlugin/LibreTranslatePlugin.md) | [Next: Labels →](../LabelMgrPlugin/Labels.md)
