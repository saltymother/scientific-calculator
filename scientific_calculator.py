#!/usr/bin/env python3
"""
Scientific Calculator - First Principles Edition
================================================
A full-featured scientific calculator capable of computing:
- Trigonometric: sin, cos, tan, asin, acos, atan, atan2
- Hyperbolic: sinh, cosh, tanh
- Roots & Powers: sqrt, cbrt, x^y
- Logarithms & Exponential: ln, log (log10), exp (e^x)
- Combinatorics: fact (n!), nPr, nCr
- Fundamental constants: pi, e
- Custom expression parsing using Dijkstra's Shunting-Yard algorithm

All core mathematical functions are implemented from basic fundamentals
(Taylor/Maclaurin series, Newton-Raphson, argument reduction).

Usage:
  Interactive REPL:
    python3 scientific_calculator.py

  Evaluate expression directly:
    python3 scientific_calculator.py "sin(30) + cos(60)"
    python3 scientific_calculator.py "sin(pi/4)" --rad

  Explain fundamental calculation step-by-step:
    python3 scientific_calculator.py --explain "sin(45)"
    python3 scientific_calculator.py --explain "sqrt(2)"
"""

import sys
import re
import argparse
from calculator_engine import CalculatorEngine
from fundamentals_explainer import FundamentalsExplainer, format_explanation_cli
import fundamental_math as fm


def print_banner():
    banner = r"""
╔══════════════════════════════════════════════════════════════════╗
║               SCIENTIFIC CALCULATOR (FIRST PRINCIPLES)          ║
║   Taylor Series • Newton-Raphson • Shunting-Yard Infix Parser   ║
╚══════════════════════════════════════════════════════════════════╝
Functions : sin, cos, tan, asin, acos, atan, sinh, cosh, tanh
Roots/Exp : sqrt, cbrt, ^ (pow), exp, ln, log (base 10)
Constants : pi (3.14159...), e (2.71828...), ans
Others    : fact(n) or n!, npr(n, r), ncr(n, r), abs, floor, ceil
Commands  : 'mode deg', 'mode rad', 'explain <fn(x)>', 'history', 'help', 'exit'
"""
    print(banner)


def handle_explain(expr: str, angle_mode: str):
    """Parses expressions like sin(45), cos(60), tan(45), sqrt(2), ln(10) to explain fundamentals."""
    match = re.match(r'^\s*([a-zA-Z]+)\s*\(\s*([^)]+)\s*\)\s*$', expr.strip())
    if not match:
        print("Explain syntax: explain <func>(<number>)")
        print("Examples: explain sin(45), explain cos(60), explain tan(45), explain sqrt(2), explain ln(10)")
        return

    func_name = match.group(1).lower()
    arg_str = match.group(2).strip()

    # Evaluate the argument in case it's an expression like pi/4
    temp_calc = CalculatorEngine(angle_mode=angle_mode)
    try:
        arg_val = temp_calc.calculate(arg_str)
    except Exception as e:
        print(f"Error evaluating argument '{arg_str}': {e}")
        return

    is_deg = (angle_mode == 'DEG')

    try:
        if func_name == 'sin':
            info = FundamentalsExplainer.explain_sin(arg_val, is_degrees=is_deg)
        elif func_name == 'cos':
            info = FundamentalsExplainer.explain_cos(arg_val, is_degrees=is_deg)
        elif func_name == 'tan':
            info = FundamentalsExplainer.explain_tan(arg_val, is_degrees=is_deg)
        elif func_name == 'sqrt':
            info = FundamentalsExplainer.explain_sqrt(arg_val)
        elif func_name == 'ln':
            info = FundamentalsExplainer.explain_ln(arg_val)
        else:
            print(f"Detailed step-by-step explainer available for: sin, cos, tan, sqrt, ln.")
            # Still compute the value normally
            res = temp_calc.calculate(f"{func_name}({arg_val})")
            print(f"Result for {func_name}({arg_val}) = {res}")
            return

        print(format_explanation_cli(info))
    except Exception as e:
        print(f"Explanation Error: {e}")


def run_repl():
    print_banner()
    calc = CalculatorEngine(angle_mode='DEG')

    while True:
        try:
            prompt_str = f"calc [{calc.angle_mode}]> "
            user_input = input(prompt_str).strip()

            if not user_input:
                continue

            cmd_lower = user_input.lower()

            if cmd_lower in ('exit', 'quit', 'q'):
                print("Exiting calculator. Goodbye!")
                break

            elif cmd_lower == 'help':
                print_banner()
                continue

            elif cmd_lower in ('mode deg', 'deg'):
                calc.set_angle_mode('DEG')
                print("Angle mode switched to DEGREES.")
                continue

            elif cmd_lower in ('mode rad', 'rad'):
                calc.set_angle_mode('RAD')
                print("Angle mode switched to RADIANS.")
                continue

            elif cmd_lower == 'mode':
                print(f"Current angle mode: {calc.angle_mode}")
                continue

            elif cmd_lower == 'history':
                if not calc.history:
                    print("No calculations in history yet.")
                else:
                    print("\nCalculation History:")
                    for idx, (exp, res, m) in enumerate(calc.history, 1):
                        print(f"  {idx:2d}. [{m}] {exp} = {res}")
                    print()
                continue

            elif cmd_lower == 'vars':
                print(f"ans = {calc.variables.get('ans', 0.0)}")
                print(f"pi  = {fm.PI}")
                print(f"e   = {fm.E}")
                continue

            elif cmd_lower.startswith('explain '):
                target_expr = user_input[8:].strip()
                handle_explain(target_expr, calc.angle_mode)
                continue

            # Standard calculation
            result = calc.calculate(user_input)
            
            # Format integer outputs neatly (e.g. 120.0 -> 120)
            if isinstance(result, float) and result.is_integer() and abs(result) < 1e14:
                formatted = f"{int(result)}"
            else:
                formatted = f"{result:.12g}"

            print(f"= {formatted}\n")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting calculator. Goodbye!")
            break
        except Exception as err:
            print(f"Error: {err}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Scientific Calculator built from First Principles (Taylor series, Newton-Raphson, Shunting-Yard)."
    )
    parser.add_argument(
        'expression',
        nargs='?',
        type=str,
        help="Mathematical expression to evaluate (e.g., 'sin(30) + cos(60)')"
    )
    parser.add_argument(
        '--rad',
        action='store_true',
        help="Use radians instead of degrees for trigonometric calculations"
    )
    parser.add_argument(
        '--explain',
        action='store_true',
        help="Show step-by-step mathematical series / iterative convergence explanation"
    )

    args = parser.parse_args()

    angle_mode = 'RAD' if args.rad else 'DEG'

    if args.expression:
        if args.explain:
            handle_explain(args.expression, angle_mode)
        else:
            calc = CalculatorEngine(angle_mode=angle_mode)
            try:
                res = calc.calculate(args.expression)
                if isinstance(res, float) and res.is_integer() and abs(res) < 1e14:
                    print(int(res))
                else:
                    print(f"{res:.12g}")
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
    else:
        run_repl()


if __name__ == '__main__':
    main()
