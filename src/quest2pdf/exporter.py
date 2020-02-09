from rlwrapper import PDFDoc


class RLInterface:
    def __init__(self, input_generator, output_file: str):
        """Item set is made of one topitem and 0 or more nesteditems.
        This class print sequence of item set (topitem, nesteditem) in pdf.
        """
        self.file_name = output_file
        self.input = input_generator
        self._first_item = 0
        self._doc = PDFDoc(output_file)

    def build(self) -> None:
        ordinal = self._first_item

        try:
            item = next(self.input)

            assert item.sublevel == 0
            self._doc.add_item(item)

            ordinal += 1
            is_following_a_topitem = True

            while True:
                item = next(self.input)

                if item.sublevel == 0:
                    self._doc.build_last_ins_item(ordinal)
                    self._doc.add_item(item)

                    ordinal += 1
                    is_following_a_topitem = True
                elif item.sublevel == 1:
                    value = 1 if is_following_a_topitem else None
                    is_following_a_topitem = False

                    self._doc.add_subitem(item, value)

        except StopIteration:
            self._doc.build_last_ins_item(ordinal)

            self._doc.build()

