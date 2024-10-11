import numpy as np
def update_limits(x, x_min, x_max):
    if x < x_min:
        x_min = x
    if x > x_max:
        x_max = x
    return x_max, x_min

def newton_method(func, x0, tol, max_iter=100):
    x_min = x0
    x_max = x0
    steps = []
    x = x0
    for i in range(max_iter):
        x_max, x_min = update_limits(x, x_min, x_max)
        fx = func(x)
        dfx = (func(x + 1e-8) - fx) / 1e-8 
        if dfx == 0:
            raise ValueError("出现导数为零")
        x_new = x - fx / dfx
        steps.append((x, fx, dfx, x_new))
        if abs(x_new - x) < tol:
            return x_new, steps,x_min, x_max
        x = x_new
    raise ValueError("收敛失败")