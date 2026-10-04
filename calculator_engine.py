"""
Scientific Calculator Engine - Tokenizer, Shunting-Yard Parser & Evaluator
==========================================================================
Implements an expression parser and evaluator completely from first principles:
- Lexical analyzer / Tokenizer (with implicit multiplication and unary handling)
- Edsger Dijkstra's Shunting-Yard algorithm (infix to postfix / RPN)
- RPN stack evaluator using `fundamental_math`
"""

import fundamental_math as fm
from typing import List, Tuple, Dict, Any, Optional

# Supported unary & binary operators with precedence and associativity
# Precedence: higher number = tighter binding
# Associativity: 'L' = Left-to-right, 'R' = Right-to-left
OPERATORS = {
    '+':   {'prec': 2, 'assoc': 'L', 'args': 2},
    '-':   {'prec': 2, 'assoc': 'L', 'args': 2},
    '*':   {'prec': 3, 'assoc': 'L', 'args': 2},
    '/':   {'prec': 3, 'assoc': 'L', 'args': 2},
    '%':   {'prec': 3, 'assoc': 'L', 'args': 2},
    '^':   {'prec': 5, 'assoc': 'R', 'args': 2},
    'u-':  {'prec': 4, 'assoc': 'R', 'args': 1},  # Unary negation
    'u+':  {'prec': 4, 'assoc': 'R', 'args': 1},  # Unary positive
}

# Function registry mapping function name to argument count
FUNCTIONS = {
    'sin': 1, 'cos': 1, 'tan': 1,
    'asin': 1, 'acos': 1, 'atan': 1,
    'sinh': 1, 'cosh': 1, 'tanh': 1,
    'sqrt': 1, 'cbrt': 1, 'ln': 1, 'log': 1, 'log10': 1,
    'exp': 1, 'abs': 1, 'fact': 1, 'floor': 1, 'ceil': 1,
    'rad': 1, 'deg': 1,
    'npr': 2, 'ncr': 2, 'pow': 2, 'atan2': 2
}

# Named Constants
CONSTANTS = {
    'pi': fm.PI,
    'e': fm.E,
}


class Token:
    """Represents a lexical token in a mathematical expression."""
    NUMBER = 'NUMBER'
    OPERATOR = 'OPERATOR'
    FUNCTION = 'FUNCTION'
    CONSTANT = 'CONSTANT'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    COMMA = 'COMMA'
    VARIABLE = 'VARIABLE'

    def __init__(self, type_: str, value: Any):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"


