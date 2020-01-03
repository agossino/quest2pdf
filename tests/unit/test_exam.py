import exam
import pytest
from pathlib import Path
import random


def test_answer_text1():
    a = exam.Answer()
    expected = ""

    assert a.text == ""


def test_answer_text2():
    text = "Roma"
    q = exam.Answer(text)

    assert q.text == text


@pytest.mark.parametrize("attribute, expected", [("image", Path("."))])
def test_answer_get(attribute, expected):
    text = "Po"
    q = exam.Answer(text)

    assert getattr(q, attribute) == expected


@pytest.mark.parametrize(
    "attribute, expected",
    [
        pytest.param("text", 0.1, marks=pytest.mark.xfail),
        ("image", Path(r"\home")),
        pytest.param("image", r"\home", marks=pytest.mark.xfail),
    ],
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
    [
        ("image", Path(".")),
        ("subject", ""),
        ("level", 0),
        ("answers", tuple()),
        ("correct_answer", None),
        ("correct_index", None),
        ("correct_letter", None)
    ],
)
def test_question_get(attribute, expected):
    """Test default attribute values
    """
    text = "What's your name?"
    q = exam.Question(text)

    assert getattr(q, attribute) == expected


@pytest.mark.parametrize(
    "attribute, expected",
    [
        pytest.param("text", 0.1, marks=pytest.mark.xfail),
        ("image", Path(r"\home")),
        pytest.param("image", r"\home", marks=pytest.mark.xfail),
        ("subject", "Math"),
        pytest.param("subject", 1000, marks=pytest.mark.xfail),
        ("level", 1000),
        pytest.param("level", 1000.01, marks=pytest.mark.xfail),
    ],
)
def test_question_set(attribute, expected):
    """Test set right and wrong attribute
    """
    q = exam.Question()
    try:
        setattr(q, attribute, expected)
    except TypeError:
        assert False

    assert getattr(q, attribute) == expected


def test_question_answer_add():
    """Test one answer addition
    """
    q = exam.Question("Who are you?")
    a = exam.Answer("That's me.")
    q.add_answer(a)

    assert a in q.answers


def test_question_answer_correct1():
    """Test correctness of the only
    answer added
    """
    q = exam.Question("Who are you?")
    a = exam.Answer("That's me.")
    q.add_answer(a)

    assert q.correct_answer == a
    assert q.correct_index == 0
    assert q.correct_letter == "A"


def test_question_answer_add2():
    """Test two answers addition
    and correctness
    """
    q = exam.Question("Who are you?")
    a1 = exam.Answer("That's me.")
    a2 = exam.Answer("That's not me.")
    q.add_answer(a1)
    q.add_answer(a2)

    assert q.answers == (a1, a2)
    assert q.correct_index == 1
    assert q.correct_letter == "B"


def test_question_answer_correct2():
    """Test correctness of the first
    answer added when the successive
    is set to wrong
    """
    q = exam.Question("Who are you?")
    a1 = exam.Answer("That's me.")
    a2 = exam.Answer("That's not me.")
    q.add_answer(a2)
    q.add_answer(a1, False)

    assert q.correct_answer == a2


def test_question_answer_correct3():
    """Test ineffectiveness of correct setting
    for the first answer added
    """
    q = exam.Question("Who are you?")
    a1 = exam.Answer("That's me.")
    q.add_answer(a1, False)

    assert q.correct_answer == a1


A1 = exam.Answer("That's me.")
A2 = exam.Answer("That's not me.")
A3 = exam.Answer("That's him")
A4 = exam.Answer("That's her.")


@pytest.mark.parametrize(
    "attribute_set, expected, attribute1_get, expected1, attribute2_get, expected2",
    [
        ("correct_answer", A2, "correct_index", 1, "correct_letter", "B"),
        ("correct_index", 0, "correct_answer", A1, "correct_letter", "A"),
        ("correct_letter", "C", "correct_index", 2, "correct_answer", A3)
    ],
)
def test_question_set_correct(attribute_set, expected,
                              attribute1_get, expected1,
                              attribute2_get, expected2):
    q = exam.Question("Who are you?")
    q.add_answer(A1)
    q.add_answer(A2)
    q.add_answer(A3)
    q.add_answer(A4)

    try:
        setattr(q, attribute_set, expected)
    except TypeError:
        assert False

    assert getattr(q, attribute_set) == expected
    assert getattr(q, attribute1_get) == expected1
    assert getattr(q, attribute2_get) == expected2


def test_question_shuffle():
    q = exam.Question("Who are you?")
    a1 = exam.Answer("That's me.")
    a2 = exam.Answer("That's not me.")
    a3 = exam.Answer("That's him")
    a4 = exam.Answer("That's her.")
    q.add_answer(a1)
    q.add_answer(a2)
    q.add_answer(a3)
    q.add_answer(a4, False)

    assert q.answers == (a1, a2, a3, a4)
    random.seed(1)
    q.shuffle()
    assert q.answers == (a4, a1, a3, a2)
    assert q.correct_answer == a3
    assert q.correct_index == 2
    assert  q.correct_letter == "C"
