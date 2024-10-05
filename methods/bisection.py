def bisection_method(func, a, b, tol, max_iter=100):
    steps = []
    fa, fb = func(a), func(b)
    
    if fa * fb > 0:
        raise ValueError("Function values at the interval endpoints must have opposite signs.")
    
    iteration = 0
    while (b - a) / 2 > tol:
        iteration += 1
        if iteration > max_iter:
            raise ValueError(f"Method failed to converge within {max_iter} iterations.")
        
        c = (a + b) / 2
        fc = func(c)
        
        steps.append((a, b, c, fc))
        
        if abs(fc) < tol:
            return c, steps
        
        if fa * fc <= 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    
    return (a + b) / 2, steps