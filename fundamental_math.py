"""
Fundamental Math Library - Built from First Principles
======================================================
This module implements scientific mathematical functions and constants
from fundamental mathematical concepts:
- Taylor / Maclaurin series expansions
- Newton-Raphson iterative root finding
- Argument and range reductions using periodicity and symmetry
- Binary exponentiation and series summation

No imports from the `math` library for core calculations!
"""

# ---------------------------------------------------------------------------
# 1. Fundamental Constants Computed from First Principles
# ---------------------------------------------------------------------------

def compute_pi(terms: int = 30) -> float:
    """
    Computes PI using John Machin's formula (1706):
        pi / 4 = 4 * arctan(1/5) - arctan(1/239)
        pi = 16 * arctan(1/5) - 4 * arctan(1/239)

    Using the Taylor series for arctan(x) = sum_{n=0}^{inf} (-1)^n * x^(2n+1) / (2n+1)
    Because 1/5 and 1/239 are small, this series converges extremely rapidly.
    """
    def _arctan_series(x: float, max_terms: int) -> float:
        x2 = x * x
        x_power = x
        total = 0.0
        sign = 1.0
        for n in range(max_terms):
            denom = 2 * n + 1
            term = sign * (x_power / denom)
            total += term
            x_power *= x2
            sign = -sign
            if abs(term) < 1e-17:
                break
        return total

    return 16.0 * _arctan_series(1.0 / 5.0, terms) - 4.0 * _arctan_series(1.0 / 239.0, terms)


def compute_e(terms: int = 35) -> float:
    """
    Computes Euler's number (e) using its Maclaurin series:
        e = sum_{n=0}^{inf} 1 / n!
          = 1 + 1/1 + 1/2! + 1/3! + 1/4! + ...
    """
    total = 1.0
    term = 1.0
    for n in range(1, terms):
        term /= n
        total += term
        if term < 1e-17:
            break
    return total


def compute_ln2(terms: int = 30) -> float:
    """
    Computes ln(2) using the rapid area-hyperbolic series:
        ln((1+y)/(1-y)) = 2 * sum_{k=0}^{inf} y^(2k+1) / (2k+1)
    Setting (1+y)/(1-y) = 2 => y = 1/3.
    """
    y = 1.0 / 3.0
    y2 = y * y
    y_power = y
    total = 0.0
    for k in range(terms):
        denom = 2 * k + 1
        term = y_power / denom
        total += term
        y_power *= y2
        if term < 1e-17:
            break
    return 2.0 * total


# Precomputed fundamental constants (using first-principles computation)
PI = compute_pi(35)
TWO_PI = 2.0 * PI
HALF_PI = PI / 2.0
E = compute_e(35)
LN2 = compute_ln2(35)
LN10 = 0.0  # Will be defined after natural log


# ---------------------------------------------------------------------------
# 2. Arithmetic & Basic Functions
# ---------------------------------------------------------------------------

def abs_val(x: float) -> float:
    """Absolute value: |x|."""
    return -x if x < 0 else x


