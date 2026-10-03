"""Day 3 tools — copied from Day 2."""

from datetime import datetime, timezone
import re

import ast
import operator


def get_current_time() -> str:
    """Return current UTC time as ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


def calculate(expression: str) -> str:
    """Evaluate a math expression and return the result as a string."""
    if not re.match(r'^[\d\s+\-*\/\(\)\.]+$', expression):
        return "Invalid input"

    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def eval_node(node):
        if isinstance(node, ast.Expression):
            return eval_node(node.body)
        elif isinstance(node, ast.BinOp):
            left = eval_node(node.left)
            right = eval_node(node.right)
            op_type = type(node.op)
            if op_type in allowed_operators:
                return allowed_operators[op_type](left, right)
            else:
                raise ValueError("Unsupported operator")
        elif isinstance(node, ast.UnaryOp):
            operand = eval_node(node.operand)
            op_type = type(node.op)
            if op_type in allowed_operators:
                return allowed_operators[op_type](operand)
            else:
                raise ValueError("Unsupported unary operator")
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError("Invalid constant")
        else:
            raise ValueError("Invalid expression")

    try:
        tree = ast.parse(expression, mode="eval")
        result = eval_node(tree)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


TOOLS: dict[str, callable] = {
    "get_current_time": get_current_time,
    "calculate": calculate,
}
