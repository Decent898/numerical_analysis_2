import matplotlib.pyplot as plt
import numpy as np
import io
import base64

import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
import json

# 中文支持
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

dic = {
    'Bisection': '二分法',
    'Aitken': '埃特肯法',
    'Secant': '割线法',
    'Newton': '牛顿切线法'
}

def update_limit(x1, y_max, y_min):
    if x1 > y_max:
        y_max = x1
    if x1 < y_min:
        y_min = x1
    return y_max, y_min

def plot_function(func, x, root, steps, method):
    # plt.figure(figsize=(10, 6))
    plt.figure(figsize=(10,10))
    y = [func(xi) for xi in x]
    valid_points = [(xi, yi) for xi, yi in zip(x, y) if yi is not None]
    y_max=-114514
    y_min=114514
    
    if valid_points:
        x_valid, y_valid = zip(*valid_points)
        plt.plot(x_valid, y_valid, label='f(x)')
    
    plt.axhline(y=0, color='r', linestyle='--',label='x轴')
    plt.scatter([root], [0], color='g', s=100, label='根')
    
    if method == 'Bisection':
        for i, step in enumerate(steps):
            plt.plot([step[0], step[1]], [0, 0], 'bo-', alpha=0.3)
            plt.plot([step[2]], [step[3]], 'ro', alpha=0.5)
            y_max,y_min=update_limit(step[3], y_max, y_min)
            plt.annotate(f'Iter {i+1}', (step[2], step[3]), xytext=(5, 5),
                         textcoords='offset points', fontsize=8)
    
    elif method == 'Aitken':
        plt.plot(x, x, label='y=x', color='purple', linestyle='--')
        for i, step in enumerate(steps):
            x0, x1, x2, x_new = step
            y_max,y_min=update_limit(x1, y_max, y_min)
            y_max,y_min=update_limit(x2, y_max, y_min)
            # fx0, fx1, fx2 = func(x0), func(x1), func(x2)
            
            # 绘制当前迭代的三个点 (x0, f(x0)), (x1, f(x1)), (x2, f(x2))
            plt.scatter([x0, x1], [x1, x2], color='blue', s=50)
            plt.scatter([x1], [x1], color='red', s=50, alpha=0.7)
            plt.plot([x0, x1, x1], [x1, x1, x2], 'b--', alpha=0.5) # 绘制 (x0, f(x0)), (x1, f(x1)), (x2, f(x2)) 的连线
            plt.plot([x0, x1], [x1, x2], 'b', alpha=0.5) # 绘制 (x1, f(x1)), (x2, f(x2)) 的连线
            
            # # 绘制 (x0, x0), (x1, x1), (x2, x2) 与函数 f(x) 的对应关系
            # plt.scatter([x0], [x0], color='red', s=50, alpha=0.7) # 绘制 (x1, x1) 与函数 f(x) 的对应关系
            # plt.scatter([x2], [x2], color='red', s=50, alpha=0.7)
            # plt.plot([x0, x0], [fx0, x0], 'r--', alpha=0.5)  # 映射线
            # plt.plot([x1, x1], [fx1, x1], 'r--', alpha=0.5)  # 映射线
            # plt.plot([x2, x2], [fx2, x2], 'r--', alpha=0.5)  # 映射线
            
            # # 绘制加速后新预测的点
            fx_new = func(x_new)
            # plt.scatter([x_new], [fx_new], color='orange', s=50, label=f'Iter {i+1}' if i == 0 else "", alpha=0.7)
            # plt.plot([x2, x_new], [fx2, fx_new], 'r--', alpha=0.5)
            
            # 添加迭代标注
            plt.annotate(f'Iter {i+1}', (x_new, fx_new), xytext=(5, 5), 
                            textcoords='offset points', fontsize=8)
            
    elif method == 'Newton':
        for i, step in enumerate(steps[:-1]):
            x0, fx0, dfx0, x1 = step
            y_max,y_min=update_limit(fx0, y_max, y_min)
            x_tangent = np.linspace(x0 - 0.5, x0 + 0.5, 100)
            y_tangent = fx0 + dfx0 * (x_tangent - x0)
            plt.plot(x_tangent, y_tangent, 'g--', alpha=0.5)
            plt.plot([x0, x1], [fx0, 0], 'ro-', alpha=0.5)
    
    elif method == 'Secant':
        for i, step in enumerate(steps[:-1]):
            x0, x1, fx0, fx1, x2 = step
            y_max,y_min=update_limit(fx0, y_max, y_min)
            plt.plot([x0, x1], [fx0, fx1], 'g--', alpha=0.5)
            plt.plot([x1, x2], [fx1, 0], 'ro-', alpha=0.5)
    
    
    plt.legend()
    plt.title(f'{dic[method]}图像')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    
    ##设置比例为1:1
    if method == 'Aitken':
        plt.gca().set_aspect('equal', adjustable='box')
    ## y轴不超过func(steps[-1][0])
    plt.ylim(y_min-1, y_max+1)
    # plt.ylim(x.min() - 1, x.max() + 1)
    print(y_min,y_max)  
    
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_url = base64.b64encode(buf.getvalue()).decode('utf8')
    plt.close()
    
    return plot_url