def factorial(n: int) -> int:
    """
    Factorial n! = 1 * 2 * ... * n for non-negative integers.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("Factorial is only defined for non-negative integers.")
    if n > 170:
        raise OverflowError("Factorial result exceeds standard floating point range.")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def int_power(base: float, exp: int) -> float:
    """
    Exponentiation by squaring (binary exponentiation) for integer exponents.
    O(log |exp|) complexity.
    """
    if exp == 0:
        return 1.0
    if base == 0.0:
        if exp < 0:
            raise ZeroDivisionError("0 cannot be raised to a negative power.")
        return 0.0

    negative = exp < 0
    exp = abs(exp)
    result = 1.0
    current = base
    while exp > 0:
        if exp % 2 == 1:
            result *= current
        current *= current
        exp //= 2

    return 1.0 / result if negative else result


# ---------------------------------------------------------------------------
# 3. Square Root and Roots via Newton-Raphson Method
# ---------------------------------------------------------------------------

def sqrt(x: float, tolerance: float = 1e-15, max_iter: int = 100) -> float:
    """
    Computes sqrt(x) using the Newton-Raphson iteration:
        x_{n+1} = 0.5 * (x_n + S / x_n)
    Root of f(y) = y^2 - x = 0.
    """
    if x < 0:
        raise ValueError("Cannot calculate square root of a negative number in real domain.")
    if x == 0.0:
        return 0.0
    if x == 1.0:
        return 1.0

    # Initial guess heuristic based on order of magnitude
    guess = x if x < 1.0 else x * 0.5
    if guess == 0.0:
        guess = 1e-8

    for _ in range(max_iter):
        next_guess = 0.5 * (guess + x / guess)
        if abs_val(next_guess - guess) <= tolerance * abs_val(guess):
            return next_guess
        guess = next_guess

    return guess


def cbrt(x: float, tolerance: float = 1e-15, max_iter: int = 100) -> float:
    """
    Computes cube root of x using Newton-Raphson:
        y_{n+1} = (2 * y_n + x / y_n^2) / 3
    """
    if x == 0.0:
        return 0.0

    neg = x < 0
    val = -x if neg else x
    guess = val * 0.5 if val > 1.0 else 1.0

    for _ in range(max_iter):
        next_guess = (2.0 * guess + val / (guess * guess)) / 3.0
        if abs_val(next_guess - guess) <= tolerance * abs_val(guess):
            return -next_guess if neg else next_guess
        guess = next_guess

    return -guess if neg else guess


def nth_root(x: float, n: int, tolerance: float = 1e-15, max_iter: int = 100) -> float:
    """
    Computes n-th root of x using Newton-Raphson:
        y_{k+1} = ((n - 1) * y_k + x / y_k^(n - 1)) / n
    """
    if n <= 0:
        raise ValueError("Root degree n must be a positive integer.")
    if x == 0.0:
        return 0.0
    if x < 0:
        if n % 2 == 0:
            raise ValueError("Even root of negative number is not real.")
        return -nth_root(-x, n, tolerance, max_iter)

    guess = x / n if x > 1.0 else 1.0
    for _ in range(max_iter):
        next_guess = ((n - 1) * guess + x / int_power(guess, n - 1)) / float(n)
        if abs_val(next_guess - guess) <= tolerance * abs_val(guess):
            return next_guess
        guess = next_guess

    return guess


# ---------------------------------------------------------------------------
# 4. Exponential and Logarithmic Functions
# ---------------------------------------------------------------------------

def exp(x: float, tolerance: float = 1e-16, max_terms: int = 100) -> float:
    """
    Computes e^x using argument reduction and Taylor series:
        e^x = (e^(x / 2^k))^(2^k)
    where k is chosen such that |x / 2^k| < 0.5.
    Then the Taylor series:
        e^u = 1 + u + u^2/2! + u^3/3! + ...
    converges with fewer than 15 terms.
    """
    if x == 0.0:
        return 1.0
    if x > 709.78:
        raise OverflowError("exp(x) overflow: input too large.")
    if x < -708.39:
        return 0.0

    # Argument reduction: x = k * ln(2) + r
    # where k = round(x / ln(2)) so that |r| <= 0.5 * ln(2) approx 0.34657
    k = int(x / LN2 + 0.5) if x >= 0 else int(x / LN2 - 0.5)
    r = x - k * LN2

    # Taylor series for e^r
    total = 1.0
    term = 1.0
    for n in range(1, max_terms):
        term = term * r / n
        total += term
        if abs_val(term) < tolerance:
            break

    # e^x = 2^k * e^r
    # Multiply by 2^k with exact binary scaling
    if k >= 0:
        mult = float(1 << k) if k < 1000 else int_power(2.0, k)
    else:
        mult = 1.0 / float(1 << (-k)) if -k < 1000 else int_power(2.0, k)

    return total * mult


def ln(x: float, tolerance: float = 1e-16, max_terms: int = 100) -> float:
    """
    Computes natural logarithm ln(x) for x > 0.
    Algorithm:
      1. Argument reduction:
         Decompose x into x = m * 2^k such that m in [0.5, 1.0].
         Then ln(x) = k * ln(2) + ln(m).
      2. Fast series for ln(m):
         Let y = (m - 1) / (m + 1), so m = (1 + y) / (1 - y).
         Then ln(m) = 2 * sum_{n=0}^{inf} y^(2n+1) / (2n+1).
    """
    if x <= 0:
        raise ValueError("Natural logarithm is only defined for positive numbers (x > 0).")
    if x == 1.0:
        return 0.0

    # Step 1: Argument reduction to [0.5, 1.0]
    k = 0
    m = x
    while m > 1.0:
        m /= 2.0
        k += 1
    while m < 0.5:
        m *= 2.0
        k -= 1

    # Step 2: Series computation
    y = (m - 1.0) / (m + 1.0)
    y2 = y * y
    y_power = y
    series_sum = 0.0

    for n in range(max_terms):
        denom = 2 * n + 1
        term = y_power / denom
        series_sum += term
        y_power *= y2
        if abs_val(term) < tolerance:
            break

    ln_m = 2.0 * series_sum
    return k * LN2 + ln_m


# Now compute ln(10) accurately
LN10 = ln(10.0)


def log10(x: float) -> float:
    """Common logarithm log_10(x) = ln(x) / ln(10)."""
    return ln(x) / LN10


def log_base(x: float, base: float) -> float:
    """Logarithm to arbitrary base: log_b(x) = ln(x) / ln(b)."""
    if base <= 0 or base == 1.0:
        raise ValueError("Logarithm base must be positive and not equal to 1.")
    return ln(x) / ln(base)


def power(base: float, exponent: float) -> float:
    """
    Computes base^exponent from fundamentals:
    - If exponent is integer: uses binary exponentiation.
    - If base > 0: uses identity base^exp = exp(exponent * ln(base)).
    - If base < 0 and exponent is an integer: computes with appropriate sign.
    """
    # Check if exponent is an integer
    if int_power_check := (exponent == int(exponent)):
        int_exp = int(exponent)
        return int_power(base, int_exp)

    if base == 0.0:
        if exponent < 0:
            raise ZeroDivisionError("0 cannot be raised to negative power.")
        return 0.0

    if base < 0:
        raise ValueError("Negative base with non-integer exponent produces a complex number.")

    return exp(exponent * ln(base))


# ---------------------------------------------------------------------------
# 5. Trigonometric Functions via Taylor / Maclaurin Series
# ---------------------------------------------------------------------------

def _reduce_angle(rad: float) -> tuple[float, int]:
    """
    Reduces an angle in radians to [-PI, PI], and returns (reduced_rad, sign_flip).
    Uses the periodicity:
        sin(x + 2*k*pi) = sin(x)
        cos(x + 2*k*pi) = cos(x)
    """
    # Bring into [-PI, PI]
    # mod with 2*PI
    rem = rad % TWO_PI
    if rem > PI:
        rem -= TWO_PI
    elif rem < -PI:
        rem += TWO_PI
    return rem


def sin(x: float, is_degrees: bool = False, tolerance: float = 1e-16, max_terms: int = 50) -> float:
    """
    Computes sine of x using its Maclaurin series:
        sin(x) = sum_{n=0}^{inf} (-1)^n * x^(2n+1) / (2n+1)!
               = x - x^3/3! + x^5/5! - x^7/7! + ...

    Angles are reduced to [-pi, pi] first to guarantee rapid convergence.
    """
    rad = x * (PI / 180.0) if is_degrees else x
    rad = _reduce_angle(rad)

    # Edge cases for exact symmetry points
    if abs_val(rad) < 1e-16:
        return 0.0
    if abs_val(rad - PI) < 1e-15 or abs_val(rad + PI) < 1e-15:
        return 0.0
    if abs_val(rad - HALF_PI) < 1e-15:
        return 1.0
    if abs_val(rad + HALF_PI) < 1e-15:
        return -1.0

    # Further reduce to [-pi/2, pi/2] using sin(pi - x) = sin(x)
    if rad > HALF_PI:
        rad = PI - rad
    elif rad < -HALF_PI:
        rad = -PI - rad

    total = 0.0
    term = rad
    rad2 = rad * rad

    for n in range(max_terms):
        total += term
        # Next term = -term * rad^2 / ((2n+2) * (2n+3))
        k = 2 * n + 1
        term = -term * rad2 / ((k + 1) * (k + 2))
        if abs_val(term) < tolerance:
            break

    return total


def cos(x: float, is_degrees: bool = False, tolerance: float = 1e-16, max_terms: int = 50) -> float:
    """
    Computes cosine of x using its Maclaurin series:
        cos(x) = sum_{n=0}^{inf} (-1)^n * x^(2n) / (2n)!
               = 1 - x^2/2! + x^4/4! - x^6/6! + ...

    Angles are reduced to [-pi, pi] first to guarantee rapid convergence.
    """
    rad = x * (PI / 180.0) if is_degrees else x
    rad = _reduce_angle(rad)

    # Exact points
    if abs_val(rad) < 1e-16:
        return 1.0
    if abs_val(rad - PI) < 1e-15 or abs_val(rad + PI) < 1e-15:
        return -1.0
    if abs_val(rad - HALF_PI) < 1e-15 or abs_val(rad + HALF_PI) < 1e-15:
        return 0.0

    # Reduce to [-pi/2, pi/2] using cos(pi - x) = -cos(x)
    sign = 1.0
    if rad > HALF_PI:
        rad = PI - rad
        sign = -1.0
    elif rad < -HALF_PI:
        rad = -PI - rad
        sign = -1.0

    total = 0.0
    term = 1.0
    rad2 = rad * rad

    for n in range(max_terms):
        total += term
        # Next term = -term * rad^2 / ((2n+1) * (2n+2))
        k = 2 * n
        term = -term * rad2 / ((k + 1) * (k + 2))
        if abs_val(term) < tolerance:
            break

    return sign * total


def tan(x: float, is_degrees: bool = False) -> float:
    """
    Computes tangent of x:
        tan(x) = sin(x) / cos(x)
    Detects singularities where cos(x) == 0 (odd multiples of pi/2).
    """
    c = cos(x, is_degrees=is_degrees)
    if abs_val(c) < 1e-15:
        deg_str = f"{x} deg" if is_degrees else f"{x} rad"
        raise ZeroDivisionError(f"tan({deg_str}) is undefined (asymptote / pole).")
    s = sin(x, is_degrees=is_degrees)
    return s / c


# ---------------------------------------------------------------------------
# 6. Inverse Trigonometric Functions
# ---------------------------------------------------------------------------

def atan(x: float, tolerance: float = 1e-16, max_terms: int = 100) -> float:
    """
    Computes arctangent atan(x) in radians.
    Fundamentals:
      If |x| <= 1:
        arctan(x) = sum_{n=0}^{inf} (-1)^n * x^(2n+1) / (2n+1)
      If |x| > 1:
        arctan(x) = sign(x) * (pi / 2) - arctan(1 / x)
      To accelerate convergence near 1:
        arctan(x) = 2 * arctan(x / (1 + sqrt(1 + x^2)))  (half-angle formula)
    """
    if x == 0.0:
        return 0.0

    # Range reduction for |x| > 1
    if abs_val(x) > 1.0:
        sign = 1.0 if x > 0 else -1.0
        return sign * HALF_PI - atan(1.0 / x, tolerance, max_terms)

    # For |x| > 0.5, apply half-angle argument reduction:
    # arctan(x) = 2 * arctan(x / (1 + sqrt(1 + x^2)))
    if abs_val(x) > 0.5:
        reduced_x = x / (1.0 + sqrt(1.0 + x * x))
        return 2.0 * atan(reduced_x, tolerance, max_terms)

    # Direct Taylor series for small x (|x| <= 0.5)
    total = 0.0
    x2 = x * x
    x_pow = x
    sign = 1.0
    for n in range(max_terms):
        term = sign * x_pow / (2 * n + 1)
        total += term
        x_pow *= x2
        sign = -sign
        if abs_val(term) < tolerance:
            break

    return total


def asin(x: float) -> float:
    """
    Computes arcsine asin(x) in radians for x in [-1, 1].
    Fundamental identity:
        asin(x) = atan(x / sqrt(1 - x^2))
    """
    if x < -1.0 or x > 1.0:
        raise ValueError(f"asin(x) domain is [-1, 1], got {x}")
    if x == 1.0:
        return HALF_PI
    if x == -1.0:
        return -HALF_PI
    if x == 0.0:
        return 0.0

    return atan(x / sqrt(1.0 - x * x))


def acos(x: float) -> float:
    """
    Computes arccosine acos(x) in radians for x in [-1, 1].
    Fundamental identity:
        acos(x) = pi / 2 - asin(x)
    """
    if x < -1.0 or x > 1.0:
        raise ValueError(f"acos(x) domain is [-1, 1], got {x}")
    return HALF_PI - asin(x)


def atan2(y: float, x: float) -> float:
    """
    Computes atan2(y, x), quadrant-aware arc tangent.
    """
    if x > 0:
        return atan(y / x)
    elif x < 0 and y >= 0:
        return atan(y / x) + PI
    elif x < 0 and y < 0:
        return atan(y / x) - PI
    elif x == 0 and y > 0:
        return HALF_PI
    elif x == 0 and y < 0:
        return -HALF_PI
    else:
        return 0.0


# ---------------------------------------------------------------------------
# 7. Hyperbolic Functions
# ---------------------------------------------------------------------------

def sinh(x: float) -> float:
    """Hyperbolic sine: sinh(x) = (e^x - e^(-x)) / 2."""
    if abs_val(x) < 1e-4:
        # Taylor series near zero to avoid catastrophic cancellation: x + x^3/6
        return x + (x * x * x) / 6.0
    ep = exp(x)
    return (ep - 1.0 / ep) / 2.0


def cosh(x: float) -> float:
    """Hyperbolic cosine: cosh(x) = (e^x + e^(-x)) / 2."""
    ep = exp(x)
    return (ep + 1.0 / ep) / 2.0


def tanh(x: float) -> float:
    """Hyperbolic tangent: tanh(x) = sinh(x) / cosh(x) = (e^(2x) - 1) / (e^(2x) + 1)."""
    if x > 20.0:
        return 1.0
    if x < -20.0:
        return -1.0
    e2x = exp(2.0 * x)
    return (e2x - 1.0) / (e2x + 1.0)


# ---------------------------------------------------------------------------
# 8. Combinatorics
# ---------------------------------------------------------------------------

def permutations(n: int, r: int) -> int:
    """nPr = n! / (n - r)!"""
    if r < 0 or r > n:
        return 0
    result = 1
    for i in range(n - r + 1, n + 1):
        result *= i
    return result


def combinations(n: int, r: int) -> int:
    """nCr = n! / (r! * (n - r)!)"""
    if r < 0 or r > n:
        return 0
    if r == 0 or r == n:
        return 1
    r = min(r, n - r)  # Symmetry: nCr = nC(n-r)
    numerator = 1
    denominator = 1
    for i in range(1, r + 1):
        numerator *= (n - i + 1)
        denominator *= i
    return numerator // denominator
