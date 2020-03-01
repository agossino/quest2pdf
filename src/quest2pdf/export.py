from enum import Enum
from collections import namedtuple
from pathlib import Path
from typing import Iterator, Generator
import rlwrapper
import exam


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

    def __init__(self, exam_alike: exam.Exam):
        self._exam: exam.Exam = exam_alike

    def serialize(self) -> Generator[Item, None, None]:
        for question in self._exam.questions:
            yield Item(ItemLevel.top, question.text, question.image)
            for answer in question.answers:
                yield Item(ItemLevel.sub, answer.text, answer.image)


class RLInterface:
    def __init__(self, input_generator: Iterator[Item], output_file: Path, **kwargs):
        """This class print a two nesting level series of items in pdf.
        """
        self.file_name = output_file
        self.input = input_generator
        self._doc = rlwrapper.PDFDoc(output_file)

    def build(self) -> None:
        try:
            item = next(self.input)
            assert item.item_level == ItemLevel.top
            self._doc.add_item(item)
            while True:
                item = next(self.input)
                if item.item_level == ItemLevel.top:
                    self._doc.add_item(item)
                elif item.item_level == ItemLevel.sub:
                    self._doc.add_sub_item(item)
                else:
                    raise ValueError
        except StopIteration:
            self._doc.build()
