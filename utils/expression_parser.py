import re

def is_safe_expression(expr):
    allowed = re.compile(r'^[\d\s+\-*/(),.xepi]+$')
    return bool(allowed.match(expr))

def parse_expression(expr_str):
    if not expr_str or expr_str.isspace():
        raise ValueError("Expression cannot be empty")
    if not is_safe_expression(expr_str):
        raise ValueError("Invalid characters in expression")
    
    expr_str = expr_str.replace('^', '**')
    
    if 'x' not in expr_str:
        raise ValueError("Expression must contain the variable 'x'")
    
    return expr_str