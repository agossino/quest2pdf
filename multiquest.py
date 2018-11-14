from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Frame, Spacer
from reportlab.lib.pagesizes import  A4
from random import shuffle

from singlequest import SingleQuest

class MultiQuest:
    '''Put more shuffled Simplequest together and save as flowable
    '''
    def __init__(self, questsLst, c):
        shuffle(questsLst)
        
        self.questsLst = []
        for quest, count in zip(questsLst, range(1, len(questsLst) + 1)):
            sQuest = SingleQuest(questID=count, **quest)
            self.questsLst.append(sQuest)
            
        self.c = c

        self._set_doc()

        return

    def _set_doc(self):
        self.setHeader('')
        self.setFooter()

        self.boundary = False

        self._set_styles()

        self._set_frames()

        return

    def _set_styles(self):
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='RightHead', fontSize=10,
                                  alignment=TA_RIGHT))
        styles.add(ParagraphStyle(name='LeftHead', fontSize=10,
                                  alignment=TA_LEFT))
        styles.add(ParagraphStyle(name='CenterFooter', fontSize=10,
                                  alignment=TA_CENTER))
        
        self.rightH = styles['RightHead']
        self.leftH = styles['LeftHead']
        self.centerF = styles['CenterFooter']

        return

    def _set_frames(self):
        A4width, A4height = A4
        
        # How much of the sheet is taken by main frame
        widthFactor = 0.9
        heightFactor = 0.9

        self.frame = {}

        self.frame['main'] = {'width': A4width * widthFactor}
        self.frame['main']['height'] = A4height * heightFactor
        self.frame['main']['x'] = ( (A4width -
                                     self.frame['main']['width']) / 2)
        self.frame['main']['y'] = ( (A4height -
                                     self.frame['main']['height']) / 2)

        self.frame['head'] = {'x': self.frame['main']['x']}
        self.frame['head']['y'] = (self.frame['main']['y'] +
                                   self.frame['main']['height'])
        self.frame['head']['width'] = self.frame['main']['width']
        self.frame['head']['height'] = ( (A4height -
                                          self.frame['main']['height']) * 0.5)

        self.frame['foot'] = {'x': self.frame['main']['x']}
        self.frame['foot']['y'] = 0
        self.frame['foot']['width'] = self.frame['main']['width']
        self.frame['foot']['height'] = ( (A4height -
                                          self.frame['main']['height']) * 0.5)

        self.sp = Spacer(mm, mm*20)

        return

    def __str__(self):
        return ''.join([item.__str__() + '\n' for item in self.questsLst])
        
    def save(self):
        main, header, footer = (self._get_frame(self.frame['main']),
                                self._get_frame(self.frame['head']),
                                self._get_frame(self.frame['foot']))
        
        header.add(Paragraph(self.headerTxt, self.rightH),
                   self.c)

        footer.add(Paragraph(self.setFooter(), self.centerF),
                   self.c)

        flowLst = [item.getFlowable()[0] for item in self.questsLst]
        
        for item in flowLst:
            if not main.add(item, self.c):
                self.c.showPage()

                main, header, footer = (self._get_frame(self.frame['main']),
                                        self._get_frame(self.frame['head']),
                                        self._get_frame(self.frame['foot']))
                main.add(item, self.c)

                header.add(Paragraph(self.headerTxt, self.rightH),
                           self.c)

                footer.add(Paragraph(self.setFooter(), self.centerF),
                           self.c)
                
            main.add(self.sp, self.c) # spaces between questions

        self.c.save()

        return

    def _get_frame(self, frameCoordDict):
        f = Frame(frameCoordDict['x'], frameCoordDict['y'],
                  frameCoordDict['width'], frameCoordDict['height'])
        
        if self.boundary:
            f.drawBoundary(self.c)

        return f

    def setHeader(self, headerTxt):
        self.headerTxt = headerTxt

        return

    def setFooter(self, footerTxt=None):
        if footerTxt is None:
            self.footerTxt = 'Pag. ' + str(self.c.getPageNumber())
        else:
            self.footerTxt = str(footerTxt)

        return self.footerTxt

def main():
    from reportlab.pdfgen.canvas import Canvas
    from pathlib import Path
    quest1 = {'question': '''Lorem ipsum dolor sit amet, consectetur adipiscing
elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore
eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,
sunt in culpa qui officia deserunt mollit anim id est laborum. (4 risposte)''',
             'image': Path('image/a.png'),
             'answers': ['giusta', 'Ad astra per aspera.',
                         'Aliena vitia in oculis habemus, a tergo nostra sunt.',
                         '''At pulchrum est digito monstrari et dicier:
hic est!'''],
             'altro 1': 'altro',
             'altro 2': 'altro'}
    quest2 = {'question': '''Non sa niente, e crede di saper tutto.
             Questo fa chiaramente prevedere una carriera politica (2 risposte)''',
             'image': '',
             'answers': ['giusta', '''La politica è forse l’unica professione
per la quale non si ritiene necessaria alcuna preparazione''', '', ''],
             'altro 1': 'altro'}
    quest3 = {'question': '''Il peggio che può capitare a un
genio è di essere compreso (1 risposta)''',
             'image': Path('image/b.png'),
             'answers': ['giusta'],
             'altro 1': 'altro',
             'altro 2': 'altro'}

    fileName = 'outputMultiQ.pdf'
    c = Canvas(fileName, pagesize=A4)

    c.setAuthor('Me')
    c.setTitle('Esame con tre domande')
    c.setSubject('Formazione')

    quests = MultiQuest([quest1, quest2, quest3], c)
    quests.setHeader('file: ' + fileName)
    quests.save()

    return

if __name__ == '__main__':
    main()

