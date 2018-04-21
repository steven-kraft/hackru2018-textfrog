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

class Window(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)

        self.master = master

        self.init_window()

    def init_window(self):

        self.master.title("TextFrog")

        self.pack(fill=BOTH, expand=1)

        #regex entry
        self.regexEntryLabel = Label(self.master,text="Enter regex:")
        self.regexEntryLabel.pack()
        self.regexEntry = Entry(self.master, bd = 5)
        self.regexEntry.pack(pady=10,fill=X)

        self.regexButton = Button(self.master, text="Set Regex", command = self.getRegexEntry)
        self.regexButton.pack(pady=5)

        #hotkey entry
        self.hotkeyEntryLabel = Label(self.master,text="Enter hotkey:")
        self.hotkeyEntryLabel.pack()
        self.hotkeyEntry = Entry(self.master, bd = 5)
        self.hotkeyEntry.pack(pady=10,fill=X)

        self.hotkeyButton = Button(self.master, text="Set HotKey", command = self.getHotkeyEntry)
        self.hotkeyButton.pack(pady=5)



        #Alt Shift Ctrl
        self.chAlt = Checkbutton(self.master, text="Alt", variable=varChAlt, onvalue = 1, offvalue = 0, height=1, width = 20)
        self.chAlt.pack(anchor = W )

        self.chShift = Checkbutton(self.master, text="Shift", variable=varChShift, onvalue = 1, offvalue = 0, height=1, width = 20)
        self.chShift.pack(anchor = W )

        self.chCtrl = Checkbutton(self.master, text="Ctrl", variable=varChCtrl, onvalue = 1, offvalue = 0, height=1, width = 20)
        self.chCtrl.pack(anchor = W)

        self.ascButton = Button(self.master, text = "Set Shift, Alt, Ctrl Keys")
        self.ascButton.pack(pady=5)

        #Display Labels
        self.regexLabel = Label(self.master, textvariable = regexVar)
        self.regexLabel.pack(pady=5)
        self.hotkeyLabel = Label(self.master, textvariable = hotkeyVar)
        self.hotkeyLabel.pack(pady=5)
        self.ascLabel = Label(self.master, textvariable = ascVar)
        self.ascLabel.pack()

        #menu
        menu = Menu(self.master)
        self.master.config(menu=menu)
        file = Menu(menu)
        file.add_command(label="Exit", command = self.client_exit)
        menu.add_cascade(label="File", menu=file)

    def client_exit(self):
        exit()

    def getRegexEntry(self):
         regexVar.set(self.regexEntry.get())

    def getHotkeyEntry(self):
        hotkeyVar.set(self.hotkeyEntry.get())

    def getascVar(self):
        """if varChAlt == 1:
            ascVar += "Alt "
        else:
            ascVar -= "Alt "
        if varChShift == 1:
            ascVar += "Shift "
        else:
            ascVar -= "Shift """



root = Tk()
regexVar = StringVar()
regexVar.set("Default")
hotkeyVar = StringVar()
hotkeyVar.set("Default")

varChAlt = IntVar()
varChShift = IntVar()
varChCtrl = IntVar()

ascVar = ""
#root.geometry("400x300")

app = Window(root)

root.mainloop()
