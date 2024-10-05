import numpy as np

def newton_method(func, x0, tol, max_iter=100):
    steps = []
    x = x0
    for i in range(max_iter):
        fx = func(x)
        if abs(fx) < tol:
            return x, steps
        dfx = (func(x + 1e-8) - fx) / 1e-8  # Numerical differentiation
        if dfx == 0:
            raise ValueError("Derivative is zero. The method fails.")
        x_new = x - fx / dfx
        steps.append((x, fx, dfx, x_new))
        if abs(x_new - x) < tol:
            return x_new, steps
        x = x_new
    raise ValueError(f"Method failed to converge within {max_iter} iterations.")