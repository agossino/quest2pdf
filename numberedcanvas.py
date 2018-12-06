#!/usr/bin/env python
# -*- coding: utf-8 -*-
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import  A4
from reportlab.lib.units import mm

class NumberedCanvas(canvas.Canvas):
    """add page info to each page (page x of y)"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

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
            "Pag. %d di %d" % (self._pageNumber, page_count))
