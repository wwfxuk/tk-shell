# -*- coding: utf-8 -*-
"""Run standalone unit tests.

Usage:

.. code-block:: bash

    pip install nox
    nox

If using rez and already installed nox using ``rez-pip``: ``rez env nox -- nox``
"""
from __future__ import absolute_import, division, print_function

import os

import nox


@nox.session(reuse_venv=True, venv_backend="venv")
def tests(session):
    """Test comamnd name replacement logic.

    These paths are all relative to the repository's root folder.
    """
    session.install("-r", os.path.join("tests", "requirements.txt"))
    session.run("pytest", os.path.join("tests", "unit", "test_replacements.py"))
