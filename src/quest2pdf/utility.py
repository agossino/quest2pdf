#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from typing import List, Dict
from pathlib import Path


def exception_printer(exeption_instance: Exception) -> str:
    """Format an exception class and instance in string
    """
    pattern: str = "\W+"
    exc_list: List[str] = re.split(pattern, str(exeption_instance.__class__))
    try:
        return (exc_list[2]
                + ": "
                + str(exeption_instance))
    except IndexError:
        return str(exeption_instance)

def add_path_to_image(ref_path: str, dicts: List[Dict[str, str]]) -> None:
    """Add the reference path to the image file name in item "image"
    """
    for row in dicts:
        if row['image']:
            row["image"] = str(Path(ref_path) / row["image"])


