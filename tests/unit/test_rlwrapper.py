from reportlab.lib.styles import ParagraphStyle
from rlwrapper import Style, get_std_aspect_image
from pathlib import Path

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
