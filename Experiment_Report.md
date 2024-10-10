# 第二章实验报告

## 1. 实验目标

建立一个图形化界面，用四大迭代方法求解方程的根。尝试用规范的格式输出迭代过程，并且绘制每次迭代的图像，尝试设计交互式图像，从而直观地的了解迭代的过程。

## 2. 实验内容

1.实现二分法、牛顿切线法和割线法来求解给定函数的根，用化简为f(x)=x的格式来用埃特肯法求解。

2.基于python flask库建立后端，负责计算迭代过程，同时还按照每种方法特性展示解的逼近过程。

3.在前端展示迭代过程（规范化的格式）、逼近过程图像、以及基于chart.js的交互式图表，可以观察每一次逼近的动态过程。

4.对于边界处理问题：埃特肯法的化简方法技巧性较强，暂未想到好的算法来化简，于是设置为用户输入；牛顿法和割线法的发散问题可以转化为迭代一定次数（max-iter）后仍然无法收敛的问题，从而提示函数不收敛。

## 3. 实验过程

1.在分析问题以后，我选择了python作为使用的语言，原因如下：

以前知道python有eval函数能直接计算表达式的值，了解python对于函数输入的处理比较方便。

我想直观地了解迭代的过程，想画一些交互式的图来加深我对迭代的理解，这就需要一个强大的绘图模块与图形化交互界面，因此选择了python的matplotlib以及考虑了html里可以导入的chart.js库来分别画静态的和动态的图。

2.四个方法具体实现：

二分法：从给定的区间开始，每次将区间二分，选择使函数值变号的子区间继续迭代。

牛顿法：使用导数信息，通过迭代公式逼近根的值。

割线法：不需要计算导数，通过两个初始点的函数值线性逼近根。

埃特肯法：根据推导所得的公式进行迭代

3.输入函数的处理：

在读入函数时，一大挑战是将输入的字符串函数转化为python可运算的表达式对象。这里选择使用python的lambda函数提取


## 4. 创建 requirements.txt

在项目根目录下创建 `requirements.txt` 文件，列出项目依赖：

```
Flask==2.0.1
numpy==1.21.0
matplotlib==3.4.2
```

## 5. 版本控制（可选但推荐）

如果您想使用 Git 进行版本控制：

```bash
git init
echo "venv/" > .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore
git add .
git commit -m "Initial commit"
```

## 6. 配置 VS Code

- 安装 Python 扩展（如果还没有安装）。
- 选择正确的 Python 解释器（应该是您刚创建的虚拟环境中的解释器）。

## 7. 运行应用

在 VS Code 的终端中（确保虚拟环境已激活）：

```bash
python app.py
```

访问 `http://localhost:5000` 查看您的应用。

## 8. 调试设置

在 VS Code 中，创建一个 `.vscode/launch.json` 文件用于调试配置：

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "app.py",
                "FLASK_ENV": "development"
            },
            "args": [
                "run",
                "--no-debugger"
            ],
            "jinja": true
        }
    ]
}
```

这将允许您直接在 VS Code 中调试 Flask 应用。
