"""
Fundamentals Explainer Module
=============================
Provides detailed, educational, step-by-step mathematical breakdowns
of how scientific calculations are performed from basic fundamentals:
- Maclaurin / Taylor Series term-by-term summation for sin, cos, tan, exp, ln
- Newton-Raphson quadratic convergence iterations for sqrt, cbrt
- Angle reductions and symmetries
- Machin-like formulas for Pi
"""

import fundamental_math as fm
from typing import Dict, Any, List

class FundamentalsExplainer:
    @staticmethod
    def explain_sin(x: float, is_degrees: bool = True) -> Dict[str, Any]:
        """Explains calculation of sin(x) from first principles."""
        orig_x = x
        rad = x * (fm.PI / 180.0) if is_degrees else x
        reduced_rad = fm._reduce_angle(rad)

        symmetric_note = ""
        effective_x = reduced_rad
        sign_flip = 1.0

        if effective_x > fm.HALF_PI:
            effective_x = fm.PI - effective_x
            symmetric_note = "Reduced from Quadrant II using sin(pi - x) = sin(x)"
        elif effective_x < -fm.HALF_PI:
            effective_x = -fm.PI - effective_x
            symmetric_note = "Reduced from Quadrant III/IV using sin(-pi - x) = -sin(x)"

        terms_data: List[Dict[str, Any]] = []
        total = 0.0
        term = effective_x
        x2 = effective_x * effective_x

        for n in range(10):
            total += term
            k = 2 * n + 1
            terms_data.append({
                'n': n,
                'formula': f"(-1)^{n} * x^{k} / {k}!",
                'term_value': term,
                'cumulative_sum': total
            })
            if fm.abs_val(term) < 1e-16:
                break
            term = -term * x2 / ((k + 1) * (k + 2))

        return {
            'function': 'sin',
            'input': orig_x,
            'unit': 'degrees' if is_degrees else 'radians',
            'radians': rad,
            'reduced_radians': effective_x,
            'symmetry_note': symmetric_note,
            'method': 'Maclaurin / Taylor Series: sin(x) = sum_{n=0}^{inf} (-1)^n * x^(2n+1) / (2n+1)!',
            'terms': terms_data,
            'result': total
        }

    @staticmethod
    def explain_cos(x: float, is_degrees: bool = True) -> Dict[str, Any]:
        """Explains calculation of cos(x) from first principles."""
        orig_x = x
        rad = x * (fm.PI / 180.0) if is_degrees else x
        reduced_rad = fm._reduce_angle(rad)

        symmetric_note = ""
        effective_x = reduced_rad
        sign_mult = 1.0

        if effective_x > fm.HALF_PI:
            effective_x = fm.PI - effective_x
            sign_mult = -1.0
            symmetric_note = "Using cos(pi - x) = -cos(x)"
        elif effective_x < -fm.HALF_PI:
            effective_x = -fm.PI - effective_x
            sign_mult = -1.0
            symmetric_note = "Using cos(-pi - x) = -cos(x)"

        terms_data: List[Dict[str, Any]] = []
        total = 0.0
        term = 1.0
        x2 = effective_x * effective_x

        for n in range(10):
            total += term
            k = 2 * n
            terms_data.append({
                'n': n,
                'formula': f"(-1)^{n} * x^{k} / {k}!",
                'term_value': term * sign_mult,
                'cumulative_sum': total * sign_mult
            })
            if fm.abs_val(term) < 1e-16:
                break
            term = -term * x2 / ((k + 1) * (k + 2))

        return {
            'function': 'cos',
            'input': orig_x,
            'unit': 'degrees' if is_degrees else 'radians',
            'radians': rad,
            'reduced_radians': effective_x,
            'symmetry_note': symmetric_note,
            'method': 'Maclaurin / Taylor Series: cos(x) = sum_{n=0}^{inf} (-1)^n * x^(2n) / (2n)!',
            'terms': terms_data,
            'result': total * sign_mult
        }

    @staticmethod
    def explain_tan(x: float, is_degrees: bool = True) -> Dict[str, Any]:
        """Explains calculation of tan(x) from fundamental identity tan(x) = sin(x)/cos(x)."""
        s_info = FundamentalsExplainer.explain_sin(x, is_degrees)
        c_info = FundamentalsExplainer.explain_cos(x, is_degrees)
        s_val = s_info['result']
        c_val = c_info['result']

        if fm.abs_val(c_val) < 1e-15:
            res_str = "Undefined (asymptote, cos(x) = 0)"
            res_val = None
        else:
            res_val = s_val / c_val
            res_str = str(res_val)

        return {
            'function': 'tan',
            'input': x,
            'unit': 'degrees' if is_degrees else 'radians',
            'sin_value': s_val,
            'cos_value': c_val,
            'method': 'Fundamental Trigonometric Identity: tan(x) = sin(x) / cos(x)',
            'sin_breakdown': s_info,
            'cos_breakdown': c_info,
            'result': res_val,
            'result_display': res_str
        }

    @staticmethod
    def explain_sqrt(x: float) -> Dict[str, Any]:
        """Explains calculation of sqrt(x) via Newton-Raphson iteration."""
        if x < 0:
            raise ValueError("Square root not defined for negative numbers in real domain.")
        if x == 0:
            return {'function': 'sqrt', 'input': 0, 'result': 0.0, 'iterations': []}

        guess = x if x < 1.0 else x * 0.5
        if guess == 0.0:
            guess = 1e-8

        iterations = []
        for i in range(12):
            next_guess = 0.5 * (guess + x / guess)
            error = fm.abs_val(next_guess * next_guess - x)
            iterations.append({
                'iteration': i + 1,
                'guess': guess,
                'next_guess': next_guess,
                'error': error
            })
            if fm.abs_val(next_guess - guess) <= 1e-15 * fm.abs_val(guess):
                break
            guess = next_guess

        return {
            'function': 'sqrt',
            'input': x,
            'method': 'Newton-Raphson Method for f(y) = y^2 - x = 0:  y_{k+1} = 0.5 * (y_k + x / y_k)',
            'iterations': iterations,
            'result': guess
        }

    @staticmethod
    def explain_ln(x: float) -> Dict[str, Any]:
        """Explains natural logarithm via argument reduction & rapid area-hyperbolic series."""
        if x <= 0:
            raise ValueError("ln(x) requires x > 0")

        k = 0
        m = x
        while m > 1.0:
            m /= 2.0
            k += 1
        while m < 0.5:
            m *= 2.0
            k -= 1

        y = (m - 1.0) / (m + 1.0)
        y2 = y * y
        y_power = y
        series_sum = 0.0
        terms = []

        for n in range(10):
            denom = 2 * n + 1
            term = y_power / denom
            series_sum += term
            terms.append({
                'n': n,
                'term': term,
                'cumulative_sum': series_sum
            })
            y_power *= y2
            if fm.abs_val(term) < 1e-16:
                break

        ln_m = 2.0 * series_sum
        final_ln = k * fm.LN2 + ln_m

        return {
            'function': 'ln',
            'input': x,
            'argument_reduction': f"x = {m:.8f} * 2^({k}) => ln(x) = {k}*ln(2) + ln(m)",
            'y_value': y,
            'method': 'Rapid Area-Hyperbolic Series: ln((1+y)/(1-y)) = 2 * sum_{n=0}^{inf} y^(2n+1) / (2n+1)',
            'terms': terms,
            'ln_m': ln_m,
            'result': final_ln
        }


