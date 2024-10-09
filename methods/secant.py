import math

def get_decimal_places(tol):
    decimal_places = max(0, -int(math.log10(tol))) + 2
    return decimal_places

def secant_method(func, x0, x1, tol, max_iter=100):
    steps = []
    
    decimal_places = get_decimal_places(tol)
    
    for i in range(max_iter):
        f0, f1 = func(x0), func(x1)
        f0 = round(f0, decimal_places)
        f1 = round(f1, decimal_places)
        
        if abs(f1) < tol:
            return round(x1, decimal_places), steps
        
        if f0 == f1:
            raise ValueError("分母为零")
        
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        x2 = round(x2, decimal_places) 
        
        steps.append((round(x0, decimal_places), round(x1, decimal_places), f0, f1, x2))
        
        if abs(x2 - x1) < tol:
            return x2, steps
        
        x0, x1 = x1, x2
    
    raise ValueError("收敛失败")
