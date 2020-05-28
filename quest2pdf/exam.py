#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO
# answers setter in question, like question setter in Exam
# Question attribute type_of_question
# open_ended, yes_no, multi_choice
# based on number of alternative answers provided
from collections import namedtuple
from enum import Enum

from pathlib import Path
from typing import Tuple, List, Iterable, Any, Callable, Mapping, Generator
import logging

from . import Question, MultiChoiceQuest, TrueFalseQuest


LOGNAME = "quest2pdf." + __name__
LOGGER = logging.getLogger(LOGNAME)


class Exam:
    """Exam is a sequence of Question managed as a whole.
    """

    def __init__(self, *args: Question):
        self._questions = list()
        self._question_type_key: str = "Question type"
        list(map(self.add_question, args))
        self._attribute_selector: Tuple[str, ...] = ()

    @property
    def questions(self) -> Tuple[Question, ...]:
        return tuple(self._questions)

    @questions.setter
    def questions(self, values: Iterable[Question]) -> None:
        """Set questions given a sequence of them, overriding any
        previous data.
        """
        # Reset
        self._questions = []

        list(map(self.add_question, values))

    @property
    def attribute_selector(self) -> Tuple[str, ...]:
        return self._attribute_selector

    @attribute_selector.setter
    def attribute_selector(self, selection: Iterable[str]) -> None:
        self._attribute_selector = tuple(str(item) for item in selection)

    def add_question(self, question: Question) -> None:
        """Add one question to the sequence.
        """
        # if isinstance(question, Question):
        #     self._questions.append(question)
        # else:
        #     raise TypeError(f"{question} is not a Question")
        self._questions.append(question)

    def add_path_parent(self, file_path: Path):
        for question in self._questions:
            question.add_parent_path(file_path)

    def load(self, iterable: Iterable[Mapping[str, Any]]) -> None:
        questions_classes = {
            "MultiChoice": MultiChoiceQuest,
            "TrueFalse": TrueFalseQuest,
        }
        default_key = "MultiChoice"
        for row in iterable:
            quest = questions_classes[row.get(self._question_type_key, default_key)]()
            if self._attribute_selector:
                data = [row[key] for key in self._attribute_selector]
            else:
                data = [row[key] for key in row]
            if data:
                self.add_question(quest)
                iterator = iter(data)
                quest.load_sequentially(iterator)

    def shuffle(self):
        for question in self._questions:
            question.shuffle()

    def __str__(self) -> str:
        output: List[str] = []
        for question in self._questions:
            output.append(question.__str__())
        return "".join(output)


class ItemLevel(Enum):
    """top level text
       top level image
           sub level text
           sub level image

           sub level test

       top level image
           sub level text

           sub level image
    """

    top = 0
    sub = 1


Item = namedtuple("Item", ["item_level", "text", "image"])


class SerializeExam:
    """Serialize questions, made of text and image, and
    answers, made of text and image.
    """

    def __init__(self, exam_alike: Exam):
        self._exam: Exam = exam_alike

    def assignment(self) -> Generator[Item, None, None]:
        for question in self._exam.questions:
            yield Item(ItemLevel.top, question.text, question.image)
            for answer in question.answers:
                yield Item(ItemLevel.sub, answer.text, answer.image)

    def correction(self) -> Generator[Item, None, None]:
        if self._exam.questions != ():
            yield Item(ItemLevel.top, f"correction", Path("."))
        for question in self._exam.questions:
            yield Item(ItemLevel.sub, f"{question.correct_option}", Path("."))