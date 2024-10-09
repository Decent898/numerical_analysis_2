import math
import numpy as np

def get_decimal_places(tol):
    decimal_places = max(0, -int(math.log10(tol))) + 4
    return decimal_places

def newton_method(func, x0, tol, max_iter=100):
    steps = []
    
    x = x0
    decimal_places = get_decimal_places(tol)
    
    for i in range(max_iter):
        fx = func(x)
        fx = round(fx, decimal_places)  
        
        if abs(fx) < tol:
            return round(x, decimal_places), steps
        
        dfx = (func(x + 1e-8) - fx) / 1e-8
        dfx = round(dfx, decimal_places)  
        
        if dfx == 0:
            raise ValueError("出现导数为零")
        
        x_new = x - fx / dfx
        x_new = round(x_new, decimal_places)  # 四舍五入保留指定位数
        
        steps.append((round(x, decimal_places), fx, dfx, x_new))
        # print(f"第{i+1}步: x = {x}, f(x) = {fx}, f'(x) = {dfx}, x_new = {x_new}")
        
        if abs(x_new - x) < tol:
            return x_new, steps
        
        x = x_new
    
    raise ValueError("收敛失败")
