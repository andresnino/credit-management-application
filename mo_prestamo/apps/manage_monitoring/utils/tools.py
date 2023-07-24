# Name:              tools.py
# Author:            Mo Tecnologias
# Developers:        Miguel Andres Garcia Niño
# Creation date:     24th July of 2023
# Modification date: 24th July of 2023
# Copyright:         (c) 2016 by Mo Tecnologias, 2023

def enum_to_choices(obj) -> list:
    return [(elem.value, elem.name) for elem in iter(obj)]
