import glob
import os
from yalex_processor import LexicalAnalyzer
from shunting_yard import ShuntingYard
from tree import SyntaxTree

def main():
    while True:
        syntax_trees = []

        # Solicitar al usuario que ingrese la ruta del archivo a analizar
        file_path = input("Ingrese la ruta del archivo a analizar: ")

        # Extraer solo el nombre del archivo sin la extensión
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # Crear una instancia de LexicalAnalyzer y analizar el archivo
        lexical_analyzer = LexicalAnalyzer()
        lexical_analyzer.analyze_file(file_path)

        # Obtener las definiciones del analizador léxico
        definitions = lexical_analyzer.definitions

        # Crear una instancia de ShuntingYard
        shunting_yard = ShuntingYard()

        # Iterar a través de cada definición
        for identifier, regex in definitions.items():
            # Convertir la expresión regular a notación postfija
            postfix_expression = shunting_yard.to_postfix(regex)

            # Generar y mostrar el árbol sintáctico para la expresión postfija
            if postfix_expression:  # Verificar si la conversión fue exitosa
                print('Expresión regular postfix:', postfix_expression)
                syntax_tree = SyntaxTree(postfix_expression, f"{file_name}_{identifier}")
                syntax_tree.visualize()
                syntax_trees.append(syntax_tree)

        # mega_tree = SyntaxTree.concatenate_trees(syntax_trees, file_name)
        # mega_tree.visualize()

        # Solicitar al usuario si desea analizar otro archivo
        another_file = input("¿Desea analizar otro archivo? (s/n): ")
        if another_file.lower() != 's':
            break

if __name__ == "__main__":
    main()