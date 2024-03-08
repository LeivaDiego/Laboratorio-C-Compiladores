class ShuntingYard:
    def __init__(self):
        self.binary_operators = {'·', '|'}
        self.unary_operators = {'*', '+', '?'}
        self.all_operators = self.binary_operators.union(self.unary_operators)
        self.special_characters = {'(', ')'}
    
    def validate_parentheses(self, regex):
        stack = []
        for char in regex:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack or stack[-1] != '(':
                    return False
                stack.pop()
        return not stack

    def apply_unary_operator(self, operand, operator):
        if operator == '*':
            return f'{operand}*'
        elif operator == '+':
            return f'({operand}{operand}*)'
        elif operator == '?':
            return f'({operand}|ϵ)'

    def transform_and_validate_subexpr(self, subexpr):
        new_expr = ""
        i = 0
        while i < len(subexpr):
            char = subexpr[i]
            if char in self.unary_operators and i > 0 and subexpr[i - 1] not in self.all_operators and subexpr[i - 1] != '(':
                if new_expr[-1] == ')':
                    balance = 1
                    j = len(new_expr) - 2
                    while j >= 0 and balance != 0:
                        if new_expr[j] == ')':
                            balance += 1
                        elif new_expr[j] == '(':
                            balance -= 1
                        j -= 1
                    operand = new_expr[j + 1:]
                    new_expr = new_expr[:j + 1]
                else:
                    operand = new_expr[-1]
                    new_expr = new_expr[:-1]

                while i < len(subexpr) and subexpr[i] in self.unary_operators:
                    operand = self.apply_unary_operator(operand, subexpr[i])
                    i += 1
                new_expr += operand
                i -= 1
            else:
                new_expr += char
            i += 1
        return new_expr

    def transform_and_validate(self, regex):
        if not self.validate_parentheses(regex):
            return False
        
        result = self.transform_and_validate_subexpr(regex)
        return result if result != "" else False

    def insert_explicit_concatenation(self, expression):
        result = ""
        for i, char in enumerate(expression):
            result += char
            if i + 1 < len(expression):
                next_char = expression[i + 1]
                if (char not in self.all_operators.union({'(', 'ϵ'}) and next_char not in self.all_operators.union({')', 'ϵ'})) or \
                   (char == ')' and next_char not in self.all_operators.union({')', 'ϵ'})) or \
                   (char not in self.all_operators.union({'(', 'ϵ'}) and next_char == '('):
                    result += '·'
        return result

    def process_expression(self, expression):
        transformed = self.transform_and_validate(expression)
        if transformed:
            return self.insert_explicit_concatenation(transformed)
        return False

test_expressions_full = [
    "a++",
    "a(b|c)*",
    "a?+*",
    "(a|b)c*",
    "a*|(b+c)",
    "(a|b)?c+",
    "ab+?c",
    "(x|y)*z?",
    "a?b*c+",
    "w+(x|y)?z*",
    "(a|b)?(c|d)*e+",
    "(0|1|2|3)(.(0|1|2|3))?(E(+|-)?(0|1|2|3))?"
]

sy = ShuntingYard()
processed_expressions = {expr: sy.process_expression(expr) for expr in test_expressions_full}
for item in processed_expressions:
    print(f"{item}: {processed_expressions[item]}")