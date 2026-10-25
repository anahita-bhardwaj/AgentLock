from enum import Enum


class Decision(Enum):
    """Possible decisions made by the AgentLock policy engine."""

    ALLOW = "allow"
    DENY = "deny"
    ASK = "ask"


class Policy:
    """Evaluate actions according to a policy."""

    def __init__(
        self,
        rules: dict[str, Decision] | None = None,
        default: Decision = Decision.DENY,
    ):
        self.rules = rules or {}
        self.default = default

    def evaluate(self, action: str) -> Decision:
        """Return the decision for an action."""
        return self.rules.get(action, self.default)