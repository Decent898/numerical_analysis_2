import math

def f(x, expr):
    try:
        safe_dict = {
            "x": x,
            "abs": abs,
            "max": max,
            "min": min,
            "pow": pow,
            "round": round,
            "e": math.e,
            "pi": math.pi,
            "exp": math.exp,
            "log": math.log,
            "log10": math.log10,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "asin": math.asin,
            "acos": math.acos,
            "atan": math.atan,
            "sinh": math.sinh,
            "cosh": math.cosh,
            "tanh": math.tanh,
            "sqrt": math.sqrt,
        }
        result = eval(expr, {"__builtins__": {}}, safe_dict)
        return float(result)
    except Exception as e:
        raise ValueError(f"Unable to evaluate expression at x = {x}: {e}")