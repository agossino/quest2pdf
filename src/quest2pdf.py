#!/usr/bin/env python
import logging
import parameter
from filereader import CSVReader
from exam import ExamDoc

logName = 'quest2pdf'
logger = logging.getLogger(logName)

def main():
    param = parameter.param_parser()
    logger.debug(str(param))

    inputFile = CSVReader(param['input'],
                          param['encoding'],
                          param['delimiter'])
    text = inputFile.to_dictlist()

    logger.debug('text[0]: ' + str(text[0]))

    exam = ExamDoc(text,
                   nDoc=param['number'],
                   examFile=param['exam'],
                   correctionFile=param['correction'],
                   to_shuffle=param['shuffle'],
                   heading=param['page_heading']
                   )
    
    exam.close()
    
    return

if __name__ == '__main__':
    main()
