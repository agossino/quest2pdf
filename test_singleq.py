#!/usr/bin/env python
# -*- coding: utf-8 -*-

from singlequest import SingleQuest, STException
from pathlib import Path
from random import seed
import pytest
from reportlab.platypus import Image, Paragraph, ListFlowable
from reportlab.lib.styles import ParagraphStyle

def test_ID():
    questDict = get_multi_quest()
    sq = SingleQuest(**questDict)

    assert sq.questID == 1

    return

def test_subject():
    questDict = get_multi_quest()
    sq = SingleQuest(**questDict)

    assert sq.subject == 'easy'

    return

def test_question():
    questDict = get_multi_quest()
    sq = SingleQuest(**questDict)

    assert sq.question == 'Lorem ipsum dolor sit amet'

    return

def test_multi_answers():
    questDict = get_multi_quest()
    seed(0)
    sq = SingleQuest(**questDict)

    assert sq.answerLst == ['At pulchrum est digito monstrari',
                            'Ad astra per aspera.',
                            'Aliena vitia in oculis habemus',
                            'giusta'
                            ]
    assert sq.right == 'giusta'
    assert sq.wrongs == ['Ad astra per aspera.',
                         'Aliena vitia in oculis habemus',
                         'At pulchrum est digito monstrari',
                         ]

    return

def test_single_answers():
    questDict = get_plain_quest()
    sq = SingleQuest(**questDict)

    assert sq.right == 'Aliena vitia in oculis habemus'
    assert sq.wrongs == []

    with pytest.raises(AttributeError):
        sq.answerLst == []

    return

def test_rightLetter():
    questDict = get_multi_quest()
    seed(0)
    sq = SingleQuest(**questDict)

    assert sq.rightLetter == 'D'
    
    questDict = get_plain_quest()
    sq = SingleQuest(**questDict)

    assert sq.rightLetter == sq.right
    
    return

def test_missing_keys():
    questDict = get_multi_quest()
    del questDict['subject']

    with pytest.raises(STException):
        sq = SingleQuest(**questDict)

    questDict = get_multi_quest()
    del questDict['question']

    with pytest.raises(STException):
        sq = SingleQuest(**questDict)

    questDict = get_multi_quest()
    del questDict['answers']

    with pytest.raises(STException):
        sq = SingleQuest(**questDict)

    return

def test_bType():
    questDict = get_multi_quest()
    sq = SingleQuest(**questDict)

    assert type(sq.bType) == str

    return

def test_output_str():
    questDict = get_multi_quest()
    sq = SingleQuest(**questDict)

    output = sq.__str__()

    assert 'scelta multipla' in output
    assert 'aperta' not in output
    assert 'vero/falso' not in output
    assert 'con immagine' in output

    questDict['answers'] = ['vero', 'falso']
    sq = SingleQuest(**questDict)

    output = sq.__str__()

    assert 'scelta multipla' not in output
    assert 'aperta' not in output
    assert 'vero/falso' in output
    assert 'con immagine' in output

    questDict = get_plain_quest()
    sq = SingleQuest(**questDict)

    output = sq.__str__()

    assert 'scelta multipla' not in output
    assert 'aperta' in output
    assert 'vero/falso' not in output
    assert 'con immagine' not in output
    
    return

def test_image():
    questDict = get_multi_quest()
    sq = SingleQuest(**questDict)

    assert type(sq._getImage(sq.image)) == Image

    assert sq.image == Path('image/test.png')

    questDict = get_plain_quest()
    sq = SingleQuest(**questDict)

    assert sq.image == ''    

    return

def test_filler():
    questDict = get_multi_quest()
    sq = SingleQuest(**questDict)

    sq._set_paragraphs()

    assert type(sq.filler) == str

    return

def test_ParagraphStyle():
    questDict = get_multi_quest()
    sq = SingleQuest(**questDict)

    sq._set_paragraphs()
    
    assert type(sq.just) == ParagraphStyle
    assert type(sq.ans) == ParagraphStyle

    return

def test_question_list():
    questDict = get_multi_quest()
    sq = SingleQuest(**questDict)

    sq._set_paragraphs()
    question_list = sq._get_question_list()
    
    assert len(question_list) == 1
    assert type(question_list[0]) == Paragraph
    assert question_list[0].text == 'easy - Lorem ipsum dolor sit amet'

    questDict = get_plain_quest()
    sq = SingleQuest(**questDict)

    sq._set_paragraphs()
    question_list = sq._get_question_list()
    text = 'easy - Lorem ipsum dolor sit amet' + sq.filler
    
    assert len(question_list) == 1
    assert type(question_list[0]) == Paragraph
    assert question_list[0].text == text

    return

def test_flowable():
    questDict = get_multi_quest()
    sq = SingleQuest(**questDict)

    flowable = sq.getFlowable()
    
    assert len(flowable) == 1
    assert type(flowable[0]) == ListFlowable
    assert len(flowable[0]._flowables) == 5

    questDict = get_plain_quest()
    sq = SingleQuest(**questDict)

    flowable = sq.getFlowable()

    assert len(flowable) == 1
    assert type(flowable[0]) == ListFlowable
    assert len(flowable[0]._flowables) == 1

    return

def get_multi_quest():
    quest = {'subject': 'easy',
             'question': 'Lorem ipsum dolor sit amet',
             'image': Path('image/test.png'),
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
             'answers': ['Aliena vitia in oculis habemus', '']
             }
    return quest
