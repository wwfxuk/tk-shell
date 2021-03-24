# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

"""Helpers to import modules and packages.

Test in Python 3.7.
"""

import importlib.util
from pathlib import Path
import sys
from typing import Union

__all__ = (
    "REPO_ROOT",
    "import_file",
    "engine",
)

REPO_ROOT = Path(__file__).parent.parent


def import_file(module_name: str, path: Union[str, Path]):
    """Used to import a file directly as a module."""
    full_path = REPO_ROOT / path
    spec = importlib.util.spec_from_file_location(module_name, full_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


engine = import_file("engine", "engine.py")
