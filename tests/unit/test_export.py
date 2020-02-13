from export import ItemLevel, Item, SerializeExam


class Sub:
    def __init__(self, *values):
        self.text, self.image = values


class Top:
    def __init__(self, *values):
        text, image, *self.answers = values
        self.questions


def test_serialize():
    exam = (Top("text 1", "image 1",
                Sub("a text 1", "a image 1"),
                Sub("a text 2", "a image 2")),
            Top ("text 2", "image 2",
                 Sub("a text 3", "a image 3")))

    expected = SerializeExam(exam).serialize()

    item = next(expected)
    assert item.item_level == ItemLevel.top
    assert item.text == exam[0].text
    assert item.image == exam[0].image
    item = next(expected)
    assert item.item_level == ItemLevel.sub
    assert item.text == exam[0].answers[0].text
    assert item.image == exam[0].answers[0].image
    item = next(expected)
    assert item.item_level == ItemLevel.sub
    assert item.text == exam[0].answers[1].text
    assert item.image == exam[0].answers[1].image
    item = next(expected)
    assert item.item_level == ItemLevel.top
    assert item.text == exam[1].text
    assert item.image == exam[1].image
    item = next(expected)
    assert item.item_level == ItemLevel.sub
    assert item.text == exam[1].answers[0].text
    assert item.image == exam[1].answers[0].image
