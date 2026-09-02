"""
Binary Calculator CLI Entrypoint
Provides an interactive menu and command-line interface for binary arithmetic.
"""

import sys
from typing import List
from binary_calculator import (
    BinaryCalculator,
    normalize_binary,
    bin_to_dec,
    dec_to_bin,
)


def print_banner():
    print("=" * 60)
    print("        BINARY ARITHMETIC CALCULATOR (CLI)        ")
    print("   Addition  *  Subtraction  *  Multiplication  *  Division   ")
    print("=" * 60)


def print_addition(res: dict):
    print("\n--- [BINARY ADDITION] ---")
    pad_a = res["padded_a"]
    pad_b = res["padded_b"]
    carries = res["carries"]
    result = res["result"]
    width = max(len(pad_a), len(pad_b), len(result), len(carries)) + 4

    print(f"  Carries:  {carries.rjust(width)}")
    print(f"            {pad_a.rjust(width)}   ({res['a_dec']})")
    print(f"          + {pad_b.rjust(width)}   ({res['b_dec']})")
    print("          " + "-" * (width + 2))
    print(f"  Result:   {result.rjust(width)}   ({res['result_dec']})")
    
    print("\nColumn-by-column breakdown:")
    for step in res["steps"]:
        print(f"  * {step}")


def print_subtraction(res: dict):
    print("\n--- [BINARY SUBTRACTION] ---")
    top = res["padded_top"]
    bottom = res["padded_bottom"]
    borrows = res["borrows"]
    result = res["result"]
    width = max(len(top), len(bottom), len(result)) + 4

    if res["is_negative"]:
        print(f"  Note: {res['a']} < {res['b']}, calculated -({res['b']} - {res['a']})")
    print(f"  Borrows:  {borrows.rjust(width)}")
    print(f"            {top.rjust(width)}   ({res['a_dec'] if not res['is_negative'] else res['b_dec']})")
    print(f"          - {bottom.rjust(width)}   ({res['b_dec'] if not res['is_negative'] else res['a_dec']})")
    print("          " + "-" * (width + 2))
    print(f"  Result:   {result.rjust(width)}   ({res['result_dec']})")

    print("\nColumn-by-column breakdown:")
    for step in res["steps"]:
        print(f"  * {step}")


def print_multiplication(res: dict):
    print("\n--- [BINARY MULTIPLICATION] ---")
    a = res["a"]
    b = res["b"]
    result = res["result"]
    width = max(len(a), len(b), len(result)) + 6

    print(f"            {a.rjust(width)}   ({res['a_dec']})")
    print(f"          x {b.rjust(width)}   ({res['b_dec']})")
    print("          " + "-" * (width + 2))

    print("  Partial Products:")
    for pp in res["partial_products"]:
        shift = pp["shift"]
        bit = pp["multiplier_bit"]
        val = pp["value"]
        print(f"          + {val.rjust(width)}   [bit {shift} = '{bit}']")

    print("          " + "=" * (width + 2))
    print(f"  Product:  {result.rjust(width)}   ({res['result_dec']})")


def print_division(res: dict):
    print("\n--- [BINARY LONG DIVISION] ---")
    dividend = res["dividend"]
    divisor = res["divisor"]
    quotient = res["quotient"]
    remainder = res["remainder"]

    print(f"  Dividend:  {dividend} ({res['dividend_dec']})")
    print(f"  Divisor:   {divisor} ({res['divisor_dec']})")
    print(f"  Quotient:  {quotient} ({res['quotient_dec']})")
    print(f"  Remainder: {remainder} ({res['remainder_dec']})")
    print(f"  Formula:   {dividend} = ({divisor} * {quotient}) + {remainder}")

    print("\nLong Division Step Details:")
    print(f"  {'Step':<6} {'Bit Down':<10} {'Current Val':<14} {'Quotient Bit':<14} {'Operation'}")
    print("  " + "-" * 60)
    for s in res["steps"]:
        print(
            f"  {s['step']:<6} {s['brought_down_bit']:<10} {s['current_value']:<14} "
            f"{s['quotient_bit']:<14} {s['subtraction']}"
        )


