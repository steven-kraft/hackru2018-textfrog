from tkinter import *
import win32clipboard
import re
import keyboard
import threading

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

def hotkeyCheck():
    keyboard.add_hotkey("ctrl+alt+v", performReg, args=("x"))
    keyboard.wait()

t = threading.Thread(target=hotkeyCheck)
t.daemon = True
t.start()

root = Tk()

w = Label(root, text="Hello!")
w.pack()

root.mainloop()
