from pathlib import Path
import pytest
from collections import namedtuple
from reportlab.lib.styles import ParagraphStyle
from rlwrapper import Style, get_std_aspect_image, PDFDoc
from reportlab.platypus import ListFlowable, ListItem

RESOURCES = Path("tests/unit/resources")


def test_style_normal():
    style = Style()

    assert type(style.normal) == ParagraphStyle
    assert style.normal.name == "Normal"


def test_style_title():
    style = Style()

    assert type(style.title) == ParagraphStyle
    assert style.title.name == "Title"


def test_style_kwargs():
    style = Style(spaceAfter=50)

    assert style.title.spaceAfter == 50
    assert style.normal.spaceAfter == 50


def test_std_aspect_image():
    file_name = "test.png"
    path = RESOURCES / file_name
    image = get_std_aspect_image(str(path))

    assert "Image" in image.identity()
    assert file_name in image.identity()


def test_std_aspect_image_fail():
    file_name = "not_exist.png"
    path = RESOURCES / file_name
    with pytest.raises(OSError):
        get_std_aspect_image(str(path))


def test_pdf_separator():
    doc = PDFDoc("FILE")

    assert "ListFlowable" in doc.separator.identity()


def test_pdfdoc(tmp_path):
    image = str(RESOURCES / "test.png")
    Item = namedtuple("Item", ["text", "image"])
    data = iter((Item("first", image),
                 Item("second", Path(".")),
                 Item("third", image),
                 Item("forth", Path("."))))
    file = tmp_path / "temp.pdf"
    doc = PDFDoc(str(file))
    doc.add_item(next(data))
    assert doc._start == 1
    assert isinstance(doc._last_ins_item[-1], ListFlowable)
    assert len(doc._last_ins_item) == 1
    assert doc._doc == []
    doc.add_item(next(data))
    assert doc._start == 2
    assert isinstance(doc._last_ins_item[-1], ListFlowable)
    assert len(doc._last_ins_item) == 1
    assert isinstance(doc._doc[-1], ListFlowable)
    assert len(doc._doc) == 2
    doc.add_sub_item(next(data))
    assert doc._start == 2
    assert isinstance(doc._last_ins_item[-1], ListItem)
    assert len(doc._last_ins_item) == 2
    assert isinstance(doc._doc[-1], ListFlowable)
    assert len(doc._doc) == 2
    doc.add_sub_item(next(data))
    assert doc._start == 2
    assert isinstance(doc._last_ins_item[-1], ListItem)
    assert len(doc._last_ins_item) == 3
    assert isinstance(doc._doc[-1], ListFlowable)
    assert len(doc._doc) == 2
    doc.build()
    assert doc._start == 3

    assert file.exists()


