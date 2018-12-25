#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys

from reportlab.lib.pagesizes import  A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (SimpleDocTemplate, Paragraph,
                                Spacer, PageTemplate, Frame)
from reportlab.lib.units import mm
from exam import Exam

from csv import DictReader
from random import shuffle
from datetime import datetime

import logging
import json
from logging.config import dictConfig

from multiquest import MultiQuest
from numberedcanvas import NumberedCanvas

__version__ = '0.1'

def getText(file_name):
    with open(file_name, 'r') as csvfile:
        reader = DictReader(csvfile)
        rows = [row for row in reader]
    return rows

def get_parser():
    description = "genera PDF da un file di prova d'esame (domande a risposta multipla, vero o falso ecc.) in formato csv"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('input', type=str, nargs='?',
                        help='nome del file di input di domande e risposte in formato csv (predefinito questions.csv)',
                        default='questions.csv')
    parser.add_argument('n', type=int, nargs='?',
                        help='numero dei file di output da generare', default=1)
    parser.add_argument('-p', '--prefix',
                        help='prefisso per il file di output: se non definito è Quest, seguono data e orario fino a ms.',
                        type=str, default='Quest')
    parser.add_argument('-l', '--logfile', help='file di log (predefinito loggingConf.json)',
                        action='store_true', default='loggingConf.json')
    parser.add_argument('-v', '--version', help='mostra la corrente versione di quest2pdf',
                        action='store_true')
    return parser

def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(__version__)
        sys.exit()

    param = {'log file name': 'loggingConf.json',
             'prefix': args['prefix'],
             'input file name': args['input'],
             'output doc number': args['n']
             }
    return param

def _start_logger(fileName):
    try:
        with open(fileName, 'r') as fd:
                loggerConf = json.load(fd)
    except FileNotFoundError:
        print('file di log' + fileName + " non trovato: indicare un file di log con l'opzione -l")
        raise

    dictConfig(loggerConf)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    return logger


def main(param):
    logger = _start_logger(param['log file name'])

    logger.debug(str(param))
    
    logger.debug('correction file: ' + correctFile)

    text = getText(param['input file name'])
    logger.debug('text[0]: ' + str(text[0]))

    author = 'Giancarlo Ossino'
    title = 'Esame intermedio'
    subject = 'Formazione'

    exam = Exam(text)
    
    for i in range(param['output doc number']):
        story = []
        # %f are microseconds, because of [:-4], last digits are cs
        now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        fileName = ''.join((param['prefix'], '-', now))[:-4] + '.pdf'
        logger.debug('filename: ' + fileName)

        doc = SimpleDocTemplate(fileName, pagesize=A4, allowSplitting=0,
                                author=author, title=title, subject=subject)

##        main_frame = get_main_frame(doc)

        questions = MultiQuest(dictLst)

        for f in questions.get_flowables():
            story.append(f)
            story.append(Spacer(mm, mm*20))

##        doc.addPageTemplates([PageTemplate(id='1Col', frames=main_frame)])
        print(reportlab.ascii())
        doc.build(story, onFirstPage=_header1,
                  onLaterPages=_header, canvasmaker=NumberedCanvas)
    
    return

if __name__ == '__main__':
    param = command_line_runner()
    main(param)
