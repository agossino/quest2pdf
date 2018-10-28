from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import  A4

from csv import DictReader
from random import shuffle
from datetime import datetime
from platform import node
from os import getlogin

from simpletest import SingleTest
from multitest import MultiTest

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
    story = []

    testFile = 'testFile/AAtest.csv'

    text = getText(testFile)
    shuffle(text)

    for row, value in zip(text, range(1,len(text)+1)):
        oneTest = SingleTest(**setDictionary(row, value))
        story.extend(oneTest.getFlowable())
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

    tests = MultiTest(story, c)
    tests.setHeader('file: ' + fileName)
    tests.print()
    
    return

if __name__ == '__main__':
    main()

