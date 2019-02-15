#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
import logging
import json
from logging.config import dictConfig

from exam import ExamDoc
from csv import DictReader

__version__ = '0.2'

def getText(file_name):
    with open(file_name, 'r') as csvfile:
        reader = DictReader(csvfile)
        rows = [row for row in reader]
    return rows

def get_parser():
    description = "genera PDF da un file di prova d'esame (domande a risposta multipla, vero o falso ecc.) in formato csv"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('input', type=str, nargs='?',
                        help='nome del file di input di domande e risposte in formato csv (predefinito domande.csv)',
                        default='domande.csv')
    parser.add_argument('n', type=int, nargs='?',
                        help='numero dei file di output da generare', default=1)
    parser.add_argument('-e', '--exam',
                        help='prefisso per il file con le domande (predefinito Esame); seguono data e orario fino a ms.',
                        type=str, default='Esame')
    parser.add_argument('-c', '--correction',
                        help="prefisso per il file correttore (predefinito Correttore); seguono data e orario fino a ms.",
                        type=str, default='Correttore')
    parser.add_argument('-l', '--conflogfile', help='file di configurazione del registro (predefinito loggingConf.json).',
                        default='loggingConf.json')
    parser.add_argument('-s', '--shuffle', help="se fornito mischia l'ordine delle domande",
                        action='store_true')
    parser.add_argument('-p', '--page_heading', help="testo di intestazione che compare all'inizio di ogni pagina (se non inidicato è il nome del file)",
                        nargs='?', const=True, default=False)
    parser.add_argument('-v', '--version', help='mostra la corrente versione di quest2pdf',
                        action='store_true')
    return parser

def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(__version__)
        sys.exit()

    param = {'conf log file name': args['conflogfile'],
             'exam': args['exam'],
             'correction': args['correction'],
             'input file name': args['input'],
             'output doc number': args['n'],
             'to be shuffled': args['shuffle'],
             'page heading': args['page_heading']             
             }
    return param

def _start_logger(fileName):
    try:
        with open(fileName, 'r') as fd:
                loggerConf = json.load(fd)
    except FileNotFoundError:
        print('file di log' + fileName + " non trovato: indicare un file di configurazione con l'opzione -l")
        raise

    dictConfig(loggerConf)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    return logger

def main(param):
    logger = _start_logger(param['conf log file name'])

    logger.debug(str(param))

    text = getText(param['input file name'])
    logger.debug('text[0]: ' + str(text[0]))

    exam = ExamDoc(text,
                   nDoc=param['output doc number'],
                   examFile=param['exam'],
                   correctionFile=param['correction'],
                   to_shuffle=param['to be shuffled'],
                   heading=param['page heading']
                   )
    
    exam.close()
    
    return

if __name__ == '__main__':
    param = command_line_runner()
    main(param)
