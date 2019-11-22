#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import parameter
from filereader import CSVReader
from tkinter import Button, mainloop
from guimixin import MainWindow
from exam import ExamDoc

logName = 'quest2pdf'
logger = logging.getLogger(logName)

class contentmix(MainWindow):
    def __init__(self):
        MainWindow.__init__(self, 'mixin', 'Main')
        Button(self, text="open", command=self.read_input_file).pack()
        Button(self, text='Say hello', command=self.say_hello).pack()
        Button(self, text='Quit', command=self.quit).pack()
        Button(self, text='Fast quit', command=self.destroy).pack()

    def say_hello(self):
        self.infobox("Hello box", "Hello!!")

    def read_input_file(self):
        param = parameter.param_parser()
        input_file = self.enter_openfile()
        file_content = CSVReader(input_file,
                                 param['encoding'],
                                 param['delimiter'])
        list_of_records = file_content.to_dictlist()

        if list_of_records:
            logger.debug("first row: %s", str(list_of_records[0]))
        else:
            logger.debug("first row empty.")
            exit(1)

        exam = ExamDoc(list_of_records,
                       nDoc=param['number'],
                       examFile=param['exam'],
                       correctionFile=param['correction'],
                       to_shuffle=param['shuffle'],
                       heading=param['page_heading']
                       )
        exam.close()


if __name__ == '__main__':
    c = contentmix()
    c.mainloop()

# def main():
#     param = parameter.param_parser()
#     logger.debug(str(param))
#
#     root = Tk()
#     root.title("File Opener")
#     label = Label(root, text="I'm BATMAN!!!", foreground="red", font=("Helvetica", 16))
#     label.config(height=10, width=20)
#     label.pack()
#
#     menu = Menu(root)
#     root.config(menu=menu)
#
#     file = Menu(menu)
#
#     file.add_command(label='Open', command=open_file)
#     file.add_command(label='Exit', command=lambda: exit())
#
#     menu.add_cascade(label='File', menu=file)
#
#     root.mainloop()
