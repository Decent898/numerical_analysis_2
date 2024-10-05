def aitken_method(func, x0, tol, max_iter=100):
    steps = []
    for i in range(max_iter):
        x1 = func(x0)
        x2 = func(x1)
        denominator = x2 - 2*x1 + x0
        if abs(denominator) < 1e-10:
            return x2, steps
        x_new = x0 - (x1 - x0)**2 / denominator
        steps.append((x0, x1, x2, x_new))
        if abs(x_new - x0) < tol:
            return x_new, steps
        x0 = x_new
    raise ValueError(f"Method failed to converge within {max_iter} iterations.")