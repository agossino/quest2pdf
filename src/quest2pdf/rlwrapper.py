from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Image, Paragraph, ListFlowable
from reportlab.lib.units import mm
from reportlab.lib import utils
import logging


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

style = Style()
ellipse_centered_para = [Paragraph("""<unichar name="Horizontal ellipsis"/>""",
                                   style.title)]
separator = ListFlowable(ellipse_centered_para,
                         bulletType="bullet",
                         start="")
