from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import  A4

from csv import DictReader
from random import shuffle
from datetime import datetime
from platform import node
from os import getlogin

import logging
import json
from logging.config import dictConfig

from simpletest import SingleTest
from multitest import MultiTest

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

def main():
    fname = 'loggingConf.json'

    with open(fname, 'r') as fd:
        loggerConf = json.load(fd)

    dictConfig(loggerConf)
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    n = 10

    host = node()
    user = getlogin()
    
    testFile = 'testFile/45MDStest.csv'
    hms = datetime.now().strftime('%H-%M-%S')
    correctFile = ''.join((user, '-', host, '-correct-', hms)) + '.txt'
    logger.debug('correction file: ' + correctFile)

    text = getText(testFile)
    logger.debug('text[0]: ' + str(text[0]))
                 
    dictLst = [setDictionary(row) for row in text]
    logger.debug('dictLst[0]: ' + str(dictLst[0]))
    
    for i in range(n):
        story = []
        # %f are microseconds, because of [:-4], last digits are cs
        now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        fileName = ''.join((user, '-', host, '-', now))[:-4] + '.pdf'
        logger.debug('filename: ' + fileName)

        c = Canvas(fileName, pagesize=A4)
        c.setAuthor('Giancarlo Ossino')
        c.setTitle('Esame intermedio')
        c.setSubject('Formazione')

        tests = MultiTest(dictLst, c)
        tests.setHeader('file: ' + fileName)
        tests.save()

        with open(correctFile, 'a') as fd:
            fd.write(fileName + '\n')
            fd.write(tests.__str__())
    
    return

if __name__ == '__main__':
    main()

