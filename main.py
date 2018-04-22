from tkinter import *
import win32clipboard
import re
import keyboard
import threading
from win10toast import ToastNotifier

def getClipboard():
    win32clipboard.OpenClipboard()
    try:
        data = win32clipboard.GetClipboardData()
    except TypeError:
        data = ""
    win32clipboard.CloseClipboard()
    return data

def setClipboard(data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(data)
    win32clipboard.CloseClipboard()

def showNotification(toaster, title, msg):
    toaster.show_toast(title, msg,
                       icon_path="icon/frogicon.ico",
                       duration=5,
                       threaded=True)

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.setHotkey()

    def init_window(self):

        self.master.title("TextFrog")

        self.pack(fill=BOTH, expand=1)

        #regex entry
        Label(self.master,text="Enter regex:").pack()
        self.regexEntry = Entry(self.master, bd = 5)
        self.regexEntry.pack(pady=10,fill=X)

        self.regexButton = Button(self.master, text="Set Regex", command = self.setRegexEntry)
        self.regexButton.pack(pady=5)

        #hotkey entry
        Label(self.master,text="Enter hotkey:").pack()
        self.hotkeyEntry = Entry(self.master, bd = 5, textvariable = keyVar)
        self.hotkeyEntry.pack(pady=10,fill=X)

        #Alt Shift Ctrl
        self.chAlt = Checkbutton(self.master, text="Alt", variable=varChAlt, onvalue = True, offvalue = False, height=1, width = 20)
        self.chAlt.pack(anchor = W)

        self.chShift = Checkbutton(self.master, text="Shift", variable=varChShift, onvalue = True, offvalue = False, height=1, width = 20)
        self.chShift.pack(anchor = W)

        self.chCtrl = Checkbutton(self.master, text="Ctrl", variable=varChCtrl, onvalue = True, offvalue = False, height=1, width = 20)
        self.chCtrl.pack(anchor = W)

        self.hotkeyButton = Button(self.master, text="Set HotKey", command = self.setHotkey)
        self.hotkeyButton.pack(pady=5)

        #Radio buttons
        self.ResultsLabel = Label(self.master, text = "Separate results by:")
        self.ResultsLabel.pack(pady=5)
        self.rButton1 = Radiobutton(self.master, text="New Line (\\n)", variable=resultVar, value=0)
        self.rButton1.pack( anchor = W )
        self.rButton2 = Radiobutton(self.master, text="Comma (,)", variable=resultVar, value=1)
        self.rButton2.pack( anchor = W)


        #Display Labels
        self.regexLabel = Label(self.master, textvariable = regexVar)
        self.regexLabel.pack(pady=5)
        self.hotkeyLabel = Label(self.master, textvariable = hotkeyVar)
        self.hotkeyLabel.pack(pady=5)

    #def resultSel(self):
        #selection = "You selected the option " + str(var.get())
        #self.ResultsLabel.config(text = selection)

    def setRegexEntry(self):
        try:
            re.compile(self.regexEntry.get())
            regexVar.set(self.regexEntry.get())
        except:
            #TODO Set Error Message in Regex Label Area
            pass


    def performReg(self):
        print("Performing Text Manipulation")
        reg = re.compile(regexVar.get())
        text = getClipboard()
        result = reg.findall(text)
        result = list(filter(None, result))
        if len(result) != 0:
            setClipboard("\n".join(result))
            showNotification(toaster, "Success!", "\n".join(result))
            print(result)
        else:
            showNotification(toaster, "No Match!", "")
        return result

    def getHotKeyString(self):
        modifiers = []
        if varChCtrl.get(): modifiers.append("Ctrl")
        if varChAlt.get(): modifiers.append("Alt")
        if varChShift.get(): modifiers.append("Shift")
        modifiers.append(self.hotkeyEntry.get())
        return "+".join(modifiers)

    def setHotkey(self):
        try:
            keyboard.unhook_all()
        except AttributeError:
            print("Hotkey not set, setting one now.")

        default = "Ctrl+Alt+V"
        try:
            hotkey = self.getHotKeyString()
            keyboard.add_hotkey(hotkey, self.performReg)
            hotkeyVar.set(hotkey)
            print("Hotkey set to %s" % hotkey)
        except ValueError:
            print("Error getting hotkey, setting default: Ctrl+Alt+V")
            keyboard.add_hotkey(default, self.performReg)
            hotkeyVar.set(default)

def limitSizeKeyVar(*args):
    value =  keyVar.get()
    if len(value) > 1: keyVar.set(value[-1])
    keyVar.set(keyVar.get().upper())

root = Tk()
root.resizable(False, False)
regexVar = StringVar()
hotkeyVar = StringVar()
resultVar = IntVar()

keyVar = StringVar()
keyVar.trace('w', limitSizeKeyVar)

varChAlt = BooleanVar()
varChShift = BooleanVar()
varChCtrl = BooleanVar()

#root.geometry("400x300")

toaster = ToastNotifier()
app = Window(root)

root.mainloop()
