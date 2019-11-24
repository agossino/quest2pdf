#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from typing import List


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
