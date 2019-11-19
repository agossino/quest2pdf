#!/usr/bin/env python
"""Input class
"""
import logging
import csv
from typing import List, Dict, Optional
from itertools import chain
# from collections import OrderedDict
# Value 'OrderedDict' is unsubscriptable

LOG_NAME = 'quest2pdf.' + __name__
LOGGER = logging.getLogger(LOG_NAME)

class CSVReader:
    """Convert from a Comma Separated Value file to different
    format.
    """
    def __init__(self, file_name: str,
                 encoding: str = 'utf-8',
                 delimiter: str = ','):
        self.file_name: str = file_name
        std_encoding: str = encoding
        self.delimiter: str = delimiter

        alternate_encodings: str = ("utf_16",
                                    "ascii",
                                    "cp037",
                                    "cp437",
                                    "cp850",
                                    "cp858",
                                    "cp1140",
                                    "cp1250",
                                    "cp1252",
                                    "latin_1",
                                    "iso8859_15"
                                    )

        for current_encoding in chain((std_encoding,),
                               alternate_encodings):
            try:
                self._read(current_encoding)
                break
            except UnicodeError as err:
                msg: str = ("Reading %s encoding %s: %s")
                LOGGER.error(msg, self.file_name, current_encoding, err)
                if current_encoding == alternate_encodings[-1]:
                    raise
                continue

    def to_dictlist(self) -> List[Dict[str, str]]:
        """Return a list of dictionaries with the file contents.
        """
        return self.rows

    def _read(self, encoding: str, err: Optional[str] = None) -> None:
        """Read the file and fill self.rows.
        """
        try:
            with open(self.file_name, 'r',
                      encoding=encoding, errors=err) as csvfile:
                cvs_reader = csv.DictReader(csvfile,
                                            delimiter=self.delimiter)
                self.rows: List[Dict[str, str]]
                self.rows = [row for row in cvs_reader]
        except FileNotFoundError:
            LOGGER.critical("File di imput %s non trovato.", self.file_name)
            raise

if __name__ == "__main__":
    READER = CSVReader("domande.csv")
    print("type: ", type(READER.to_dictlist()))
    print("first 2 elements:")
    for elm in READER.to_dictlist()[:2]:
        print("type: ", type(elm))
        for key, value in elm.items():
            print("key: ", key)
            print("value: ", value)
