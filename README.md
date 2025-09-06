# JSON Circuit Solver

## Overview
A lightweight command-line tool that computes the total resistance of a resistor network described in **JSON**. 
The input uses three primitives:
- `R(value)` for resistors
- `S([...])` for series connections
- `P([...])` for parallel connections

The program loads the JSON file, recursively computes the total resistance, and prints the result.

## Example JSON Circuit
File: `examples/series_parallel.json`
```json
{
  "type": "S",
  "children": [
    {"type": "R", "value": 100},
    {
      "type": "P",
      "children": [
        {"type": "R", "value": 200},
        {"type": "R", "value": 300}
      ]
    },
    {"type": "R", "value": 50}
  ]
}
```
## Run the Program
`python project.py --file examples/series_parallel.json`

Output:

`Total resistance: 270 Ω`

## Function Descriptions
`load_netlist(path)` → loads a JSON file describing the circuit

`parallel(values)` → computes equivalent resistance for parallel resistors

`compute_total_resistance(node)` → recursively computes total resistance of any circuit node

`main()` → provides the command-line interface

## Test
This project includes `test_project.py` for pytest.
`pytest -q`

## Motivation
I wanted a small but robust project that ties programming to electrical engineering. This tool showcases how I turn a specification into working code with tests: parse a structured format (JSON), model the circuit as a tree, apply well-defined rules (series/parallel), and report a clear result. It’s intentionally scoped to be dependable and easy to extend (e.g., more components later) while demonstrating clean design, documentation, and testable logic.
