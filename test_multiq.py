#!/usr/bin/env python
# -*- coding: utf-8 -*-
from multiquest import MultiQuest
from itertools import count
from reportlab.pdfgen.canvas import Canvas

def test_ID():
    q1, q2, q3 = get_multi_quest(), get_plain_quest(),  get_truefalse_quest()
    c = Canvas('')

    mq = MultiQuest([q1, q2, q3], c)
    for i, sq in zip(count(), mq.questsLst):
        assert sq.questID == i + 1

    return

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
