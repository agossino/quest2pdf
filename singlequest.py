from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import mm
from reportlab.platypus import (Paragraph, ListFlowable,
                                Image, ListItem, Spacer)
from reportlab.lib.pagesizes import  A4
from reportlab.lib import utils
from random import shuffle

class STException(Exception): pass

class SingleQuest:
    '''Provide a ListFlowable made of the subject, one question, an image
    and answers.
    At least, the subject, one question and one answer must be provided.
    The first answer is the right one (answers ordered is then shuffled).
    '''
    
    def __init__(self, questID=1, **args):
        '''questID: number
        subject: string
        question: string
        answers: sequence of string (the first is the good one)
        image: string (path name)
        '''
        self.questID = questID

        (self.subject, self.question,
         self.right, self.wrongs) = self._get_items(args)
        
        try:
            self.image = args['image']
        except KeyError:
            self.image = ''

        # answers bullet type are capital letters
        # if not a letters rightLetter must be changed
        self.bType = 'A'

        self._set_answers() # answers are shuffled and the right answers is kept

        self._set_output_str()

        return
            
    def _get_items(self, args):
        try:
            subject = args['subject']
            question = args['question']
            right = args['answers'][0]
        except (IndexError, KeyError):
##            text = 'subject, question and, at least, one answer must be provided'
            text = 'materia, domanda e almento una risposta (etichette subject, question, A) devono essere fornite'
            raise STException(text)
        
        # '' answers ara accepted but not used
        wrongs = [ans for ans in args['answers'][1:] if ans != '']

        return subject, question, right, wrongs

    def _set_answers(self):
        if self.wrongs != []: # Multi choice or True/False question case         
            self.answerLst = self.wrongs + [self.right]
            shuffle(self.answerLst)
            self.rightLetter = (chr(self.answerLst.index(self.right)
                                    + ord(self.bType)))
        else:
            # in case of plain text, rightletter is the right sentence
            self.rightLetter = self.right
        return

    def _set_paragraphs(self):
        # space for written answer, in case of plain text
        self.fillSpace = '_'
        self.fillTimes = 1000
        self.filler = self.fillSpace * self.fillTimes

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', fontSize=12,
                                  alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(name='Answer', fontSize=12,
                                  spaceBefore=10,
                                  alignment=TA_JUSTIFY))
        self.just, self.ans = styles['Justify'], styles['Answer']
        
        return

    def _set_output_str(self):
        if len(self.wrongs) == 0:
            self.questType =  ' - aperta '
        elif len(self.wrongs) == 1:
            self.questType = ' - vero/falso '
        else:
            self.questType = ' - scelta multipla '
            
        if self.image != '':
            self.questType = self.questType + 'con immagine.'
        else:
            self.questType = self.questType + 'senza immagine.'
        return

    def __str__(self):
        return str(self.questID) + '\t ' + self.rightLetter + self.questType

    def _getImage(self, name, width=50*mm):
        '''Return Image with original aspect and given width.
        name: string (image file path name)
        width: number
        return: Image
        '''
        try:
            img = utils.ImageReader(str(name))
        except:
            print('Errore nella lettura di ', str(name))
            raise
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        
        return Image(str(name), width=width, height=(width * aspect)) 

    def getFlowable(self):
        '''ListFlowable([ListItem(ListFlowable([question, image])),
                         ListItem(answer1),
                         ListItem(answer2),
                         ...
                         ListItem(answerN)])
        '''        
        self._set_paragraphs()

        questLst = self._get_question_list()

        if self.image != '':
            questLst.append(self._getImage(self.image))
            
        listFlow = ListFlowable(questLst, bulletType='bullet', start='')

        listItem = [ListItem(listFlow, value=self.questID)]

        # If Multi choice or True/False question
        if self.wrongs != []:
            self._add_answers(listItem)
            
        return [ListFlowable(listItem)]
        
    def _get_question_list(self):
        subj_and_quest = self.subject + ' - ' + self.question
        
        if self.wrongs != []:            
            paraLst = [Paragraph(subj_and_quest, self.just)]
            
        else: # Set filler for plain text question
            paraLst = [Paragraph(subj_and_quest + self.filler, self.just)]
            
        return paraLst

    def _add_answers(self, listItem):
        # First choice: A
        listItem.append(ListItem(Paragraph(self.answerLst[0], self.ans),
                                 bulletType=self.bType,
                                 leftIndent=30, value=1))
        
        # Following choices: B, C ...
        for answer in self.answerLst[1:]:
            listItem.append(ListItem(Paragraph(answer, self.ans),
                                     bulletType=self.bType, leftIndent=30))

        return listItem
