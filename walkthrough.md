# Walkthrough - Binary Arithmetic Calculator Project

We created a modular binary arithmetic project that supports **Addition**, **Subtraction**, **Multiplication**, and **Division** with manual column-by-column simulation, carry/borrow tracking, partial product displays, long division steps, an interactive CLI, a comprehensive unit test suite, and a standalone browser-based web interface.

---

## Changes Made

### 1. Core Engine
- Created [binary_calculator.py](file:///c:/Users/Mark/Downloads/Sample%20Project/binary_calculator.py):
  - `add`: Simulates binary full-adder column addition with carry tracking.
  - `subtract`: Simulates binary column subtraction with borrow propagation; handles signed negative results if $A < B$.
  - `multiply`: Simulates binary shift-and-add partial product multiplication.
  - `divide`: Simulates binary long division producing quotient, remainder, and step-by-step table; handles division by zero safely.
  - `normalize_binary`, `bin_to_dec`, `dec_to_bin`: Validation and standard conversion helpers.

### 2. Command Line Interface (CLI)
- Created [main.py](file:///c:/Users/Mark/Downloads/Sample%20Project/main.py):
  - Interactive terminal menu for all 4 operations, conversions, and a pre-set demonstration.
  - Support for direct one-line command invocation (e.g. `python main.py 1101 + 1011`).
  - Aligned column rendering for carries, borrows, and partial products.

### 3. Automated Test Suite
- Created [test_binary_calculator.py](file:///c:/Users/Mark/Downloads/Sample%20Project/test_binary_calculator.py):
  - 6 test suites covering input normalization, conversions, all arithmetic operations, edge cases (zeros, large numbers, unequal operand lengths), and error handling (`ZeroDivisionError`, invalid characters).

### 4. Interactive Web Interface
- Created [index.html](file:///c:/Users/Mark/Downloads/Sample%20Project/index.html):
  - Responsive single-page app with binary keypad buttons (`0`, `1`, `⌫`).
  - Real-time decimal synchronization.
  - Formatted text display with step-by-step calculation cards and sample presets.

### 5. Documentation
- Created [README.md](file:///c:/Users/Mark/Downloads/Sample%20Project/README.md) with complete usage guides, CLI commands, and test instructions.

---

## Verification Results

### Automated Tests
Ran:
```bash
python -m unittest test_binary_calculator.py -v
```
Output:
```text
test_addition (test_binary_calculator.TestBinaryCalculator.test_addition) ... ok
test_conversions (test_binary_calculator.TestBinaryCalculator.test_conversions) ... ok
test_division (test_binary_calculator.TestBinaryCalculator.test_division) ... ok
test_multiplication (test_binary_calculator.TestBinaryCalculator.test_multiplication) ... ok
test_normalize_binary (test_binary_calculator.TestBinaryCalculator.test_normalize_binary) ... ok
test_subtraction (test_binary_calculator.TestBinaryCalculator.test_subtraction) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK
```

### CLI Operations & Demo
Tested all 4 operations and built-in demo:
- Addition: `1101 + 1011 = 11000` (13 + 11 = 24) with carries `11110`
- Subtraction: `11001 - 1010 = 1111` (25 - 10 = 15) with borrow tracking
- Multiplication: `1011 * 101 = 110111` (11 * 5 = 55) with 3 partial products
- Division: `1101 / 10 = 110 R 1` (13 / 2 = 6 rem 1) with 4 long division steps
- Division by Zero: Caught cleanly with informative error message
