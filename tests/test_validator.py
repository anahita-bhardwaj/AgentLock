
import pytest

from agentlock.validator import validate_command


def test_validate_command_accepts_valid_command():
    assert validate_command(["cmd", "/c", "echo", "hello"]) is None


def test_validate_command_rejects_empty_list():
    with pytest.raises(ValueError, match="non-empty list"):
        validate_command([])


def test_validate_command_rejects_non_list():
    with pytest.raises(ValueError, match="non-empty list"):
        validate_command("cmd")


def test_validate_command_rejects_non_string_argument():
    with pytest.raises(ValueError, match="Every command argument"):
        validate_command(["cmd", 123])


def test_validate_command_rejects_blank_executable():
    with pytest.raises(ValueError, match="executable name"):
        validate_command(["   ", "hello"])
