from anytree import Node, RenderTree
from anytree.exporter import DotExporter

class SyntaxTree:
    def __init__(self, postfix_expr, name):
        self.postfix_expr = postfix_expr
        self.name = name
        self.root = self.build_tree()

    def build_tree(self):
        stack = []
        for char in self.postfix_expr:
            if char == '·' or char == '|':
                # Operadores binarios
                right = stack.pop()
                left = stack.pop()
                node = Node(char, children=[left, right])
                stack.append(node)
            elif char == '*':
                # Operador unario
                child = stack.pop()
                node = Node(char, children=[child])
                stack.append(node)
            else:
                # Operandos
                node = Node(char)
                stack.append(node)
        return stack.pop()  # La raíz del árbol está en la cima de la pila

    def display(self):
        for pre, _, node in RenderTree(self.root):
            treestr = u"%s%s" % (pre, node.name)
            print(treestr.ljust(8))
    
    def visualize(self):
        dot_filename = f"{self.name}.dot"
        png_filename = f"{self.name}.png"
        DotExporter(self.root).to_dotfile(dot_filename)
        DotExporter(self.root).to_picture(png_filename)
        print(f"Árbol guardado como {dot_filename} y {png_filename}")