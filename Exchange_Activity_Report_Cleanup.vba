Sub DeleteSpecificColumns()
    Dim ws As Worksheet
    On Error Resume Next ' Prevent macro from stopping on errors
    Set ws = ThisWorkbook.Sheets("Sheet1") ' Change "Sheet1" to your actual sheet name
    
    If ws Is Nothing Then
        MsgBox "Worksheet not found! Please check the name.", vbCritical
        Exit Sub
    End If
    On Error GoTo 0 ' Reset error handling

    ' List of columns to delete, in reverse order
    Dim columnsToDelete As Variant
    columnsToDelete = Array("AF", "AE", "AD", "AC", "X", "S", "R", "Q", _
                            "P", "J", "I", "H", "G", "E", "D", "C", "B", "A")
    
    Dim i As Integer
    For i = LBound(columnsToDelete) To UBound(columnsToDelete)
        On Error Resume Next ' Skip missing columns
        ws.Columns(columnsToDelete(i)).Delete
        On Error GoTo 0
    Next i

    MsgBox "Specified columns have been deleted successfully.", vbInformation
End Sub
