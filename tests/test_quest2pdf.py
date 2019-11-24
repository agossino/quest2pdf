#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from reportlab.platypus import (SimpleDocTemplate, Paragraph,                                Spacer, PageTemplate, Frame)
from reportlab.lib.pagesizes import  A4
from multiquest import MultiQuest


def test_f():
    q1, q2, q3 = get_multi_quest(), get_plain_quest(),  get_truefalse_quest()
    
    mq = MultiQuest([q1, q2, q3])

    file_name = 'test.pdf'

    story = []

    doc = SimpleDocTemplate(file_name, pagesize=A4, allowSplitting=0)

    for f in mq.get_flowables():
        story.append(f)

    doc.build(story)

    try:
        with open(file_name, 'rb') as handler:
            data = handler.read()
    except:
        pass
    finally:
        os.remove(file_name)

    assert data

    
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

test_f()

