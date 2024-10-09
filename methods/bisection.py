import math

def get_decimal_places(tol):
    decimal_places = max(0, -int(math.log10(tol)))+ 2
    # print("保留位数:", decimal_places)
    return decimal_places

def bisection_method(func, a, b, tol, max_iter=100):
    steps = []
    fa, fb = func(a), func(b)
    
    if fa * fb > 0:
        raise ValueError(f"区间端点的函数值必须异号 此处 f(a)={fa} , f(b)={fb}")

    # 根据 tol 计算需要的精度
    decimal_places = get_decimal_places(tol)
    
    iteration = 0
    while True:
        iteration += 1
        if iteration > max_iter:
            raise ValueError("收敛失败")
        
        a= round(a, decimal_places)
        b = round(b, decimal_places)
        
        c = (a + b) / 2
        c= round(c, decimal_places)
        fc = func(c)
        fc= round(fc, decimal_places)
        
        # 指定的小数位数
        steps.append((
            a,b,c,fc
        ))

        # 收敛判定
        if abs(b - a) < tol:
            break
        
        if fa * fc <= 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    
    return round((a + b) / 2, decimal_places), steps
