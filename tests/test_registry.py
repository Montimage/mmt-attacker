"""Tests for the ``matcha.registry`` attack registry."""

from __future__ import annotations

import pytest

from matcha.registry import (
    CATEGORY_APPLICATION,
    CATEGORY_NETWORK,
    CATEGORY_REPLAY,
    AttackEntry,
    ParamDef,
    all_attack_names,
    get_attack,
    list_attacks,
)


# ---------------------------------------------------------------------------
# Registry completeness
# ---------------------------------------------------------------------------

def test_total_attack_count():
    """The registry must contain exactly 26 attacks."""
    assert len(all_attack_names()) == 26


def test_network_layer_count():
    """Network-layer category should have 12 attacks."""
    grouped = list_attacks()
    assert len(grouped[CATEGORY_NETWORK]) == 12


def test_application_layer_count():
    """Application-layer category should have 13 attacks."""
    grouped = list_attacks()
    assert len(grouped[CATEGORY_APPLICATION]) == 13


def test_replay_count():
    """Replay category should have 1 attack."""
    grouped = list_attacks()
    assert len(grouped[CATEGORY_REPLAY]) == 1


def test_no_duplicate_names():
    """Attack names must be unique."""
    names = all_attack_names()
    assert len(names) == len(set(names))


# ---------------------------------------------------------------------------
# Entry structure
# ---------------------------------------------------------------------------

def test_every_entry_is_attack_entry():
    """Every value returned by list_attacks is an AttackEntry."""
    for entries in list_attacks().values():
        for entry in entries:
            assert isinstance(entry, AttackEntry)


def test_every_entry_has_required_fields():
    """Each entry must have name, description, category, module_path, class_name, params."""
    for name in all_attack_names():
        entry = get_attack(name)
        assert entry.name
        assert entry.description
        assert entry.category
        assert entry.module_path
        assert entry.class_name
        assert isinstance(entry.params, list)


def test_every_param_is_param_def():
    """Each parameter in every entry must be a ParamDef."""
    for name in all_attack_names():
        entry = get_attack(name)
        for param in entry.params:
            assert isinstance(param, ParamDef)


def test_param_def_has_required_fields():
    """Each ParamDef must have name, type, required, default, help."""
    for name in all_attack_names():
        entry = get_attack(name)
        for param in entry.params:
            assert param.name
            assert param.type in ("str", "int", "float", "bool")
            assert isinstance(param.required, bool)
            assert param.help


def test_every_entry_has_at_least_one_param():
    """Every attack should define at least one parameter."""
    for name in all_attack_names():
        entry = get_attack(name)
        assert len(entry.params) > 0, f"{name} has no params"


def test_required_params_have_none_default():
    """Required parameters should have None as default."""
    for name in all_attack_names():
        entry = get_attack(name)
        for param in entry.params:
            if param.required:
                assert param.default is None, (
                    f"{name}.{param.name}: required param should have default=None"
                )


# ---------------------------------------------------------------------------
# Category consistency
# ---------------------------------------------------------------------------

def test_categories_are_valid():
    """Every entry category must be one of the three known categories."""
    valid = {CATEGORY_NETWORK, CATEGORY_APPLICATION, CATEGORY_REPLAY}
    for name in all_attack_names():
        entry = get_attack(name)
        assert entry.category in valid, f"{name} has unknown category {entry.category!r}"


def test_list_attacks_keys():
    """list_attacks() keys must be exactly the three known categories."""
    grouped = list_attacks()
    assert set(grouped.keys()) == {CATEGORY_NETWORK, CATEGORY_APPLICATION, CATEGORY_REPLAY}


def test_list_attacks_sorted():
    """Entries within each category should be sorted by name."""
    for _cat, entries in list_attacks().items():
        names = [e.name for e in entries]
        assert names == sorted(names)


# ---------------------------------------------------------------------------
# get_attack()
# ---------------------------------------------------------------------------

def test_get_attack_known():
    """get_attack returns the correct entry for a known attack."""
    entry = get_attack("syn-flood")
    assert entry.name == "syn-flood"
    assert entry.category == CATEGORY_NETWORK
    assert entry.class_name == "SYNFloodAttack"
    assert entry.module_path == "scripts.syn_flood.syn_flood"


def test_get_attack_unknown_raises_key_error():
    """get_attack raises KeyError for an unknown attack."""
    with pytest.raises(KeyError, match="Unknown attack"):
        get_attack("nonexistent-attack")


def test_get_attack_returns_attack_entry():
    """get_attack must return an AttackEntry instance."""
    entry = get_attack("arp-spoof")
    assert isinstance(entry, AttackEntry)


# ---------------------------------------------------------------------------
# list_attacks()
# ---------------------------------------------------------------------------

def test_list_attacks_total_count():
    """Sum of all entries across categories must equal 26."""
    grouped = list_attacks()
    total = sum(len(entries) for entries in grouped.values())
    assert total == 26


def test_list_attacks_returns_dict():
    """list_attacks() must return a dict."""
    assert isinstance(list_attacks(), dict)


# ---------------------------------------------------------------------------
# all_attack_names()
# ---------------------------------------------------------------------------

def test_all_attack_names_sorted():
    """all_attack_names() must return a sorted list."""
    names = all_attack_names()
    assert names == sorted(names)


def test_all_attack_names_returns_list():
    """all_attack_names() must return a list of strings."""
    names = all_attack_names()
    assert isinstance(names, list)
    assert all(isinstance(n, str) for n in names)


# ---------------------------------------------------------------------------
# Specific attack spot checks
# ---------------------------------------------------------------------------

def test_pcap_replay_entry():
    """pcap-replay should be in the Replay category."""
    entry = get_attack("pcap-replay")
    assert entry.category == CATEGORY_REPLAY
    assert entry.class_name == "PCAPReplayAttack"


def test_slowloris_entry():
    """slowloris should be in the Application-layer category."""
    entry = get_attack("slowloris")
    assert entry.category == CATEGORY_APPLICATION
    assert entry.class_name == "SlowlorisAttack"


def test_credential_harvester_entry():
    """credential-harvester class should be CredentialHarvester."""
    entry = get_attack("credential-harvester")
    assert entry.class_name == "CredentialHarvester"


def test_module_paths_use_dot_notation():
    """All module_path values should use dot notation (no slashes)."""
    for name in all_attack_names():
        entry = get_attack(name)
        assert "/" not in entry.module_path, f"{name} module_path contains a slash"
        assert "\\" not in entry.module_path, f"{name} module_path contains a backslash"


# ---------------------------------------------------------------------------
# Dataclass immutability
# ---------------------------------------------------------------------------

def test_attack_entry_is_frozen():
    """AttackEntry instances should be immutable (frozen dataclass)."""
    entry = get_attack("syn-flood")
    with pytest.raises(AttributeError):
        entry.name = "something-else"


def test_param_def_is_frozen():
    """ParamDef instances should be immutable (frozen dataclass)."""
    entry = get_attack("syn-flood")
    param = entry.params[0]
    with pytest.raises(AttributeError):
        param.name = "something-else"
