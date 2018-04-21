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

class Window(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.setHotkey()

    def init_window(self):

        self.master.title("TextFrog")

        self.pack(fill=BOTH, expand=1)

        #regex entry
        self.regexEntryLabel = Label(self.master,text="Enter regex:")
        self.regexEntryLabel.pack()
        self.regexEntry = Entry(self.master, bd = 5)
        self.regexEntry.pack(pady=10,fill=X)

        self.regexButton = Button(self.master, text="Set Regex", command = self.setRegexEntry)
        self.regexButton.pack(pady=5)

        #hotkey entry
        self.hotkeyEntryLabel = Label(self.master,text="Enter hotkey:")
        self.hotkeyEntryLabel.pack()
        self.hotkeyEntry = Entry(self.master, bd = 5)
        self.hotkeyEntry.pack(pady=10,fill=X)

        self.hotkeyButton = Button(self.master, text="Set HotKey", command = self.setHotkeyEntry)
        self.hotkeyButton.pack(pady=5)

        #Display Labels
        self.regexLabel = Label(self.master, textvariable = regexVar)
        self.regexLabel.pack(pady=5)
        self.hotkeyLabel = Label(self.master, textvariable = hotkeyVar)
        self.hotkeyLabel.pack(pady=5)
        self.ascLabel = Label(self.master, textvariable = ascVar)
        self.ascLabel.pack()

        #radio buttons
        self.rAlt = Radiobutton(self.master, text="Alt", variable=ascVar, value="Alt",command=self.sel)
        self.rAlt.pack(anchor = W )

        self.rShift = Radiobutton(self.master, text="Shift", variable=ascVar, value="Shift",command=self.sel)
        self.rShift.pack(anchor = W )

        self.rCtrl = Radiobutton(self.master, text="Ctrl", variable=ascVar, value="Ctrl",command=self.sel)
        self.rCtrl.pack(anchor = W)

        #menu
        menu = Menu(self.master)
        self.master.config(menu=menu)
        file = Menu(menu)
        file.add_command(label="Exit", command = self.client_exit)
        menu.add_cascade(label="File", menu=file)

    def client_exit(self):
        exit()

    def setRegexEntry(self):
         regexVar.set(self.regexEntry.get())

    def setHotkeyEntry(self):
        hotkeyVar.set(self.hotkeyEntry.get())
        self.setHotkey()

    def sel(self):
        selection = str(ascVar.get())
        ascVar.set(selection)

    def getHotKeyString(self):
        #TODO return full hotkey string
        return hotkeyVar.get()

    def setHotkey(self):
        try:
            keyboard.unhook_all()
        except AttributeError:
            print("Hotkey not set, setting one now.")

        try:
            keyboard.add_hotkey(self.getHotKeyString(), performReg, args=[regexVar.get()])
        except ValueError:
            print("Error getting hotkey, setting default: Ctrl+Alt+V")
            keyboard.add_hotkey("ctrl+alt+v", performReg, args=[regexVar.get()])

root = Tk()
regexVar = StringVar()
regexVar.set("Default")
hotkeyVar = StringVar()
hotkeyVar.set("")

ascVar = StringVar()
ascVar.set("Default")
#root.geometry("400x300")

app = Window(root)

root.mainloop()
