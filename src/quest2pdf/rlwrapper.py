from pathlib import Path
import logging
from typing import List
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, ListFlowable, ListItem
from reportlab.lib.units import mm
from reportlab.lib import utils

NON_BREAK_SP = "<div>&nbsp;</div>"


class Style:
    def __init__(self, **kwargs):
        self._style_sheet = getSampleStyleSheet()
        for key in kwargs:
            for style_name in self._style_sheet.byName:
                obj = self._style_sheet[style_name]
                setattr(obj, key, kwargs[key])

    @property
    def normal(self) -> ParagraphStyle:
        return self._style_sheet["Normal"]

    @property
    def title(self):
        return self._style_sheet["Title"]


def get_std_aspect_image(file_name: str, width: int = 50 * mm) -> Image:
    """Return Image with original aspect and given width.
    """
    try:
        image_reader = utils.ImageReader(file_name)
    except OSError:
        logging.critical('OS Error reading %s', file_name)
        raise

    orig_width, orig_height = image_reader.getSize()
    aspect = orig_height / float(orig_width)

    return Image(str(file_name), width=width, height=(width * aspect))


class PDFDoc:
    def __init__(self, output_file: str):
        self._file_name: str = output_file
        self._doc: List[ListFlowable, ...] = []
        self._last_ins_item = []
        self._text_separator = """<unichar name="Horizontal ellipsis"/>"""

    @property
    def separator(self):
        style = Style()
        return ListFlowable([Paragraph(self._text_separator,
                                       style.title)],
                            bulletType="bullet",
                            start="")

    def build_last_ins_item(self, ordinal):
        question_set = ListFlowable(self._last_ins_item,
                                    bulletType='1',
                                    start=ordinal)

        self._doc.extend([question_set, self.separator])

    def add_item(self, item):
        self._last_ins_item = [self._build_item(item)]

    def add_sub_item(self, item, value):
        item_list = self._build_item(item)
        self._last_ins_item.append(ListItem(item_list, bulletType='A', value=value))

    def _build_item(self, item):
        style = Style(spaceAfter=25)
        if item.image != Path("."):
            image = get_std_aspect_image(item.image, width=80)
            question = [Paragraph(item.text + NON_BREAK_SP, style.normal),
                        image]
        else:
            question = [Paragraph(item.text,
                                  style.normal)]
        return ListFlowable(question, leftIndent=0,
                            bulletType='bullet', start='')

    def build(self):
        doc = SimpleDocTemplate(self._file_name)
        doc.build(self._doc)
