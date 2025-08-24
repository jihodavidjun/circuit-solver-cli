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

