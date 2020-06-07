#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO
# answers setter in question, like question setter in Exam
# Question attribute type_of_question
# open_ended, yes_no, multi_choice
# based on number of alternative answers provided

from pathlib import Path
from typing import Tuple, List, Optional, Iterator, Iterable, Any, Callable, Mapping
import logging
from random import shuffle
from utility import safe_int

CasterType = Callable[[Any], Any]
LOGNAME = "quest2pdf." + __name__
LOGGER = logging.getLogger(LOGNAME)
LETTER_A = "A"
SPACE = " "


class Answer:
    """An answer with optional image.
    """

    def __init__(self):
        self._attr_load_sequence: Tuple[str] = tuple()
        self._type_caster_sequence: Tuple[CasterType, ...] = tuple()

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

        attribute: Optional[str] = next(attribute_iterator, None)
        caster: Optional[CasterType] = next(caster_iterator, None)

        while attribute is not None and caster is not None:
            setattr(self, attribute, caster(next(iterator)))

            attribute = next(attribute_iterator, None)
            caster = next(caster_iterator, None)

    def __str__(self) -> str:
        output: List[str] = [f"{self.__class__}\n"]
        for attribute in self._attr_load_sequence:
            label: str = attribute
            value: Any = getattr(self, attribute)
            output.append(f"{label}: {value}\n")
        return "".join(output)


class MultiChoiceAnswer(Answer):
    def __init__(self, text: str = "", image: Path = Path()):
        self.text: str = text
        self.image: Path = image
        super().__init__()
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


class TrueFalseAnswer(Answer):
    def __init__(self, boolean: bool = False, image: Path = Path()):
        self.boolean: bool = boolean
        self.image: Path = image
        self._text = "True" if self.boolean else "False"
        super().__init__()
        self._attr_load_sequence: Tuple[str, ...] = ("boolean", "image")
        self._type_caster_sequence: Tuple[CasterType, ...] = (bool, Path)

    @property
    def boolean(self) -> bool:
        return self._boolean

    @boolean.setter
    def boolean(self, boolean):
        self._boolean, self._text = (True, "True") if boolean else (False, "False")

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
    def text(self):
        return self._text


class Question:
    """Question is the question with the correct answer. Optionally it can
    have image, the subject (math, science ...), an integer representing
    the level of difficulty.
    """

    def __init__(
        self, text: str = "", subject: str = "", image: Path = Path(), level: int = 0
    ):
        self.text: str = text
        self.subject: str = subject
        self.image: Path = image
        self.level: int = level
        self._answer_type = Answer
        self._answers: List[self._answer_type] = []
        self._correct_answer: Optional[self._answer_type] = None  # setter bypassed
        self._correct_index: Optional[int] = None  # setter bypassed
        self._attr_load_sequence: Tuple[str, ...] = (
            "text",
            "subject",
            "image",
            "level",
        )
        self._type_caster_sequence: Tuple[CasterType, ...] = (str, str, Path, safe_int)
        self._marker = "*"

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

    def add_answer(self, answer, is_correct: bool = False) -> None:
        """Add an Answer. Correct answer is set.
        The first answer is the correct one: successive answers
        are set accordingly to is_correct argument.
        """
        self._answers.append(answer)
        if is_correct or self._correct_answer is None:
            self.correct_answer = answer

    @property
    def correct_answer(self):
        return self._correct_answer

    @correct_answer.setter
    def correct_answer(self, value) -> None:
        """Set the given answer as the correct one.
        """
        if value in self._answers:
            self._correct_answer = value
        else:
            raise ValueError(f"correct_answer argument has never been added")
        pointer = self._answers.index(self._correct_answer)
        self._correct_index = pointer
        # self._correct_letter = chr(ord(LETTER_A) + pointer)

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
        # self._correct_letter = chr(ord(LETTER_A) + value)

    def add_parent_path(self, file_path: Path) -> None:
        self.image = (
            file_path.parent / self.image if self.image != Path() else self.image
        )
        for answer in self.answers:
            answer.image = (
                file_path.parent / answer.image
                if answer.image != Path()
                else answer.image
            )

    @property
    def attr_load_sequence(self) -> Tuple[str, ...]:
        return self._attr_load_sequence

    @property
    def type_caster_sequence(self) -> Tuple[CasterType, ...]:
        return self._type_caster_sequence

    def load_sequentially(self, iterator: Iterator[Any]) -> None:
        """Load all the attribute sequentially from iterator, according to
        attr_load_sequence and type_caster_sequence. Empty answers are skipped.
        Empty means without text and image. Returns when
        iterator is exhausted and StopIteration is caught.
        """
        attribute_iterator: Iterator[str] = iter(self.attr_load_sequence)
        caster_iterator: Iterator[CasterType] = iter(self._type_caster_sequence)

        attribute: Optional[str] = next(attribute_iterator, None)
        caster: Optional[CasterType] = next(caster_iterator, None)

        try:
            while attribute is not None and caster is not None:
                setattr(self, attribute, caster(next(iterator)))

                attribute = next(attribute_iterator, None)
                caster = next(caster_iterator, None)

            self._load_answers(iterator)

        except StopIteration:
            pass

    def _load_answers(self, iterator: Iterator[Any]) -> None:
        """Load answers. An answer is filled even if there are not enough elements
        in the iterator. Empty answers are not loaded.
        Returns when iterator is exhausted and StopIteration is caught.
        """
        wrote_attr = 1

        while wrote_attr:
            answer = self._answer_type()
            wrote_attr = self._load_1_answer(answer, iterator)

    def _load_1_answer(self, answer, iterator: Iterator[Any]) -> int:
        iter_to_list = []
        is_empty = True
        attributes = 0
        try:
            for _ in answer.attr_load_sequence:
                iter_to_list.append(next(iterator))
                attributes += 1
                if iter_to_list[-1] != "":
                    is_empty = False
            if not is_empty:
                answer.load_sequentially(iter(iter_to_list))
                self.add_answer(answer)
        except StopIteration:
            if len(iter_to_list) > 0 and not is_empty:
                try:
                    answer.load_sequentially(iter(iter_to_list))
                except StopIteration:
                    self.add_answer(answer)
                    raise
            raise
        return attributes

    def __str__(self) -> str:
        output: List[str] = [f"{self.__class__}\n"]
        for attribute in self._attr_load_sequence:
            label: str = attribute
            value: Any = getattr(self, attribute)
            output.append(f"{label}: {value}\n")
        for ordinal, answer in enumerate(self.answers):
            correct_marker = self._marker if ordinal == self.correct_index else SPACE
            output.append(f"{chr(ord(LETTER_A) + ordinal)}{correct_marker} - ")
            output.append(answer.__str__())
        return "".join(output)


