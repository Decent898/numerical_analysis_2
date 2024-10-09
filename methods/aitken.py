import math

def get_decimal_places(tol):
    decimal_places = max(0, -int(math.log10(tol))) + 2
    return decimal_places

def aitken_method(func, x0, tol, max_iter=100):
    steps = []

    decimal_places = get_decimal_places(tol)
    
    for i in range(max_iter):
        x1 = func(x0)
        x2 = func(x1)
        
        x1 = round(x1, decimal_places)
        x2 = round(x2, decimal_places)
        
        denominator = x2 - 2 * x1 + x0
        denominator = round(denominator, decimal_places)
        
        if abs(denominator) < 1e-10:
            return round(x2, decimal_places), steps
        
        x_new = (x0 * x2 - x1 ** 2) / denominator
        x_new = round(x_new, decimal_places)
        
        steps.append((round(x0, decimal_places), x1, x2, x_new))
        
        if abs(x_new - x0) < tol:
            return x_new, steps
        
        x0 = x_new
    
    raise ValueError("收敛失败")
