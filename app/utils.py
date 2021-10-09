#!/usr/bin/python3
from importlib import import_module


def get_class(module: str, class_name: str):
    m = import_module(module)
    c = getattr(m, class_name)
    return c
