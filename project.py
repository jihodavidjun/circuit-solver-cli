import argparse  
import json       


def load_netlist(path: str) -> dict: # json to python dict.
    with open(path, "r") as f:   
        data = json.load(f)     
    return data                  


def parallel(values: list[float]) -> float: # total resistance of resistors in parallel.
    """
    Formula: 1/R_total = 1/R1 + 1/R2 + ...
    Special rules:
      - If any resistor = 0, total is 0 (short circuit).
      - If there are no resistors, total is infinite (open circuit).
    """
    if not values:               
        return float("inf")      # open circuit
    inv = 0.0                    # inv is the sum of reciprocals
    for v in values:             
        if v == 0.0:             
            return 0.0           
        inv += 1.0 / v           # add reciprocal 1/R to the sum
    return 1.0 / inv             # total resistance


def compute_total_resistance(node: dict) -> float:
    """
    Recursive method to compute resistance of a circuit node.
    Each node is a dict with:
      - {"type": "R", "value": 100}
      - {"type": "S", "children": [ ... ]}
      - {"type": "P", "children": [ ... ]}
    """
    kind = node["type"]          # read the type of node ("R", "S", or "P")

    if kind == "R":              # single resistor
        return float(node["value"])  

    if kind == "S":              # series: add all
        total = 0.0
        for child in node.get("children", []): # return [] if children's missing
            total += compute_total_resistance(child)
        return total

    if kind == "P":              # parallel: use the helper function
        values = [compute_total_resistance(ch) for ch in node.get("children", [])]
        return parallel(values)

    raise ValueError(f"Unknown node type: {kind}")


def main():
    parser = argparse.ArgumentParser(description="JSON Circuit Solver (Resistors Only)")
    parser.add_argument("--file", required=True, help="Path to JSON netlist file")
    args = parser.parse_args()

    data = load_netlist(args.file)
    total = compute_total_resistance(data)
  
    print(f"Total resistance: {total:.6g} Ω")


if __name__ == "__main__":
    main()