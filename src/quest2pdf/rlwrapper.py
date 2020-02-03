from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph,
                                ListFlowable, Spacer,
                                Image, ListItem)

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

style = Style()
ellipse_centered_para = [Paragraph("""<unichar name="Horizontal ellipsis"/>""",
                                   style.title)]
separator = ListFlowable(ellipse_centered_para,
                         bulletType="bullet",
                         start="")
