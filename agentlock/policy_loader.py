
from pathlib import Path

import yaml

from agentlock.policy import Decision, Policy


def load_policy(path: str | Path) -> Policy:
    """Load a policy from a YAML file."""
    policy_path = Path(path)

    with policy_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, dict):
        raise ValueError("Policy file must contain a YAML mapping.")

    raw_rules = data.get("rules", {})

    if not isinstance(raw_rules, dict):
        raise ValueError("'rules' must be a mapping.")

    rules = {}

    for action, decision in raw_rules.items():
        if not isinstance(action, str):
            raise ValueError("Policy action names must be strings.")

        if not isinstance(decision, str):
            raise ValueError(
                f"Decision for '{action}' must be a string."
            )

        try:
            rules[action] = Decision(decision.lower())
        except ValueError:
            allowed = ", ".join(item.value for item in Decision)
            raise ValueError(
                f"Invalid decision '{decision}' for '{action}'. "
                f"Choose one of: {allowed}."
            ) from None

    raw_default = data.get("default", "deny")

    if not isinstance(raw_default, str):
        raise ValueError("'default' must be a string.")

    try:
        default = Decision(raw_default.lower())
    except ValueError:
        allowed = ", ".join(item.value for item in Decision)
        raise ValueError(
            f"Invalid default decision '{raw_default}'. "
            f"Choose one of: {allowed}."
        ) from None

    return Policy(rules=rules, default=default)
