class ShuntingYard:
    def __init__(self):
        """
        Inicializa la clase ShuntingYard.

        Esta clase se utiliza para realizar la conversión de una expresión regular
        en notación infija a notación postfija utilizando el algoritmo Shunting Yard.

        Atributos:
        - binary_operators: Un conjunto que contiene los operadores binarios válidos.
        - unary_operators: Un conjunto que contiene los operadores unarios válidos.
        - all_operators: Unión de los conjuntos de operadores binarios y unarios.
        - special_characters: Un conjunto que contiene los caracteres especiales válidos.
        """
        self.binary_operators = {'·', '|'}
        self.unary_operators = {'*', '+', '?'}
        self.all_operators = self.binary_operators.union(self.unary_operators)
        self.special_characters = {'(', ')'}
    

    def get_precedence(self, operator):
        """
        Obtiene la precedencia de un operador.

        Esta función se utiliza para determinar la precedencia de los operadores
        en el algoritmo Shunting Yard. Los operadores unarios tienen la mayor
        precedencia, seguidos por el operador de concatenación y luego el operador de unión.

        Parámetros:
        - operator (str): El operador cuya precedencia se va a obtener.

        Retorna:
        - int: La precedencia del operador. Si el operador no está en el diccionario,
               se retorna 0.
        """
        precedence = {
            '*': 3,
            '+': 3,
            '?': 3,
            '·': 2,
            '|': 1
        }
        return precedence.get(operator, 0)


    def validate_parentheses(self, regex):
            """
            Valida si los paréntesis en la expresión regular están balanceados.

            Args:
                regex (str): La expresión regular a validar.

            Returns:
                bool: True si los paréntesis están balanceados, False en caso contrario.
            """
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
            """
            Aplica un operador unario al operando dado.

            Parámetros:
            operand (str): El operando al que se le aplicará el operador unario.
            operator (str): El operador unario a aplicar.

            Retorna:
            str: El resultado de aplicar el operador unario al operando.
            """
            if operator == '*':
                return f'{operand}*'
            elif operator == '+':
                return f'({operand}{operand}*)'
            elif operator == '?':
                return f'({operand}|ϵ)'


    def transform_and_validate_subexpr(self, subexpr):
            """
            Transforma y valida una subexpresión.

            Esta función recibe una subexpresión y aplica transformaciones y validaciones a la misma.
            Retorna la subexpresión transformada y validada.

            Parámetros:
            - subexpr: La subexpresión a transformar y validar.

            Retorna:
            - La subexpresión transformada y validada.
            """
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
            """
            Transforma y valida una expresión regular.

            Parámetros:
            regex (str): La expresión regular a transformar y validar.

            Retorna:
            bool: True si la expresión regular es válida, False en caso contrario.
            """
            if not self.validate_parentheses(regex):
                return False
            
            result = self.transform_and_validate_subexpr(regex)
            return result if result != "" else False


    def insert_explicit_concatenation(self, expression):
        """
        Inserta la concatenación explícita en la expresión.

        Esta función recorre la expresión y, cuando encuentra dos caracteres que deben estar concatenados,
        inserta un operador de concatenación '·' entre ellos.

        Parámetros:
        - expression (str): La expresión en la que se insertará la concatenación explícita.

        Retorna:
        - str: La expresión con la concatenación explícita insertada.
        """
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

    

    def to_postfix(self, expression):
            """
            Convierte una expresión matemática en notación infija a notación postfija utilizando el algoritmo Shunting Yard.

            Parámetros:
            - expression: La expresión matemática en notación infija a ser convertida.

            Retorna:
            - La expresión matemática en notación postfija.
            """
            transformed = self.transform_and_validate(expression)
            if transformed:
                concat_transformed = self.insert_explicit_concatenation(transformed)
            else:
                return False


            output = []
            operator_stack = []

            for char in concat_transformed:
                if char.isalpha() or char.isdigit() or char == 'ϵ':
                    output.append(char)
                elif char in self.all_operators:
                    while operator_stack and operator_stack[-1] != '(' and self.get_precedence(operator_stack[-1]) >= self.get_precedence(char):
                        output.append(operator_stack.pop())
                    operator_stack.append(char)
                elif char == '(':
                    operator_stack.append(char)
                elif char == ')':
                    top_token = operator_stack.pop()
                    while top_token != '(':
                        output.append(top_token)
                        top_token = operator_stack.pop()

            while operator_stack:
                output.append(operator_stack.pop())

            return ''.join(output)


# Lista de expresiones de prueba
test_expressions_full = [
    "a|b)",
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

# Crear una instancia de la clase ShuntingYard
sy = ShuntingYard()

# Procesar todas las expresiones de prueba y almacenar los resultados en un diccionario
# La clave es la expresión de prueba y el valor es el resultado de la conversión a notación postfija
processed_expressions = {expr: sy.to_postfix(expr) for expr in test_expressions_full}

# Imprimir todas las expresiones de prueba y sus correspondientes resultados
for item in processed_expressions:
    print(f"{item}: {processed_expressions[item]}")