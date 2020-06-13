import exam
import pytest
from pathlib import Path
from utility import safe_int
import random


@pytest.fixture
def fake_exam():
    q1, q2, q3, q4, q5 = (
        exam.Question("q1 text"),
        exam.Question("q2 text"),
        exam.Question("q3 text"),
        exam.Question("q4 text"),
        exam.Question("q5 text")
    )

    return exam.Exam(q1, q2, q3, q4, q5)


def test_answer_load0():
    """test empty iterator without attribute:
    StopIteration must not be raised
    """
    a = exam.Answer()
    a.load_sequentially(iter(tuple()))

    assert True


def test_answer_load1():
    """test empty iterator;
    one attribute is expected
    """
    a = exam.Answer()
    a._attr_load_sequence = ("A",)
    a._type_caster_sequence = (str,)
    try:
        a.load_sequentially(iter(tuple()))
    except StopIteration:
        pass


def test_answer_load2():
    """test iterator with one item and one
    attribute is expected
    """
    a = exam.Answer()
    a._attr_load_sequence = ("A",)
    a._type_caster_sequence = (int,)
    test_tuple = ("2",)
    iterator = iter(test_tuple)

    a.load_sequentially(iterator)

    assert a.A == int(test_tuple[0])

    with pytest.raises(StopIteration):
        next(iterator)


def test_answer_load3():
    """test iterator with one item and two
    attribute is expected
    """
    a = exam.Answer()
    a._attr_load_sequence = ("A", "B")
    a._type_caster_sequence = (int, str)
    test_tuple = ("2",)
    iterator = iter(test_tuple)

    with pytest.raises(StopIteration):
        a.load_sequentially(iterator)

    assert a.A == int(test_tuple[0])


def test_answer_load4():
    """test iterator with two items and one
    attribute is expected;
    test last item left in the iterator
    """
    a = exam.Answer()
    a._attr_load_sequence = ("A",)
    a._type_caster_sequence = (int,)
    test_tuple = ("2", "abc")
    iterator = iter(test_tuple)

    a.load_sequentially(iterator)

    assert a.A == int(test_tuple[0])
    assert next(iterator) == test_tuple[1]


def test_answer_load5():
    """test iterator with wrong type
    """
    a = exam.Answer()
    a._attr_load_sequence = ("A",)
    a._type_caster_sequence = (int,)
    iterator = iter("a")

    with pytest.raises(ValueError):
        a.load_sequentially(iterator)


def test_multichoiceanswer_init0():
    """test default arguments
    """
    a = exam.MultiChoiceAnswer()

    assert a.text == ""
    assert a.image == Path()


def test_multichoiceanswer_init1():
    """Test init assignment
    """
    text = "text"
    image = Path("my_pic.jpg")
    a = exam.MultiChoiceAnswer(text, image)

    assert a.text == text
    assert a.image == image


def test_multichoiceanswer_init2():
    """Test wrong arguments
    """
    image = Path()

    with pytest.raises(TypeError):
        exam.MultiChoiceAnswer(image)


def test_multichoiceanswer_init3():
    """Test wrong arguments
    """
    text = "text"
    with pytest.raises(TypeError):
        exam.MultiChoiceAnswer(image=text)


def test_multichoiceanswer_attribute():
    """Test attribute
    """
    a = exam.MultiChoiceAnswer()
    expected_attr_load_sequence = ("text", "image")
    expected_type_caster_sequence = (str, Path)

    assert a.attr_load_sequence == expected_attr_load_sequence
    assert a.type_caster_sequence == expected_type_caster_sequence


@pytest.mark.parametrize(
    "attribute, expected",
    [
        ("test", "abc"),
        pytest.param("text", 0.1, marks=pytest.mark.xfail),
        ("image", Path(r"\home")),
        pytest.param("image", r"\image.png", marks=pytest.mark.xfail),
    ],
)
def test_multichoiceanswer_set(attribute, expected):
    a = exam.MultiChoiceAnswer()
    try:
        setattr(a, attribute, expected)
    except TypeError:
        assert False

    assert getattr(a, attribute) == expected


