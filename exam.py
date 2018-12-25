#!/usr/bin/env python
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import  A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (SimpleDocTemplate, Paragraph,
                                Spacer, PageTemplate, Frame)
from reportlab.lib.units import mm

from datetime import datetime

import logging
import json
from logging.config import dictConfig

from multiquest import MultiQuest
from numberedcanvas import NumberedCanvas


class CorrectionDoc:
    def __init__(self, fileName):
        self.correctionDoc = SimpleDocTemplate(correctionFile)

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

class ExamDoc(MultiQuest):
    def __init__(self, quests, nDoc,
                 fileName='questions.pdf',
                 correctionFile='correction.pdf')

    self.correctionDoc = SimpleDocTemplate(correctionFile)

    dictLst = [self._setDictionary(row) for row in quests]

    for i in range(nDoc):
        story = []
        # %f are microseconds, because of [:-4], last significant digits are cs
        now = datetime.now().strftime('%Y-%m-%d-T%H-%M-%S-%f')
        fileName = ''.join((param['prefix'], '-', now))[:-4] + '.pdf'
        
        doc = SimpleDocTemplate(fileName, pagesize=A4, allowSplitting=0,
                                author=author, title=title, subject=subject)

        questions = MultiQuest(dictLst)

        for f in questions.get_flowables():
            story.append(f)
            story.append(Spacer(mm, mm*20))

        doc.build(story, onFirstPage=self._header1,
                  onLaterPages=self._header, canvasmaker=NumberedCanvas)
    

    def _setDictionary(self, row):
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

    def _header1(self, canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()
        text = 'This is a multi-line header.  It goes on 1st page. '

        # Header
        header = Paragraph(text, styles['Normal'])
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.bottomMargin + doc.topMargin/2 - h)

        # Release the canvas
        canvas.restoreState()

        return

    def _header(self, canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()
        text = 'This is a multi-line header.  It goes on every page.   ' * 5

        # Header
        header = Paragraph(text, styles['Normal'])
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

        # Release the canvas
        canvas.restoreState()

        return

    def _footer(self, canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()
        text = 'This is a multi-line footer.  It goes on every page.   ' * 5

        # Footer
        footer = Paragraph(text, styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)

        # Release the canvas
        canvas.restoreState()

        return

def main(param):
    logger = _start_logger(param['log file name'])

    logger.debug(str(param))
    
    hms = datetime.now().strftime('%H-%M-%S')
    correctFile = ''.join((param['prefix'], '-correction-H', hms)) + '.pdf'
    logger.debug('correction file: ' + correctFile)

    text = getText(param['input file name'])
    logger.debug('text[0]: ' + str(text[0]))
                 
    dictLst = [setDictionary(row) for row in text]
    logger.debug('dictLst[0]: ' + str(dictLst[0]))

    correctionDoc = CorrectionDoc(correctFile)

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