def format_explanation_cli(info: Dict[str, Any]) -> str:
    """Formats an explanation dictionary into a terminal-friendly ASCII report."""
    lines = []
    fn = info.get('function')
    lines.append("=" * 65)
    lines.append(f"  FUNDAMENTALS EXPLANATION: {fn.upper()} CALCULATOR")
    lines.append("=" * 65)
    lines.append(f"Input:    {info.get('input')} {info.get('unit', '')}")
    lines.append(f"Method:   {info.get('method')}")

    if 'radians' in info:
        lines.append(f"Radians:  {info['radians']:.10f}")
    if 'reduced_radians' in info:
        lines.append(f"Reduced:  {info['reduced_radians']:.10f} rad")
    if info.get('symmetry_note'):
        lines.append(f"Symmetry: {info['symmetry_note']}")

    if 'terms' in info:
        lines.append("\nTaylor / Maclaurin Series Convergence Steps:")
        lines.append("-" * 65)
        lines.append(f"{'Term (n)':<10} | {'Term Value':<24} | {'Cumulative Sum':<24}")
        lines.append("-" * 65)
        for t in info['terms']:
            n = t['n']
            tv = t.get('term_value', t.get('term', 0.0))
            cs = t['cumulative_sum']
            lines.append(f"n = {n:<6} | {tv:+22.15f} | {cs:+22.15f}")

    if 'iterations' in info:
        lines.append("\nNewton-Raphson Iterative Convergence Steps:")
        lines.append("-" * 65)
        lines.append(f"{'Iter':<6} | {'Current Guess':<24} | {'Error |y^2 - x|':<24}")
        lines.append("-" * 65)
        for it in info['iterations']:
            lines.append(f"{it['iteration']:<6} | {it['next_guess']:<24.15f} | {it['error']:<24.4e}")

    if 'sin_value' in info and 'cos_value' in info:
        lines.append(f"\nsin({info['input']}) = {info['sin_value']:.15f}")
        lines.append(f"cos({info['input']}) = {info['cos_value']:.15f}")
        lines.append(f"tan({info['input']}) = sin / cos = {info['result_display']}")

    lines.append("-" * 65)
    lines.append(f"FINAL RESULT: {info.get('result', info.get('result_display'))}")
    lines.append("=" * 65)
    return "\n".join(lines)