def plot_function_interactive(func, x, root, steps, method):
    # 创建数据结构，用于存储各个点
    chart_data = {
        'function_points': [],  # 函数曲线的点
        'root_point': {'x': root, 'y': 0},  # 根点
        'steps': []  # 各个迭代步骤的点
    }

    # 生成函数曲线的点
    y = [func(xi) for xi in x]
    chart_data['function_points'] = [{'x': xi, 'y': yi} for xi, yi in zip(x, y)]

    # 根据不同方法记录步骤
    if method == 'Bisection':
        for i, step in enumerate(steps):
            chart_data['steps'].append({
                'iter': i + 1,
                'a': {'x': step[0], 'y': 0},  # 区间左端点
                'b': {'x': step[1], 'y': 0},  # 区间右端点
                'mid': {'x': step[2], 'y': step[3]}  # 中点
            })

    elif method == 'Aitken':
        # 生成 y=x 曲线的点
        chart_data['y_equals_x'] = [{'x': xi, 'y': xi} for xi in x]
        
        for i, step in enumerate(steps):
            x0, x1, x2, x_new = step
            fx0, fx1, fx2 = func(x0), func(x1), func(x2)
            fx_new = func(x_new)
            chart_data['steps'].append({
                'iter': i + 1,
                'points': [
                    {'x': x0, 'y': fx0},
                    {'x': x1, 'y': fx1},
                    {'x': x2, 'y': fx2}
                ],
                'mappings': [
                    {'x': x0, 'y': x0},  # (x0, x0) 映射点
                    {'x': x1, 'y': x1},  # (x1, x1) 映射点
                    {'x': x2, 'y': x2}   # (x2, x2) 映射点
                    
                ],
                'new_prediction': {'x': x_new, 'y': fx_new}  # 新预测点
            })

    if method == 'Newton':
        for i, step in enumerate(steps[:-1]):
            x0, fx0, dfx0, x1 = step

            # 计算切线与x轴的交点
            x_intersection = x0 - fx0 / dfx0

            # 生成切线的点：从x0到x轴的交点
            x_tangent = np.linspace(x0, x_intersection, 100)
            y_tangent = fx0 + dfx0 * (x_tangent - x0)

            # 保存每次迭代的切线和根的近似
            chart_data['steps'].append({
                'iter': i + 1,
                'tangent': [{'x': xt, 'y': yt} for xt, yt in zip(x_tangent, y_tangent)],
                'root_approx': {'x': x1, 'y': 0}  # 每次迭代得到的近似根
            })

    if method == 'Secant':
        for i, step in enumerate(steps[:-1]):
            x0, x1, fx0, fx1, x2 = step
            
            # 弦线：通过 x0 和 x1
            chart_data['steps'].append({
                'iter': i + 1,
                'secant': [{'x': x0, 'y': fx0}, {'x': x1, 'y': fx1}],  # 弦线
                'root_approx': {'x': x2, 'y': 0}  # 弦线与x轴交点，即近似根
            })


    # 转换为 JSON 格式
    graph_json = json.dumps(chart_data)

    return graph_json