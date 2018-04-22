from tkinter import *
import win32clipboard
import re
import keyboard
import threading
from win10toast import ToastNotifier

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

def showNotification(toaster, title, msg):
    toaster.show_toast(title, msg,
                       icon_path="icon/frogicon.ico",
                       duration=5,
                       threaded=True)

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
        Label(self.master,text="Enter regex:").pack()
        self.regexEntry = Entry(self.master, bd = 5)
        self.regexEntry.pack(pady=10,fill=X)

        self.regexButton = Button(self.master, text="Set Regex", command = self.setRegexEntry)
        self.regexButton.pack(pady=5)

        #hotkey entry
        Label(self.master,text="Enter hotkey:").pack()
        self.hotkeyEntry = Entry(self.master, bd = 5, textvariable = hotkeyVar)
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

        #Display Labels
        self.regexLabel = Label(self.master, textvariable = regexVar)
        self.regexLabel.pack(pady=5)
        self.hotkeyLabel = Label(self.master, textvariable = hotkeyVar)
        self.hotkeyLabel.pack(pady=5)


        #menu
        menu = Menu(self.master)
        self.master.config(menu=menu)
        file = Menu(menu)
        file.add_command(label="Exit", command = exit)
        menu.add_cascade(label="File", menu=file)

    def setRegexEntry(self):
         regexVar.set(self.regexEntry.get())

    def performReg(self):
        reg = re.compile(regexVar.get())
        text = getClipboard()
        result = reg.findall(text)
        if len(result) != 0:
            setClipboard("\n".join(result))
            showNotification(toaster, "Success!", "\n".join(result))
            print(result)
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

        try:
            hotkey = self.getHotKeyString()
            keyboard.add_hotkey(hotkey, self.performReg)
            #hotkeyVar.set(hotkey)
            print("Hotkey set to %s" % hotkey)
        except ValueError:
            print("Error getting hotkey, setting default: Ctrl+Alt+V")
            keyboard.add_hotkey("ctrl+alt+v", self.performReg)

def limitSizeHotkeyVar(*args):
    value =  hotkeyVar.get()
    if len(value) > 1: hotkeyVar.set(value[:1])

root = Tk()
regexVar = StringVar()
regexVar.set("")
hotkeyVar = StringVar()
hotkeyVar.set("")
hotkeyVar.trace('w', limitSizeHotkeyVar)

varChAlt = BooleanVar()
varChShift = BooleanVar()
varChCtrl = BooleanVar()


#root.geometry("400x300")


"""toaster.show_toast("Hello World!!!",
                   "Python is 10 seconds awsm!",
                   icon_path="icon/frogicon.ico",
                   duration=10,
                   threaded=True)
toaster.show_toast("Example two",
                   "This notification is in it's own thread!",
                   icon_path=None,
                   duration=5,
                   threaded=True)"""

toaster = ToastNotifier()
app = Window(root)

root.mainloop()
