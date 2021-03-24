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
]


def import_file(module_name, path):
    full_path = Path(__file__).parent.parent / path
    spec = importlib.util.spec_from_file_location(module_name, full_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def mocked_engine(test_case):
    engine = import_file("engine", "engine.py")

    def get_settings_side_effect(name, default=None):
        if name == "replaced_commands_names":
            return test_case["replaced_commands_names"]
        return DEFAULT

    with patch("engine.ShellEngine") as mocked_engine_def:
        instance = mocked_engine_def.return_value
        instance.logger = Mock(spec_set=logging.getLoggerClass())
        instance.commands.return_value = test_case["commands"]


def test_basic():
    engine = import_file("engine", "engine.py")

    for test_case in TEST_CASES:
        mocked_engine_instance = MagicMock()
        mocked_engine_instance.logger = Mock(spec_set=logging.getLoggerClass())
        mocked_engine_instance.commands.return_value = test_case["commands"]

        results = engine.ShellEngine.validated_name_replacements(
            mocked_engine_instance, test_case["replaced_commands_names"]
        )
        assert results == test_case["expected"]
