# test_project.py
# Run with: pytest --cov=project --cov-branch --cov-report=term-missing -q

import math, json, sys, pytest
from project import load_netlist, compute_total_resistance, parallel, main as cli

def close(a, b, tol=1e-9):
    return math.isclose(a, b, rel_tol=0.0, abs_tol=tol)

# ---------------- Core tests ----------------

def test_single_resistor():
    data = {"type": "R", "value": 123.4}
    result = compute_total_resistance(data)
    assert close(result, 123.4)

def test_series_plus_parallel():
    data = {
        "type": "S",
        "children": [
            {"type": "R", "value": 100},
            {"type": "P", "children": [
                {"type": "R", "value": 200},
                {"type": "R", "value": 300},
            ]},
            {"type": "R", "value": 50},
        ],
    }
    result = compute_total_resistance(data)
    expected = 100 + (200 * 300) / (200 + 300) + 50
    assert close(result, expected)

def test_empty_parallel_infinite():
    data = {"type": "P", "children": []}
    result = compute_total_resistance(data)
    assert result == float("inf")

def test_parallel_helper_short_circuit():
    assert parallel([0, 200, 300]) == 0.0

def test_invalid_spec_raises():
    bad = {"type": "R", "value": -5}
    with pytest.raises(ValueError):
        compute_total_resistance(bad)

def test_series_only():
    data = {"type": "S", "children": [
        {"type": "R", "value": 10},
        {"type": "R", "value": 20},
        {"type": "R", "value": 30},
    ]}
    assert compute_total_resistance(data) == 60

def test_parallel_only():
    data = {"type": "P", "children": [
        {"type": "R", "value": 100},
        {"type": "R", "value": 300},
    ]}
    expected = 1 / (1/100 + 1/300)  # 75
    assert close(compute_total_resistance(data), expected)

# ---------------- Extra coverage tests ----------------

def test_resistor_value_type_check():
    with pytest.raises(ValueError):
        compute_total_resistance({"type": "R", "value": "100"})  # string not allowed

def test_series_empty_identity_zero():
    assert compute_total_resistance({"type": "S", "children": []}) == 0.0

def test_parallel_single_child_identity():
    data = {"type": "P", "children": [{"type": "R", "value": 75}]}
    assert compute_total_resistance(data) == 75.0

def test_unknown_type_raises():
    with pytest.raises(ValueError):
        compute_total_resistance({"type": "X"})

def test_load_netlist_reads_json(tmp_path):
    p = tmp_path / "net.json"
    p.write_text(json.dumps({"type": "R", "value": 42}))
    loaded = load_netlist(str(p))
    assert loaded["value"] == 42

def test_cli_outputs_number(tmp_path, monkeypatch, capsys):
    p = tmp_path / "net.json"
    p.write_text(json.dumps({"type": "R", "value": 5}))
    monkeypatch.setattr(sys, "argv", ["prog", "--file", str(p)])
    cli()
    out = capsys.readouterr().out
    assert "Total resistance:" in out and "5" in out

def test_parallel_helper_empty_is_inf():
    assert parallel([]) == float("inf")

def test_parallel_helper_regular_values():
    assert close(parallel([100, 300]), 75.0)

def test_tree_parallel_short_inside_tree():
    data = {"type": "P", "children": [
        {"type": "R", "value": 0},
        {"type": "R", "value": 999},
    ]}
    assert compute_total_resistance(data) == 0.0

def test_bool_not_allowed():
    import pytest
    with pytest.raises(ValueError):
        compute_total_resistance({"type": "R", "value": True})

import sys, subprocess, json

def test_cli_entrypoint(tmp_path):
    p = tmp_path / "net.json"
    p.write_text(json.dumps({"type": "R", "value": 5}))
    res = subprocess.run(
        [sys.executable, "-m", "project", "--file", str(p)],
        capture_output=True, text=True, check=True
    )
    assert "Total resistance:" in res.stdout
