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
    '''Provide a ListFlowable made of one question, an image and answers.
    At least, one question and one answer must be provided. The first
    answer is the right one (answers ordered is then shuffled)'''
    
    def __init__(self, questID=1, **args):
        '''questID: number
        question: string
        answers: sequence of string (the first is the good one)
        image: string (path name)
        '''
        self.questID = questID

        self.question, self.right, self.wrongs = self._get_items(args)
        
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
            question = args['question']
            right = args['answers'][0]
        except (IndexError, KeyError):
            text = 'One question and, at least, one answer must be provided'
            raise STException(text)
        
        # '' answers ara accepted but not used
        wrongs = [ans for ans in args['answers'][1:] if ans != '']

        return question, right, wrongs

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
            self.questType =  ' - open '
        elif len(self.wrongs) == 1:
            self.questType = ' - true/false '
        else:
            self.questType = ' - multiple choice '
            
        if self.image != '':
            self.questType = self.questType + 'with image.'
        else:
            self.questType = self.questType + 'without image.'
        return

    def __str__(self):
        return str(self.questID) + ': ' + self.rightLetter + self.questType

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
        if self.wrongs != []:
            paraLst = [Paragraph(self.question, self.just)]
            
        else: # Set filler for plain text question
            paraLst = [Paragraph(self.question + self.filler, self.just)]
            
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


def main():
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
    from reportlab.platypus import Frame
    from pathlib import Path
    
    quest1 = {'questID': 1,
             'question': '''Lorem ipsum dolor sit amet, consectetur adipiscing
elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore
eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,
sunt in culpa qui officia deserunt mollit anim id est laborum.''',
             'image': Path('image/a.png'),
             'answers': ['giusta', 'Ad astra per aspera.',
                         'Aliena vitia in oculis habemus, a tergo nostra sunt.',
                         'At pulchrum est digito monstrari et dicier: hic est!'],
             'altro 1': 'altro',
             'altro 2': 'altro'}
    quest2 = {'questID': 2,
             'question': '''Non sa niente, e crede di saper tutto.
             Questo fa chiaramente prevedere una carriera politica''',
             'image': '',
             'answers': ['giusta', '''La politica è forse l’unica professione
per la quale non si ritiene necessaria alcuna preparazione''', '', ''],
             'altro 1': 'altro'}
    quest3 = {'questID': 3,
             'question': '''Il peggio che può capitare a un genio
è di essere compreso''',
             'image': Path('image/b.png'),
             'answers': ['giusta'],
             'altro 1': 'altro',
             'altro 2': 'altro'}
    
    A4width, A4height = A4
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='RightHead', fontSize=10,
                              alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='LeftHead', fontSize=10,
                              alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='CenterFooter', fontSize=10,
                              alignment=TA_CENTER))
    
    rightH = styles['RightHead']
    leftH = styles['LeftHead']
    centerF = styles['CenterFooter']
    
    Story = []
    sp = Spacer(mm, mm*20)

    for quest in (quest1, quest2, quest3):
        oneQuest = SingleQuest(**quest)
        Story.extend(oneQuest.getFlowable())
        print(oneQuest)
        
    fileName = 'outputSimpleQ.pdf'

    c = Canvas(fileName, pagesize=A4)
    
    c.setAuthor('Me')
    c.setTitle('Test esame con tre domande')
    c.setSubject('Formazione')

    widthFactor = 0.9
    heightFactor = 0.9

    frameW = A4width * widthFactor
    frameH = A4height * heightFactor
    frameXLowLeftCorner = 0 + (A4width - frameW) / 2
    frameYLowLeftCorner = 0 + (A4height - frameH) / 2

    headerXLowLeftCorner = frameXLowLeftCorner
    headerYLowLeftCorner = frameYLowLeftCorner + frameH + 1
    headerW = frameW
    headerH = (A4height - frameH) * 0.49

    footerXLowLeftCorner = frameXLowLeftCorner
    footerYLowLeftCorner = 0
    footerW = frameW
    footerH = (A4height - frameH) * 0.49

    f = Frame(frameXLowLeftCorner, frameYLowLeftCorner,
              frameW, frameH, showBoundary=1)
    f.drawBoundary(c)

    header = Frame(headerXLowLeftCorner, headerYLowLeftCorner,
                   headerW, headerH)
    header.drawBoundary(c)

    footer = Frame(footerXLowLeftCorner, footerYLowLeftCorner,
                   footerW, footerH)
    footer.drawBoundary(c)

    htext = 'file: ' + fileName    
    hPara = Paragraph(htext, rightH)
    header.add(hPara, c)

    ftext = 'Pag. ' + str(c.getPageNumber())
    fPara = Paragraph(ftext, centerF)
    footer.add(fPara, c)

    for item in Story:
        if  not f.add(item, c):
            c.showPage()
            f = Frame(frameXLowLeftCorner, frameYLowLeftCorner,
                      frameW, frameH, showBoundary=1)
            f.drawBoundary(c)
            
            header = Frame(headerXLowLeftCorner, headerYLowLeftCorner,
                           headerW, headerH)
            header.drawBoundary(c)

            footer = Frame(footerXLowLeftCorner, footerYLowLeftCorner,
                   footerW, footerH)
            footer.drawBoundary(c)

            f.add(item, c)

            htext = 'file: '+fileName    
            hPara = Paragraph(htext, rightH)
            header.add(hPara, c)

            ftext = 'Pag. ' + str(c.getPageNumber())
            fPara = Paragraph(ftext, centerF)
            footer.add(fPara, c)
            
        f.add(sp, c)

    c.save()
    
    return

if __name__ == '__main__':
    main()

