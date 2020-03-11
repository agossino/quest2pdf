#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import parameter
from tkinter import Menu, Label, YES, BOTH
import _thread, queue
from pathlib import Path
from typing import Mapping, Dict, Any
from filereader import CSVReader
from guimixin import MainWindow
from exam import Exam
from export import SerializeExam, RLInterface
import utility
from _version import __version__


LOGNAME = 'quest2pdf'
LOGGER = logging.getLogger(LOGNAME)


def main():
    """Reads parameter and start loop.
    """
    param: Dict[str, Any] = parameter.param_parser()
    LOGGER.debug(str(param))

    c = contentmix(param)
    c.mainloop()


class contentmix(MainWindow):
    def __init__(self, app_parameters: Mapping[str, str]):
        """Get application parameters and show the main window.
        """
        self.parameters = app_parameters
        MainWindow.__init__(self, Path(__file__).stem)
        self.data_queue = queue.Queue()
        self.geometry("500x500")
        wellcome = "Da tabella a PDF: genera un file di domande "
        wellcome += "a scelta multipla in formato PDF, a partire "
        wellcome += "da un file in formato Comma Separated Value."
        Label(self, text=wellcome, wraplength=500).pack(expand=YES, fill=BOTH)

        menu = Menu(self)
        self.config(menu=menu)
        file = Menu(menu)

        file.add_command(label="Converti", command=self.read_input_file)
        file.add_command(label="Configura", command=self.notdone)
        file.add_command(label="Termina", command=self.quit)
        menu.add_cascade(label="File", menu=file)

        info = Menu(menu)
        info.add_command(label="Guida", command=self.show_handbook)
        info.add_command(label="Versione", command=self.show_version)
        menu.add_cascade(label="Info", menu=info)

    def read_input_file(self):
        while True:
            input_file, output_folder = self.enter_openfile()
            if input_file and output_folder:
                _thread.start_new_thread(self.to_pdf, (input_file, output_folder))
                break
            # TODO in case of abort, exit from this dialog
            self.errorbox("Indicare sorgente e destinazione")

    def to_pdf(self, input_file, output_folder):
        try:
            file_content = CSVReader(input_file,
                                     self.parameters['encoding'],
                                     self.parameters['delimiter'])

            list_of_records = file_content.to_dictlist()
        except Exception as err:
            LOGGER.critical("CSVReader failed: %s %s",
                            err.__class__, err)
            self.errorbox(utility.exception_printer(err))
            raise

        if not list_of_records:
            LOGGER.warning("Empty rows.")
            self.errorbox("dati non validi")
            return

        utility.add_path_to_image(Path(input_file).parent,
                                  list_of_records)

        try:
            exam = Exam()
            exam.attribute_selector = ("question", "subject", "image", "void",
                                       "A", "void", "B", "void",
                                       "C", "void", "D", "void")
            exam.load(list_of_records)
            serial_exam = SerializeExam(exam)
            to_pdf_interface = RLInterface(serial_exam.assignment(),
                                           Path("exam.pdf"),
                                           nDoc=self.parameters['number'],
                                           exam_filename=self.parameters['exam'],
                                           correction_filename=self.parameters['correction'],
                                           destination=output_folder,
                                           to_shuffle=self.parameters['shuffle'],
                                           heading=self.parameters['page_heading']
                                           )
            to_pdf_interface.build()
        except Exception as err:
            LOGGER.critical("CSVReader failed: %s %s",
                            err.__class__, err)
            self.errorbox(utility.exception_printer(err))
            raise
        self.infobox("Avviso", "Conversione effettuata")

        self.data_queue.put("end")

    def show_version(self) -> None:
        """Show application version
        """
        self.infobox("Versione", "{app_name}: {version}".format(app_name=Path(__file__).stem,
                                                                version=__version__))

    def show_handbook(self) -> None:
        """Show handbook/how-to (long text).
        """
        help_file_name: str = "help.txt"
        script_path: Path = Path(__file__).resolve().parent
        try:
            self.handbook(str(script_path.joinpath(help_file_name)))
        except Exception as err:
            LOGGER.critical("Handbook opening failed: %s %s",
                            err.__class__, err)
            self.errorbox(utility.exception_printer(err))
            raise


if __name__ == "__main__":
    main()