def test_multichoiceanswer_load():
    a = exam.MultiChoiceAnswer()
    tupl = ("text",)

    with pytest.raises(StopIteration):
        a.load_sequentially(iter(tupl))
    assert a.text == tupl[0]
    assert a.image == Path()


def test_multichoiceanswer_print():
    a = exam.MultiChoiceAnswer()
    text = "Answer text"
    image = "home/mydir/image.jpg"
    i = iter((text, image))
    a.load_sequentially(i)

    assert f"text: {text}" in a.__str__()
    assert f"image: {image}" in a.__str__()


def test_truefalse_init0():
    a = exam.TrueFalseAnswer()

    assert a.boolean is False
    assert a.text == "False"


def test_truefalse_init1():
    a = exam.TrueFalseAnswer(True, Path())

    assert a.boolean is True
    assert a.text == "True"
    assert a.image == Path()


def test_truefalse_init2():
    a = exam.TrueFalseAnswer(True)
    a.boolean = False

    assert a.boolean is False
    assert a.text == "False"


def test_truefalse_init3():
    a = exam.TrueFalseAnswer(1)

    assert a.boolean is True
    assert a.text == "True"


def test_truefalse_init4():
    a = exam.TrueFalseAnswer(0)

    assert a.boolean is False
    assert a.text == "False"


def test_truefalse_attribute():
    a = exam.TrueFalseAnswer(True)
    expected_attr_load_sequence = ("boolean", "image")
    expected_type_caster_sequence = (bool, Path)

    assert a.attr_load_sequence == expected_attr_load_sequence
    assert a.type_caster_sequence == expected_type_caster_sequence


def test_question_init0():
    """Test default arguments
    """
    q = exam.Question()
    expected = ""

    assert q.text == expected


@pytest.mark.parametrize(
    "text, subject, image, level", [("text", "subject", Path(), 0)]
)
def test_question_init2(text, subject, image, level):
    """Test arguments assignments
    """
    q = exam.Question(text, subject=subject, image=image, level=level)

    assert q.text == text
    assert q.subject == subject
    assert q.image == image
    assert q.level == level