def run_demo():
    print("\n>>> RUNNING DEMONSTRATION EXAMPLES <<<\n")
    
    # 1. Addition
    print("1. Addition: 1101 + 1011 (13 + 11)")
    print_addition(BinaryCalculator.add("1101", "1011"))
    
    # 2. Subtraction
    print("\n" + "=" * 60)
    print("2. Subtraction: 11001 - 1010 (25 - 10)")
    print_subtraction(BinaryCalculator.subtract("11001", "1010"))

    # 3. Multiplication
    print("\n" + "=" * 60)
    print("3. Multiplication: 1011 * 101 (11 * 5)")
    print_multiplication(BinaryCalculator.multiply("1011", "101"))

    # 4. Division
    print("\n" + "=" * 60)
    print("4. Division: 1101 / 10 (13 / 2)")
    print_division(BinaryCalculator.divide("1101", "10"))
    print("=" * 60 + "\n")


def prompt_binary(prompt_text: str) -> str:
    while True:
        raw = input(prompt_text).strip()
        try:
            return normalize_binary(raw)
        except ValueError as e:
            print(f"  Error: {e}. Please enter a valid binary number (0s and 1s only).")


def interactive_menu():
    print_banner()
    while True:
        print("\nSelect an Operation:")
        print("  [1] Addition       (+)")
        print("  [2] Subtraction    (-)")
        print("  [3] Multiplication (*)")
        print("  [4] Division       (/)")
        print("  [5] Run Pre-set Demo")
        print("  [6] Decimal <-> Binary Converter")
        print("  [0] Exit")

        choice = input("\nEnter choice (0-6): ").strip()
        if choice == "0":
            print("Goodbye!")
            break

        if choice == "1":
            a = prompt_binary("Enter first binary number:  ")
            b = prompt_binary("Enter second binary number: ")
            res = BinaryCalculator.add(a, b)
            print_addition(res)

        elif choice == "2":
            a = prompt_binary("Enter binary minuend (A):    ")
            b = prompt_binary("Enter binary subtrahend (B): ")
            res = BinaryCalculator.subtract(a, b)
            print_subtraction(res)

        elif choice == "3":
            a = prompt_binary("Enter binary multiplicand: ")
            b = prompt_binary("Enter binary multiplier:   ")
            res = BinaryCalculator.multiply(a, b)
            print_multiplication(res)

        elif choice == "4":
            a = prompt_binary("Enter binary dividend (numerator):   ")
            b = prompt_binary("Enter binary divisor (denominator): ")
            try:
                res = BinaryCalculator.divide(a, b)
                print_division(res)
            except ZeroDivisionError as e:
                print(f"\n  Error: {e}")

        elif choice == "5":
            run_demo()

        elif choice == "6":
            sub_choice = input("Convert [1] Binary to Decimal or [2] Decimal to Binary? ").strip()
            if sub_choice == "1":
                b_str = prompt_binary("Enter binary: ")
                print(f"  {b_str} in decimal is: {bin_to_dec(b_str)}")
            elif sub_choice == "2":
                try:
                    d_int = int(input("Enter non-negative decimal integer: ").strip())
                    print(f"  {d_int} in binary is: {dec_to_bin(d_int)}")
                except ValueError:
                    print("  Invalid decimal integer.")
            else:
                print("  Invalid conversion option.")
        else:
            print("Invalid selection. Please enter a number between 0 and 6.")


def handle_cli_args(args: List[str]):
    """
    Allows executing calculations directly via CLI args:
    e.g. python main.py 1101 + 1011
    """
    if len(args) == 1 and args[0].lower() in ("--demo", "demo"):
        run_demo()
        return

    if len(args) == 3:
        a_str, op, b_str = args
        try:
            if op == "+":
                print_addition(BinaryCalculator.add(a_str, b_str))
            elif op == "-":
                print_subtraction(BinaryCalculator.subtract(a_str, b_str))
            elif op in ("*", "x", "X"):
                print_multiplication(BinaryCalculator.multiply(a_str, b_str))
            elif op == "/":
                print_division(BinaryCalculator.divide(a_str, b_str))
            else:
                print(f"Unknown operator '{op}'. Supported: +, -, *, /")
        except Exception as e:
            print(f"Error executing operation: {e}")
        return

    print("Usage:")
    print("  python main.py                     (Interactive Menu)")
    print("  python main.py --demo              (Run Built-in Demo)")
    print("  python main.py <bin1> <op> <bin2>  (e.g., python main.py 1101 + 1011)")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        handle_cli_args(sys.argv[1:])
    else:
        interactive_menu()

