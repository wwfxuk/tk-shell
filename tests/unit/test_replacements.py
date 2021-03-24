# -*- coding: utf-8 -*-
"""Unit test to check the command name repalcement logic.

Test in Python 3.7
"""

from __future__ import absolute_import, division, print_function

import importlib.util
import logging
from pathlib import Path
import sys
from typing import Union
from unittest.mock import Mock, MagicMock

import pytest


PASSING_CASES = [
    pytest.param(
        {"Katana 4.0.2": {"properties": {"short_name": "katana_4.0.2"}}},
        {"katana_4.0.2": "katana"},
        {"Katana 4.0.2": "katana"},
        id="basic",
    ),
    pytest.param(
        {"setup_folders": {"properties": {"short_name": "setup_folders"}}},
        {"katana_4.0.2": "katana"},
        {},
        id="no_matching_commands",
    ),
    pytest.param(
        {},
        {"katana_4.0.2": "katana"},
        {},
        id="no_commands",
    ),
    pytest.param(
        {"setup_folders": {"properties": {"short_name": "setup_folders"}}},
        {},
        {},
        id="nothing_to_rename",
    ),
    pytest.param(
        {
            "katana_3.6": {"properties": {"short_name": "katana_3.6"}},
            "Katana 4.0.2": {"properties": {"short_name": "katana_4.0.2"}},
        },
        {
            "katana_4.0.2": "katana",
            "katana_3.6": "katana",
        },
        {},
        id="empty_upon_clash",
    ),
    pytest.param(
        {
            "katana_3.6": {"properties": {"short_name": "katana_3.6"}},
            "Jump to Screening Room in RV": {
                "properties": {"short_name": "screening_room_rv"}
            },
            "Jump to Screening Room Web Player": {
                "properties": {"short_name": "screening_room_web"}
            },
            "katana_4.0.2": {"properties": {"short_name": "katana_4.0.2"}},
            "Shotgun Toolkit Demos": {"properties": {"short_name": "demos"}},
            "Publish in-place...": {"properties": {"short_name": "publish_in_place"}},
            "setup_folders": {"properties": {"short_name": "setup_folders"}},
            "mari": {"properties": {"short_name": "mari"}},
            "Open Log Folder": {"properties": {"short_name": "open_log_folder"}},
        },
        {
            "katana_3.6": "katana3",
            "screening_room_rv": "rv",
            "katana_4.0.2": "katana",
            "open_log_folder": "logs",
        },
        {
            "katana_3.6": "katana3",
            "Jump to Screening Room in RV": "rv",
            "katana_4.0.2": "katana",
            "Open Log Folder": "logs",
        },
        id="production",
    ),
]


def import_file(module_name: str, path: Union[str, Path]):
    """Used to import a file directly as a module."""
    full_path = Path(__file__).parent.parent / path
    spec = importlib.util.spec_from_file_location(module_name, full_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


engine = import_file("engine", "engine.py")


@pytest.mark.parametrize("commands,replaced_commands_names,expected", PASSING_CASES)
def test_valid_validated_name_replacements(commands, replaced_commands_names, expected):
    """Isolate and check the dictionary processing logic."""
    instance = MagicMock()
    instance.logger = Mock(spec_set=logging.getLoggerClass())
    instance.commands = commands

    assert expected == engine.ShellEngine.validated_name_replacements(
        instance, replaced_commands_names
    )
