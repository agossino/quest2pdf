#!/usr/bin/env python
"""Input class
"""
import logging
import csv
from typing import List, Dict, Optional
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
        self.encoding: str = encoding
        self.delimiter: str = delimiter

        try:
            self._read()
        except UnicodeDecodeError as err:
            msg: str = ('Reading ' + self.file_name + ' ' +
                        'encoding ' + self.encoding + ' ')
            LOGGER.error(msg, str(err))
            raise

    def to_dictlist(self) -> List[Dict[str, str]]:
        """Return a list of dictionaries with the file contents.
        """
        return self.rows

    def _read(self, err: Optional[str] = None) -> None:
        """Read the file and fill self.rows.
        """
        try:
            with open(self.file_name, 'r',
                      encoding=self.encoding, errors=err) as csvfile:
                cvs_reader = csv.DictReader(csvfile,
                                            delimiter=self.delimiter)
                self.rows: List[Dict[str, str]]
                self.rows = [row for row in cvs_reader]
        except FileNotFoundError:
            LOGGER.critical(self.file_name, ' file di imput non trovato')
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
