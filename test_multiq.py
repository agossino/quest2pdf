#!/usr/bin/env python
# -*- coding: utf-8 -*-
from multiquest import MultiQuest
from itertools import count
from reportlab.pdfgen.canvas import Canvas

def test_ID():
    q1, q2, q3 = get_multi_quest(), get_plain_quest(),  get_truefalse_quest()
    
    mq = MultiQuest([q1, q2, q3])
    for i, sq in zip(count(), mq.questsLst):
        assert sq.questID == i + 1

    return

def test_output_str():
    q1, q2, q3 = get_multi_quest(), get_plain_quest(),  get_truefalse_quest()
    
    mq = MultiQuest([q1, q2, q3])

    output = mq.__str__()

    assert isinstance(output, str) == True

    return

##def test_pdf():
##    from reportlab.pdfgen.canvas import Canvas
##    from reportlab.lib.pagesizes import  A4
##    from pathlib import Path
##    quest1 = {'subject': 'Geografia',
##              'question': '''Lorem ipsum dolor sit amet, consectetur adipiscing
##elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
##Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
##nisi ut aliquip ex ea commodo consequat.
##Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore
##eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,
##sunt in culpa qui officia deserunt mollit anim id est laborum. (4 risposte)''',
##             'image': Path('image/a.png'),
##             'answers': ['giusta', 'Ad astra per aspera.',
##                         'Aliena vitia in oculis habemus, a tergo nostra sunt.',
##                         '''At pulchrum est digito monstrari et dicier:
##hic est!'''],
##             'altro 1': 'altro',
##             'altro 2': 'altro'}
##    quest2 = {'subject': 'Storia',
##              'question': '''Non sa niente, e crede di saper tutto.
##             Questo fa chiaramente prevedere una carriera politica (2 risposte)''',
##             'image': '',
##             'answers': ['giusta', '''La politica è forse l’unica professione
##per la quale non si ritiene necessaria alcuna preparazione''', '', ''],
##             'altro 1': 'altro'}
##    quest3 = {'subject': 'Matematica',
##              'question': '''Il peggio che può capitare a un
##genio è di essere compreso (1 risposta)''',
##             'image': Path('image/b.png'),
##             'answers': ['giusta'],
##             'altro 1': 'altro',
##             'altro 2': 'altro'}
##
##    fileName = 'outputMultiQ.pdf'
##    c = Canvas(fileName, pagesize=A4)
##
##    c.setAuthor('Me')
##    c.setTitle('Esame con tre domande')
##    c.setSubject('Formazione')
##
##    quests = MultiQuest([quest1, quest2, quest3])
##    quests.setHeader('file: ' + fileName)
##    quests.save()
##
##    # Genera outputMultiQ.pdf: da visualizzare
##    assert True
##
##    return

def get_multi_quest():
    quest = {'subject': 'easy',
             'question': 'Lorem ipsum dolor sit amet',
             'image': 'image/test.png',
             'answers': ['giusta', 'Ad astra per aspera.',
                         'Aliena vitia in oculis habemus',
                         '',
                         'At pulchrum est digito monstrari'],
             'altro 1': 'altro 1',
             'altro 2': 'altro 1'}
    return quest

def get_plain_quest():
    quest = {'subject': 'easy',
             'question': 'Lorem ipsum dolor sit amet',
             'answers': ['Aliena vitia in oculis habemus']
             }
    return quest

def get_truefalse_quest():
    quest = {'subject': 'hard',
             'question': 'Pacta sunt servanda:',
             'answers': ['vero', 'false']
             }
    return quest
