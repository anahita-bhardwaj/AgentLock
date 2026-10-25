
from pathlib import Path

import pytest

from agentlock.policy import Decision
from agentlock.policy_loader import load_policy


POLICY_FILE = (
    Path(__file__).resolve().parents[1]
    / "policies"
    / "default.yaml"
)


def test_load_default_policy():
    policy = load_policy(POLICY_FILE)

    assert policy.evaluate("read_file") == Decision.ALLOW
    assert policy.evaluate("write_file") == Decision.DENY
    assert policy.evaluate("network_access") == Decision.ASK


def test_unknown_action_defaults_to_deny():
    policy = load_policy(POLICY_FILE)

    assert policy.evaluate("unknown_action") == Decision.DENY


def test_invalid_decision_is_rejected(tmp_path):
    policy_file = tmp_path / "invalid.yaml"
    policy_file.write_text(
        "rules:\n  read_file: maybe\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Invalid decision"):
        load_policy(policy_file)


def test_missing_policy_file_raises_error(tmp_path):
    missing_file = tmp_path / "missing.yaml"

    with pytest.raises(FileNotFoundError):
        load_policy(missing_file)
