from antlr4 import InputStream, CommonTokenStream
from hmLexer import hmLexer
from hmParser import hmParser
from hmVisitor import hmVisitor
from antlr4.error.ErrorListener import ErrorListener
import streamlit as st
import pandas as pd
from dataclasses import dataclass
from typing import Union, List
from streamlit import graphviz_chart


def main():
    st.markdown("""## HiNer Interpreter Nico Llorens\nIngrese una expresion en el cuadro de texto y presione el botón "Evaluate" para obtener el resultado.""")
    expression = st.text_area('Expresion','(+) 2 x')

    if st.button('Evaluate'):
        
        input_stream = InputStream(expression)  # Utiliza InputStream en lugar de FileStream
        lexer = hmLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = hmParser(token_stream)
        tree = parser.evaluate()
            
        if parser.getNumberOfSyntaxErrors() != 0:
            st.error(f"Se encontraron {parser.getNumberOfSyntaxErrors()} error(es) de sintaxis")
        else:
            visitor = hmVisitor()
            semantic_tree = visitor.visitEvaluate(tree)
            visitor.generate_dot(semantic_tree)
            df = visitor.getTable()
            st.table(df)
            dot_representation = visitor.get_graph()
            st.graphviz_chart(dot_representation)
            
            st.success("Expresion evaluada correctamente")
    

if __name__ == '__main__':
    main()
