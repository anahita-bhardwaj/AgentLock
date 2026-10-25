from agentlock.policy import Decision, Policy


def test_decision_values():
    assert Decision.ALLOW.value == "allow"
    assert Decision.DENY.value == "deny"
    assert Decision.ASK.value == "ask"


def test_decisions_are_distinct():
    assert Decision.ALLOW != Decision.DENY
    assert Decision.ALLOW != Decision.ASK
    assert Decision.DENY != Decision.ASK


def test_policy_uses_matching_rules():
    policy = Policy(
        rules={
            "read_file": Decision.ALLOW,
            "write_file": Decision.DENY,
            "network_access": Decision.ASK,
        }
    )

    assert policy.evaluate("read_file") == Decision.ALLOW
    assert policy.evaluate("write_file") == Decision.DENY
    assert policy.evaluate("network_access") == Decision.ASK


def test_policy_defaults_to_deny():
    policy = Policy(
        rules={
            "read_file": Decision.ALLOW,
        }
    )

    assert policy.evaluate("unknown_action") == Decision.DENY