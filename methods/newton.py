import numpy as np

def newton_method(func, x0, tol, max_iter=100):
    steps = []
    x = x0
    for i in range(max_iter):
        fx = func(x)
        if abs(fx) < tol:
            return x, steps
        dfx = (func(x + 1e-8) - fx) / 1e-8 
        if dfx == 0:
            raise ValueError("出现导数为零")
        x_new = x - fx / dfx
        steps.append((x, fx, dfx, x_new))
        if abs(x_new - x) < tol:
            return x_new, steps
        x = x_new
    raise ValueError("收敛失败")