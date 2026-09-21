import ast
import operator as op

COURSE_FEES = {
    "CS101": 12000,
    "AI202": 18000,
    "DS303": 15000
}


def get_course_fee(course_code):
    course_code = course_code.upper()

    if course_code in COURSE_FEES:
        return COURSE_FEES[course_code]

    return None


def calculator(expression):
    allowed_operators = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv
    }

    def evaluate(node):
        if isinstance(node, ast.Constant):
            return node.value

        if isinstance(node, ast.BinOp):
            operator = allowed_operators.get(type(node.op))

            if operator is None:
                raise ValueError("Operator not allowed")

            return operator(
                evaluate(node.left),
                evaluate(node.right)
            )

        raise ValueError("Invalid expression")

    tree = ast.parse(expression, mode="eval")
    return evaluate(tree.body)