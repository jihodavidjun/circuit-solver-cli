# pytest -q

from project import load_netlist, compute_total_resistance, parallel


def test_single_resistor():
    # Result in original value
    data = {"type": "R", "value": 123.4}
    result = compute_total_resistance(data)
    assert abs(result - 123.4) < 1e-9 # Result should be close to 123.4 (floating point numbers need tolerance sometimes)


def test_series_plus_parallel():
    # Circuit: 100 in series with (200 parallel 300) in series with 50
    data = {
        "type": "S",
        "children": [
            {"type": "R", "value": 100},
            {"type": "P", "children": [
                {"type": "R", "value": 200},
                {"type": "R", "value": 300}
            ]},
            {"type": "R", "value": 50}
        ]
    }
    result = compute_total_resistance(data)
    # Expected: 100 + (200||300) + 50 = 100 + 120 + 50 = 270
    expected = 100 + (200 * 300) / (200 + 300) + 50
    assert abs(result - expected) < 1e-9


def test_empty_parallel_infinite():
    # Result in infinity
    data = {"type": "P", "children": []}
    result = compute_total_resistance(data)
    assert result == float("inf")


def test_parallel_helper_short_circuit():
    # If any resistor is 0 in parallel, total = 0 (short circuit rule)
    result = parallel([0, 200, 300])
    assert result == 0.0