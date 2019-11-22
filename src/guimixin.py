"""
###############################################################################
a "mixin" class for other frames: common methods for canned dialogs,
spawning programs, simple text viewers, etc; this class must be mixed
with a Frame (or a subclass derived from Frame) for its quit method
###############################################################################
"""

from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

class GuiMixin:
    def infobox(self, title, text, *args):  # use standard dialogs
        return showinfo(title, text)  # *args for bkwd compat

    def errorbox(self, text):
        showerror('Error!', text)

    def question(self, title, text, *args):
        return askyesno(title, text)  # return True or False

    def notdone(self):
        showerror('Not implemented', 'Option not available')

    def quit(self):
        ans = self.question('Verify quit', 'Are you sure you want to quit?')
        if ans:
            Frame.quit(self)  # quit not recursive!

    def help(self):
        self.infobox('RTFM', 'See figure 1...')  # override this better

    def select_openfile(self, file="", dir="."):  # use standard dialogs
        return askopenfilename(initialdir=dir, initialfile=file)

    def select_savefile(self, file="", dir="."):
        return asksaveasfilename(initialfile=file, initialdir=dir)

    def clone(self, args=()):  # optional constructor args
        new = Toplevel()  # make new in-process version of me
        myclass = self.__class__  # instance's (lowest) class object
        myclass(new, *args)  # attach/run instance to new window

    def browser(self, filename):  # if tkinter.scrolledtext
        new = Toplevel()  # included for reference
        text = ScrolledText(new, height=30, width=85)
        text.config(font=('courier', 10, 'normal'))
        text.pack(expand=YES, fill=BOTH)
        new.title("Text Viewer")
        new.iconname("browser")
        text.insert('0.0', open(filename, 'r').read())

    def enter_openfile(self):  # a new top-level window
        win = Toplevel()  # with 2 row frames + ok button
        win.title("Seleziona il file delle domande")
        selection = self._form_row(win, label='file delle domande')
        Button(win, text='OK', command=win.destroy).pack()
        win.grab_set()
        win.focus_set()  # go modal: mouse grab, keyboard focus, wait
        win.wait_window()  # wait till destroy; else returns now
        return selection.get()  # fetch linked var values

    """"
    Example 10-9. PP4E\Gui\ShellGui\formrows.py
    create a label+entry row frame, with optional file open browse button;
    this is a separate module because it can save code in other programs too;
    caller (or callbacks here): retain returned linked var while row is in use;
    """

    def _form_row(self, parent, label, width=15, browse=True, extend=False):
        var = StringVar()
        row = Frame(parent)
        lab = Label(row, text=label + '?', relief=RIDGE, width=width)
        ent = Entry(row, relief=SUNKEN, textvariable=var)
        row.pack(fill=X)  # uses packed row frames
        lab.pack(side=LEFT)  # and fixed-width labels
        ent.pack(side=LEFT, expand=YES, fill=X)  # or use grid(row, col)
        if browse:
            btn = Button(row, text='browse...')
            btn.pack(side=RIGHT)
            if not extend:
                btn.config(command=
                           lambda: var.set(self.select_openfile() or var.get()))
            else:
                btn.config(command=
                           lambda: var.set(var.get() + ' ' + self.select_openfile()))
        return var

"""
###############################################################################
Classes that encapsulate top-level interfaces.
Allows same GUI to be main, pop-up, or attached; content classes may inherit
from these directly, or be mixed together with them per usage mode; may also
be called directly without a subclass; designed to be mixed in after (further
to the right than) app-specific classes: else, subclass gets methods here
(destroy, okayToQuit), instead of from app-specific classes--can't redefine.
###############################################################################
"""

import os, glob
from tkinter import Tk, Toplevel, Frame, YES, BOTH, RIDGE

class _window:
    """
    mixin shared by main and pop-up windows
    """
    foundicon = None                                       # shared by all inst
    iconpatt  = '*.ico'                                    # may be reset
    iconmine  = 'py.ico'

    def configBorders(self, app, kind, iconfile):
        if not iconfile:                                   # no icon passed?
            iconfile = self.findIcon()                     # try curr,tool dirs
        title = app
        if kind: title += ' - ' + kind
        self.title(title)                                  # on window border
        self.iconname(app)                                 # when minimized
        if iconfile:
            try:
                self.iconbitmap(iconfile)                  # window icon image
            except:                                        # bad py or platform
                pass
        self.protocol('WM_DELETE_WINDOW', self.quit)       # don't close silent

    def findIcon(self):
        if _window.foundicon:                              # already found one?
            return _window.foundicon
        iconfile  = None                                   # try curr dir first
        iconshere = glob.glob(self.iconpatt)               # assume just one
        if iconshere:                                      # del icon for red Tk
            iconfile = iconshere[0]
        else:                                              # try tools dir icon
            mymod  = __import__(__name__)                  # import self for dir
            path   = __name__.split('.')                   # poss a package path
            for mod in path[1:]:                           # follow path to end
                mymod = getattr(mymod, mod)                # only have leftmost
            mydir  = os.path.dirname(mymod.__file__)
            myicon = os.path.join(mydir, self.iconmine)    # use myicon, not tk
            if os.path.exists(myicon): iconfile = myicon
        _window.foundicon = iconfile                       # don't search again
        return iconfile

class MainWindow(Tk, _window, GuiMixin):
    """
    when run in main top-level window
    """
    def __init__(self, app, kind='', iconfile=None):
        self.findIcon()
        Tk.__init__(self)
        self.__app = app
        self.configBorders(app, kind, iconfile)

    def quit(self):
        print("quit")
        if self.okayToQuit():                                # threads running?
            ans = self.question('Verify quit', 'Are you sure you want to quit?')
            if ans:
                self.destroy()                               # quit whole app
        else:
            self.showinfo(self.__app, 'Quit not allowed')    # or in okayToQuit?

    def destroy(self):                                       # exit app silently
        print("Destroy")
        Tk.quit(self)                                        # redef if exit ops

    def okayToQuit(self):                                    # redef me if used
        return True                                          # e.g., thread busy
