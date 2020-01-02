#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Tuple, List
import logging
from random import shuffle


LOGNAME = "quest2pdf." + __name__
LOGGER = logging.getLogger(LOGNAME)


class Answer:
    def __init__(self, text: str = ""):
        self.text: str = text
        self.image: Path = Path(".")

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str):
        if isinstance(text, str):
            self._text = text
        else:
            raise TypeError(f"{text} is not a string")

    @property
    def is_correct(self) -> bool:
        return self._is_correct

    @is_correct.setter
    def is_correct(self, value: bool):
        if isinstance(value, bool):
            self._is_correct = value
        else:
            raise TypeError(f"{value} is not a Path")

    @property
    def image(self) -> Path:
        return self._image

    @image.setter
    def image(self, file_path: str):
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
        self._correct_answer = None

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str):
        if isinstance(text, str):
            self._text = text
        else:
            raise TypeError(f"{text} in not a string")

    @property
    def image(self) -> Path:
        return self._image

    @image.setter
    def image(self, file_path: str):
        if isinstance(file_path, Path):
            self._image = file_path
        else:
            raise TypeError(f"{file_path} is not a Path")

    @property
    def subject(self) -> str:
        return self._subject

    @subject.setter
    def subject(self, name: str):
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
    def answers(self) -> Tuple[Answer]:
        return tuple(self._answers)

    def add_answer(self, answer: Answer, is_correct: bool = True) -> None:
        """Add an Answer. As side effect, correct answer is set.
        The first answer is the correct one: successive answers
        are set accordingly to is_correct.
        """
        if isinstance(answer, Answer):
            self._correct_answer = self._set_correctness(answer, is_correct)
            self._answers.append(answer)
        else:
            raise TypeError(f"{answer} is not an Answer")

    @property
    def correct_answer(self) -> Answer:
        return self._correct_answer

    def _set_correctness(self, answer: Answer, is_correct: bool) -> Answer:
        if len(self._answers) == 0 or is_correct:
            return answer
        else:
            return self._correct_answer

    def shuffle(self) -> None:
        shuffle(self._answers)
        ix = self._answers.index(self._correct_answer)
        print(ix, chr(ord("A") + ix))


if __name__ == "__main__":
    q = Question("Who are you?")
    a1 = Answer("That's me.")
    a2 = Answer("That's not me.")
    a3 = Answer("That's him")
    a4 = Answer("That's her.")
    q.add_answer(a1)
    q.add_answer(a2)
    q.add_answer(a3)
    q.add_answer(a4)
    from random import seed

    seed(1)
    q.shuffle()
    q.shuffle()