@pytest.mark.parametrize(
    "attribute, expected",
    [
        ("image", Path()),
        ("subject", ""),
        ("level", 0),
        ("answers", tuple()),
        ("correct_answer", None),
        ("attr_load_sequence", ("text", "subject", "image", "level")),
        ("_type_caster_sequence", (str, str, Path, safe_int)),
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


def test_question_answer_add0():
    """Test one answer addition
    and correctness
    """
    q = exam.Question("Who are you?")
    a = exam.Answer()
    q.add_answer(a)

    assert a in q.answers
    assert q.correct_answer == a
    assert q.correct_index == 0


def test_question_answer_add1():
    """Test two answers addition
    and correctness
    """
    q = exam.Question("Who are you?")
    a1 = exam.Answer()
    a2 = exam.Answer()
    q.add_answer(a1)
    q.add_answer(a2)

    assert q.answers == (a1, a2)
    assert q.correct_answer == a1
    assert q.correct_index == 0


def test_question_answer_setter0():
    """Test tuple addition, overwriting
    previous addition and
    correctness
    """
    q = exam.Question("Who are you?")
    a = exam.Answer()
    q.add_answer(a)
    b = exam.Answer()
    c = exam.Answer()
    q.answers = (b, c)

    assert a not in q.answers
    assert b in q.answers
    assert c in q.answers
    assert q.correct_answer == b
    assert q.correct_index == 0


def test_question_answer_correct0():
    """Test correctness of the last
    answer added when is set to correct
    """
    q = exam.Question("Who are you?")
    a1 = exam.Answer()
    a2 = exam.Answer()
    q.add_answer(a2)
    q.add_answer(a1, True)

    assert q.correct_answer == a1
    assert q.correct_index == 1


def test_question_answer_correct1():
    """Test ineffectiveness of correct setting
    for the first answer added
    """
    q = exam.Question("Who are you?")
    a1 = exam.Answer()
    q.add_answer(a1, False)

    assert q.correct_answer == a1


def test_question_correct_answer_set0():
    """Test set correct answer
    """
    q = exam.Question("Who are you?")
    a1 = exam.Answer()
    a2 = exam.Answer()
    q.add_answer(a1)
    q.add_answer(a2)
    q.correct_answer = a2

    assert q.correct_answer == a2
    assert q.correct_index == 1


def test_question_correct_answer_set1():
    """Test set correct answer index
    """
    q = exam.Question("Who are you?")
    a1 = exam.Answer()
    a2 = exam.Answer()
    q.add_answer(a1)
    q.add_answer(a2)
    q.correct_index = 1

    assert q.correct_answer == a2
    assert q.correct_index == 1


def test_question_correct_answer_set_invalid():
    """Test set invalid correct answer
    """
    q = exam.Question("Who are you?")
    a1 = exam.Answer()
    a2 = exam.Answer()
    a3 = exam.Answer()
    q.add_answer(a1)
    q.add_answer(a2)
    with pytest.raises(ValueError):
        q.correct_answer = a3


def test_question_correct_index_set_invalid():
    """Test set invalid correct answer index
    """
    q = exam.Question("Who are you?")
    a1 = exam.Answer()
    a2 = exam.Answer()
    q.add_answer(a1)
    q.add_answer(a2)
    with pytest.raises(ValueError):
        q.correct_index = 2


A1 = exam.Answer()
A2 = exam.Answer()
A3 = exam.Answer()
A4 = exam.Answer()


@pytest.mark.parametrize(
    "attribute_set, expected, attribute1_get, expected1",
    [
        ("correct_answer", A2, "correct_index", 1),
        ("correct_index", 0, "correct_answer", A1),
        ("correct_index", 2, "correct_answer", A3),
    ],
)
def test_question_set_correct(attribute_set, expected, attribute1_get, expected1):
    """Test correct set by answer and index
    """
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


def test_question_add_path_parent0():
    """Test whether path is added to Answer.image
    """
    path = Path("home/my_home/file.txt")
    quest = exam.Question("question text", image=Path())
    image_path = Path("image1.png")
    answer_1 = exam.Answer()
    answer_1.image = image_path
    answer_2 = exam.Answer()
    answer_2.image = Path()
    quest.answers = (answer_1, answer_2)
    quest.add_parent_path(path)

    assert quest.image == Path()
    assert quest.answers[0].image == path.parent / image_path
    assert quest.answers[1].image == Path()


def test_question_add_path_parent1():
    """Test whether path is added to Answer.image and
    Question.image
    """
    path = Path("home/my_home/file.txt")
    image_path = Path("image1.png")
    quest = exam.Question("question text", image=image_path)
    answer_1 = exam.Answer()
    answer_1.image = Path()
    answer_2 = exam.Answer()
    answer_2.image = image_path
    quest.answers = (answer_1, answer_2)
    quest.add_parent_path(path)

    assert quest.image == path.parent / image_path
    assert quest.answers[0].image == Path()
    assert quest.answers[1].image == path.parent / image_path


def test_question_load0():
    """Empty iterator.
    """
    tupl = ()
    quest = exam.Question()
    quest.load_sequentially(iter(tupl))

    assert quest.text == ""
    assert quest.subject == ""
    assert quest.image == Path()
    assert quest.level == 0
    assert quest.answers == ()


def test_question_load1():
    """load question text and subject; check for default image, level;
    no answer.
    """
    tupl = ("t1", "s1")
    quest = exam.Question()
    quest.load_sequentially(iter(tupl))

    assert quest.text == tupl[0]
    assert quest.subject == tupl[1]
    assert quest.image == Path()
    assert quest.level == 0
    assert quest.answers == ()


def test_question_load2():
    """load a complete question;
    no answer.
    """
    tupl = ("t1", "s1", "p1", "1")
    quest = exam.Question()
    quest.load_sequentially(iter(tupl))

    assert quest.text == tupl[0]
    assert quest.subject == tupl[1]
    assert quest.image == Path(tupl[2])
    assert quest.level == int(tupl[3])
    assert quest.answers == ()


def test_question_load3():
    """load a complete question; the last item is lost
    because answer does not have any attribute
    """
    tupl = ("t1", "s1", "p1", "1", "a1")
    quest = exam.Question()
    quest.load_sequentially(iter(tupl))

    assert quest.text == tupl[0]
    assert quest.subject == tupl[1]
    assert quest.image == Path(tupl[2])
    assert quest.level == int(tupl[3])
    assert quest.answers == ()


def test_question_load4(monkeypatch):
    """load a complete question and one more item
    for partly fill an answer
    """

    class MonkeyAnswer(exam.Answer):
        def __init__(self):
            super().__init__()
            self._attr_load_sequence = ("text", "image")
            self._type_caster_sequence = (str, str)

    tupl = ("t1", "s1", "p1", "1", "a1")
    quest = exam.Question()
    monkeypatch.setattr(quest, "_answer_type", MonkeyAnswer)
    quest.load_sequentially(iter(tupl))

    assert quest.text == tupl[0]
    assert quest.subject == tupl[1]
    assert quest.image == Path(tupl[2])
    assert quest.level == int(tupl[3])
    assert quest.answers[0].text == tupl[4]


def test_question_load5(monkeypatch):
    """load a complete question and answer
    """

    class MonkeyAnswer(exam.Answer):
        def __init__(self):
            super().__init__()
            self._attr_load_sequence = ("text",)
            self._type_caster_sequence = (str,)

    tupl = ("t1", "s1", "p1", "1", "a1")
    quest = exam.Question()
    monkeypatch.setattr(quest, "_answer_type", MonkeyAnswer)
    quest.load_sequentially(iter(tupl))

    assert quest.text == tupl[0]
    assert quest.subject == tupl[1]
    assert quest.image == Path(tupl[2])
    assert quest.level == int(tupl[3])
    assert quest.answers[0].text == tupl[4]


def test_question_load6(monkeypatch):
    """load a complete question and two answers
    """

    class MonkeyAnswer(exam.Answer):
        def __init__(self):
            super().__init__()
            self._attr_load_sequence = ("text", "image")
            self._type_caster_sequence = (str, str)

    tupl = ("t1", "s1", "p1", "1", "a00", "a01", "a10")
    quest = exam.Question()
    monkeypatch.setattr(quest, "_answer_type", MonkeyAnswer)
    quest.load_sequentially(iter(tupl))

    assert quest.text == tupl[0]
    assert quest.subject == tupl[1]
    assert quest.image == Path(tupl[2])
    assert quest.level == int(tupl[3])
    assert quest.answers[0].text == tupl[4]
    assert quest.answers[0].image == tupl[5]
    assert quest.answers[1].text == tupl[6]


def test_question_print():
    """test __str__ method
    """
    quest = exam.Question()
    quest_text = "Text"
    quest_subject = "Subject"
    quest_image = "dir/ec/tor/y"
    quest_level = 1
    iterator = iter((quest_text, quest_subject, quest_image, quest_level))
    quest.load_sequentially(iterator)

    assert f"text: {quest.text}" in quest.__str__()
    assert f"subject: {quest_subject}" in quest.__str__()
    assert f"image: {quest_image}" in quest.__str__()
    assert f"level: {quest_level}" in quest.__str__()


def test_mcquestion_init0():
    """test init with no answer
    """
    q = exam.MultiChoiceQuest()

    assert q.text == ""
    assert q.subject == ""
    assert q.image == Path()
    assert q.level == 0


def test_mcquestion_init1():
    """test init with no answer
    """
    text, subject, image, level = ("q text", "q subject", Path("image.png"), 2)
    q = exam.MultiChoiceQuest(text, subject, image, level)

    assert q.text == text
    assert q.subject == subject
    assert q.image == image
    assert q.level == level


def test_mcquestion_add():
    """Test add answer
    """
    q = exam.MultiChoiceQuest("Who are you?")
    a1 = exam.MultiChoiceAnswer("That's me.")
    q.add_answer(a1)

    assert q.correct_answer == a1
    assert q.correct_index == 0
    assert q.correct_option == "A"


def test_mcquestion_shuffle1():
    """Test shuffle with one question added
    """
    q = exam.MultiChoiceQuest("Who are you?")
    a1 = exam.MultiChoiceAnswer("That's me.")
    q.add_answer(a1)
    random.seed(1)
    q.shuffle()

    assert q.correct_answer == a1
    assert q.correct_index == 0
    assert q.correct_option == "A"


def test_mcquestion_shuffle2():
    """Test shuffle with more question added
    """
    q = exam.MultiChoiceQuest("Who are you?")
    a1 = exam.MultiChoiceAnswer("That's me.")
    a2 = exam.MultiChoiceAnswer("That's not me.")
    a3 = exam.MultiChoiceAnswer("That's him")
    a4 = exam.MultiChoiceAnswer("That's her.")
    q.add_answer(a1)
    q.add_answer(a2, True)
    q.add_answer(a3)
    q.add_answer(a4)
    random.seed(1)
    q.shuffle()

    assert q.answers == (a4, a1, a3, a2)
    assert q.correct_answer == a2
    assert q.correct_index == 3
    assert q.correct_option == "D"


def test_mcquestion_load0():
    """load question and two answers.
    """
    tupl = ("t", "s", "i", 1, "a1", "ai1", "a", "ai2")
    quest = exam.MultiChoiceQuest()
    quest.load_sequentially(iter(tupl))

    assert quest.text == tupl[0]
    assert quest.subject == tupl[1]
    assert quest.image == Path(tupl[2])
    assert quest.level == tupl[3]
    assert quest.answers != ()
    assert quest.answers[0].text == tupl[4]
    assert quest.answers[0].image == Path(tupl[5])
    assert quest.answers[1].text == tupl[6]
    assert quest.answers[1].image == Path(tupl[7])
    with pytest.raises(IndexError):
        _ = quest.answers[2]


def test_mcquestion_load1():
    """load question and only answer text;
    answer image checked for default value.
    """
    quest = exam.MultiChoiceQuest()
    sequence = ("Text", "Subject", "dir/ec/tor/y", 1, "Answer")
    iterator = iter(sequence)
    quest.load_sequentially(iterator)

    assert quest.text == sequence[0]
    assert quest.subject == sequence[1]
    assert quest.image == Path(sequence[2])
    assert quest.level == sequence[3]
    assert quest.answers[0].text == sequence[4]
    assert quest.answers[0].image == Path(".")
    with pytest.raises(IndexError):
        _ = quest.answers[1]


def test_mcquestion_load2():
    """load question and only some empty answers;
    check empty answers are not loaded.
    """
    quest = exam.MultiChoiceQuest()
    sequence = (
        "Text",
        "Subject",
        "dir/ec/tor/y",
        1,
        "",
        "",
        "Answer",
        "",
        "",
        "",
        "",
        "image.png",
    )
    iterator = iter(sequence)
    quest.load_sequentially(iterator)

    assert quest.text == sequence[0]
    assert quest.subject == sequence[1]
    assert quest.image == Path(sequence[2])
    assert quest.level == sequence[3]
    assert quest.answers[0].text == sequence[6]
    assert quest.answers[0].image == Path(".")
    assert quest.answers[1].text == sequence[10]
    assert quest.answers[1].image == Path(sequence[11])
    with pytest.raises(IndexError):
        _ = quest.answers[2]


def test_tfquestion_init0():
    quest = exam.TrueFalseQuest()

    assert quest.text == ""
    assert quest.subject == ""
    assert quest.image == Path()
    assert quest.level == 0


def test_tfquestion_init1():
    """test init with no answer
    """
    text, subject, image, level = ("q text", "q subject", Path("image.png"), 2)
    quest = exam.TrueFalseQuest(text, subject, image, level)

    assert quest.text == text
    assert quest.subject == subject
    assert quest.image == image
    assert quest.level == level


def test_tfquestion_add0():
    """test add an answer
    """
    answer = exam.TrueFalseAnswer(True)
    quest = exam.TrueFalseQuest()
    quest.add_answer(answer)

    assert quest.answers == (answer,)
    assert quest.correct_answer == answer


def test_tfquestion_add1():
    """test add 2 answer
    """
    true_answer = exam.TrueFalseAnswer(True)
    false_answer = exam.TrueFalseAnswer(False)
    quest = exam.TrueFalseQuest()
    quest.answers = (true_answer, false_answer)

    assert quest.answers == (true_answer, false_answer)
    assert quest.correct_answer == true_answer


def test_tfquestion_add2():
    """test add 2 answer
    """
    true_answer_1 = exam.TrueFalseAnswer(True)
    true_answer_2 = exam.TrueFalseAnswer(True)
    quest = exam.TrueFalseQuest()
    quest.add_answer(true_answer_1)

    with pytest.raises(ValueError):
        quest.add_answer(true_answer_2)


def test_tfquestion_add3():
    """test add 3 answer ... maybe redundant
    """
    true_answer_1 = exam.TrueFalseAnswer(True)
    false_answer = exam.TrueFalseAnswer(False)
    true_answer_2 = exam.TrueFalseAnswer(True)
    quest = exam.TrueFalseQuest()
    quest.add_answer(true_answer_1)

    with pytest.raises(ValueError):
        quest.answers = (true_answer_1, false_answer, true_answer_2)


def test_tfquestion_load0():
    """load question and two answers.
    """
    tupl = ("t", "s", "i", 1, "1", "image", "", "")
    quest = exam.TrueFalseQuest()
    quest.load_sequentially(iter(tupl))

    assert quest.text == tupl[0]
    assert quest.subject == tupl[1]
    assert quest.image == Path(tupl[2])
    assert quest.level == tupl[3]
    assert quest.answers != ()
    assert quest.answers[0].boolean == bool(tupl[4])
    assert quest.answers[0].image == Path(tupl[5])
    assert quest.answers[1].boolean == bool(tupl[6])
    assert quest.answers[1].image == Path(tupl[7])
    with pytest.raises(IndexError):
        _ = quest.answers[2]


def test_exam():
    """test Exam with no args
    """
    ex = exam.Exam()

    assert ex.questions == tuple()


def test_exam_init():
    """test Exam with one and two arguments
    """
    q1, q2 = exam.Question("q1 text", "q1 image"), exam.Question("q2 text", "q2 image")
    ex1 = exam.Exam(q1)
    ex2 = exam.Exam(q1, q2)

    assert ex1.questions == (q1,)
    assert ex2.questions == (q1, q2)


def test_exam_questions_setter0():
    """test question set
    """
    q1, q2 = exam.Question("q1 text", "q1 image"), exam.Question("q2 text", "q2 image")
    ex = exam.Exam()
    ex.add_question(q1)
    ex.add_question(q2)

    assert q1 in ex.questions
    assert q2 in ex.questions


def test_exam_questions_setter1():
    """test question set; question added before overwritten
    """
    q1, q2 = exam.Question("q1 text", "q1 image"), exam.Question("q2 text", "q2 image")
    ex = exam.Exam()
    ex.add_question(q1)
    ex.questions = (q2,)

    assert q1 not in ex.questions
    assert q2 in ex.questions


def test_exam_attribute_selector1():
    """test attribute_selector default value"""
    ex = exam.Exam()

    assert ex.attribute_selector == ()


def test_exam_attribute_selector2():
    """test attribute_selector set and type conversion
    """
    ex = exam.Exam()
    expected = ("hello", "2", "times")
    ex.attribute_selector = (expected[0], int(expected[1]), expected[2])

    assert ex.attribute_selector == expected


def test_exam_add_path_parent():
    image = Path("images/image.png")
    path = Path("/project/A/")
    q1 = exam.MultiChoiceQuest("q1 text", "")
    q1.answers = (
        exam.MultiChoiceAnswer("a1 text", image),
        exam.MultiChoiceAnswer("a2 text", image),
    )
    q2 = exam.MultiChoiceQuest("q2 text", "", image)
    q2.add_answer(exam.MultiChoiceAnswer("a3 text"))
    ex = exam.Exam(q1, q2)
    ex.add_path_parent(path)

    assert ex.questions[0].image == Path()
    assert ex.questions[0].answers[0].image == path.parent / image
    assert ex.questions[0].answers[1].image == path.parent / image
    assert ex.questions[1].image == path.parent / image
    assert ex.questions[1].answers[0].image == Path()


def test_exam_load1():
    """test empty iterable
    """
    ex = exam.Exam()
    ex.load(iter(()))

    assert ex.questions == tuple()


def test_exam_load2():
    """test without setting _attribute_selector
    2 rows -> 2 questions with 2 answers each but second answer image is not provided
    """
    data = (
        dict(
            [
                ("text", "ab"),
                ("subject", "ac"),
                ("image", "ad"),
                ("level", "1"),
                ("a0 text", "ae"),
                ("a0 image", "af"),
                ("a1 text", "ag"),
            ]
        ),
        dict(
            [
                ("text", "ba"),
                ("subject", "bc"),
                ("image", "bd"),
                ("level", "2"),
                ("a0 text", "be"),
                ("a0 image", "bf"),
                ("a1 text", "bg"),
            ]
        ),
    )
    ex = exam.Exam()
    ex.load(data)

    for i in (0, 1):
        assert ex.questions[i].text == data[i]["text"]
        assert ex.questions[i].subject == data[i]["subject"]
        assert ex.questions[i].image == Path(data[i]["image"])
        assert ex.questions[i].level == int(data[i]["level"])
        assert ex.questions[i].answers[0].text == data[i]["a0 text"]
        assert ex.questions[i].answers[0].image == Path(data[i]["a0 image"])
        assert ex.questions[i].answers[1].text == data[i]["a1 text"]
        assert ex.questions[i].answers[1].image == Path()  # default value

    # third answer of second question is not provided
    with pytest.raises(IndexError):
        _ = ex.questions[1].answers[2]

    # third question is not provided
    with pytest.raises(IndexError):
        _ = ex.questions[2]


def test_exam_load3():
    """test without setting _attribute_selector
    and missing row
    """
    ex = exam.Exam()
    reader = (dict([]), dict([("A", "What?"), ("B", "topic")]))
    ex.load(reader)

    assert ex.questions[0].text == "What?"
    assert ex.questions[0].subject == "topic"


def test_exam_load4():
    """test setting _attribute_selector
    """
    data = (
        dict(
            [
                ("A text", "A"),
                ("B text", "B"),
                ("text", "T"),
                ("C text", "A3"),
                ("D text", "A4"),
                ("subject", "S"),
                ("level", 2),
                ("void", ""),
            ]
        ),
    )
    ex = exam.Exam()
    ex.attribute_selector = (
        "text",
        "subject",
        "void",
        "level",
        "A text",
        "void",
        "B text",
        "void",
        "C text",
    )
    ex.load(data)

    assert ex.questions[0].text == data[0]["text"]
    assert ex.questions[0].subject == data[0]["subject"]
    assert ex.questions[0].image == Path()
    assert ex.questions[0].level == data[0]["level"]
    assert ex.questions[0].answers[0].text == data[0]["A text"]
    assert ex.questions[0].answers[0].image == Path()
    assert ex.questions[0].answers[1].text == data[0]["B text"]
    assert ex.questions[0].answers[1].image == Path()
    assert ex.questions[0].answers[2].text == data[0]["C text"]
    assert ex.questions[0].answers[2].image == Path()

    # no further elements loaded
    with pytest.raises(IndexError):
        _ = ex.questions[0].answers[3]
    with pytest.raises(IndexError):
        _ = ex.questions[1].answers[2]


def test_answers_shuffle():
    data = (
        dict(
            [
                ("question", " Q1"),
                ("A", "A1"),
                ("B", "B1"),
                ("C", "C1"),
                ("D", "D1"),
                ("E", "E1"),
                ("void", ""),
            ]
        ),
        dict(
            [
                ("question", "Q2"),
                ("A", "A2"),
                ("B", "B2"),
                ("C", "C2"),
                ("D", "D2"),
                ("E", "E2"),
                ("void", ""),
            ]
        ),
    )
    correct_values = ("D", "C")
    ex = exam.Exam()
    ex.attribute_selector = (
        "question",
        "void",
        "void",
        "void",
        "A",
        "void",
        "B",
        "void",
        "C",
        "void",
        "D",
        "void",
        "E",
    )
    ex.load(data)
    ex.answers_shuffle()

    for question, value in zip(ex.questions, correct_values):
        assert question.correct_option == value


def test_questions_shuffle(fake_exam):
    """GIVEN exam with five questions
    WHEN questions_shuffle is called (questions order is mixed)
    THEN questions order is changed
    """
    expected_text = ("q3 text", "q4 text", "q5 text", "q1 text", "q2 text")

    ex = fake_exam
    random.seed(1)
    ex.questions_shuffle()

    for i, question in enumerate(ex.questions):
        assert question.text == expected_text[i]


def test_exam_print():
    data = (
        dict(
            [
                ("field A", "A1"),
                ("field B", "A2"),
                ("field C", "T"),
                ("field D", "A3"),
                ("field E", "A4"),
                ("field F", "S"),
                ("field G", 2),
                ("void", ""),
            ]
        ),
    )
    text, q_image, level, a_image = f"text: A1", f"image: .", f"level: 2", f"image: S"
    ex = exam.Exam()
    ex.attribute_selector = ("field A", "void", "void", "field G", "void", "field F")
    ex.load(data)

    assert text in ex.__str__()
    assert q_image in ex.__str__()
    assert level in ex.__str__()
    assert a_image in ex.__str__()


def test_exam_mcquestion():
    mcquestion1 = exam.MultiChoiceQuest("mc quest1 text", "subject")
    mcquestion1.answers = (
        exam.MultiChoiceAnswer("Q1 A1"),
        exam.MultiChoiceAnswer("Q1 A2"),
        exam.MultiChoiceAnswer("Q1 A3"),
    )
    mcquestion2 = exam.MultiChoiceQuest("mc quest2 text", "subject")
    mcquestion2.answers = (
        exam.MultiChoiceAnswer("Q2 A1"),
        exam.MultiChoiceAnswer("Q2 A2"),
        exam.MultiChoiceAnswer("Q2 A3"),
    )

    ex = exam.Exam(mcquestion1, mcquestion2)

    assert ex.questions[0].answers[1].image == Path()
    assert ex.questions[0].correct_answer.text == "Q1 A1"
    assert ex.questions[1].text == "mc quest2 text"


def test_exam_tfquestion():
    tfquestion1 = exam.MultiChoiceQuest("mc quest1 text", "subject")
    tfquestion1.answers = (exam.TrueFalseAnswer(True), exam.TrueFalseAnswer(False))
    tfquestion2 = exam.MultiChoiceQuest("mc quest2 text", "subject")
    tfquestion2.answers = (exam.TrueFalseAnswer(False), exam.TrueFalseAnswer(True))

    ex = exam.Exam(tfquestion1, tfquestion2)

    assert ex.questions[0].answers[1].image == Path()
    assert ex.questions[0].correct_answer.boolean is True
    assert ex.questions[1].text == "mc quest2 text"
    assert ex.questions[1].correct_answer.text == "False"


def test_exam_mixquestion():
    mcquestion = exam.MultiChoiceQuest("mc quest1 text", "subject")
    mcquestion.answers = (
        exam.MultiChoiceAnswer("Q1 A1"),
        exam.MultiChoiceAnswer("Q1 A2"),
        exam.MultiChoiceAnswer("Q1 A3"),
    )
    tfquestion = exam.MultiChoiceQuest("mc quest2 text", "subject")
    tfquestion.answers = (exam.TrueFalseAnswer(False), exam.TrueFalseAnswer(True))

    ex = exam.Exam(mcquestion, tfquestion)

    assert ex.questions[0].answers[1].image == Path()
    assert ex.questions[0].correct_option == "A"
    assert ex.questions[1].text == "mc quest2 text"
    assert ex.questions[1].correct_answer.text == "False"
