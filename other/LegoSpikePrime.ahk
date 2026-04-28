/*
Lego SPIKE prime doesn't provide a keyboard shortcut for 
saving a file and when it saves it saves it in a binary format.
I want to save the source code to a text file instead of binary,
so this script copies all the text in the code window to a file
when you press control-s
*/

#Requires AutoHotkey v2
#SingleInstance Force

;this function reloads the script every time you save it via control-s
;(this is useful for any AutoHotkey script)
#HotIf WinActive("ahk")
~^s::{
    ToolTip("Reloading")
    Sleep 500
    Reload
}
#HotIf

;This actually does the thing explained at the top.
;It copies everything via control-a and control-c
#HotIf WinActive("SPIKE")
~^s::{
    static FileToSave := ""
    Send("^a^c")
    FileToSave := FileSelect("S", FileToSave)
    If StrLen(FileToSave) > 0{
        If FileExist(FileToSave){
            FileDelete(FileToSave)
        }
        FileAppend(A_Clipboard, FileToSave)
    }
}
F5::{
    Send "{Click 1855 940}"
}
#HotIf
