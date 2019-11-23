#!/usr/bin/env python
import configparser
import argparse
import logging
import logging.config
import json
import pathlib

logName = 'quest2pdf.' + __name__
logger = logging.getLogger(logName)

class myArgparser(argparse.ArgumentParser):
    '''Record for every argument added the default parameter.
    '''
    def __init__(self, *args, **kwargs):
        self._defaultLst = []
        return super().__init__(*args, **kwargs)
    
    def add_argument(self, *args, **kwargs):
        dest = args[0][1:] if args[0][0] == '-' else args[0][:]

        try:
            dest = args[1][2:]
        except IndexError:
            pass
        
        dest = kwargs.get('dest', dest)
        
        try:
            self._defaultLst.append((dest, kwargs['default']))
        except KeyError:
            pass
        else:
            return super().add_argument(*args, **kwargs)

        try:
            action = kwargs['action']
        except KeyError:
            return super().add_argument(*args, **kwargs)

        if action == 'store_true':
            self._defaultLst.append((dest, False))
        elif action == 'store_false':
            self._defaultLst.append((dest, True))

        return super().add_argument(*args, **kwargs)

    def defaults_set(self):
        output = {}
        for key, value in self._defaultLst:
            if key == 'help':
                continue
            output[key] = value
            
        return output

def start_logger(fileName):
    scriptPath = pathlib.Path(__file__).resolve().parent
    homePath = pathlib.Path.home()

    for file in (fileName,
                 scriptPath.joinpath(fileName),
                 homePath.joinpath(fileName)):
        result = try_log_conf_file(file)
        if result is True:
            return
        
    logger.warning('file di configurazione del log non trovato: viene usata configurazione predefinita')
    return

def try_log_conf_file(filePath):
    '''It tryes to open a log configuration file.
    filePath: filePath
    return: boolean (True is successed, False otherwise)
    '''
    output = {}
    config = configparser.ConfigParser()
    filePath = str(filePath)
    global logger
    
    try:
        with open(filePath, 'r') as f:
            loggerConf = json.load(f)
            logging.config.dictConfig(loggerConf)
            logger = logging.getLogger(__name__)
            logger.debug('logger started from ' + str(pathlib.Path.cwd()))
            logger.info(filePath + ' trovato')
            return True
    except FileNotFoundError as e:
        msg = filePath + ' non trovato'
        logger.info(msg + str(e))
        return False

def conf_file_parser(file_name):
    scriptPath = pathlib.Path(__file__).resolve().parent
    homePath = pathlib.Path.home()

    for file in (file_name,
                 scriptPath.joinpath(file_name),
                 homePath.joinpath(file_name)):
        output = try_conf_file(file)
        if output is not None:
            return output
        
    msg = 'file di configurazione non trovato in . ' + str(scriptPath) + str(homePath)
    logger.critical(msg)
    raise FileNotFoundError(msg)

def try_conf_file(filePath):
    output = {}
    config = configparser.ConfigParser()
    filePath = str(filePath)
    
    try:
        with open(filePath, 'r') as f:
            config.read_file(f)
            logger.info(filePath + ' trovato')
            for key, value in config['Default'].items():
                output[key] = value
    except FileNotFoundError as e:
        msg = filePath + ' non trovato'
        logger.info(msg + str(e))
        return None
    
    return output

def cli_parser():
    description = "genera PDF da un file di prova d'esame in formato testo: domande a risposta multipla, vero o falso o aperte."
    parser = myArgparser(description=description,
                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input', type=str, nargs='?',
                        help='nome del file di input di domande e risposte in formato testo.',
                        default='domande.csv')
    parser.add_argument('-n', '--number', type=int, nargs='?',
                        help='numero dei file di output da generare',
                        default=1)
    parser.add_argument('-e', '--exam',
                        help='prefisso per il file di esame; a questo verranno accodati data e orario fino a ms.',
                        type=str,
                        default='Esame')
    parser.add_argument('-c', '--correction',
                        help="prefisso per il file correttore; a questo verranno accodati data e orario fino a ms.",
                        type=str,
                        default='Correttore')
    parser.add_argument('-f', '--conffile',
                        help="file di configurazione dell'applicazione.",
                        default='conf.ini')
    parser.add_argument('-l', '--conflogfile',
                        help='file di configurazione del file di registro.',
                        default='loggingConf.json')
    parser.add_argument('-s', '--shuffle',
                        help="se fornito mischia l'ordine delle domande.",
                        action='store_true')
    parser.add_argument('-p', '--page_heading',
                        help="testo di intestazione che compare all'inizio di ogni pagina (se il nome è omesso appare il nome del file di esame).",
                        nargs='?', const=True,
                        default=False)
    parser.add_argument('-E', '--encoding',
                        help='codifica per i caratteri del file di testo.',
                        default='utf-8')    
    parser.add_argument('-d', '--delimiter', choices=['exclamation', 'dash', 'period',
                                                     'space', 'comma', 'semicolon', 'colon', 'tab'],
                        help='carattere utilizzato per separare i campi del file di testo, ad es. comma, colon, tab ecc.',
                        default='comma')
    parser.add_argument('-v', '--version',
                        help='mostra la corrente versione.',
                        action='version', version='%(prog)s 2.0.0')
    return parser

def param_parser():
    '''Arguments from command line have precedence over the ones
    coming from configurazion file.
    '''
    default_delim = ','
    delimiters = {'colon': ':',
                  'comma': ',',
                  'dash': '-',
                  'exclamation': '!',
                  'period': '.',
                  'semicolon': ';',
                  'space': ' ',
                  'tab': '\t',
                  }
    parser = cli_parser()
    cli_args = vars(parser.parse_args())

    start_logger(cli_args['conflogfile'])

    defaults = parser.defaults_set()
    # defaults values are compared in order to know if
    # arguments are set in cli
    chosen = {}
    for key, value in cli_args.items():
        if value != defaults.get(key, None):
            chosen[key] = value
            
    # congiguration file is added: from cli, if set, or the default one
    chosen['conffile'] = cli_args['conffile']

    #default values are updated with the ones coming from cli and config file
    cfile_args = conf_file_parser(cli_args['conffile'])
    cfile_args.update(chosen)
    defaults.update(cfile_args)

    defaults['delimiter'] = delimiters.get(defaults['delimiter'],
                                           default_delim)

    return defaults
