def secant_method(func, x0, x1, tol, max_iter=100):
    steps = []
    for i in range(max_iter):
        f0, f1 = func(x0), func(x1)
        if abs(f1) < tol:
            return x1, steps
        if f0 == f1:
            raise ValueError("Division by zero in secant method.")
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        steps.append((x0, x1, f0, f1, x2))
        if abs(x2 - x1) < tol:
            return x2, steps
        x0, x1 = x1, x2
    raise ValueError(f"Method failed to converge within {max_iter} iterations.")