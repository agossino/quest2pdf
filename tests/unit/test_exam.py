import exam
import pytest
from pathlib import Path
from _collections import OrderedDict
import random


def test_answer_text1():
    a = exam.Answer()
    expected = ""

    assert a.text == expected


def test_answer_text2():
    text = "Roma"
    a = exam.Answer(text)

    assert a.text == text


def test_answer_get():
    text = "my answer"
    a = exam.Answer(text)
    expected_image = Path(".")
    expected_attr_load_sequence = ('text', 'image')
    expected_type_caster_sequence = (str, Path)

    assert a.image == expected_image
    assert a.attr_load_sequence == expected_attr_load_sequence
    assert a.type_caster_sequence == expected_type_caster_sequence


@pytest.mark.parametrize(
    "attribute, expected",
    [
        pytest.param("text", 0.1, marks=pytest.mark.xfail),
        ("image", Path(r"\home")),
        pytest.param("image", r"\home", marks=pytest.mark.xfail),
    ],
)
def test_answer_set(attribute, expected):
    a = exam.Answer()
    try:
        setattr(a, attribute, expected)
    except TypeError:
        assert False

    assert getattr(a, attribute) == expected


def test_answer_load0():
    """test empty iterator: load default values
    """
    a = exam.Answer()
    expected = tuple()
    i = iter(expected)
    try:
        a.load_sequentially(i)
    except StopIteration:
        pass

    assert a.text == ""
    assert a.image == Path(".")


def test_answer_load1():
    """test load only text: image has default value
    """
    a = exam.Answer()
    expected = ("Answer text",)
    i = iter(expected)
    try:
        a.load_sequentially(i)
    except StopIteration:
        pass

    assert a.text == expected[0]
    assert a.image == Path(".")


def test_answer_load2():
    """test load answer and image
    """
    a = exam.Answer()
    expected = ("Answer text", r"home/mydir/image.jpg")
    i = iter(expected)
    a.load_sequentially(i)

    assert a.text == expected[0]
    assert a.image == Path(expected[1])


def test_answer_load3():
    """test iterator bigger then answer: check last value availability
    """
    a = exam.Answer()
    expected = ("Answer text", "home/mydir/image.jpg", "rest")
    i = iter(expected)
    a.load_sequentially(i)

    assert a.text == expected[0]
    assert a.image == Path(expected[1])
    assert next(i) == expected[2]  # the last element is still available


def test_answer_print():
    a = exam.Answer()
    text = "Answer text"
    image = "home/mydir/image.jpg"
    i = iter((text, image))
    a.load_sequentially(i)

    assert f"text: {text}" in a.__str__()
    assert f"image: {image}" in a.__str__()


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
        ("correct_letter", None),
        ("attr_load_sequence", ("text", "subject", "image", "level")),
        ("type_caster_sequence", (str, str, Path, int))
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
    assert q.correct_index == 0
    assert q.correct_letter == "A"


def test_question_answer_add_wrong():
    """Test wrong answer addition
    """
    q = exam.Question("Who are you?")
    a = "That's me."
    with pytest.raises(TypeError):
        q.add_answer(a)


def test_question_answer_setter():
    """Test tuple addition and removal
    previous addition
    """
    q = exam.Question("Who are you?")
    a = exam.Answer("That's me.")
    q.add_answer(a)
    b = exam.Answer("I do not know.")
    c = exam.Answer("Somebody else.")
    q.answers = (b, c)

    assert a not in q.answers
    assert b in q.answers
    assert c in q.answers


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


def test_question_answer_correct2():
    """Test correctness of the first
    answer added when two are added
    """
    q = exam.Question("Who are you?")
    a1 = exam.Answer("That's me.")
    a2 = exam.Answer("That's not me.")
    q.add_answer(a2)
    q.add_answer(a1)

    assert q.correct_answer == a2


def test_question_answer_correct3():
    """Test correctness of the last
    answer added when is set to correct
    """
    q = exam.Question("Who are you?")
    a1 = exam.Answer("That's me.")
    a2 = exam.Answer("That's not me.")
    q.add_answer(a2)
    q.add_answer(a1, True)

    assert q.correct_answer == a1


def test_question_answer_correct4():
    """Test ineffectiveness of correct setting
    for the first answer added
    """
    q = exam.Question("Who are you?")
    a1 = exam.Answer("That's me.")
    q.add_answer(a1, False)

    assert q.correct_answer == a1


