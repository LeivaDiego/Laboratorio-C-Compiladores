import os

class LexicalAnalyzer:
    def __init__(self):
        self.raw_code = []
        self.code = [] 
        self.definitions = {}

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
analyzer.substitute_identifiers()
print('Definiciones actualizadas:')
print(analyzer.definitions)