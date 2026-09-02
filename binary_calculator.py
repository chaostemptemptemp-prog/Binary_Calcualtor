"""
Binary Calculator Module
Implements binary arithmetic operations (addition, subtraction, multiplication, division)
using algorithmic simulation of digital logic and manual column-by-column calculation.
"""

from typing import Dict, Any, List, Tuple


def normalize_binary(s: str) -> str:
    """
    Cleans and standardizes binary string input.
    Removes whitespace, underscores, and optional '0b' prefix.
    """
    if not isinstance(s, str):
        s = str(s)
    s = s.strip().lower()
    if s.startswith("0b"):
        s = s[2:]
    if not s:
        raise ValueError("Binary string cannot be empty.")
    if not all(c in "01" for c in s):
        raise ValueError(f"Invalid binary string '{s}'. Must contain only '0' and '1'.")
    # Strip leading zeros, but keep at least one '0' if the number is zero
    stripped = s.lstrip("0")
    return stripped if stripped else "0"


def bin_to_dec(s: str) -> int:
    """Converts a valid binary string to a decimal integer."""
    clean = normalize_binary(s)
    return int(clean, 2)


def dec_to_bin(n: int) -> str:
    """Converts a non-negative decimal integer to a binary string."""
    if n < 0:
        raise ValueError("Only non-negative integers supported in dec_to_bin.")
    return bin(n)[2:]


