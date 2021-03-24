# -*- coding: utf-8 -*-
"""Unit test to check the command name repalcement logic.

Test in Python 3.7
"""

from __future__ import absolute_import, division, print_function

import importlib.util
import logging
from pathlib import Path
import sys
from unittest.mock import DEFAULT, Mock, MagicMock, patch

from pytest import MonkeyPatch


TEST_CASES = [
    {
        "commands": {"Katana 4.0.2": {"properties": {"short_name": "katana_4.0.2"}}},
        "replaced_commands_names": {"katana_4.0.2": "katana"},
        "expected": {"Katana 4.0.2": "katana"},
    },
    {
        "commands": {
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
        "replaced_commands_names": {
            "katana_3.6": "katana3",
            "screening_room_rv": "rv",
            "katana_4.0.2": "katana",
            "open_log_folder": "logs",
        },
        "expected": {
            "katana_3.6": "katana3",
            "Jump to Screening Room in RV": "rv",
            "katana_4.0.2": "katana",
            "Open Log Folder": "logs",
        },
    },
]


def import_file(module_name, path):
    full_path = Path(__file__).parent.parent / path
    spec = importlib.util.spec_from_file_location(module_name, full_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_basic():
    engine = import_file("engine", "engine.py")

    for test_case in TEST_CASES:
        mocked_engine_instance = MagicMock()
        mocked_engine_instance.logger = Mock(spec_set=logging.getLoggerClass())
        mocked_engine_instance.commands = test_case["commands"]

        results = engine.ShellEngine.validated_name_replacements(
            mocked_engine_instance, test_case["replaced_commands_names"]
        )
        assert results == test_case["expected"]
