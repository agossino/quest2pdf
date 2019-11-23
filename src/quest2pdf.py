#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import parameter
from filereader import CSVReader
from tkinter import Menu, Label, YES, BOTH
from guimixin import MainWindow
from exam import ExamDoc
import _thread, queue

LOGNAME = 'quest2pdf'
LOGGER = logging.getLogger(LOGNAME)

def main():
    """Reads parameter and start loop.
    """
    param = parameter.param_parser()
    LOGGER.debug(str(param))

    c = contentmix()
    c.mainloop()


class contentmix(MainWindow):
    def __init__(self):
        MainWindow.__init__(self, __file__)
        self.data_queue = queue.Queue()
        self.geometry("500x500")
        wellcome = "Da tabella a PDF: converte un file di domande"
        wellcome += "a scelta multipla in formato Comma Separated Value in PDF."
        Label(self, text=wellcome, wraplength=500).pack(expand=YES, fill=BOTH)
        menu = Menu(self)
        self.config(menu=menu)
        file = Menu(menu)
        file.add_command(label='Apri', command=self.read_input_file)
        file.add_command(label='Termina', command=self.quit)
        menu.add_cascade(label='File', menu=file)

    def read_input_file(self):
        input_file = self.select_openfile()
        _thread.start_new_thread(self.to_pdf, (input_file,))

    def to_pdf(self, input_file):
        try:
            file_content = CSVReader(input_file,
                                     param['encoding'],
                                     param['delimiter'])

            list_of_records = file_content.to_dictlist()
        except Exception as err:
            self.errorbox(err)
            raise

        if not list_of_records:
            LOGGER.debug("first row empty.")
            exit(1)

        try:
            exam = ExamDoc(list_of_records,
                           nDoc=param['number'],
                           examFile=param['exam'],
                           correctionFile=param['correction'],
                           to_shuffle=param['shuffle'],
                           heading=param['page_heading']
                           )
            exam.close()
        except Exception as err:
            self.errorbox(err)
            raise

        self.data_queue.put("end")


if __name__ == '__main__':
    main()
