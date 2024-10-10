from flask import Flask, render_template, request
from methods.bisection import bisection_method
from methods.newton import newton_method
from methods.secant import secant_method
from methods.aitken import aitken_method
from utils.expression_parser import parse_expression
from utils.function_evaluator import f
from utils.plotting import plot_function
from utils.plotting import plot_function_interactive
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 非图形界面后端

app = Flask(__name__)

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
                x = np.linspace(a-1, b+1, 100)
                template = 'result_bisection.html'
            elif method == 'aitken':
                x0 = float(request.form['aitken_x0'])
                root, steps = aitken_method(lambda x: f(x, expr), x0, tol)
                x = np.linspace(x0-1, x0+1, 100) if root is None else np.linspace(min(x0, root)-1, max(x0, root)+1, 100)
                template = 'result_aitken.html'
            elif method == 'newton':
                x0 = float(request.form['x0'])
                root, steps = newton_method(lambda x: f(x, expr), x0, tol)
                x = np.linspace(x0-1, x0+1, 100) if root is None else np.linspace(min(x0, root)-1, max(x0, root)+1, 100)
                template = 'result_newton.html'
            elif method == 'secant':
                x0, x1 = float(request.form['x0']), float(request.form['x1'])
                root, steps = secant_method(lambda x: f(x, expr), x0, x1, tol)
                x = np.linspace(min(x0, x1)-1, max(x0, x1)+1, 100)
                template = 'result_secant.html'
            else:
                return render_template('error.html', message="无效方法选择。")
            
            if root is None:
                return render_template('error.html', message="方法未能收敛。请输入不同的初值。")
            
            parsed_expr = parse_expression(expr)
            latex_expr = parsed_expr.replace('**', '^')  # Replace Python's power operator with LaTeX's
            
            plot_url = plot_function(lambda x: f(x, expr), x, root, steps, method.capitalize())
            # return render_template(template, root=root, steps=steps, plot_url=plot_url, expression=latex_expr, method=method.capitalize())
            
            # graph_json = plot_function_interactive(lambda x: f(x, expr), x, root, steps,  method.capitalize())
            # x_data = np.linspace(a - 1, b + 1, 100).tolist()  # 将 numpy 数组转换为 Python 列表
            # y_data = [f(xi, parsed_expr) for xi in x_data]  # 计算对应的 y 值
            # 调用 plot_function_interactive 生成 JSON 数据（chart_data）
            
            chart_data = plot_function_interactive(lambda x: f(x, expr), x, root, steps, method.capitalize())
            
            # 将 chart_data 传递给前端模板
            return render_template(template, root=root,steps=steps, plot_url=plot_url,chart_data=chart_data, expression=latex_expr,method=method.capitalize())
        except ValueError as e:
            return render_template('error.html', message=str(e))
        except Exception as e:
            return render_template('error.html', message=f"严重错误： {str(e)}")
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,port=5516)