class MultiChoiceQuest(Question):
    """Multi choice question.
    """

    def __init__(self, *args):
        self._correct_option: Optional[str] = None  # setter bypassed
        super().__init__(*args)
        self._answer_type = MultiChoiceAnswer
        self._answers: List[self._answer_type] = []

    @Question.correct_answer.setter
    def correct_answer(self, value) -> None:
        """Set the given answer as the correct one.
        """
        Question.correct_answer.fset(self, value)
        self._correct_option = chr(ord(LETTER_A) + self.correct_index)

    @property
    def correct_option(self) -> Optional[str]:
        return self._correct_option

    @correct_option.setter
    def correct_option(self, value: str) -> None:
        """Set the correct answer according to the given letter,
        where the first answer added is labeled A"""
        try:
            pointer = ord(value) - ord(LETTER_A)
            self._correct_answer = self._answers[pointer]
        except IndexError as index_error:
            raise ValueError(f"no answer with letter {value}") from index_error
        self._correct_index = pointer
        self._correct_option = chr(ord(LETTER_A) + pointer)

    def shuffle(self) -> None:
        """Shuffle the answers.
        """
        if self._correct_answer:
            shuffle(self._answers)
            pointer = self._answers.index(self._correct_answer)
            self._correct_index = pointer
            self._correct_option = chr(ord(LETTER_A) + pointer)

    def __str__(self):
        option = f"{self._correct_option}\n"
        output = super().__str__() + option
        return output


class TrueFalseQuest(Question):
    """Multi choice question.
    """

    def __init__(self, *args):
        super().__init__(*args)
        self._answer_type = TrueFalseAnswer
        self._answers: List[self._answer_type] = []
        self.correct_option: str = ""

    def add_answer(self, answer, is_correct: bool = False) -> None:
        """Add an Answer. Correct answer is set.
        The first answer is the correct one: successive answers
        are set accordingly to is_correct argument.
        """
        logging.warning("actual answar: %s", answer)
        for ans in self.answers:
            logging.warning("pre answer: %s", ans)

        if len(self._answers) == 0:
            self._answers.append(answer)
            self.correct_answer = answer
            self.correct_option = self.correct_answer.boolean
        elif len(self._answers) == 1:
            if answer.boolean == self._correct_answer.boolean:
                raise ValueError("Only two alternative answers are allowed")
            self._answers.append(answer)
            if is_correct:
                self.correct_answer = answer
                self.correct_option = self.correct_answer.boolean
        else:
            raise ValueError("Only two alternative answers are allowed")

    def _load_1_answer(self, answer, iterator: Iterator[Any]) -> int:
        if len(self._answers) == 2:
            return 0
        iter_to_list = []
        attributes = 0
        try:
            for _ in answer.attr_load_sequence:
                iter_to_list.append(next(iterator))
                attributes += 1
            logging.warning("bool/image: %s", iter_to_list)
            answer.load_sequentially(iter(iter_to_list))
            self.add_answer(answer)
        except StopIteration:
            if len(iter_to_list) > 0:
                try:
                    answer.load_sequentially(iter(iter_to_list))
                except StopIteration:
                    self.add_answer(answer)
                    raise
            raise
        return attributes

    def shuffle(self):
        try:
            if self.answers[1].boolean:
                correct_answer = self.correct_answer
                self.answers = (self._answers[1], self._answers[0])
                self.correct_answer = correct_answer
                self.correct_option = self.correct_answer.boolean
        except IndexError:
            pass


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
