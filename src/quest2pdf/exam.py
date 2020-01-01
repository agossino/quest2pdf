#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Set
import logging


LOGNAME = 'quest2pdf.' + __name__
LOGGER = logging.getLogger(LOGNAME)


class Answer:
    def __init__(self, text: str = ""):
        self.text: str = text
        self.is_correct: bool = True
        self.image: Path = Path(".")

    @property
    def text(self):
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
        self._answers: Set[Answer] = set()

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
    def answers(self) -> Set[Answer]:
        return self._answers

    def add_answer(self, answer: Answer) -> None:
        if isinstance(answer, Answer):
            self._answers.add(answer)
        else:
            raise TypeError(f"{answer} is not an Answer")


if __name__ == "__main__":
    q = Question("ciao")
    a1 = Answer("That's me.")
    a2 = Answer("That's me.")
    q.add_answer(a2)
    q.add_answer(a1)
    print(q.answers)


