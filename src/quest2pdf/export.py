from enum import Enum
from collections import namedtuple
from rlwrapper import PDFDoc


class ItemLevel(Enum):
    top = 0
    sub = 1


Item = namedtuple("Item", ["item_level", "text", "image"])


class SerializeExam:
    def __init__(self, exam):
        self._exam = exam

    def serialize(self):
        for question in self._exam.questions:
            yield Item(ItemLevel.top, question.text, question.image)
            for answer in question.answers:
                yield Item(ItemLevel.sub, answer.text, answer.image)


class RLInterface:
    def __init__(self, input_generator, output_file: str):
        """This class print a two nesting level series of items in pdf.
        """
        self.file_name = output_file
        self.input = input_generator
        self._doc = PDFDoc(output_file)

    def build(self) -> None:
        try:
            item = next(self.input)
            assert item.item_level == ItemLevel.top
            self._doc.add_item(item)
            while True:
                item = next(self.input)
                if item.sublevel == 0:
                    self._doc.add_item(item)
                elif item.sublevel == 1:
                    self._doc.add_sub_item(item)
        except StopIteration:
            self._doc.build()

