from antlr4 import InputStream, CommonTokenStream
from hmLexer import hmLexer
from hmParser import hmParser
from hmVisitor import hmVisitor
from antlr4.error.ErrorListener import ErrorListener
import streamlit as st
from dataclasses import dataclass
from typing import Union, List
from streamlit import graphviz_chart


# Ejemplo de uso:
#expression_tree = ExpressionNode(ApplicationNode(AbstractionNode('x', AtomNode(2)), FunctionNode('+')))


def main():
    st.markdown("""## HiNer Interpreter Nico Llorens\nIngrese una expresion en el cuadro de texto y presione el botón "Evaluate" para obtener el resultado.""")
    expression = st.text_area('Expresion','(+) 2 x')

    if st.button('Evaluate'):
        
        input_stream = InputStream(expression)  # Utiliza InputStream en lugar de FileStream
        lexer = hmLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = hmParser(token_stream)
        tree = parser.evaluate()
        print(tree)
            
        if parser.getNumberOfSyntaxErrors() != 0:
            st.error(f"Se encontraron {parser.getNumberOfSyntaxErrors()} error(es) de sintaxis")
        else:
            visitor = hmVisitor()
            semantic_tree = visitor.visitEvaluate(tree)
            print(semantic_tree)
            visitor.generate_dot(semantic_tree)
            dot_representation = visitor.get_graph()
            st.graphviz_chart(dot_representation)

            st.success("Expresion evaluada correctamente")
    

if __name__ == '__main__':
    main()
