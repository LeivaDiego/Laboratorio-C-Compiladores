import os

class LexicalAnalyzer:
    def __init__(self):
        self.raw_code = []
        self.code = [] 
        self.definitions = {}
        self.symbol_table = {
            '+': 'PLUS',
            '-': 'MINUS',
            '*': 'STAR',
            '/': 'DIV',
            '(': 'LPAREN',
            ')': 'RPAREN',
            '\t': 'TAB',
            '\n': 'NEWLINE',
            '\r': 'CARRIAGE_RETURN',
            ';': 'SEMICOLON',
            ',': 'COMMA',
            '=': 'EQUALS',
            '<': 'LESS_THAN',
            '>': 'GREATER_THAN',
            '?': 'QUESTION',
            ' ': 'WHITESPACE',

        }

    def file_scanner(self, filepath):
        if not os.path.isfile(filepath):
            print(f"Archivo no encontrado.")
            return 
        with open(filepath, 'r') as file:
            self.raw_code = [line.strip() for line in file.readlines()]

    def cleanup(self):
        in_comment = False  
        for line in self.raw_code:
            if '(*' in line:
                in_comment = True
            if '*)' in line:
                in_comment = False
                continue 
            if not in_comment:
                cleaned_line = ' '.join(line.split())
                if cleaned_line:
                    self.code.append(cleaned_line)

    def parse_path(self, path):
        path = path.replace('"', '')
        path = path.replace('\\', '/')
        return path
    
    def extract_definitions(self):
        for line in self.code:
            if line.startswith('let'):
                parts = line.split('=')
                identifier = parts[0][4:].strip()
                regex = parts[1].strip()

                if self.is_balanced(regex):
                    self.definitions[identifier] = regex
                else:
                    raise ValueError(f"La expresión regular para {identifier} no está balanceada correctamente.")

    def is_balanced(self, expression):
        stack = []
        in_single_quotes = False  
        for char in expression:
            if char == "'" and not in_single_quotes:
                in_single_quotes = True
            elif char == "'" and in_single_quotes:
                in_single_quotes = False
            elif char in ['[', '('] and not in_single_quotes:
                stack.append(char)
            elif char == ']' and not in_single_quotes:
                if not stack or stack[-1] != '[':
                    return False
                stack.pop()
            elif char == ')' and not in_single_quotes:
                if not stack or stack[-1] != '(':
                    return False
                stack.pop()
        return not stack

    def substitute_identifiers(self):
        substitutions = 1
        while substitutions > 0:
            substitutions = 0
            for ident, regex in self.definitions.items():
                for target_ident in self.definitions.keys():
                    if target_ident in regex and target_ident != ident:
                        new_regex = regex.replace(target_ident, f'({self.definitions[target_ident]})')
                        if new_regex != regex:
                            self.definitions[ident] = new_regex
                            substitutions += 1


    def is_character_class(self, regex):
        # Verifica si la cadena contiene al menos un patrón 'caracter1'-'caracter2'
        return regex.count("'-'") >= 1 and regex.startswith("['") and regex.endswith("']")

    def is_normal_character_set(self, regex):
        # Verifica si la entrada es un conjunto de caracteres normales
        return regex.startswith("['") and regex.endswith("']") and all(c not in self.symbol_table for c in regex[2:-2])

    def is_special_character_set(self, regex):
        # Verifica si la entrada es un conjunto de caracteres especiales.
        if not (regex.startswith("['") and regex.endswith("']")):
            return False
        
        # Extraer el contenido entre [' y '] y dividirlo por '' para manejar correctamente las secuencias de escape.
        content = regex[2:-2].split("''")
        for item in content:
            if len(item) == 1 and item in self.symbol_table:
                return True
            elif len(item) > 1 and item.encode().decode('unicode_escape') in self.symbol_table:
                return True
        return False

    def range_to_regex(self, regex):
        if not self.is_character_class(regex):
            raise ValueError("La entrada no es una clase de caracteres o no contiene rangos válidos.")
        regex = regex[1:-1]
        ranges = regex.split("''")
        regex_result = ""
        for range_str in ranges:
            if '-' in range_str:
                start_char, end_char = range_str.replace("'", "").split('-')
                for char_code in range(ord(start_char), ord(end_char) + 1):
                    regex_result += chr(char_code) + "|"
            else:
                regex_result += range_str.replace("'", "") + "|"
        return regex_result.rstrip("|")

    def convert_normal_character_set(self, regex):
        characters = regex[2:-2].replace("'", "")  # Eliminar los corchetes y comillas simples
        return '|'.join(characters)

    def convert_special_character_set(self, regex):
        content = regex[2:-2].split("''")
        regex_result = ''
        for item in content:
            if item in self.symbol_table:
                regex_result += self.symbol_table[item] + '|'
            else:
                # Manejar la secuencia de escape.
                decoded_item = item.encode().decode('unicode_escape')
                if decoded_item in self.symbol_table:
                    regex_result += self.symbol_table[decoded_item] + '|'
                else:
                    regex_result += decoded_item + '|'
        return regex_result.rstrip('|')


    def convert_regex(self, regex):
        if self.is_normal_character_set(regex):
            return self.convert_normal_character_set(regex)
        elif self.is_special_character_set(regex):
            return self.convert_special_character_set(regex)
        elif self.is_character_class(regex):
            return self.range_to_regex(regex)
        else:
            raise ValueError("La entrada no coincide con ningún formato conocido.")

    def convert_definitions(self):
        for ident, regex in self.definitions.items():
            try:
                self.definitions[ident] = self.convert_regex(regex)
            except ValueError:
                continue

analyzer = LexicalAnalyzer()
path = input("Enter the path to the file: ")
updated_path = analyzer.parse_path(path)
analyzer.file_scanner(updated_path)
analyzer.cleanup()
print('Codigo limpio y separado:')
print(analyzer.code)
analyzer.extract_definitions()
print('Definiciones:')
print(analyzer.definitions)
analyzer.convert_definitions()
print('Definiciones convertidas:')
print(analyzer.definitions)
analyzer.substitute_identifiers()
print('Definiciones actualizadas:')
print(analyzer.definitions)