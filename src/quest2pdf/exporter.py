from reportlab.platypus import (SimpleDocTemplate, Paragraph,
                                ListFlowable, Spacer,
                                Image, ListItem)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib import utils
from pathlib import Path

from rlwrapper import Style, separator

class RLInterface:
    def __init__(self, input_generator, output_file: str):
        """Item set is made of one top item (sublevel is 0)
        and 0 or more nested items (sublevel is 1).
        This class print sequence of item set in pdf.
        """
        self.file_name = output_file
        self.input = input_generator
        self._first_item = 0

        self._style = Style()

        self._spaceAfter50_style = getSampleStyleSheet()
        self._spaceAfter50_style["Normal"].spaceAfter = 50

        self._spaceAfter25_style = getSampleStyleSheet()
        self._spaceAfter25_style["Normal"].spaceAfter = 25


        self._question_set_separator = separator
        self._listFlowable = []

    def build(self) -> None:
        ordinal = self._first_item

        try:
            item = next(self.input)

            assert item.sublevel == 0
            item_set = self._get_item_set(item)

            ordinal += 1
            is_following_a_0_item = True

            while True:
                item = next(self.input)

                if item.sublevel == 0:

                    self._append_item_set(item_set, ordinal)

                    item_set = self._get_item_set(item)

                    ordinal += 1
                    is_following_a_0_item = True
                elif item.sublevel == 1:
                    value = 1 if is_following_a_0_item else None
                    is_following_a_0_item = False
                    item_set.append(ListItem(Paragraph(item.text,
                                                       self._style.normal),
                                             bulletType='A',
                                             value=value))

        except StopIteration:
            self._append_item_set(item_set, ordinal)

            doc = SimpleDocTemplate(self.file_name)

            doc.build(self._listFlowable)

    def _original_ratio_img(self, name: str, width: int = 50 * mm) -> Image:
        """Return Image with original ratio and given width.
        """
        try:
            img = utils.ImageReader(str(name))
        except:
            print('Errore nella lettura di ', str(name))
            raise
        iw, ih = img.getSize()
        aspect = ih / float(iw)

        return Image(str(name), width=width, height=(width * aspect))

    def _get_item_set(self, item):
        if item.image != Path("."):
            image = self._original_ratio_img(item.image, width=80)
            question = [Paragraph(item.text,
                                  self._spaceAfter25_style['Normal']),
                        image]
        else:
            question = [Paragraph(item.text,
                                  self._spaceAfter25_style['Normal'])]
        item_set = [ListFlowable(question,
                                 leftIndent=0,
                                 bulletType='bullet',
                                 start='')]
        return item_set

    def _append_item_set(self, item_set, ordinal):
        question_set = ListFlowable(item_set,
                                    bulletType='1',
                                    start=ordinal)
        self._listFlowable.extend([question_set,
                                   self._question_set_separator])
