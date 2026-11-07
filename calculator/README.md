# Calculator

A small command-line calculator for evaluating arithmetic expressions. Results are printed as formatted JSON.

## Requirements

- Python 3.10 or newer
- No third-party packages required

## Usage

Pass an expression as a quoted argument. **Separate every number and operator with whitespace**:

```sh
python main.py "3 + 5"
```

Output:

```json
{
  "expression": "3 + 5",
  "result": 8
}
```

The calculator supports addition (`+`), subtraction (`-`), multiplication (`*`), division (`/`), and exponentiation (`^`). Standard precedence applies: exponentiation first, then multiplication/division, then addition/subtraction. Operators of equal precedence are evaluated left to right, except exponentiation, which is right-associative.

Examples:

```sh
python main.py "3 + 7 * 2"   # result: 17
python main.py "2 ^ 3"       # result: 8
python main.py "2 ^ 3 ^ 2"   # result: 512 (2 ^ (3 ^ 2))
python main.py "10 / 4"      # result: 2.5
```

Only binary operations are supported, and the current parser does not support parentheses or unary operators. For example, use `2 - 3` rather than `- 1`.

Invalid expressions produce an error message. Running without an expression displays the usage hint.

## Use from Python

```python
from pkg.calculator import Calculator

calculator = Calculator()
print(calculator.evaluate("2 ^ 3"))  # 8.0
```

`evaluate` returns a number, or `None` for an empty/whitespace-only expression. Invalid tokens or malformed expressions raise `ValueError`.

## Tests

Run the test suite from the project directory:

```sh
python -m unittest
```
