from __future__ import annotations

import os
import runpy
from pathlib import Path

from setuptools import build_meta as _orig
from setuptools.build_meta import *  # noqa: F401,F403 - re-export PEP 517 hooks

_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):  # type: ignore[override]
    return _orig.build_wheel(wheel_directory, config_settings, metadata_directory)


def build_sdist(sdist_directory, config_settings=None):  # type: ignore[override]
    return _orig.build_sdist(sdist_directory, config_settings)


def build_editable(wheel_directory, config_settings=None, metadata_directory=None):  # type: ignore[override]
    # PEP 660 editable install hook (pip -e). Ensure the file exists here too.
    return _orig.build_editable(wheel_directory, config_settings, metadata_directory)


def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):  # type: ignore[override]
    return _orig.prepare_metadata_for_build_wheel(metadata_directory, config_settings)


def prepare_metadata_for_build_editable(metadata_directory, config_settings=None):  # type: ignore[override]
    return _orig.prepare_metadata_for_build_editable(
        metadata_directory, config_settings
    )
