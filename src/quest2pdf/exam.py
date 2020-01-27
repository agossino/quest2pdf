#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO
# answers setter in question, like question setter in Exam
# Question attribute type_of_question
# open_ended, yes_no, multi_choice
# based on number of alternative answers provided

from pathlib import Path
from typing import (
    Tuple,
    List,
    Optional,
    Iterator,
    Iterable,
    Any,
    Sequence,
    Callable,
    Mapping,
    Union,
)
from typing_extensions import Literal
import logging
import csv
from random import shuffle

CasterType = Callable[[Any], Any]
LOGNAME = "quest2pdf." + __name__
LOGGER = logging.getLogger(LOGNAME)
LETTER_A = "A"


class Answer:
    """An answer with optional image.
    """

    def __init__(self, text: str = ""):
        self.text: str = text
        self.image: Path = Path(".")
        self._attr_load_sequence: Tuple[str, ...] = ("text", "image")
        self._type_caster_sequence: Tuple[CasterType, ...] = (str, Path)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        """Text is the answer.
        """
        if isinstance(text, str):
            self._text = text
        else:
            raise TypeError(f"{text} is not a string")

    @property
    def image(self) -> Path:
        """Image associated with the answer: it can help or
        can be the answer.
        """
        return self._image

    @image.setter
    def image(self, file_path: Path) -> None:
        if isinstance(file_path, Path):
            self._image = file_path
        else:
            raise TypeError(f"{file_path} is not a Path")

    @property
    def attr_load_sequence(self) -> Tuple[str, ...]:
        """Answer can be set by load_sequentially method: this attribute
        return the order the attribute are set"""
        return self._attr_load_sequence

    @property
    def type_caster_sequence(self) -> Tuple[CasterType, ...]:
        return self._type_caster_sequence

    def load_sequentially(self, iterator: Iterator[Any]) -> None:
        """Load all the attribute sequentially from iterator. Return
        when all attribute are filled. If the elements in the iterator
        are less then the attributes, StopIteration is not caught.
        """
        attribute_iterator: Iterator[str] = iter(self.attr_load_sequence)
        caster_iterator: Iterator[CasterType] = iter(self._type_caster_sequence)

        attribute: Union[str, Literal[False]] = next(attribute_iterator, False)
        caster: Union[CasterType, Literal[False]] = next(caster_iterator, False)

        while attribute and caster:
            setattr(self, attribute, caster(next(iterator)))

            attribute = next(attribute_iterator, False)
            caster = next(caster_iterator, False)

    def __str__(self) -> str:
        output: List[str, ...] = [f"{self.__class__}\n"]
        for attribute in self._attr_load_sequence:
            label: str = attribute
            value: Any = getattr(self, attribute)
            output.append(f"{label}: {value}\n")
        return "".join(output)


