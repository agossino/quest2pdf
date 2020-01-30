#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import  A4
from multiquest import MultiQuest
from utility import add_path_to_image
from typing import List, Dict


def test_add_path_to_image():
    dict_of_lists: List[Dict[str, str]] = get_dictlist()
    expected: List[Dict[str, str]] = get_dictlist()
    ref_path: str = "/home/dude/tmp"

    add_path_to_image(ref_path, dict_of_lists)

    expected[1]["image"] = str(Path(ref_path) / dict_of_lists[1]["image"])
    expected[2]["image"] = str(Path(ref_path) / dict_of_lists[2]["image"])

    assert dict_of_lists == expected

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

def get_dictlist() -> List[Dict[str, str]]:
    return [{'subject': 'math',
             'question': 'who?',
             'A': 'no', 'B': 'yes',
             'C': 'yes no', 'D': 'maybe'},
            {'subject': 'grammar',
             'question': "where?",
             'A': 'here', 'B': 'there',
             'C': 'somewhere', 'D': 'somewhere',
             'image': 'image/a.png'},
            {'subject': 'system',
             'question': 'what?',
             'A': 'this', 'B': 'that',
             'C': 'none', 'D': 'all',
             'image': ''}]

def get_multi_quest():
    image_file =  'image/test.png'
    script_path: Path = Path(__file__).resolve().parent
    quest = {'subject': 'easy',
             'question': 'Lorem ipsum dolor sit amet',
             'image': str(script_path.joinpath(image_file)),
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

