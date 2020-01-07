#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO
# Question attribute type_of_question
# open_ended, yes_no, multi_choice
# based on number of alternative answers provided

from pathlib import Path
from typing import (Tuple, List, Optional, Iterator,
                    Mapping, Any, Sequence, Callable)
import logging
from random import shuffle


LOGNAME = "quest2pdf." + __name__
LOGGER = logging.getLogger(LOGNAME)
LETTER_A = "A"


class SorterSelector:
    """Provide an iterator to the decorated function
    with only the values with the keys given in the
    decorator arguments, and with the given order.
    """
    def __init__(self, sequence_of_keys_to_be_in: Sequence[str]):
        self._sequence: Sequence[str] = sequence_of_keys_to_be_in

    def __call__(self,
                 function: Callable[Iterator[Any], None]) -> Mapping[str, Any]:
        def wrapper(mapping: Mapping[str, Any]) -> Callable[[Iterator[Any]], None]:
            iterator: Iterator[Any] = (mapping[key] for key in self._sequence)
            return function(iterator)

        return wrapper


class Answer:
    def __init__(self, text: str = ""):
        self.text: str = text
        self.image: Path = Path(".")

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        if isinstance(text, str):
            self._text = text
        else:
            raise TypeError(f"{text} is not a string")

    @property
    def image(self) -> Path:
        return self._image

    @image.setter
    def image(self, file_path: Path) -> None:
        if isinstance(file_path, Path):
            self._image = file_path
        else:
            raise TypeError(f"{file_path} is not a Path")


class Question:
    def __init__(self, text: str = ""):
        self.text: str = text
        self.image: Path = Path(".")
        self.subject: str = ""
        self.level: int = 0
        self._answers: List[Answer] = []
        self._correct_answer: Optional[Answer] = None  # setter bypassed
        self._correct_index: Optional[int] = None  # setter bypassed
        self._correct_letter: Optional[str] = None  # setter bypassed

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        if isinstance(text, str):
            self._text = text
        else:
            raise TypeError(f"{text} in not a string")

    @property
    def image(self) -> Path:
        return self._image

    @image.setter
    def image(self, file_path: Path) -> None:
        if isinstance(file_path, Path):
            self._image = file_path
        else:
            raise TypeError(f"{file_path} is not a Path")

    @property
    def subject(self) -> str:
        return self._subject

    @subject.setter
    def subject(self, name: str) -> None:
        if isinstance(name, str):
            self._subject = name
        else:
            raise TypeError(f"{name} is not a string")

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value: int) -> None:
        if isinstance(value, int):
            self._level = value
        else:
            raise TypeError(f"{value} is not a string")

    @property
    def answers(self) -> Tuple[Answer, ...]:
        return tuple(self._answers)

    def add_answer(self, answer: Answer, is_correct: bool = False) -> None:
        """Add an Answer. As side effect, correct answer is set.
        The first answer is the correct one: successive answers
        are set accordingly to is_correct.
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
        """Load all the attribute sequentially
        from iterator.
        """
        try:
            self.text = next(iterator)
            self.subject = next(iterator)
            self.image = Path(next(iterator))
            while True:
                answer = Answer()
                answer.text = next(iterator)
                self.add_answer(answer)
                answer.image = Path(next(iterator))
        except StopIteration:
            pass
