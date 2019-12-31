import exam
import pytest
from pathlib import Path


def test_question_get_text1():
    q = exam.Question()
    expected = ""

    assert q.text == expected


def test_question_set_text2():
    text = "How old are you?"
    q = exam.Question(text)

    assert q.text == text


@pytest.mark.parametrize(
    "attribute, expected",
    [("image", Path(".")),
     ("subject", ""),
     ("level", 0)],
)
def test_question_get(attribute, expected):
    text = "What's your name?"
    q = exam.Question(text)

    assert q.__getattribute__(attribute) == expected

@pytest.mark.parametrize(
    "attribute, expected",
    [pytest.param("text", 0.1, marks=pytest.mark.xfail),
     ("image", Path(r"\home")),
     pytest.param("image", r"\home", marks=pytest.mark.xfail),
     ("subject", "Math"),
     pytest.param("subject", 1_000, marks=pytest.mark.xfail),
     ("level", 1_000),
     pytest.param("level", 1_000.1, marks=pytest.mark.xfail)],
)
def test_question_set(attribute, expected):
    q = exam.Question()
    setattr(q, attribute, expected)

    assert getattr(q, attribute) == expected
