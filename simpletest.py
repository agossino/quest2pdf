from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import mm
from reportlab.platypus import (Paragraph, ListFlowable,
                                Image, ListItem, Spacer)
from reportlab.lib.pagesizes import  A4
from reportlab.lib import utils
from random import shuffle

class STException(Exception): pass

class SingleTest:
    '''Provide a ListFlowable of one question, an image and answers.
    At least, one question and one answer must be provided. The first
    answer is the right one (answers ordered is shuffled)'''
    def __init__(self, testID=1, **args):
        '''testID: number
        question: string
        answers: sequence of string
        image: string (path name)
        '''
        self.testID = testID
        try:
            self.question = args['question']
            self.right = args['answers'][0]
        except (IndexError, KeyError):
            text = 'One question and, at least, one answer must be provided'
            raise STException(text)
        
        # '' answers ara accepted but not used
        self.wrong = [ans for ans in args['answers'][1:] if ans != '']
        
        try:
            self.image = args['image']
        except KeyError:
            self.image = ''

        # in case of plain text, rightletter is the right sentece
        self.rightLetter = self.right

        self.bType = 'A' # answers bullet are capital letters, if not a letters
        # rightLetter must be changed

        if self.wrong != []: # Multi choice or True/False question            
            self.answerLst = self.wrong + [self.right]
            shuffle(self.answerLst)
            self.rightLetter = (chr(self.answerLst.index(self.right)
                                    + ord(self.bType)))

        self.fillSpace = '_'
        self.fillTimes = 1000
        self.filler = self.fillSpace * self.fillTimes # space for written answer

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', fontSize=12,
                                  alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(name='Answer', fontSize=12,
                                  spaceBefore=10,
                                  alignment=TA_JUSTIFY))
        self.just, self.ans = styles['Justify'], styles['Answer']

        if len(self.wrong) == 0:
            self.type =  ' - open '
        elif len(self.wrong) == 1:
            self.type = ' - true/false '
        else:
            self.type = ' - multiple choice '
            
        if self.image != '':
            self.type = self.type + 'with image.'
        else:
            self.type = self.type + 'without image.'

        return
            
    def __str__(self):
        return str(self.testID) + ': ' + self.rightLetter + self.type

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
        if self.wrong != []:
            flowLst = [Paragraph(self.question, self.just)]
        else: # Set filler for plain text question
            flowLst = [Paragraph(self.question + self.filler, self.just)]

        if self.image != '':
            flowLst.append(self._getImage(self.image))
            
        listFlow = ListFlowable(flowLst, bulletType='bullet', start='')

        story = []
                     
        if self.wrong != []: # Multi choice or True/False question
            listItem = [ListItem(listFlow, value=self.testID)]            
            # First choice: A
            listItem.append(ListItem(Paragraph(self.answerLst[0], self.ans),
                                     bulletType=self.bType,
                                     leftIndent=30, value=1))
            
            for answer in self.answerLst[1:]: # Following choices
                listItem.append(ListItem(Paragraph(answer, self.ans),
                                         bulletType=self.bType, leftIndent=30))
            story.extend([ListFlowable(listItem)])
            return story
        else: # Plain text question
            listItem = [ListItem(listFlow, value=self.testID)]
            story.extend([ListFlowable(listItem)])
            return story

def main():
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
    from reportlab.platypus import Frame
    from pathlib import Path
    
    test1 = {'testID': 1,
             'question': '''Lorem ipsum dolor sit amet, consectetur adipiscing
elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore
eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,
sunt in culpa qui officia deserunt mollit anim id est laborum.''',
             'image': Path('/home/ago/Devel/Reportlab/image/a.png'),
             'answers': ['giusta', 'Ad astra per aspera.',
                         'Aliena vitia in oculis habemus, a tergo nostra sunt.',
                         'At pulchrum est digito monstrari et dicier: hic est!'],
             'altro 1': 'altro',
             'altro 2': 'altro'}
    test2 = {'testID': 2,
             'question': '''Non sa niente, e crede di saper tutto.
             Questo fa chiaramente prevedere una carriera politica''',
             'image': '',
             'answers': ['giusta', '''La politica è forse l’unica professione
per la quale non si ritiene necessaria alcuna preparazione''', '', ''],
             'altro 1': 'altro'}
    test3 = {'testID': 3,
             'question': '''Il peggio che può capitare a un genio
è di essere compreso''',
             'image': Path('/home/ago/Devel/Reportlab/image/b.png'),
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
    
##    Story = [SingleTest(**test) for test in (test1, test2, test3)]
    Story = []
    sp = Spacer(mm, mm*20)

    for test in (test1, test2, test3):
        oneTest = SingleTest(**test)
        Story.extend(oneTest.getFlowable())
        print(oneTest)
        
    fileName = 'output.pdf'

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