class CalculatorEngine:
    def __init__(self, angle_mode: str = 'DEG'):
        """
        angle_mode: 'DEG' (degrees) or 'RAD' (radians)
        """
        self.angle_mode = angle_mode.upper()
        self.variables = {'ans': 0.0}
        self.history = []

    def set_angle_mode(self, mode: str):
        mode = mode.upper()
        if mode not in ('DEG', 'RAD'):
            raise ValueError("Angle mode must be 'DEG' or 'RAD'")
        self.angle_mode = mode

    # -----------------------------------------------------------------------
    # 1. Lexer / Tokenizer
    # -----------------------------------------------------------------------
    def tokenize(self, expr: str) -> List[Token]:
        """
        Tokenizes an expression string into a list of Token objects.
        Handles:
        - Floating point numbers (e.g. 3.1415, .5, 1e-4)
        - Function names and constants
        - Operators (+, -, *, /, ^, %)
        - Parentheses and commas
        - Implicit multiplication (e.g. 2pi -> 2 * pi, 2(3) -> 2 * (3))
        - Unary operators (e.g. -5, 3*-2, sin(-pi/2))
        """
        raw_tokens: List[Token] = []
        i = 0
        n = len(expr)

        while i < n:
            ch = expr[i]

            # Whitespace
            if ch.isspace():
                i += 1
                continue

            # Number
            if ch.isdigit() or (ch == '.' and i + 1 < n and expr[i + 1].isdigit()):
                start = i
                has_dot = False
                while i < n and (expr[i].isdigit() or (expr[i] == '.' and not has_dot)):
                    if expr[i] == '.':
                        has_dot = True
                    i += 1
                
                # Check for scientific notation (e.g. 1e-5 or 2.5E+3)
                if i < n and expr[i] in 'eE':
                    if i + 1 < n and (expr[i + 1].isdigit() or (expr[i + 1] in '+-' and i + 2 < n and expr[i + 2].isdigit())):
                        i += 1
                        if expr[i] in '+-':
                            i += 1
                        while i < n and expr[i].isdigit():
                            i += 1

                num_str = expr[start:i]
                raw_tokens.append(Token(Token.NUMBER, float(num_str)))
                continue

            # Identifiers: functions, constants, or variables
            if ch.isalpha() or ch == '_':
                start = i
                while i < n and (expr[i].isalnum() or expr[i] == '_'):
                    i += 1
                name = expr[start:i].lower()

                if name in FUNCTIONS:
                    raw_tokens.append(Token(Token.FUNCTION, name))
                elif name in CONSTANTS:
                    raw_tokens.append(Token(Token.CONSTANT, CONSTANTS[name]))
                elif name in self.variables:
                    raw_tokens.append(Token(Token.VARIABLE, name))
                else:
                    raise ValueError(f"Unknown function, constant, or variable: '{name}'")
                continue

            # Two-character or single-character operators
            if ch == '(':
                raw_tokens.append(Token(Token.LPAREN, '('))
                i += 1
            elif ch == ')':
                raw_tokens.append(Token(Token.RPAREN, ')'))
                i += 1
            elif ch == ',':
                raw_tokens.append(Token(Token.COMMA, ','))
                i += 1
            elif ch in '+-*/^%':
                # Check for factorial shortcut '!'
                raw_tokens.append(Token(Token.OPERATOR, ch))
                i += 1
            elif ch == '!':
                # Treat postfix factorial as a special function/operator
                raw_tokens.append(Token(Token.FUNCTION, 'fact'))
                i += 1
            else:
                raise ValueError(f"Unexpected character in expression: '{ch}'")

        # Disambiguate unary operators and inject implicit multiplication
        processed_tokens: List[Token] = []
        m = len(raw_tokens)

        for idx in range(m):
            curr = raw_tokens[idx]
            prev = raw_tokens[idx - 1] if idx > 0 else None

            # 1. Unary minus / plus detection
            if curr.type == Token.OPERATOR and curr.value in ('+', '-'):
                # Unary if at start or follows an operator, LPAREN, or COMMA
                if prev is None or prev.type in (Token.OPERATOR, Token.LPAREN, Token.COMMA):
                    curr = Token(Token.OPERATOR, 'u-' if curr.value == '-' else 'u+')

            # 2. Implicit multiplication:
            # E.g. Number followed by LPAREN, FUNCTION, CONSTANT, or VARIABLE:
            # 2(3), 2sin(x), 2pi, 2ans
            # Also RPAREN followed by LPAREN, NUMBER, CONSTANT, FUNCTION
            if prev is not None:
                prev_is_val = prev.type in (Token.NUMBER, Token.CONSTANT, Token.VARIABLE, Token.RPAREN)
                curr_is_val_or_fn = curr.type in (Token.NUMBER, Token.CONSTANT, Token.VARIABLE, Token.FUNCTION, Token.LPAREN)
                
                # Check if implicit multiplication should be inserted
                if prev_is_val and curr_is_val_or_fn and not (curr.type == Token.OPERATOR):
                    # Edge case: don't multiply before comma or rparen
                    processed_tokens.append(Token(Token.OPERATOR, '*'))

            processed_tokens.append(curr)

        return processed_tokens

    # -----------------------------------------------------------------------
    # 2. Shunting-Yard Parser (Infix -> RPN)
    # -----------------------------------------------------------------------
    def parse_to_rpn(self, tokens: List[Token]) -> List[Token]:
        """
        Converts infix tokens to Reverse Polish Notation (RPN)
        using Dijkstra's Shunting-yard algorithm.
        """
        output_queue: List[Token] = []
        op_stack: List[Token] = []

        for token in tokens:
            if token.type in (Token.NUMBER, Token.CONSTANT, Token.VARIABLE):
                output_queue.append(token)

            elif token.type == Token.FUNCTION:
                op_stack.append(token)

            elif token.type == Token.COMMA:
                while op_stack and op_stack[-1].type != Token.LPAREN:
                    output_queue.append(op_stack.pop())
                if not op_stack:
                    raise ValueError("Misplaced comma or mismatched parentheses.")

            elif token.type == Token.OPERATOR:
                o1 = token.value
                o1_info = OPERATORS[o1]
                o1_prec = o1_info['prec']
                o1_assoc = o1_info['assoc']

                while op_stack:
                    top = op_stack[-1]
                    if top.type == Token.OPERATOR:
                        o2 = top.value
                        o2_info = OPERATORS[o2]
                        o2_prec = o2_info['prec']

                        if (o1_assoc == 'L' and o1_prec <= o2_prec) or (o1_assoc == 'R' and o1_prec < o2_prec):
                            output_queue.append(op_stack.pop())
                        else:
                            break
                    elif top.type == Token.FUNCTION:
                        output_queue.append(op_stack.pop())
                    else:
                        break
                op_stack.append(token)

            elif token.type == Token.LPAREN:
                op_stack.append(token)

            elif token.type == Token.RPAREN:
                while op_stack and op_stack[-1].type != Token.LPAREN:
                    output_queue.append(op_stack.pop())
                if not op_stack:
                    raise ValueError("Mismatched parentheses: missing '('")
                op_stack.pop()  # Discard the '('

                # If token at top of stack is a function, pop it to output
                if op_stack and op_stack[-1].type == Token.FUNCTION:
                    output_queue.append(op_stack.pop())

        while op_stack:
            top = op_stack.pop()
            if top.type in (Token.LPAREN, Token.RPAREN):
                raise ValueError("Mismatched parentheses.")
            output_queue.append(top)

        return output_queue

    # -----------------------------------------------------------------------
    # 3. RPN Stack Evaluator
    # -----------------------------------------------------------------------
    def evaluate_rpn(self, rpn_tokens: List[Token]) -> float:
        """
        Evaluates an RPN token list using a stack and fundamental math functions.
        """
        stack: List[float] = []

        for token in rpn_tokens:
            if token.type == Token.NUMBER:
                stack.append(token.value)
            elif token.type == Token.CONSTANT:
                stack.append(token.value)
            elif token.type == Token.VARIABLE:
                stack.append(self.variables[token.value])

            elif token.type == Token.OPERATOR:
                op = token.value
                info = OPERATORS[op]

                if info['args'] == 1:
                    if not stack:
                        raise ValueError(f"Insufficient operands for operator '{op}'")
                    val = stack.pop()
                    if op == 'u-':
                        stack.append(-val)
                    elif op == 'u+':
                        stack.append(val)
                elif info['args'] == 2:
                    if len(stack) < 2:
                        raise ValueError(f"Insufficient operands for binary operator '{op}'")
                    b = stack.pop()
                    a = stack.pop()

                    if op == '+':
                        stack.append(a + b)
                    elif op == '-':
                        stack.append(a - b)
                    elif op == '*':
                        stack.append(a * b)
                    elif op == '/':
                        if b == 0.0:
                            raise ZeroDivisionError("Division by zero.")
                        stack.append(a / b)
                    elif op == '%':
                        if b == 0.0:
                            raise ZeroDivisionError("Modulo by zero.")
                        stack.append(a % b)
                    elif op == '^':
                        stack.append(fm.power(a, b))

            elif token.type == Token.FUNCTION:
                fn_name = token.value
                arg_count = FUNCTIONS[fn_name]

                if len(stack) < arg_count:
                    raise ValueError(f"Function '{fn_name}' expects {arg_count} argument(s), got {len(stack)}")

                if arg_count == 1:
                    arg = stack.pop()
                    res = self._execute_unary_func(fn_name, arg)
                    stack.append(res)
                elif arg_count == 2:
                    arg2 = stack.pop()
                    arg1 = stack.pop()
                    res = self._execute_binary_func(fn_name, arg1, arg2)
                    stack.append(res)

        if len(stack) != 1:
            raise ValueError(f"Invalid expression syntax: evaluation ended with {len(stack)} values on stack.")

        return stack[0]

    def _execute_unary_func(self, name: str, x: float) -> float:
        """Executes unary mathematical function respecting current angle mode."""
        is_deg = (self.angle_mode == 'DEG')

        if name == 'sin':
            return fm.sin(x, is_degrees=is_deg)
        elif name == 'cos':
            return fm.cos(x, is_degrees=is_deg)
        elif name == 'tan':
            return fm.tan(x, is_degrees=is_deg)
        elif name == 'asin':
            rad = fm.asin(x)
            return rad * (180.0 / fm.PI) if is_deg else rad
        elif name == 'acos':
            rad = fm.acos(x)
            return rad * (180.0 / fm.PI) if is_deg else rad
        elif name == 'atan':
            rad = fm.atan(x)
            return rad * (180.0 / fm.PI) if is_deg else rad
        elif name == 'sinh':
            return fm.sinh(x)
        elif name == 'cosh':
            return fm.cosh(x)
        elif name == 'tanh':
            return fm.tanh(x)
        elif name == 'sqrt':
            return fm.sqrt(x)
        elif name == 'cbrt':
            return fm.cbrt(x)
        elif name == 'ln':
            return fm.ln(x)
        elif name in ('log', 'log10'):
            return fm.log10(x)
        elif name == 'exp':
            return fm.exp(x)
        elif name == 'abs':
            return fm.abs_val(x)
        elif name == 'fact':
            if x != int(x) or x < 0:
                raise ValueError("Factorial only defined for non-negative integers.")
            return float(fm.factorial(int(x)))
        elif name == 'floor':
            return float(int(x) if x >= 0 or x == int(x) else int(x) - 1)
        elif name == 'ceil':
            return float(int(x) if x <= 0 or x == int(x) else int(x) + 1)
        elif name == 'rad':
            return x * (fm.PI / 180.0)
        elif name == 'deg':
            return x * (180.0 / fm.PI)
        else:
            raise ValueError(f"Unknown unary function: {name}")

    def _execute_binary_func(self, name: str, a: float, b: float) -> float:
        """Executes binary mathematical function."""
        if name == 'npr':
            return float(fm.permutations(int(a), int(b)))
        elif name == 'ncr':
            return float(fm.combinations(int(a), int(b)))
        elif name == 'pow':
            return fm.power(a, b)
        elif name == 'atan2':
            rad = fm.atan2(a, b)
            return rad * (180.0 / fm.PI) if self.angle_mode == 'DEG' else rad
        else:
            raise ValueError(f"Unknown binary function: {name}")

    # -----------------------------------------------------------------------
    # 4. High-Level Evaluation API
    # -----------------------------------------------------------------------
    def calculate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression from raw string to final answer.
        Updates internal `ans` variable and calculation history.
        """
        cleaned = expression.strip()
        if not cleaned:
            raise ValueError("Expression is empty.")

        tokens = self.tokenize(cleaned)
        rpn = self.parse_to_rpn(tokens)
        result = self.evaluate_rpn(rpn)

        # Clean tiny floating point noise (e.g. 1e-16 -> 0.0)
        if abs(result) < 1e-15:
            result = 0.0

        self.variables['ans'] = result
        self.history.append((cleaned, result, self.angle_mode))
        return result
