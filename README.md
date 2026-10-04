# Scientific Calculator (Engineered from First Principles)

A precision scientific calculator built from **basic mathematical fundamentals**, completely from scratch. It avoids relying on pre-baked trigonometric library wrappers or lookup tables, computing every operation from core mathematical definitions.

---

## 🧮 Mathematical Fundamentals & Algorithms

### 1. Trigonometric Functions (`sin`, `cos`, `tan`)
- **Sine $\sin(x)$**:
  Computed using the Maclaurin / Taylor polynomial series:
  $$\sin(x) = \sum_{n=0}^{\infty} (-1)^n \frac{x^{2n+1}}{(2n+1)!} = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \frac{x^7}{7!} + \dots$$
- **Cosine $\cos(x)$**:
  $$\cos(x) = \sum_{n=0}^{\infty} (-1)^n \frac{x^{2n}}{(2n)!} = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \frac{x^6}{6!} + \dots$$
- **Tangent $\tan(x)$**:
  Computed from the fundamental quotient definition $\tan(x) = \frac{\sin(x)}{\cos(x)}$ with asymptote/pole detection whenever $\cos(x) \approx 0$ (e.g. at $90^\circ$).
- **Range & Periodicity Reduction**:
  To ensure rapid and stable convergence, angles are reduced modulo $2\pi$ into $[-\pi, \pi]$ and quadrant symmetries are applied ($\sin(\pi - x) = \sin(x)$, $\cos(\pi - x) = -\cos(x)$) so the Taylor series operates on $|x| \le \frac{\pi}{2}$.

### 2. Fundamental Constants
- **$\pi$ (Pi)**:
  Computed using John Machin's rapid arctangent formula (1706):
  $$\pi = 16 \arctan\left(\frac{1}{5}\right) - 4 \arctan\left(\frac{1}{239}\right)$$
  where $\arctan(x)$ is computed via its Taylor series $\sum_{n=0}^\infty (-1)^n \frac{x^{2n+1}}{2n+1}$.
- **$e$ (Euler's Number)**:
  Computed via the Maclaurin series:
  $$e = \sum_{n=0}^{\infty} \frac{1}{n!} = 1 + 1 + \frac{1}{2!} + \frac{1}{3!} + \dots$$

### 3. Roots via Newton-Raphson Method
- **Square Root $\sqrt{S}$**:
  Solves $f(x) = x^2 - S = 0$ using Newton-Raphson quadratic iterations:
  $$x_{k+1} = \frac{1}{2}\left(x_k + \frac{S}{x_k}\right)$$
  Doubles the number of accurate decimal places with each step.
- **Cube Root $\sqrt[3]{S}$**:
  $$x_{k+1} = \frac{1}{3}\left(2 x_k + \frac{S}{x_k^2}\right)$$

### 4. Logarithm & Exponential Functions
- **Natural Log $\ln(x)$**:
  Argument reduction decomposing $x = m \cdot 2^k$ with $m \in [0.5, 1.0]$, then applying the rapid area-hyperbolic series for $y = \frac{m-1}{m+1}$:
  $$\ln(m) = 2 \sum_{n=0}^{\infty} \frac{y^{2n+1}}{2n+1}, \quad \ln(x) = k \ln(2) + \ln(m)$$
- **Exponential $e^x$**:
  Decomposing $x = k \ln(2) + r$ such that $|r| \le \frac{1}{2}\ln(2)$, computing $e^r = \sum_{n=0}^\infty \frac{r^n}{n!}$, and scaling by $2^k$.
- **Powers $x^y$**:
  Computed via $x^y = e^{y \ln(x)}$ for real exponents, and binary exponentiation (repeated squaring) for integers.

### 5. Expression Tokenizer & Dijkstra's Shunting-Yard Parser
- Parses arbitrary infix expressions with full operator precedence:
  - Parentheses: `(` and `)`
  - Exponentiation: `^` (right-associative)
  - Unary minus and plus: `-x`, `+x`
  - Multiplication, division, modulo: `*`, `/`, `%`
  - Addition and subtraction: `+`, `-`
  - Implicit multiplication: `2pi`, `2(3+4)`, `3sin(30)`
- Converts tokens to Reverse Polish Notation (RPN) and evaluates via a stack.

---

## 🚀 Usage

### 1. Interactive CLI (REPL)
Launch the interactive terminal calculator:
```bash
python3 scientific_calculator.py
```
Inside the REPL:
```text
calc [DEG]> sin(30) + cos(60)
= 1

calc [DEG]> sqrt(16) * tan(45)
= 4

calc [DEG]> 2pi
= 6.28318530718

calc [DEG]> mode rad
Angle mode switched to RADIANS.

calc [RAD]> sin(pi/2)
= 1
```

### 2. Direct Expression Evaluation
```bash
python3 scientific_calculator.py "sin(30) + cos(60)"
python3 scientific_calculator.py "sin(pi/4)" --rad
```

### 3. Step-by-Step Fundamentals Explanation
To inspect the underlying Taylor series expansion or Newton-Raphson iteration table:
```bash
python3 scientific_calculator.py --explain "sin(45)"
python3 scientific_calculator.py --explain "sqrt(2)"
python3 scientific_calculator.py --explain "tan(45)"
```

### 4. Interactive Web Application
Open [`index.html`](file:///Users/vaibhav/Antigravity/index.html) directly in any web browser (Safari, Chrome, Firefox, Edge):
```bash
open index.html
```
Features of the web UI:
- Full scientific keyboard (`sin`, `cos`, `tan`, `sin⁻¹`, `cos⁻¹`, `tan⁻¹`, `sinh`, `cosh`, `tanh`, `ln`, `log`, `√x`, `∛x`, `xʸ`, `π`, `e`, etc.).
- `DEG` / `RAD` angle mode switch.
- **Fundamentals Inspector**: Automatically shows the exact Taylor series convergence table or Newton-Raphson iteration breakdown for whatever function you calculate!
- Full computer keyboard support (type numbers and operators directly, `Enter` to calculate).

---

## 🧪 Running Tests

A comprehensive unit test suite validates accuracy against standard reference benchmarks across all mathematical domains:
```bash
python3 -m unittest test_calculator.py
```
All 13 tests execute in ~1ms with machine-precision accuracy ($10^{-12}$ to $10^{-16}$).
