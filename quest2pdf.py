#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import  A4

from csv import DictReader
from random import shuffle
from datetime import datetime

import logging
import json
from logging.config import dictConfig

from singlequest import SingleQuest
from multiquest import MultiQuest

__version__ = '0.0'

def getText(file_name):
    with open(file_name, 'r') as csvfile:
        reader = DictReader(csvfile)
        rows = [row for row in reader]
    return rows

def setDictionary(row):
    '''Give the right format for SimpleTest argument.
    '''
    output = {'category': row['category'],
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
                        help='nome del file di input di domande e risposte in formato csv',
                        default='questions.csv')
    parser.add_argument('n', type=int, nargs='?',
                        help='numero dei file di output da generare', default=1)
    parser.add_argument('-p', '--prefix',
                        help='prefisso per il file di output: se non definito è Quest, seguono data e orario fino a ms.',
                        type=str, default='Quest')
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
        print('file ' + fileName + ' not found.')

    dictConfig(loggerConf)
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    return logger

def main(param):
    logger = _start_logger(param['log file name'])

    logger.debug(str(param))
    
    hms = datetime.now().strftime('%H-%M-%S')
    correctFile = ''.join((param['prefix'], '-correct-', hms)) + '.txt'
    logger.debug('correction file: ' + correctFile)

    text = getText(param['input file name'])
    logger.debug('text[0]: ' + str(text[0]))
                 
    dictLst = [setDictionary(row) for row in text]
    logger.debug('dictLst[0]: ' + str(dictLst[0]))
    
    for i in range(param['output doc number']):
        story = []
        # %f are microseconds, because of [:-4], last digits are cs
        now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        fileName = ''.join((param['prefix'], '-', now))[:-4] + '.pdf'
        logger.debug('filename: ' + fileName)

        c = Canvas(fileName, pagesize=A4)
        c.setAuthor('Giancarlo Ossino')
        c.setTitle('Esame intermedio')
        c.setSubject('Formazione')

        tests = MultiQuest(dictLst, c)
        tests.setHeader('file: ' + fileName +
                        ' Firma esaminando:______________')
        tests.save()

        with open(correctFile, 'a') as fd:
            fd.write(fileName + '\n')
            fd.write(tests.__str__())
    
    return

if __name__ == '__main__':
    param = command_line_runner()
    main(param)
