import random
import subprocess
from pathlib import Path
from itertools import chain

import pytest

from exam import (
    MultiChoiceAnswer,
    TrueFalseAnswer,
    MultiChoiceQuest,
    TrueFalseQuest,
    Exam,
)
from export import SerializeExam, RLInterface
from utility import CSVReader
from unit_helper import fd_input, save_mono_question_data


@pytest.fixture
def dummy_exam():
    q1 = MultiChoiceQuest(
        "question 1: correct is n. 2", "subject 1", Path("resources/a.png")
    )
    a1 = MultiChoiceAnswer("answer 1", Path("resources/b.png"))
    a2 = MultiChoiceAnswer("answer 2", Path("resources/c.png"))
    a3 = MultiChoiceAnswer("answer 3", Path("resources/a.png"))
    q1.answers = (a1, a2, a3)
    q1.correct_option = "B"

    q2 = MultiChoiceQuest(
        "question 2: correct is n. 1", "subject 1", Path("resources/a.png")
    )
    a1 = MultiChoiceAnswer("answer 1")
    a2 = MultiChoiceAnswer("answer 2")
    a3 = MultiChoiceAnswer("answer 3")
    q2.answers = (a1, a2, a3)

    q3 = TrueFalseQuest("question 3: correct is True (first)")
    a1 = TrueFalseAnswer(True)
    a2 = TrueFalseAnswer(False)
    q3.answers = (a1, a2)

    q4 = MultiChoiceQuest("question 4: no answer", "subject 2", Path("resources/b.png"))

    q5 = TrueFalseQuest("question 5: correct is False (first))")
    a1 = TrueFalseAnswer(False)
    a2 = TrueFalseAnswer(True)
    q5.answers = (a1, a2)

    q6 = MultiChoiceQuest(
        "question 6: correct is n. 3", "subject 4", Path("resources/c.png")
    )
    a1 = MultiChoiceAnswer("answer 1")
    a2 = MultiChoiceAnswer("answer 2")
    a3 = MultiChoiceAnswer("answer 3")
    a4 = MultiChoiceAnswer("answer 4")
    q6.add_answer(a1)
    q6.add_answer(a2)
    q6.add_answer(a3, is_correct=True)
    q6.add_answer(a4)
    dummy_ex = Exam(q1, q2, q3, q4, q5, q6)

    return dummy_ex


def test_print_have_a_look(tmp_path, dummy_exam):
    image_folder = Path("tests/unit/resources")
    image_tmp_folder = tmp_path / image_folder.name
    image_tmp_folder.mkdir()
    for file in chain(image_folder.glob("*.png"), image_folder.glob("*.jpg")):
        data = file.read_bytes()
        copied_file = tmp_path / image_folder.name / file.name
        copied_file.write_bytes(data)

    random.seed()

    exam_file_path = tmp_path / "Exam"
    correction_file_path = tmp_path / "Correction"
    ex = dummy_exam
    folder = image_tmp_folder
    ex.add_path_parent(folder)
    ex.shuffle()
    serial_exam = SerializeExam(ex)
    pdf_interface = RLInterface(serial_exam.assignment(), exam_file_path)
    pdf_interface.build()
    pdf_interface = RLInterface(
        serial_exam.correction(),
        correction_file_path,
        top_item_bullet_type="A",
        sub_item_bullet_type="1",
    )
    pdf_interface.build()

    subprocess.Popen(["evince", str(exam_file_path)])
    subprocess.call(["evince", str(correction_file_path)])

    answer = fd_input("Is it correct (y)? ")

    assert answer == "y\n"


def test_shuffle_from_csv(tmp_path):
    data_file = tmp_path / "data.csv"
    save_mono_question_data(data_file)

    data = CSVReader(str(data_file))
    rows = data.to_dictlist()

    exam = Exam()
    exam.attribute_selector = (
        "question",
        "subject",
        "image",
        "void",
        "A",
        "void",
        "B",
        "void",
        "C",
        "void",
        "D",
        "void",
    )

    exam.load(rows)
    exam.add_path_parent(data_file)
    random.seed(1)
    exam.shuffle()

    for question in exam.questions:
        assert question.correct_answer.text == "a"
    assert exam.questions[0]._answers[0].text == "d"
    assert exam.questions[1]._answers[0].text == "d"
