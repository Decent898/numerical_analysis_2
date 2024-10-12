def update_limits(x, x_min, x_max):
    if x < x_min:
        x_min = x
    if x > x_max:
        x_max = x
    return x_max, x_min

def aitken_method(func, x0, tol, max_iter=100):
    x_min = x0
    x_max = x0
    steps = []
    for i in range(max_iter):
        x1 = func(x0)
        x2 = func(x1)
        x_max, x_min = update_limits(x0, x_min, x_max)
        
        denominator = x2 - 2 * x1 + x0
        if abs(denominator) < 1e-10: 
            return x0, steps,x_min, x_max # 避免除以零错误
        

        x_new = x0 - (x1 - x0)**2 / denominator
        
        steps.append((x0, x1, x2, x_new))  
        # print(f"Step {i+1}: {steps[-1]}")
        

        if abs(x_new - x0) < tol:
            return x_new, steps,x_min, x_max
        
        x0 = x_new

    raise ValueError("收敛失败")
