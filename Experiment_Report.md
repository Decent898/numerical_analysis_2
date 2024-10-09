# 第二章实验报告

## 1. 实验目标

建立一个图形化界面，用四大迭代方法求解方程的根。尝试用规范的格式输出迭代过程，并且绘制每次迭代的图像，从而直观地的了解迭代的过程。


## 2. 实验内容

激活虚拟环境后，安装项目所需的依赖：

```bash
pip install flask numpy matplotlib
```

## 3. 创建项目结构

在 VS Code 中，创建以下文件和文件夹结构：

```
your_project_folder/
│
├── app.py
├── requirements.txt
├── static/
│   └── css/
│       └── style.css
└── templates/
    ├── index.html
    └── result.html
```

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