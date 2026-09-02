# Binary Arithmetic Calculator

A clean, modular binary arithmetic project that performs **Addition**, **Subtraction**, **Multiplication**, and **Division** with step-by-step column calculations, carry/borrow tracking, and decimal verification.

Includes both a Python CLI and a standalone interactive Web UI.

---

## Features

- **Binary Addition (`+`)**: Column-by-column binary addition with carry tracking and aligned vertical representation.
- **Binary Subtraction (`-`)**: Standard binary column subtraction with borrows. Supports signed negative results when $A < B$.
- **Binary Multiplication (`*`)**: Shift-and-add binary multiplier showing all partial products.
- **Binary Division (`/`)**: Binary long division yielding both quotient and remainder, complete with step-by-step table and zero-division protection.
- **Interactive CLI & Quick Mode**: Run interactively or execute one-liners directly from your shell.
- **Web Visualizer (`index.html`)**: Beautiful, responsive browser-based calculator with real-time decimal sync and click-to-load examples.
- **Full Test Suite**: Automated unit tests verifying arithmetic algorithms and edge cases.

---

## Project Structure

```text
Sample Project/
├── binary_calculator.py    # Core arithmetic engine and algorithm implementations
├── main.py                 # Interactive terminal UI & CLI argument dispatcher
├── test_binary_calculator.py # Unit tests (unittest)
├── index.html              # Standalone web calculator UI
└── README.md               # Project documentation
```

---

## Quick Start (CLI)

### 1. Interactive Menu
Launch the interactive terminal interface:
```bash
python main.py
```
Menu options:
```text
Select an Operation:
  [1] Addition       (+)
  [2] Subtraction    (-)
  [3] Multiplication (*)
  [4] Division       (/)
  [5] Run Pre-set Demo
  [6] Decimal <-> Binary Converter
  [0] Exit
```

### 2. Direct Command-Line Calculations
You can also run calculations directly as arguments:

```bash
# Addition
python main.py 1101 + 1011

# Subtraction
python main.py 11001 - 1010

# Multiplication
python main.py 1011 "*" 101

# Division
python main.py 1101 / 10

# Run all built-in demo examples
python main.py --demo
```

---

## Web Interface

Double click [index.html](file:///c:/Users/Mark/Downloads/Sample%20Project/index.html) or open it in any web browser (Chrome, Edge, Firefox).
- Includes binary keypads (`0`, `1`, `⌫`).
- Real-time decimal translation badges.
- Formatted alignment of carries, borrows, and partial products.
- Clickable sample calculation presets.

---

## Running Automated Tests

Run the unit test suite:
```bash
python -m unittest test_binary_calculator.py -v
```

All 6 test suites verify:
- Binary normalization & format validation
- Conversions between binary and decimal
- Unequal length operands & zero operands
- Carry propagation in addition
- Borrow propagation in subtraction (and negative differences)
- Partial products summation in multiplication
- Long division steps, non-zero remainders, and `ZeroDivisionError`

