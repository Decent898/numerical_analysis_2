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
        if abs(denominator) < 1e-10:  # 防止除以零
            return x0, steps  # 返回x0，因为方法无法进一步加速
        
        # Aitken 加速步骤
        x_new = x0 - (x1 - x0)**2 / denominator
        
        steps.append((x0, x1, x2, x_new))  # 保存每一步的值
        # print(f"Step {i+1}: {steps[-1]}")
        
        # 收敛判定：使用新点和当前点之间的差异
        if abs(x_new - x0) < tol:
            return x_new, steps,x_min, x_max
        
        # 更新 x0 为新点以进入下一步
        x0 = x_new

    # 若达到最大迭代次数仍未收敛，抛出错误
    raise ValueError(f"Method failed to converge within {max_iter} iterations.")
