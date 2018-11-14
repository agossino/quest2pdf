#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

def getText(file_name):
    with open(file_name, 'r') as csvfile:
        reader = DictReader(csvfile)
        rows = [row for row in reader]
    return rows

def setDictionary(row):
    '''Give the right format for SimpleTest argument.
    '''
    output = {'question': row['question'],
              'image': row['image']
              }
    
    answerKeys = ('A', 'B', 'C', 'D')
    answers = [row[key] for key in answerKeys]

    output['answers'] = answers
    
    return output

def _get_param():
    param = {'log file name': 'loggingConf.json',
             'doc title': '18UH90Ageninfo',
             'test file name': 'questFile/geninfotest25-30.csv',
             'output doc number': 2
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

def main():
    param = _get_param()

    logger = _start_logger(param['log file name'])
    
    hms = datetime.now().strftime('%H-%M-%S')
    correctFile = ''.join((param['doc title'], '-correct-', hms)) + '.txt'
    logger.debug('correction file: ' + correctFile)

    text = getText(param['test file name'])
    logger.debug('text[0]: ' + str(text[0]))
                 
    dictLst = [setDictionary(row) for row in text]
    logger.debug('dictLst[0]: ' + str(dictLst[0]))
    
    for i in range(param['output doc number']):
        story = []
        # %f are microseconds, because of [:-4], last digits are cs
        now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        fileName = ''.join((param['doc title'], '-', now))[:-4] + '.pdf'
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
    main()

