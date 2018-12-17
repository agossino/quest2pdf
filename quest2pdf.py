#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys

from reportlab.lib.pagesizes import  A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (SimpleDocTemplate, Paragraph,
                                Spacer, PageTemplate, Frame)
from reportlab.lib.units import mm

from csv import DictReader
from random import shuffle
from datetime import datetime

import logging
import json
from logging.config import dictConfig

from singlequest import SingleQuest
from multiquest import MultiQuest
from numberedcanvas import NumberedCanvas

__version__ = '0.1'

class Basedoc:
    def __init__(self, fileName):
        self.doc = SimpleDocTemplate(fileName)

        self.text = []

        self.styles = getSampleStyleSheet()

        return

    def addLines(self, lstOfLines):
        for line in lstOfLines:
            para = Paragraph(line+'\n', self.styles["Normal"])
            self.text.append(para)

        self.text.append(Spacer(mm, mm * 20)) 

        return

    def close(self):
        self.doc.build(self.text)
        return

def getText(file_name):
    with open(file_name, 'r') as csvfile:
        reader = DictReader(csvfile)
        rows = [row for row in reader]
    return rows

def setDictionary(row):
    '''Give the right format for SimpleTest argument.
    '''
    output = {'subject': row['subject'],
              'question': row['question'],
              'image': row['image']
              }
    
    answerKeys = ('A', 'B', 'C', 'D')
    answers = [row[key] for key in answerKeys]

    output['answers'] = answers
    
    return output

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

def get_main_frame(doc):
    return Frame(doc.leftMargin, doc.bottomMargin, doc.width,
                 doc.height, id='colF')

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

def _header_footer(canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()
 
        # Header
        header = Paragraph('This is a multi-line header.  It goes on every page.   ' * 5, styles['Normal'])
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)
 
        # Footer
        footer = Paragraph('This is a multi-line footer.  It goes on every page.   ' * 5, styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)
 
        # Release the canvas
        canvas.restoreState()

def main(param):
    logger = _start_logger(param['log file name'])

    logger.debug(str(param))
    
    hms = datetime.now().strftime('%H-%M-%S')
    correctFile = ''.join((param['prefix'], '-correct-', hms)) + '.pdf'
    logger.debug('correction file: ' + correctFile)

    text = getText(param['input file name'])
    logger.debug('text[0]: ' + str(text[0]))
                 
    dictLst = [setDictionary(row) for row in text]
    logger.debug('dictLst[0]: ' + str(dictLst[0]))

    baseDoc = Basedoc(correctFile)

    author = 'Giancarlo Ossino'
    title = 'Esame intermedio'
    subject = 'Formazione'
    
    for i in range(param['output doc number']):
        story = []
        # %f are microseconds, because of [:-4], last digits are cs
        now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        fileName = ''.join((param['prefix'], '-', now))[:-4] + '.pdf'
        logger.debug('filename: ' + fileName)

        doc = SimpleDocTemplate(fileName, pagesize=A4, allowSplitting=0,
                                author=author, title=title, subject=subject)

        main_frame = get_main_frame(doc)

        questions = MultiQuest(dictLst)

        for f in questions.get_flowables():
            story.append(f)
            story.append(Spacer(mm, mm*20))

        doc.addPageTemplates([PageTemplate(id='1Col', frames=main_frame)])
        doc.build(story, onFirstPage=_header_footer,
                  onLaterPages=_header_footer, canvasmaker=NumberedCanvas)
        
##        tests.setHeader('file: ' + fileName +
##                        ' Firma esaminando:______________')
##        tests.save()
##
##        text = fileName + '\n' + tests.__str__()
##
##        baseDoc.addLines(text.split('\n'))
##
##    baseDoc.close()
    
    return

if __name__ == '__main__':
    param = command_line_runner()
    main(param)