class Question:
    """Question is the question with the correct answer. Optionally it can
    have image, the subject (math, science ...), an integer representing
    the level of difficulty.
    """

    def __init__(self, text: str = ""):
        self.text: str = text
        self.subject: str = ""
        self.image: Path = Path(".")
        self.level: int = 0
        self._answers: List[Answer] = []
        self._correct_answer: Optional[Answer] = None  # setter bypassed
        self._correct_index: Optional[int] = None  # setter bypassed
        self._correct_letter: Optional[str] = None  # setter bypassed
        self._attr_load_sequence: Tuple[str, ...] = (
            "text",
            "subject",
            "image",
            "level",
        )
        self._type_caster_sequence: Tuple[CasterType, ...] = (str, str, Path, int)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        """Text is the question.
        """
        if isinstance(text, str):
            self._text = text
        else:
            raise TypeError(f"{text} in not a string")

    @property
    def image(self) -> Path:
        return self._image

    @image.setter
    def image(self, file_path: Path) -> None:
        """Image cha help or can be the question itself.
        """
        if isinstance(file_path, Path):
            self._image = file_path
        else:
            raise TypeError(f"{file_path} is not a Path")

    @property
    def subject(self) -> str:
        return self._subject

    @subject.setter
    def subject(self, name: str) -> None:
        """The subject of the question.
        """
        if isinstance(name, str):
            self._subject = name
        else:
            raise TypeError(f"{name} is not a string")

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value: int) -> None:
        """The level of difficulty.
        """
        if isinstance(value, int):
            self._level = value
        else:
            raise TypeError(f"{value} is not an int")

    @property
    def answers(self) -> Tuple[Answer, ...]:
        return tuple(self._answers)

    @answers.setter
    def answers(self, values: Iterable[Answer]) -> None:
        """Set answers given a sequence of them, overriding any
        previous data.
        """
        # Reset
        self._answers = []
        self._correct_answer = None

        list(map(self.add_answer, values))

    def add_answer(self, answer: Answer, is_correct: bool = False) -> None:
        """Add an Answer. As side effect, correct answer is set.
        The first answer is the correct one: successive answers
        are set accordingly to is_correct argument.
        """
        if isinstance(answer, Answer):
            correct_answer = self._get_correct_answer(answer, is_correct)
            self._answers.append(answer)
            self.correct_answer = correct_answer
        else:
            raise TypeError(f"{answer} is not an Answer")

    @property
    def correct_answer(self) -> Optional[Answer]:
        return self._correct_answer

    @correct_answer.setter
    def correct_answer(self, value: Answer) -> None:
        """Set the given answer as the correct one.
        """
        if value in self._answers:
            self._correct_answer = value
        else:
            raise ValueError(f"{value} is not already added")
        pointer = self._answers.index(self._correct_answer)
        self._correct_index = pointer
        self._correct_letter = chr(ord(LETTER_A) + pointer)

    @property
    def correct_index(self) -> Optional[int]:
        return self._correct_index

    @correct_index.setter
    def correct_index(self, value: int) -> None:
        """Set the correct answer given its index.
        """
        try:
            self._correct_answer = self._answers[value]
        except IndexError as index_error:
            raise ValueError(f"no answer with index {value}") from index_error
        self._correct_index = value
        self._correct_letter = chr(ord(LETTER_A) + value)

    @property
    def correct_letter(self) -> Optional[str]:
        return self._correct_letter

    @correct_letter.setter
    def correct_letter(self, value: str) -> None:
        """Set the correct answer according to the given letter,
        where the first answer added is labeled A"""
        try:
            pointer = ord(value) - ord(LETTER_A)
            self._correct_answer = self._answers[pointer]
        except IndexError as index_error:
            raise ValueError(f"no answer with letter {value}") from index_error
        self._correct_index = pointer
        self._correct_letter = chr(ord(LETTER_A) + pointer)

    @property
    def attr_load_sequence(self) -> Tuple[str, ...]:
        return self._attr_load_sequence

    @property
    def type_caster_sequence(self) -> Tuple[CasterType, ...]:
        return self._type_caster_sequence

    def _get_correct_answer(self, answer: Answer, is_correct: bool) -> Answer:
        """Return the correct answer: if no other answers are already added
        or the given is_correct is True, the given answer is returned,
        otherwise the stored correct answer is returned."""
        if self._correct_answer is None or is_correct:
            return answer
        else:
            return self._correct_answer

    def shuffle(self) -> None:
        """Shuffle the answers.
        """
        if self._correct_answer:
            shuffle(self._answers)
            pointer = self._answers.index(self._correct_answer)
            self._correct_index = pointer
            self._correct_letter = chr(ord(LETTER_A) + pointer)

    def load_sequentially(self, iterator: Iterator[Any]) -> None:
        """Load all the attribute sequentially from iterator. Returns when
        iterator is exhausted and StopIteration is caught.
        """
        attribute_iterator: Iterator[str] = iter(self.attr_load_sequence)
        caster_iterator: Iterator[CasterType] = iter(self._type_caster_sequence)

        attribute: Union[str, Literal[False]] = next(attribute_iterator, False)
        caster: Union[CasterType, Literal[False]] = next(caster_iterator, False)

        try:
            while attribute and caster:
                setattr(self, attribute, caster(next(iterator)))

                attribute = next(attribute_iterator, False)
                caster = next(caster_iterator, False)

            while True:
                answer = Answer()
                self.add_answer(answer)
                answer.load_sequentially(iterator)
        except StopIteration:
            pass

    def __str__(self) -> str:
        output: List[str, ...] = [f"{self.__class__}\n"]
        for attribute in self._attr_load_sequence:
            label: str = attribute
            value: Any = getattr(self, attribute)
            output.append(f"{label}: {value}\n")
        for ordinal, answer in enumerate(self.answers):
            output.append(f"{chr(ord(LETTER_A) + ordinal)} - ")
            output.append(answer.__str__())
        return "".join(output)


class StopQuestion(Exception):
    """Raised each time serialize ends a question."""
    pass

class Exam:
    """Exam is a sequence of Question managed as a whole.
    """

    def __init__(self, *args: Question):
        self._questions: List[Question] = list()
        list(map(self.add_question, args))
        self._attribute_selector: Tuple[Optional[str]] = ()

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
    def attribute_selector(self) -> Tuple[Optional[str]]:
        return self._attribute_selector

    @attribute_selector.setter
    def attribute_selector(self, selection: Iterable[str]) -> None:
        self._attribute_selector = tuple(str(item) for item in selection)

    def add_question(self, question: Question) -> None:
        """Add one question to the sequence.
        """
        if isinstance(question, Question):
            self._questions.append(question)
        else:
            raise TypeError(f"{question} is not a Question")

    def load(self, iterable: Iterable[Mapping[str, Any]]) -> None:
        for row in iterable:
            if self._attribute_selector:
                data = [row[key] for key in self._attribute_selector]
            else:
                data = [row[key] for key in row]
            if data:
                quest = Question()
                self.add_question(quest)
                iterator = iter(data)
                quest.load_sequentially(iterator)

    def serialize(self):
        for question in self.questions:
            yield question.text
            yield question.subject
            yield question.image
            yield question.level
            for answer in question.answers:
                yield answer.text
                yield answer.image
            raise StopQuestion

    def __str__(self) -> str:
        output: List[str] = []
        for q in self._questions:
            output.append(q.__str__())
        return "".join(output)
