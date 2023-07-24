# Name:              customers.py
# Author:            Mo Tecnologias
# Developers:        Miguel Andres Garcia Niño
# Creation date:     22nd July of 2023
# Modification date: 22nd July of 2023
# Copyright:         (c) 2016 by Mo Tecnologias, 2023

from enum import Enum


class Status(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