def test_question_correct_answer_set():
    """Test set correct answer
    """
    q = exam.Question("Who are you?")
    a1 = exam.Answer("That's me.")
    a2 = exam.Answer("That's not me.")
    q.add_answer(a1)
    q.add_answer(a2)
    q.correct_answer = a2

    assert q.correct_answer == a2


def test_question_correct_answer_set_invalid():
    """Test set invalid correct answer
    """
    q = exam.Question("Who are you?")
    a1 = exam.Answer("That's me.")
    a2 = exam.Answer("That's not me.")
    a3 = "That is"
    q.add_answer(a1)
    q.add_answer(a2)
    with pytest.raises(ValueError):
        q.correct_answer = a3


def test_question_correct_index_set_invalid():
    """Test set invalid correct answer index
    """
    q = exam.Question("Who are you?")
    a1 = exam.Answer("That's me.")
    a2 = exam.Answer("That's not me.")
    q.add_answer(a1)
    q.add_answer(a2)
    with pytest.raises(ValueError):
        q.correct_index = 2


def test_question_correct_letter_set_invalid():
    """Test set invalid correct answer letter
    """
    q = exam.Question("Who are you?")
    a1 = exam.Answer("That's me.")
    a2 = exam.Answer("That's not me.")
    q.add_answer(a1)
    q.add_answer(a2)
    with pytest.raises(ValueError):
        q.correct_letter = "Z"


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
    """Test set correct answer by answer, index and letter
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
    assert getattr(q, attribute2_get) == expected2


def test_question_shuffle1():
    """Test shuffle with no question added
    """
    q = exam.Question("Who are you?")
    random.seed(1)
    q.shuffle()

    assert q.answers == ()
    assert q.correct_answer is None
    assert q.correct_index is None
    assert q.correct_letter is None


def test_question_shuffle2():
    """Test shuffle with one question added
    """
    q = exam.Question("Who are you?")
    a1 = exam.Answer("That's me.")
    q.add_answer(a1)
    random.seed(1)
    q.shuffle()

    assert q.correct_answer == a1
    assert q.correct_index == 0
    assert q.correct_letter == "A"


def test_question_shuffle3():
    """Test shuffle with more question added
    """
    q = exam.Question("Who are you?")
    a1 = exam.Answer("That's me.")
    a2 = exam.Answer("That's not me.")
    a3 = exam.Answer("That's him")
    a4 = exam.Answer("That's her.")
    q.add_answer(a1)
    q.add_answer(a2, True)
    q.add_answer(a3)
    q.add_answer(a4)
    random.seed(1)
    q.shuffle()

    assert q.answers == (a4, a1, a3, a2)
    assert q.correct_answer == a2
    assert q.correct_index == 3
    assert  q.correct_letter == "D"


@pytest.mark.parametrize(
    "iterator, q_text, q_subject",
    [(iter(("q1", "s1")),
      "q1", "s1"),
     (iter(("", "s1")),
      "", "s1")
     ],
)
def test_question_load1(iterator, q_text, q_subject):
    """load question text and subject; check for default image,  level
    and no answer.
    """
    quest = exam.Question()
    quest.load_sequentially(iterator)

    assert quest.text == q_text
    assert quest.subject == q_subject
    assert quest.image == Path(".")
    assert quest.level == 0
    with pytest.raises(IndexError):
        assert quest.answers[0].text == ""
    with pytest.raises(IndexError):
        assert quest.answers[0].image == Path("")


@pytest.mark.parametrize(
    "iterator, q_text, q_subject, q_image, q_level, a1_text, a1_image, a2_text, a2_image",
    [(iter(("d1", "s1", "i1", 1, "a11", "ai11", "a12", "ai12")),
      "d1", "s1", Path("i1"), 1, "a11", Path("ai11"), "a12", Path("ai12")),
     (iter(("", "s1", "", 2, "a11", "ai11", "", "ai12")),
      "", "s1", Path("."), 2, "a11", Path("ai11"), "", Path("ai12"))
     ],)
def test_question_load2(iterator, q_text, q_subject, q_image, q_level,
                        a1_text, a1_image, a2_text, a2_image):
    """load question and two answers.
    """
    quest = exam.Question()
    quest.load_sequentially(iterator)
    print(quest.answers)

    assert quest.text == q_text
    assert quest.subject == q_subject
    assert quest.image == q_image
    assert quest.answers[0].text == a1_text
    assert quest.answers[0].image == a1_image
    assert quest.answers[1].text == a2_text
    assert quest.answers[1].image == a2_image
    with pytest.raises(IndexError):
        assert quest.answers[2].text == ""
    with pytest.raises(IndexError):
        assert quest.answers[2].image == Path(".")


def test_question_load3():
    """load question and only answer text;
    answer image checked for default value.
    """
    quest = exam.Question()
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
        assert quest.answers[1].text == ""
    with pytest.raises(IndexError):
        assert quest.answers[1].image == Path(".")


def test_question_print():
    """test __str__ method
    """
    quest = exam.Question()
    quest_text = "Text"
    quest_subject = "Subject"
    quest_image = "dir/ec/tor/y"
    quest_level = 1
    answer_text = "Answer"
    iterator = iter((quest_text, quest_subject, quest_image, quest_level,
                     answer_text))
    quest.load_sequentially(iterator)

    assert f"text: {quest.text}" in quest.__str__()
    assert f"subject: {quest_subject}" in quest.__str__()
    assert f"image: {quest_image}" in quest.__str__()
    assert f"level: {quest_level}" in quest.__str__()
    assert f"text: {answer_text}" in quest.__str__()
    assert f"image: ." in quest.__str__()


@pytest.fixture
def set_questions():
    return (exam.Question(),
            exam.Question("Who?"),
            exam.Question("What?"),
            exam.Question("When?"))


def test_exam():
    """test Exam with no args
    """
    ex = exam.Exam()

    assert ex.questions == tuple()


def test_exam_init(set_questions):
    """test Exam with one and two arguments
    """
    ex1 = exam.Exam(set_questions[1])
    ex2 = exam.Exam(set_questions[1],
                    set_questions[2])

    assert ex1.questions == (set_questions[1],)
    assert ex2.questions == (set_questions[1],
                             set_questions[2])


def test_exam_questions_getter():
    """test question get with no question;
    question get with contents is tested before
    """
    ex = exam.Exam()

    assert len(ex.questions) == 0


def test_exam_questions_setter(set_questions):
    """test question set; question added before disappear
    """
    ex = exam.Exam()
    ex.add_question(set_questions[1])
    ex.questions = (set_questions[2], set_questions[3])

    assert set_questions[1] not in ex.questions
    assert set_questions[2] in ex.questions
    assert set_questions[3] in ex.questions


def test_exam_attribute_selector1():
    """test attribute_selector default value"""
    ex = exam.Exam()

    assert ex.attribute_selector == ()


def test_exam_attribute_selector2():
    """test attribute_selector set and type conversion
    """
    ex = exam.Exam()
    expected = ("hello", "2", "times")
    ex.attribute_selector = (expected[0],
                             int(expected[1]),
                             expected[2])

    assert ex.attribute_selector == expected


def test_exam_add_question1():
    """test add wrong question
    """
    ex = exam.Exam()
    not_a_question = "This is not a question"
    with pytest.raises(TypeError):
        ex.add_question(not_a_question)


def test_exam_add_question2(set_questions):
    """test add one question
    """
    ex = exam.Exam()
    ex.add_question(set_questions[0])

    assert ex.questions == (set_questions[0],)


def test_exam_add_question3(set_questions):
    """test add two questions
    """
    ex = exam.Exam()
    ex.add_question(set_questions[2])
    ex.add_question(set_questions[3])

    assert ex.questions == (set_questions[2],
                            set_questions[3])


def test_exam_load1():
    """test empty iterable
    """
    ex = exam.Exam()
    ex.load(iter(()))

    assert ex.questions == tuple()


@pytest.mark.parametrize(("iterator, text0, subject0, image0, level0, a00_text, a00_image, a01_text, a01_image, "
                          + "text1, subject1, image1, level1, a10_text, a10_image, a11_text, a11_image"),
                         [((OrderedDict([('field A', 'ab'), ('field B', 'ac'), ('field C', 'ad'), ('field D', '1'),
                                        ('field E', 'ae'), ('field F', 'af'), ('field G', 'ag')]),
                            OrderedDict([('field A', 'ba'), ('field B', 'bc'), ('field C', 'bd'), ('field D', '2'),
                                        ('field E', 'be'), ('field F', 'bf'), ('field G', 'bg')])),
                           "ab", "ac", Path("ad"), 1, "ae", Path("af"), "ag", Path("."),
                           "ba", "bc", Path("bd"), 2, "be", Path("bf",), "bg", Path("."))])
def test_exam_load2(iterator, text0, subject0, image0, level0, a00_text, a00_image, a01_text, a01_image,
                    text1, subject1, image1, level1, a10_text, a10_image, a11_text, a11_image):
    """test without setting _attribute_selector
    2 rows -> 2 questions with 2 answers each but second answer image is not provided
    """
    ex = exam.Exam()
    ex.load(iterator)

    assert ex.questions[0].text == text0  # first question
    assert ex.questions[0].subject == subject0
    assert ex.questions[0].image == image0
    assert ex.questions[0].level == level0
    assert ex.questions[0].answers[0].text == a00_text
    assert ex.questions[0].answers[0].image == a00_image
    assert ex.questions[0].answers[1].text == a01_text
    assert ex.questions[0].answers[1].image == a01_image  # default value

    assert ex.questions[1].text == text1  # second question
    assert ex.questions[1].subject == subject1
    assert ex.questions[1].image == image1
    assert ex.questions[1].level == level1
    assert ex.questions[1].answers[0].text == a10_text
    assert ex.questions[1].answers[0].image == a10_image
    assert ex.questions[1].answers[1].text == a11_text
    assert ex.questions[1].answers[1].image == a11_image  # default value

    # third answer of second question is not provided
    with pytest.raises(IndexError):
        assert ex.questions[1].answers[2].text == ""

    # third question is not provided
    with pytest.raises(IndexError):
        assert ex.questions[2].text == ""  # Not provided


def test_exam_load3():
    """test without setting _attribute_selector
    and missing row
    """
    ex = exam.Exam()
    reader = (OrderedDict([]),
              OrderedDict([("A", "What?"), ("B", "topic")]))
    ex.load(reader)

    print(ex)

    assert ex.questions[0].text == "What?"
    assert ex.questions[0].subject == "topic"


@pytest.mark.parametrize(("iterator, text, subject, image, level, "
                          + "a0_text, a0_image, a1_text, a1_image, a2_text, a2_image"),
                         [((OrderedDict([('field A', 'A1'), ('field B', 'A2'), ('field C', 'T'),
                                         ('field D', 'A3'), ('field E', 'A4'), ('field F', 'S'),
                                         ('field G', 2), ('void', '')]),),
                           "T", "S", Path("."), 2, "A1", Path("."), "A2", Path("."), "A3", Path("."))])
def test_exam_load4(iterator, text, subject, image, level,
                    a0_text, a0_image, a1_text, a1_image, a2_text, a2_image):
    """test setting _attribute_selector
    """
    ex = exam.Exam()
    ex.attribute_selector = ("field C",
                             "field F",
                             "void",
                             "field G",
                             "field A",
                             "void",
                             "field B",
                             "void",
                             "field D")
    ex.load(iterator)

    assert ex.questions[0].text == text
    assert ex.questions[0].subject == subject
    assert ex.questions[0].image == image
    assert ex.questions[0].level == level
    assert ex.questions[0].answers[0].text == a0_text
    assert ex.questions[0].answers[0].image == a0_image
    assert ex.questions[0].answers[1].text == a1_text
    assert ex.questions[0].answers[1].image == a1_image
    assert ex.questions[0].answers[2].text == a2_text
    assert ex.questions[0].answers[2].image == a2_image

    # no further elements loaded
    with pytest.raises(IndexError):
        assert ex.questions[0].answers[3].text == ""
    with pytest.raises(IndexError):
        assert ex.questions[1].answers[2].image == Path(".")


@pytest.mark.parametrize("iterator, text, q_image, level, a_image",
                         [((OrderedDict([('field A', 'A1'), ('field B', 'A2'), ('field C', 'T'),
                                         ('field D', 'A3'), ('field E', 'A4'), ('field F', 'S'),
                                         ('field G', 2), ('void', '')]),),
                           f"text: A1", f"image: .", f"level: 2", f"image: S")])
def test_exam_print(iterator, text, q_image, level, a_image):
    ex = exam.Exam()
    ex.attribute_selector = ("field A",
                             "void",
                             "void",
                             "field G",
                             "void",
                             "field F")
    ex.load(iterator)

    assert text in ex.__str__()
    assert q_image in ex.__str__()
    assert level in ex.__str__()
    assert a_image in ex.__str__()
