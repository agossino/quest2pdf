#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import parameter
from filereader import CSVReader
from tkinter import Menu
from guimixin import MainWindow
from exam import ExamDoc

logName = 'quest2pdf'
logger = logging.getLogger(logName)

class contentmix(MainWindow):
    def __init__(self):
        MainWindow.__init__(self, __file__)
        self.geometry("500x500")
        menu = Menu(self)
        self.config(menu=menu)
        file = Menu(menu)
        file.add_command(label='Apri', command=self.read_input_file)
        file.add_command(label='Termina', command=self.quit)
        menu.add_cascade(label='File', menu=file)
        # Button(self, text="Apri file", command=self.read_input_file).pack()
        # Button(self, text='Termina', command=self.quit).pack()

    def read_input_file(self):
        param = parameter.param_parser()
        input_file = self.enter_openfile()
        try:
            file_content = CSVReader(input_file,
                                     param['encoding'],
                                     param['delimiter'])
        except Exception as err:
            self.errorbox(err)
            raise

        try:
            list_of_records = file_content.to_dictlist()
        except Exception as err:
            self.errorbox(err)
            raise

        if not list_of_records:
            logger.debug("first row empty.")
            exit(1)

        try:
            exam = ExamDoc(list_of_records,
                           nDoc=param['number'],
                           examFile=param['exam'],
                           correctionFile=param['correction'],
                           to_shuffle=param['shuffle'],
                           heading=param['page_heading']
                           )
        except Exception as err:
            self.errorbox(err)
            raise

        try:
            exam.close()
        except Exception as err:
            self.errorbox(err)
            raise


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
