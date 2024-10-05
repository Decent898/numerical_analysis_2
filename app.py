from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import math
import re

app = Flask(__name__)

def is_safe_expression(expr):
    # 只允许包含数字、基本数学运算符、x 和一些数学函数
    allowed = re.compile(r'^[\d\s+\-*/(),.xepi]+$')
    return bool(allowed.match(expr))

def parse_expression(expr_str):
    if not expr_str or expr_str.isspace():
        raise ValueError("Expression cannot be empty")
    if not is_safe_expression(expr_str):
        raise ValueError("Invalid characters in expression")
    
    # 替换 ^ 为 **
    expr_str = expr_str.replace('^', '**')
    
    # 检查表达式是否包含 x
    if 'x' not in expr_str:
        raise ValueError("Expression must contain the variable 'x'")
    
    return expr_str

def f(x, expr):
    try:
        # 创建一个包含允许的数学函数和常数的安全环境
        safe_dict = {
            "x": x,
            "abs": abs,
            "max": max,
            "min": min,
            "pow": pow,
            "round": round,
            "e": math.e,
            "pi": math.pi,
            "exp": math.exp,
            "log": math.log,
            "log10": math.log10,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "asin": math.asin,
            "acos": math.acos,
            "atan": math.atan,
            "sinh": math.sinh,
            "cosh": math.cosh,
            "tanh": math.tanh,
            "sqrt": math.sqrt,
        }
        result = eval(expr, {"__builtins__": {}}, safe_dict)
        return float(result)
    except Exception as e:
        raise ValueError(f"Unable to evaluate expression at x = {x}: {e}")

def safe_eval(func, x):
    try:
        return func(x)
    except Exception as e:
        print(f"Warning: {e}")
        return None

def bisection_method(func, a, b, tol):
    steps = []
    fa, fb = safe_eval(func, a), safe_eval(func, b)
    if fa is None or fb is None:
        return None, steps
    if fa * fb >= 0:
        return None, steps  # 区间端点函数值同号，方法失败
    while (b - a) / 2 > tol:
        c = (a + b) / 2
        fc = safe_eval(func, c)
        if fc is None:
            return None, steps
        steps.append((a, b, c, fc))
        if abs(fc) < tol:
            return c, steps
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    return (a + b) / 2, steps

def aitken_method(func, x0, tol, max_iter=100):
    steps = []
    for i in range(max_iter):
        x1 = safe_eval(func, x0)
        if x1 is None:
            return None, steps
        x2 = safe_eval(func, x1)
        if x2 is None:
            return None, steps
        denominator = x2 - 2*x1 + x0
        if abs(denominator) < 1e-10:  # 防止除以零
            return x0, steps
        x_new = x0 - (x1 - x0)**2 / denominator
        steps.append((x0, x1, x2, x_new))
        if abs(x_new - x0) < tol:
            return x_new, steps
        x0 = x_new
    return x0, steps

def newton_method(func, x0, tol, max_iter=100):
    steps = []
    h = 1e-5  # 用于数值微分的小步长
    for i in range(max_iter):
        fx = safe_eval(func, x0)
        if fx is None:
            return None, steps
        if abs(fx) < tol:
            return x0, steps
        # 数值微分
        dfx = (safe_eval(func, x0 + h) - fx) / h
        if dfx is None or abs(dfx) < 1e-10:  # 防止除以零
            return None, steps  # 导数接近零，方法失败
        x1 = x0 - fx / dfx
        steps.append((x0, fx, dfx, x1))
        if abs(x1 - x0) < tol:
            return x1, steps
        x0 = x1
    return x0, steps

def secant_method(func, x0, x1, tol, max_iter=100):
    steps = []
    for i in range(max_iter):
        fx0, fx1 = safe_eval(func, x0), safe_eval(func, x1)
        if fx0 is None or fx1 is None:
            return None, steps
        if abs(fx1) < tol:
            return x1, steps
        if abs(fx1 - fx0) < 1e-10:  # 防止除以零
            return None, steps  # 函数值相等，方法失败
        x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        steps.append((x0, x1, fx0, fx1, x2))
        if abs(x2 - x1) < tol:
            return x2, steps
        x0, x1 = x1, x2
    return x1, steps

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        method = request.form['method']
        tol = float(request.form['tolerance'])
        expr_str = request.form['expression']
        
        try:
            expr = parse_expression(expr_str)
            
            if method == 'bisection':
                a, b = float(request.form['a']), float(request.form['b'])
                root, steps = bisection_method(lambda x: f(x, expr), a, b, tol)
            elif method == 'aitken':
                x0 = float(request.form['x0'])
                root, steps = aitken_method(lambda x: f(x, expr), x0, tol)
            elif method == 'newton':
                x0 = float(request.form['x0'])
                root, steps = newton_method(lambda x: f(x, expr), x0, tol)
            elif method == 'secant':
                x0, x1 = float(request.form['x0']), float(request.form['x1'])
                root, steps = secant_method(lambda x: f(x, expr), x0, x1, tol)
            else:
                return render_template('error.html', message="Invalid method selected.")
            
            if root is None:
                return render_template('error.html', message="Method failed to converge. Try different initial values.")

            # 生成图表
            plt.figure(figsize=(10, 6))
            if root is not None:
                x = np.linspace(float(root) - 2, float(root) + 2, 100)
            else:
                x = np.linspace(-10, 10, 100)  # 如果没有找到根，使用默认范围
            y = [safe_eval(lambda xi: f(xi, expr), xi) for xi in x]
            valid_points = [(xi, yi) for xi, yi in zip(x, y) if yi is not None]
            if valid_points:
                x_valid, y_valid = zip(*valid_points)
                plt.plot(x_valid, y_valid, label='f(x)')
            plt.axhline(y=0, color='r', linestyle='--')
            plt.scatter([step[-1] for step in steps], [safe_eval(lambda x: f(x, expr), step[-1]) for step in steps], color='g', label='Steps')
            plt.legend()
            plt.title(f'{method.capitalize()} Method')
            plt.xlabel('x')
            plt.ylabel('f(x)')
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plot_url = base64.b64encode(buf.getvalue()).decode('utf8')
            
            return render_template('result.html', root=root, steps=steps, plot_url=plot_url, expression=expr_str)
        
        except ValueError as e:
            return render_template('error.html', message=str(e))
        except Exception as e:
            return render_template('error.html', message=f"An unexpected error occurred: {str(e)}")
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    