import re

def is_safe_expression(expr):
    allowed = re.compile(r'^[\d\s+\-*/(),.xepi]+$')
    return bool(allowed.match(expr))

def parse_expression(expr_str):
    if not expr_str or expr_str.isspace():
        raise ValueError("表达式不能为空")
    # if not is_safe_expression(expr_str):
    #     raise ValueError("表达式有无效字符")
    
    expr_str = expr_str.replace('^', '**')
    
    if 'x' not in expr_str:
        raise ValueError("表达式必须包含 'x'")
    
    return expr_str