class BinaryCalculator:
    """
    Provides binary addition, subtraction, multiplication, and division
    with algorithmic step tracking (carries, borrows, partial products, remainders).
    """

    @staticmethod
    def add(bin_a: str, bin_b: str) -> Dict[str, Any]:
        """
        Performs binary column addition of bin_a and bin_b.
        Tracks carry bits at each position.
        """
        a = normalize_binary(bin_a)
        b = normalize_binary(bin_b)
        
        max_len = max(len(a), len(b))
        padded_a = a.zfill(max_len)
        padded_b = b.zfill(max_len)
        
        carry = 0
        result_bits: List[str] = []
        carries: List[int] = []  # Carries generated from right to left
        step_descriptions: List[str] = []

        # Iterate from least significant bit (right) to most significant (left)
        for i in range(max_len - 1, -1, -1):
            bit_a = int(padded_a[i])
            bit_b = int(padded_b[i])
            
            total = bit_a + bit_b + carry
            out_bit = total % 2
            next_carry = total // 2
            
            step_descriptions.append(
                f"Col {max_len - 1 - i}: {bit_a} + {bit_b} + carry({carry}) = {total} -> bit {out_bit}, carry {next_carry}"
            )
            
            result_bits.append(str(out_bit))
            carries.append(carry)
            carry = next_carry

        if carry:
            result_bits.append(str(carry))
            step_descriptions.append(f"Final carry-out: {carry}")
        
        result_bits.reverse()
        result_str = "".join(result_bits).lstrip("0") or "0"
        
        # Carries aligned with padded inputs (with final carry at left)
        carry_line = str(carry) + "".join(str(c) for c in reversed(carries))

        return {
            "operation": "addition",
            "a": a,
            "b": b,
            "a_dec": bin_to_dec(a),
            "b_dec": bin_to_dec(b),
            "result": result_str,
            "result_dec": bin_to_dec(result_str),
            "padded_a": padded_a,
            "padded_b": padded_b,
            "carries": carry_line,
            "steps": step_descriptions,
        }

    @staticmethod
    def subtract(bin_a: str, bin_b: str) -> Dict[str, Any]:
        """
        Performs binary subtraction (bin_a - bin_b).
        If bin_a < bin_b, computes -(bin_b - bin_a).
        Tracks borrows column by column.
        """
        a = normalize_binary(bin_a)
        b = normalize_binary(bin_b)
        
        dec_a = bin_to_dec(a)
        dec_b = bin_to_dec(b)
        is_negative = dec_a < dec_b

        top, bottom = (b, a) if is_negative else (a, b)
        max_len = max(len(top), len(bottom))
        padded_top = top.zfill(max_len)
        padded_bottom = bottom.zfill(max_len)

        # Work with mutable list of digits for top to simulate borrowing
        top_digits = [int(c) for c in padded_top]
        bottom_digits = [int(c) for c in padded_bottom]
        
        result_bits: List[str] = []
        borrows: List[int] = [0] * max_len
        step_descriptions: List[str] = []

        for i in range(max_len - 1, -1, -1):
            t = top_digits[i]
            b_val = bottom_digits[i]

            if t < b_val:
                # Need to borrow from the nearest higher column with a 1
                borrow_col = i - 1
                while borrow_col >= 0 and top_digits[borrow_col] == 0:
                    borrow_col -= 1
                
                if borrow_col >= 0:
                    top_digits[borrow_col] -= 1
                    for k in range(borrow_col + 1, i):
                        top_digits[k] += 1  # 0 becomes 1 after borrow passes through
                    top_digits[i] += 2
                    borrows[i] = 1
                    step_descriptions.append(
                        f"Col {max_len - 1 - i}: Borrow needed. Borrowed from Col {max_len - 1 - borrow_col}."
                    )
            
            diff = top_digits[i] - b_val
            result_bits.append(str(diff))
            step_descriptions.append(
                f"Col {max_len - 1 - i}: {top_digits[i]} - {b_val} = {diff}"
            )

        result_bits.reverse()
        result_str = "".join(result_bits).lstrip("0") or "0"
        if is_negative and result_str != "0":
            signed_result = f"-{result_str}"
        else:
            signed_result = result_str

        return {
            "operation": "subtraction",
            "a": a,
            "b": b,
            "a_dec": dec_a,
            "b_dec": dec_b,
            "is_negative": is_negative,
            "result": signed_result,
            "result_dec": dec_a - dec_b,
            "padded_top": padded_top,
            "padded_bottom": padded_bottom,
            "borrows": "".join(str(b) for b in borrows),
            "steps": step_descriptions,
        }

    @staticmethod
    def multiply(bin_a: str, bin_b: str) -> Dict[str, Any]:
        """
        Performs binary multiplication using shift-and-add (partial products).
        """
        a = normalize_binary(bin_a)
        b = normalize_binary(bin_b)
        
        dec_a = bin_to_dec(a)
        dec_b = bin_to_dec(b)

        partial_products: List[Dict[str, Any]] = []
        step_descriptions: List[str] = []

        # Iterate through multiplier bits from right to left
        for shift, bit in enumerate(reversed(b)):
            if bit == "1":
                pp_value = a + ("0" * shift)
                step_descriptions.append(
                    f"Bit {shift} is '1': add {a} shifted left by {shift} -> {pp_value}"
                )
            else:
                pp_value = "0" * (len(a) + shift)
                step_descriptions.append(
                    f"Bit {shift} is '0': add 0 shifted left by {shift} -> {pp_value}"
                )
            
            partial_products.append({
                "shift": shift,
                "multiplier_bit": bit,
                "value": pp_value
            })

        prod_dec = dec_a * dec_b
        result_bin = dec_to_bin(prod_dec)

        return {
            "operation": "multiplication",
            "a": a,
            "b": b,
            "a_dec": dec_a,
            "b_dec": dec_b,
            "result": result_bin,
            "result_dec": prod_dec,
            "partial_products": partial_products,
            "steps": step_descriptions,
        }

    @staticmethod
    def divide(bin_a: str, bin_b: str) -> Dict[str, Any]:
        """
        Performs binary long division (bin_a / bin_b).
        Returns quotient and remainder, alongside step-by-step long division history.
        Raises ZeroDivisionError if bin_b == '0'.
        """
        a = normalize_binary(bin_a)
        b = normalize_binary(bin_b)

        dec_b = bin_to_dec(b)
        if dec_b == 0:
            raise ZeroDivisionError("Binary division by zero is undefined.")

        dec_a = bin_to_dec(a)
        divisor = dec_b

        quotient_bits: List[str] = []
        current_remainder = 0
        steps: List[Dict[str, Any]] = []

        for idx, bit in enumerate(a):
            bit_val = int(bit)
            current_remainder = (current_remainder << 1) | bit_val
            
            if current_remainder >= divisor:
                q_bit = "1"
                subtrahend = divisor
                new_remainder = current_remainder - divisor
                steps.append({
                    "step": idx + 1,
                    "brought_down_bit": bit,
                    "current_value": dec_to_bin(current_remainder),
                    "quotient_bit": "1",
                    "subtraction": f"{dec_to_bin(current_remainder)} - {b} = {dec_to_bin(new_remainder)}",
                    "remainder": dec_to_bin(new_remainder)
                })
                current_remainder = new_remainder
            else:
                q_bit = "0"
                steps.append({
                    "step": idx + 1,
                    "brought_down_bit": bit,
                    "current_value": dec_to_bin(current_remainder),
                    "quotient_bit": "0",
                    "subtraction": "None (current < divisor)",
                    "remainder": dec_to_bin(current_remainder)
                })
            quotient_bits.append(q_bit)

        quotient_str = "".join(quotient_bits).lstrip("0") or "0"
        remainder_str = dec_to_bin(current_remainder)

        return {
            "operation": "division",
            "dividend": a,
            "divisor": b,
            "dividend_dec": dec_a,
            "divisor_dec": dec_b,
            "quotient": quotient_str,
            "quotient_dec": bin_to_dec(quotient_str),
            "remainder": remainder_str,
            "remainder_dec": current_remainder,
            "steps": steps,
        }

