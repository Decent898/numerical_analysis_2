def update_limits(x, x_min, x_max):
    if x < x_min:
        x_min = x
    if x > x_max:
        x_max = x
    return x_max, x_min

def secant_method(func, x0, x1, tol, max_iter=100):
    x_min=x0
    x_max=x0
    steps = []
    for i in range(max_iter):
        x_max, x_min = update_limits(x0, x_min, x_max)
        x_max, x_min = update_limits(x1, x_min, x_max)
        f0, f1 = func(x0), func(x1)
        if f0 == f1:
            raise ValueError("分母为零")
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        steps.append((x0, x1, f0, f1, x2))
        if abs(x2 - x1) < tol:
            return x2, steps,x_min, x_max
        x0, x1 = x1, x2
    raise ValueError("收敛失败")