"""
Example 10-10. PP4E\Gui\ShellGui\packdlg.py
popup a GUI dialog for packer script arguments, and run it
"""

from tkinter import *
import parameter
from filereader import CSVReader
from exam import ExamDoc
from formrows import make_form_row


def pack_dialog():  # a new top-level window
    win = Toplevel()  # with 2 row frames + ok button
    win.title("Seleziona il file delle domande")
    selection = make_form_row(win, label='file delle domande')
    Button(win, text='OK', command=win.destroy).pack()
    win.grab_set()
    win.focus_set()  # go modal: mouse grab, keyboard focus, wait
    win.wait_window()  # wait till destroy; else returns now
    return selection.get()  # fetch linked var values


def run_pack_dialog():
    selection = pack_dialog()
    param = parameter.param_parser()
    input_file = CSVReader(param['input'],
                           param['encoding'],
                           param['delimiter'])
    text = input_file.to_dictlist()

    if text:
        logger.debug("first row: %s", str(text[0]))
    else:
        logger.debug("first row empty.")
        exit(1)

    exam = ExamDoc(text,
                   nDoc=param['number'],
                   examFile=param['exam'],
                   correctionFile=param['correction'],
                   to_shuffle=param['shuffle'],
                   heading=param['page_heading']
                   )

    exam.close()


if __name__ == '__main__':
    root = Tk()
    Button(root, text='popup', command=run_pack_dialog).pack(fill=X)
    Button(root, text='bye', command=root.quit).pack(fill=X)
    root.mainloop()
