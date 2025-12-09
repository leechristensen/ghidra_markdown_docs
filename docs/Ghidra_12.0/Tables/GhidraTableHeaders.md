# Ghidra Tables


Most table headers in Ghidra support some or all of the following features:


1. [the ability to sort one or more columns](#sortingcolumns),
2. [the ability to hide columns](#selectcolumns),
3. [the ability to add additional columns](#selectcolumns), and
4. [the ability to change appearance settings for some columns](#columnsettings).


If you are using a table that does not offer one of the above features, and you would like
us to add that feature, then please contact the Ghidra team to request additional support.


> **Note:** In addition to table header actions, many
tables support a common set of actions when right-clicking in the body of the table, such
as: Copy (also available via Ctrl-C , and the ability to export a table to a comma-separated value (CSV) file . Select All (also available via Ctrl-A .


## Sorting Columns


Sorting a table on a particular column is as easy as left-clicking that column.  A
sorted column is denoted by an icon that shows the sort direction.


![](../shared/note.yellow.png)
If you click a table column header and no sorting takes place, then that particular
table does not support sorting on columns.


When you click a column to sort the data, the default sort will be ascending.  If you
click the column while it is already sorted, then the sort direction will be changed
and the table resorted.


To sort on multiple columns, press the **Control** key while left-clicking a table
column header.  This will cause the clicked column to become the next sort column.  As
an example, suppose you are sorted on *column one*, and then add a secondary
sort to *column two*, then the
data will be sorted first on *column one*, and then, when equal values are found for
that column, a secondary sort will take place on *column two*.  You may sort on as many
columns as you wish.  When a multiple column sort is in effect, a number will appear
next to each column's sort direction icon, which indicates that column's order in the
sorting process. 		Below is a picture of the **Functions** table sorted on
multiple columns:



![](images/MultipleColumnSortDialog.png)


With multiple sorted columns, you may change the direction of any individual
sort column by left-clicking that column.



> **Tip:** To remove a sort column from a multiple column sort, Ctrl-left-click that column.
This will even work when only one column is sorted, thus effectively disabling
sorting for the table . Disabling sorting can greatly increase the
table's performance when the number of rows is large


> **Note:** It is possible to cancel some tables while they are loading or sorting their data.
If this happens, you can trigger a reload of the data by sorting on one of the
columns.


## Choosing Columns


![](images/SelectColumnsDialog.png)


The **Select Columns** dialog allows you to change the columns visible for a given
table.  The dialog shows a table of columns that are available.  At the very least, you
may turn off columns that you do not wish to see.  Additionally, the table you are using
may support discoverable column types.  If this is the case, they you will see
additional columns appear in the table.  Discovered columns will be marked as
**Non-default** in the **Is Default?** table column.


## Column Settings


Some columns allow you to alter the settings of the column, which will change how the
column displays its data.  As an example, consider the **Bytes Settings** dialog below:


![](images/BytesSettingsDialog.png)


This dialog allows you to change various features of the bytes column, such as endianness
and the number of bytes that appear in the display.


## Copy


This action will copy the contents of the **selected rows** into the system clipboard
in a space-separated format.  This data will **not** include the column names.


## Copy Current Column


This action will copy only the contents of the cell in the current column of the current
row.  To use this action, you must first click the cell you wish to copy in order to
make that cell's column the selected column.


## Copy Columns...


This action works the same as the copy action with the added ability to restrict the
columns that are copied.


## Export to CSV Text File


Exports the current table to a comma-separated value (CSV) text file. The CSV file
will export the selected columns in the order displayed.  The first row of ouput will
contain the table's column names.




![](../shared/note.yellow.png)This action uses the current
table selection when deciding what to export.  If no row is selected, then  no data is
exported.  To select all rows, use the **Select All** action or press **Ctrl-A** on
the keyboard.


## Export to CSV Text File by Columns...


This action is the same as the **Export to CSV Text File** action but adds the
additional ability to pick which columns get exported.


## Select All


This action will select all rows in the table.


extra space at the bottom of the page (for readability)


**Related Topics:**


- [Table Filtering](../Trees/GhidraTreeFilter.md)
