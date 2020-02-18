from pathlib import Path
import logging
from typing import List
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Image,
    Paragraph,
    ListFlowable,
    ListItem,
    Spacer
)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import  A4
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
    def title(self) -> ParagraphStyle:
        return self._style_sheet["Title"]


def get_std_aspect_image(file_name: Path, width: int = 50 * mm) -> Image:
    """Return Image with original aspect and given width.
    """
    try:
        image_reader = utils.ImageReader(str(file_name))
    except OSError:
        logging.critical("OS Error reading %s", file_name)
        raise

    orig_width, orig_height = image_reader.getSize()
    aspect = orig_height / float(orig_width)

    return Image(str(file_name), width=width, height=(width * aspect))


class PDFDoc:
    def __init__(self, output_file: Path):
        self._file_name: str = str(output_file)
        self._doc: List[ListFlowable, ...] = []
        self._last_ins_item = []
        self._start: int = 1
        self._space_text_image: int = 10
        self._space_after_item = 20
        self._text_separator: str = """<unichar name="Horizontal ellipsis"/>"""
        self._1st_page_header_text = "header text"
        self._later_pages_header_text = "header text"
        self._footer_text = "footer text"
        self._author = "Giancarlo"
        self._title = "esame"
        self._subject = "Corso"

    @property
    def separator(self):
        style = Style()
        return ListFlowable(
            [Paragraph(self._text_separator, style.title)],
            bulletType="bullet",
            start="",
        )

    def build_last_ins_item(self):
        question_set = ListFlowable(
            self._last_ins_item, bulletType="1", start=self._start
        )
        self._start += 1
        self._doc.extend([question_set, self.separator])

    def add_item(self, item):
        if len(self._last_ins_item) != 0:
            self.build_last_ins_item()
        self._last_ins_item = [self._build_item(item)]

    def add_sub_item(self, item):
        item_list = self._build_item(item)
        value = 1 if len(self._last_ins_item) == 1 else None
        self._last_ins_item.append(ListItem(item_list, bulletType="A", value=value))

    def _build_item(self, item):
        style = Style(spaceAfter=self._space_text_image)
        space = Spacer(1, self._space_after_item)
        if item.image != Path("."):
            image = get_std_aspect_image(item.image, width=80)
            question = [Paragraph(item.text + NON_BREAK_SP, style.normal),
                        image,
                        space]
        else:
            question = [Paragraph(item.text, style.normal), space]
        return ListFlowable(question, leftIndent=0, bulletType="bullet", start="")

    def build(self):
        if len(self._last_ins_item) != 0:
            self.build_last_ins_item()

        doc = SimpleDocTemplate(self._file_name, pagesize=A4, allowSplitting=1,
                                author=self._author, title=self._title, subject=self._subject)

        doc.build(self._doc, onFirstPage=self._first_page_head,
                  onLaterPages=self._later_page_head,
                  canvasmaker=NumberedCanvas)

    def _first_page_head(self, actual_canvas, doc):
        # Save the state of our canvas so we can draw on it
        actual_canvas.saveState()
        style = Style()

        # Header
        header = Paragraph(self._1st_page_header_text, style.normal)
        width, height = header.wrap(doc.width, doc.topMargin)
        header.drawOn(actual_canvas, doc.leftMargin,
                      doc.height + doc.bottomMargin + doc.topMargin / 2 - height)

        # Footer
        footer = Paragraph(self._footer_text, style.normal)
        width, height = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(actual_canvas, doc.leftMargin, height)

        # Release the canvas
        actual_canvas.restoreState()

    def _later_page_head(self, actual_canvas, doc):
        # Save the state of our canvas so we can draw on it
        actual_canvas.saveState()
        style = Style

        # Header
        header = Paragraph(self._later_pages_header_text, style.normal)
        width, height = header.wrap(doc.width, doc.topMargin)
        header.drawOn(actual_canvas, doc.leftMargin,
                      doc.height + doc.bottomMargin + doc.topMargin / 2 - height)

        # Footer
        footer = Paragraph(self._footer_text, style.normal)
        width, height = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(actual_canvas, doc.leftMargin, height)

        # Release the canvas
        actual_canvas.restoreState()


class NumberedCanvas(canvas.Canvas):
    """add page info to each page (page x of y)"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
        self._text = "Pag. %d di %d"

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        w, h = A4
        self.setFont("Helvetica", 9)
        self.drawCentredString(w/2, 20*mm,
            self._text % (self._pageNumber, page_count))


