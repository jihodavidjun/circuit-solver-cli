import argparse
import json

def load_netlist(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)

def _checked_value(v) -> float:
    # Must be a real number (bools are ints, so exclude them) and non-negative.
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ValueError("Resistance must be a number")
    if v < 0:
        raise ValueError("Resistance must be non-negative")
    return float(v)

def parallel(values: list[float]) -> float:
    """
    1/R_total = sum(1/Ri)
    - any 0-ohm branch => 0 (short)
    - empty list => inf (open)
    """
    if not values:
        return float("inf")
    inv = 0.0
    for v in values:
        v = _checked_value(v)
        if v == 0.0:
            return 0.0
        inv += 1.0 / v
    return 1.0 / inv

def compute_total_resistance(node: dict) -> float:
    """
    Node forms:
      {"type": "R", "value": 100}
      {"type": "S", "children": [...]}
      {"type": "P", "children": [...]}
    """
    kind = node["type"]

    if kind == "R":
        return _checked_value(node.get("value"))

    if kind == "S":
        return sum(compute_total_resistance(ch) for ch in node.get("children", []))

    if kind == "P":
        children = node.get("children", [])
        if not children:
            return float("inf")
        denom = 0.0
        for ch in children:
            r = compute_total_resistance(ch)
            if r == 0.0:
                return 0.0
            denom += 1.0 / r
        return 1.0 / denom

    raise ValueError(f"Unknown node type: {kind}")

def main():
    parser = argparse.ArgumentParser(description="JSON Circuit Solver (Resistors Only)")
    parser.add_argument("--file", required=True, help="Path to JSON netlist file")
    args = parser.parse_args()
    total = compute_total_resistance(load_netlist(args.file))
    print(f"Total resistance: {total:.6g} Ω")

if __name__ == "__main__":
    main()
