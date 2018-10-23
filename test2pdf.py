from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.units import mm
from reportlab.platypus import (Paragraph, Frame, ListFlowable,
                                Image, ListItem, Spacer, KeepTogether)
from reportlab.lib.pagesizes import  A4
from reportlab.lib import utils
from csv import DictReader
from random import shuffle
from datetime import datetime
from platform import node
from os import getlogin

class STException(Exception): pass

class SingleTest:
    def __init__(self, testID=1, **args):
        self.testID = testID
        try:
            self.question = args['question']
            self.right = args['answers'][0]
        except (IndexError, KeyError):
            raise STException('One question and, at least, one answer must be provided')
        
        self.wrong = [ans for ans in args['answers'][1:] if ans != '']
        
        try:
            self.image = args['image']
        except KeyError:
            self.image = ''

        self.fillSpace = '_'
        self.fillTimes = 1000
        self.filler = self.fillSpace * self.fillTimes # space for written answer

        self.bType = 'A'

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', fontSize=12,
                                  alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(name='Answer', fontSize=12,
                                  spaceBefore=10,
                                  alignment=TA_JUSTIFY))
        self.just, self.ans = styles['Justify'], styles['Answer']

        self.rightAns = self.right
        
        if len(self.wrong) == 0:
            self.output = str(self.testID) + ' aperta '
        elif len(self.wrong) == 1:
            self.output = str(self.testID) + ' vero/falso '
        else:
            self.output = str(self.testID) + ' scelta multipla '
            
        if self.image != '':
            self.output = self.output + 'con immagine '

        return
            
    def __str__(self):
        return self.output + self.rightAns

    def _getImage(self, name, width=50*mm):
        '''Return Image with original aspect and given width.
        name: string (image file path name)
        width: number
        return: Image
        '''
        if name == '':
            name = 'image/a.png'
            
        img = utils.ImageReader(name)
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        
        return Image(name, width=width, height=(width * aspect)) 

    def getFlowable(self):
        if self.wrong != []:
            flowLst = [Paragraph(self.question, self.just)]
        else: # Set filler for plain text question
            flowLst = [Paragraph(self.question + self.filler, self.just)]

        if self.image != '':
            flowLst.append(self._getImage(self.image))
            
        listFlow = ListFlowable(flowLst, bulletType='bullet', start='')

        story = []
                     
        if self.wrong != []: # Multi choice or True/False question
            # question with image, if applicable
            listItem = [ListItem(listFlow, value=self.testID)]
            
            answerLst = self.wrong + [self.right]
            shuffle(answerLst)
            self.rightAns = chr(answerLst.index(self.right) + ord(self.bType))
            
            # First choice: A
            listItem.append(ListItem(Paragraph(answerLst[0], self.ans),
                                     bulletType=self.bType,
                                     leftIndent=30, value=1))
            
            for answer in answerLst[1:]: # Following choices
                listItem.append(ListItem(Paragraph(answer, self.ans),
                                         bulletType=self.bType, leftIndent=30))
##            story.extend([ListFlowable(listItem, value=self.testID)])
            story.extend([ListFlowable(listItem)])
            return story
        else: # Plain text question
            listItem = [ListItem(listFlow, value=self.testID)]
            story.extend([ListFlowable(listItem)])
            return story

def getText(file_name):
    with open(file_name, 'r') as csvfile:
        reader = DictReader(csvfile)
        rows = [row for row in reader]
    return rows

def setDictionary(row, value):
    '''Give the right format for SimpleTest argument.
    '''
    output = {'testID': value,
              'question': row['question'],
              'image': row['image']
              }
    
    answerKeys = ('A', 'B', 'C', 'D')
    answers = [row[key] for key in answerKeys]

    output['answers'] = answers
    
    return output

def main():
    A4width, A4height = A4
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='RightHead', fontSize=8,
                              spaceAfter=5,
                              alignment=TA_RIGHT))
    
    rightH = styles['RightHead']
    Story = []
    sp = Spacer(mm, mm*20)

    text = getText('testFile/AAtest.csv')
    shuffle(text)

    for row, value in zip(text, range(1,len(text)+1)):
        oneTest = SingleTest(**setDictionary(row, value))
        Story.extend(oneTest.getFlowable())
        print(oneTest)

    host = node()
    user = getlogin()
    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
    fileName = ''.join((user, '-', host, '-', now))[:-4] + '.pdf'

    c = Canvas(fileName, pagesize=A4)
    print(fileName)
    c.setAuthor('Giancarlo')
    c.setTitle('Esame')
    c.setSubject('Formazione')

    frameW = A4width * 0.8
    frameH = A4height * 0.8
    frameXLowLeftCorner = 0 + (A4width - frameW) / 2
    frameYLowLeftCorner = 0 + (A4height - frameH) / 2

    headerXLowLeftCorner = frameXLowLeftCorner
    headerYLowLeftCorner = frameYLowLeftCorner + frameH + 1
    headerW = frameW
    headerH = (A4height - frameH) * 0.49

    f = Frame(frameXLowLeftCorner, frameYLowLeftCorner,
              frameW, frameH, showBoundary=1)
    f.drawBoundary(c)

    header = Frame(headerXLowLeftCorner, headerYLowLeftCorner,
                   headerW, headerH)
    header.drawBoundary(c)

    header.add(Paragraph('file: '+fileName, rightH), c)

    for item in Story:
        if  not f.add(item, c):
            c.showPage()
            f = Frame(frameXLowLeftCorner, frameYLowLeftCorner,
                      frameW, frameH, showBoundary=1)
            f.drawBoundary(c)
            f.add(item, c)
            header = Frame(headerXLowLeftCorner, headerYLowLeftCorner,
                           headerW, headerH)
            header.drawBoundary(c)
            header.add(Paragraph('Left Aligned Heading', rightH), c)
        f.add(sp, c)

    c.save()
    
    return

if __name__ == '__main__':
    main()

