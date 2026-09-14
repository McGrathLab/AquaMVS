"""Tests for CUDA caching-allocator configuration."""

import os
import sys
from unittest.mock import patch

import pytest

from aquamvs.cli import main
from aquamvs.cuda_alloc import ALLOC_CONF_VAR, configure_cuda_allocator


@pytest.fixture
def posix(monkeypatch):
    """Run as a non-Windows platform with no allocator config set."""
    monkeypatch.setattr(sys, "platform", "linux")
    monkeypatch.delenv(ALLOC_CONF_VAR, raising=False)
    return monkeypatch


def test_sets_expandable_segments_when_unset(posix):
    configure_cuda_allocator()

    assert os.environ[ALLOC_CONF_VAR] == "expandable_segments:True"


def test_appends_to_existing_options(posix):
    posix.setenv(ALLOC_CONF_VAR, "max_split_size_mb:128")

    configure_cuda_allocator()

    assert (
        os.environ[ALLOC_CONF_VAR] == "max_split_size_mb:128,expandable_segments:True"
    )


@pytest.mark.parametrize(
    "user_value",
    ["expandable_segments:False", "max_split_size_mb:64,expandable_segments:True"],
)
def test_respects_explicit_user_setting(posix, user_value):
    posix.setenv(ALLOC_CONF_VAR, user_value)

    configure_cuda_allocator()

    assert os.environ[ALLOC_CONF_VAR] == user_value


def test_is_idempotent(posix):
    configure_cuda_allocator()
    configure_cuda_allocator()

    assert os.environ[ALLOC_CONF_VAR] == "expandable_segments:True"


def test_noop_on_windows(monkeypatch):
    monkeypatch.setattr(sys, "platform", "win32")
    monkeypatch.delenv(ALLOC_CONF_VAR, raising=False)

    configure_cuda_allocator()

    assert ALLOC_CONF_VAR not in os.environ


def test_cli_main_configures_allocator(posix):
    with patch("sys.argv", ["aquamvs"]), pytest.raises(SystemExit):
        main()  # no subcommand: prints help and exits

    assert os.environ[ALLOC_CONF_VAR] == "expandable_segments:True"
