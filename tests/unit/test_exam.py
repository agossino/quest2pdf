import exam
import pytest
from pathlib import Path


def test_answer_text1():
    a = exam.Answer()
    expected = ""

    assert a.text == ""


def test_answer_text2():
    text = "Roma"
    q = exam.Answer(text)

    assert q.text == text


@pytest.mark.parametrize(
    "attribute, expected",
    [("image", Path(".")),
     ("is_correct", True)],
)
def test_answer_get(attribute, expected):
    text = "Po"
    q = exam.Answer(text)

    assert getattr(q, attribute) == expected


@pytest.mark.parametrize(
    "attribute, expected",
    [pytest.param("text", 0.1, marks=pytest.mark.xfail),
     ("image", Path(r"\home")),
     pytest.param("image", r"\home", marks=pytest.mark.xfail),
     ("is_correct", False),
     pytest.param("is_correct", 1_000, marks=pytest.mark.xfail)],
)
def test_answer_set(attribute, expected):
    q = exam.Answer()
    try:
        setattr(q, attribute, expected)
    except TypeError:
        assert False

    assert getattr(q, attribute) == expected


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
     ("level", 0),
     ("answers", set())],
)
def test_question_get(attribute, expected):
    text = "What's your name?"
    q = exam.Question(text)

    assert getattr(q, attribute) == expected


@pytest.mark.parametrize(
    "attribute, expected",
    [pytest.param("text", 0.1, marks=pytest.mark.xfail),
     ("image", Path(r"\home")),
     pytest.param("image", r"\home", marks=pytest.mark.xfail),
     ("subject", "Math"),
     pytest.param("subject", 1_000, marks=pytest.mark.xfail),
     ("level", 1_000),
     pytest.param("level", 1_000.01, marks=pytest.mark.xfail)],
)
def test_question_set(attribute, expected):
    q = exam.Question()
    try:
        setattr(q, attribute, expected)
    except TypeError:
        assert False

    assert getattr(q, attribute) == expected


def test_question_answer_add():
    q = exam.Question("Who are you?")
    a = exam.Answer("That's me.")
    q.add_answer(a)

    assert a in q.answers


def test_question_answer_add_autoset():
    q = exam.Question("Who are you?")
    a1 = exam.Answer("That's me.")
    a2 = exam.Answer("That's not me.")
    q.add_answer(a2)
    q.add_answer(a1)

    assert a1 in q.answers
