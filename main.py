from tkinter import *
import win32clipboard
import re
import pyHook

def getClipboard():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data

def setClipboard(data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(data)
    win32clipboard.CloseClipboard()

def performReg(reg):
    reg = re.compile(reg)
    text = getClipboard()
    result = reg.findall(text)[0]
    #TODO Add Notification that Modification was made
    setClipboard(result)
    return result

def OnKeyboardEvent(event):
    ctrl_pressed = pyHook.GetKeyState(162) == 128
    alt_pressed = pyHook.GetKeyState(164) == 128
    letter_pressed = pyHook.HookConstants.IDToName(event.KeyID) == 'V'
    if ctrl_pressed and alt_pressed and letter_pressed:
        performReg("x")
        print("Success")
    return True

hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()

root = Tk()

w = Label(root, text="Hello!")
w.pack()

root.mainloop()
