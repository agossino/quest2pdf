import pytest
from export import ItemLevel, Item, SerializeExam


class Ans:
    def __init__(self, *values):
        self.text, self.image = values


class Quest:
    def __init__(self, *values):
        self.text, self.image, *self.answers = values


class Ex:
    def __init__(self, *values):
        self.questions = values


def test_serialize0():
    exam = Ex()
    expected = SerializeExam(exam).serialize()

    with pytest.raises(StopIteration):
        next(expected)


def test_serialize1():
    exam = Ex(Quest("1", "2", Ans("3", "4"), Ans("5", "6")),
              Quest("7", "8"),
              Quest("9", "10", Ans("11", "12")))
    expected = SerializeExam(exam).serialize()

    item = next(expected)
    assert item.item_level == ItemLevel.top
    assert item.text == exam.questions[0].text
    assert item.image == exam.questions[0].image
    item = next(expected)
    assert item.item_level == ItemLevel.sub
    assert item.text == exam.questions[0].answers[0].text
    assert item.image == exam.questions[0].answers[0].image
    item = next(expected)
    assert item.item_level == ItemLevel.sub
    assert item.text == exam.questions[0].answers[1].text
    assert item.image == exam.questions[0].answers[1].image
    item = next(expected)
    assert item.item_level == ItemLevel.top
    assert item.text == exam.questions[1].text
    assert item.image == exam.questions[1].image
    item = next(expected)
    assert item.item_level == ItemLevel.top
    assert item.text == exam.questions[2].text
    assert item.image == exam.questions[2].image
    item = next(expected)
    assert item.item_level == ItemLevel.sub
    assert item.text == exam.questions[2].answers[0].text
    assert item.image == exam.questions[2].answers[0].image

    with pytest.raises(StopIteration):
        next(expected)
