# JSON Circuit Solver

## Overview
This project is my final submission for Harvard's CS50P (Introduction to Programming with Python).  
It is a simple command-line tool that computes the total resistance of resistor circuits.

Circuits are described in a **JSON file** using only:
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
As an Electrical Engineering student, I wanted my CS50P final to connect to my field.
This project simulates basic resistor circuits, showing both my programming and EE interests while keeping the scope small and beginner-appropriate.
