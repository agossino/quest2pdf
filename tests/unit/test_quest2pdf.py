import random
import subprocess
from pathlib import Path
from itertools import chain

import pytest

from exam import Exam, Question, Answer
from export import SerializeExam, RLInterface
from unit_helper import fd_input


@pytest.fixture
def dummy_exam():
    q1 = Question(
        "question 1: correct is n. 2", "subject 1", Path("resources/a.png")
    )
    a1 = Answer("answer 1", Path("resources/b.png"))
    a2 = Answer("answer 2", Path("resources/c.png"))
    a3 = Answer("answer 3", Path("resources/a.png"))
    q1.answers = (a1, a2, a3)
    q1.correct_option = "B"

    q2 = Question(
        "question 2: no answer", "subject 2", Path("resources/b.png")
    )

    q4 = Question(
        "question 4: correct is n. 3", "subject 4", Path("resources/c.png")
    )
    a1 = Answer("answer 1")
    a2 = Answer("answer 2")
    a3 = Answer("answer 3")
    a4 = Answer("answer 4")
    q4.add_answer(a1)
    q4.add_answer(a2)
    q4.add_answer(a3, is_correct=True)
    q4.add_answer(a4)
    dummy_ex = Exam(q1, q2, q4)

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
    serial_exam = SerializeExam(ex)
    pdf_interface = RLInterface(serial_exam.assignment(), exam_file_path)
    pdf_interface.build()
    pdf_interface = RLInterface(serial_exam.correction(), correction_file_path)
    pdf_interface.build()

    subprocess.Popen(["evince", str(exam_file_path)])
    subprocess.call(["evince", str(correction_file_path)])

    answer = fd_input("Is it correct (y)? ")

    assert answer == "y\n"