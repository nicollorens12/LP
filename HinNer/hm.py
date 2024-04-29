from antlr4 import InputStream, CommonTokenStream
from hmLexer import hmLexer
from hmParser import hmParser
from hmVisitor import hmVisitor
from antlr4.error.ErrorListener import ErrorListener
import streamlit as st
from dataclasses import dataclass
from typing import Union, List
from streamlit import graphviz_chart

@dataclass
class ApplicationNode:
    abstraction: Union['AbstractionNode', 'FunctionNode']
    atom: Union['AtomNode', 'FunctionNode']

@dataclass
class AbstractionNode:
    variable: str
    expression: Union['ExpressionNode', 'AbstractionNode', 'FunctionNode']

@dataclass
class FunctionNode:
    operator: str

@dataclass
class AtomNode:
    value: Union[int, str]

@dataclass
class ExpressionNode:
    node: Union[ApplicationNode, AbstractionNode, FunctionNode, AtomNode]

# Ejemplo de uso:
#expression_tree = ExpressionNode(ApplicationNode(AbstractionNode('x', AtomNode(2)), FunctionNode('+')))

def generate_dot(node):
    dot = 'digraph G {\n'
    node_id = 0

    def generate_node(node):
        nonlocal node_id
        current_id = node_id
        node_id += 1

        if isinstance(node, ApplicationNode):
            dot += f'  node{current_id} [label="Application"];\n'
            dot += f'  node{current_id} -> node{generate_node(node.abstraction)};\n'
            dot += f'  node{current_id} -> node{generate_node(node.atom)};\n'
        elif isinstance(node, AbstractionNode):
            dot += f'  node{current_id} [label="Abstraction ({node.variable})"];\n'
            dot += f'  node{current_id} -> node{generate_node(node.expression)};\n'
        elif isinstance(node, FunctionNode):
            dot += f'  node{current_id} [label="Function ({node.operator})"];\n'
        elif isinstance(node, AtomNode):
            dot += f'  node{current_id} [label="Atom ({node.value})"];\n'

        return current_id

    generate_node(node)
    dot += '}\n'
    return dot

class SyntaxErrorListener(ErrorListener):
    def __init__(self):
        super(SyntaxErrorListener, self).__init__()
        self.syntax_errors = 0

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.syntax_errors += 1

def main():
    st.markdown("""## HiNer Interpreter Nico Llorens\nIngrese una expresion en el cuadro de texto y presione el botón "Evaluate" para obtener el resultado.""")
    expression = st.text_area('Expresion','(+) 2 x')

    if st.button('Evaluate'):
        try:
            input_stream = InputStream(expression)  # Utiliza InputStream en lugar de FileStream
            lexer = hmLexer(input_stream)
            token_stream = CommonTokenStream(lexer)
            parser = hmParser(token_stream) 
            parser.removeErrorListeners()  # Eliminar los listeners de errores predeterminados
            error_listener = SyntaxErrorListener()
            parser.addErrorListener(error_listener)  # Agregar nuestro propio listener de errores
            print("Expresion:", expression)

            tree = parser.expression()
            
            visitor = hmVisitor()
            tree = visitor.visitEvaluate(tree)
            dot = generate_dot(tree)
            graphviz_chart(dot)
            print(tree)
            
            if error_listener.syntax_errors > 0:
                st.error(f"Se encontraron {error_listener.syntax_errors} error(es) de sintaxis")
            else:
                st.success("Expresion evaluada correctamente")
        except Exception as e:
            st.error(f"Error de análisis: {e}")
    

if __name__ == '__main__':
    main()
