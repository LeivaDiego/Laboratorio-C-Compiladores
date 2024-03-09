import os

class LexicalAnalyzer:
    def __init__(self):
        self.raw_code = []
        self.code = [] 

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
    
analyzer = LexicalAnalyzer()
path = input("Enter the path to the file: ")
updated_path = analyzer.parse_path(path)
analyzer.file_scanner(updated_path)
analyzer.cleanup()
print(analyzer.code)