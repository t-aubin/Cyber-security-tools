'-Steps to Implement
'-Rename Sheet to Sheet1
'-Open VBA Editor:

'-Press Alt + F11 in Excel.
'-Insert the Script:

'-Click Insert > Module and paste the code above.
'-Run the Macro:

'-Press Alt + F8, select DeleteSpecifiedColumns, and click Run.

'-Remove module and save 

Sub DeleteSpecifiedColumns()
    Dim ws As Worksheet
    On Error Resume Next ' Continue even if an error occurs
    Set ws = ThisWorkbook.Sheets("Sheet1") ' Change "Sheet1" to your actual sheet name
    
    If ws Is Nothing Then
        MsgBox "Worksheet not found! Please check the name.", vbCritical
        Exit Sub
    End If
    On Error GoTo 0 ' Stop ignoring errors after this point

    ' List of columns to delete, in reverse order
    Dim columnsToDelete As Variant
    columnsToDelete = Array("AR", "AQ", "AP", "AO", "AN", "AM", "AL", "AK", _
                            "AJ", "AI", "AG", "AF", "AE", "AD", "AC", "AB", _
                            "AA", "Z", "Y", "X", "W", "T", "S", "Q", "P", _
                            "O", "N", "M", "L", "C")
    
    Dim i As Integer
    For i = LBound(columnsToDelete) To UBound(columnsToDelete)
        On Error Resume Next ' Skip missing columns
        ws.Columns(columnsToDelete(i)).Delete
        On Error GoTo 0
    Next i

    MsgBox "Specified columns have been deleted successfully.", vbInformation
End Sub
