# from export import ItemLevel, SerializeExam, Item, RLInterface


# def test_assignment1(dummy_exam):
#     my_exam = dummy_exam
#     expected = SerializeExam(my_exam).assignment()
#
#     item = next(expected)
#     assert item.item_level == ItemLevel.top
#     assert item.text == my_exam.questions[0].text
#     assert item.image == my_exam.questions[0].image
#     item = next(expected)
#     assert item.item_level == ItemLevel.sub
#     assert item.text == my_exam.questions[0].answers[0].text
#     assert item.image == my_exam.questions[0].answers[0].image
#     item = next(expected)
#     assert item.item_level == ItemLevel.sub
#     assert item.text == my_exam.questions[0].answers[1].text
#     assert item.image == my_exam.questions[0].answers[1].image
#     item = next(expected)
#     assert item.item_level == ItemLevel.top
#     assert item.text == my_exam.questions[1].text
#     assert item.image == my_exam.questions[1].image
#     item = next(expected)
#     assert item.item_level == ItemLevel.top
#     assert item.text == my_exam.questions[2].text
#     assert item.image == my_exam.questions[2].image
#     item = next(expected)
#     assert item.item_level == ItemLevel.sub
#     assert item.text == my_exam.questions[2].answers[0].text
#     assert item.image == my_exam.questions[2].answers[0].image
#
#     with pytest.raises(StopIteration):
#         next(expected)
#
#
# def test_correction0():
#     my_exam = exam.Exam()
#     expected = SerializeExam(my_exam).correction()
#
#     with pytest.raises(StopIteration):
#         next(expected)
#
#
# def test_correction1(dummy_exam):
#     my_exam = dummy_exam
#     expected = SerializeExam(my_exam).correction()
#
#     item = next(expected)
#     assert item.item_level == ItemLevel.top
#     assert item.text == f"correction"
#     assert item.image == pathlib.Path(".")
#     item = next(expected)
#     assert item.item_level == ItemLevel.sub
#     assert item.text == f"{my_exam.questions[0].correct_option}"
#     assert item.image == pathlib.Path(".")
#     item = next(expected)
#     assert item.item_level == ItemLevel.sub
#     assert item.text == f"{my_exam.questions[1].correct_option}"
#     assert item.image == pathlib.Path(".")
#     item = next(expected)
#     assert item.item_level == ItemLevel.sub
#     assert item.text == f"{my_exam.questions[2].correct_option}"
#     assert item.image == pathlib.Path(".")
#
#     with pytest.raises(StopIteration):
#         next(expected)
#
#
# class MonkeyPDFDoc:
#     output = {"init": [], "item": []}
#
#     def __init__(self, output_file, **kwargs):
#         MonkeyPDFDoc.output["init"].append(output_file)
#
#     @staticmethod
#     def add_item(item):
#         MonkeyPDFDoc.output["item"].append(item)
#
#     @staticmethod
#     def add_sub_item(item):
#         MonkeyPDFDoc.output["item"].append(item)
#
#     def build(self):
#         pass
#
#     @staticmethod
#     def clear():
#         MonkeyPDFDoc.output = {"init": [], "item": []}
#
#
# def test_rlinterface1(monkeypatch):
#     MonkeyPDFDoc.clear()
#     monkeypatch.setattr("rlwrapper.PDFDoc", MonkeyPDFDoc)
#     input_iter = iter(())
#     file_name = pathlib.Path("file")
#     interface = RLInterface(input_iter, file_name)
#     interface.build()
#
#     assert MonkeyPDFDoc.output == {"init": [file_name], "item": []}
#
#
# def test_rlinterface2(monkeypatch):
#     MonkeyPDFDoc.clear()
#     monkeypatch.setattr("rlwrapper.PDFDoc", MonkeyPDFDoc)
#     input_iter = iter((Item(ItemLevel.sub, "text", "image"),))
#     file_name = pathlib.Path("file")
#     interface = RLInterface(input_iter, file_name)
#     with pytest.raises(AssertionError):
#         interface.build()
#
#
# def test_rlinterface3(monkeypatch):
#     MonkeyPDFDoc.clear()
#     monkeypatch.setattr("rlwrapper.PDFDoc", MonkeyPDFDoc)
#     input_iter = iter((Item(ItemLevel.top, "text", "image"),))
#     file_name = pathlib.Path("file")
#     interface = RLInterface(input_iter, file_name)
#     interface.build()
#
#     assert MonkeyPDFDoc.output == {
#         "init": [file_name],
#         "item": [Item(ItemLevel.top, "text", "image")],
#     }
#
#
# def test_rlinterface4(monkeypatch):
#     MonkeyPDFDoc.clear()
#     monkeypatch.setattr("rlwrapper.PDFDoc", MonkeyPDFDoc)
#     input_iter = iter(
#         (
#             Item(ItemLevel.top, "text 1", "image 1"),
#             Item(ItemLevel.top, "text 2", "image 2"),
#         )
#     )
#     file_name = pathlib.Path("file")
#     interface = RLInterface(input_iter, file_name)
#     interface.build()
#
#     assert MonkeyPDFDoc.output == {
#         "init": [file_name],
#         "item": [
#             Item(ItemLevel.top, "text 1", "image 1"),
#             Item(ItemLevel.top, "text 2", "image 2"),
#         ],
#     }
#
#
# def test_rlinterface5(monkeypatch):
#     MonkeyPDFDoc.clear()
#     monkeypatch.setattr("rlwrapper.PDFDoc", MonkeyPDFDoc)
#     input_iter = iter(
#         (
#             Item(ItemLevel.top, "text 1", "image 1"),
#             Item(ItemLevel.sub, "text 2", "image 2"),
#         )
#     )
#     file_name = pathlib.Path("file")
#     interface = RLInterface(input_iter, file_name)
#     interface.build()
#
#     assert MonkeyPDFDoc.output == {
#         "init": [file_name],
#         "item": [
#             Item(ItemLevel.top, "text 1", "image 1"),
#             Item(ItemLevel.sub, "text 2", "image 2"),
#         ],
#     }
#
#
# def test_rlinterface6(monkeypatch):
#     MonkeyPDFDoc.clear()
#     monkeypatch.setattr("rlwrapper.PDFDoc", MonkeyPDFDoc)
#     input_iter = iter(
#         (
#             Item(ItemLevel.top, "text 1", "image 1"),
#             Item(ItemLevel.top, "text 2", "image 2"),
#             Item(3, "text 3", "image 3"),
#         )
#     )
#     file_name = pathlib.Path("file")
#     interface = RLInterface(input_iter, file_name)
#     with pytest.raises(ValueError):
#         interface.build()
#
#
# def test_rlinterface7(monkeypatch):
#     MonkeyPDFDoc.clear()
#     monkeypatch.setattr("rlwrapper.PDFDoc", MonkeyPDFDoc)
#     input_iter = iter(
#         (
#             Item(ItemLevel.top, "text 1", "image 1"),
#             Item(ItemLevel.top, "text 2", "image 2"),
#             Item(ItemLevel.sub, "text 3", "image 3"),
#             Item(ItemLevel.sub, "text 4", "image 4"),
#         )
#     )
#     file_name = pathlib.Path("file")
#     interface = RLInterface(input_iter, file_name)
#     interface.build()
#
#     assert MonkeyPDFDoc.output == {
#         "init": [file_name],
#         "item": [
#             Item(ItemLevel.top, "text 1", "image 1"),
#             Item(ItemLevel.top, "text 2", "image 2"),
#             Item(ItemLevel.sub, "text 3", "image 3"),
#             Item(ItemLevel.sub, "text 4", "image 4"),
#         ],
#     }
