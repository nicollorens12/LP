from antlr4 import InputStream, CommonTokenStream
from hmLexer import hmLexer
from hmParser import hmParser
from hmVisitor import hmVisitor, TypeInferenceError
import streamlit as st
import pandas as pd

# Define the function to load and cache the type_df
@st.cache_data
def load_type_df():
    return pd.DataFrame(columns=['Elemento', 'Tipo'])

def main():
    st.markdown("""## HiNer Interpreter Nico Llorens\nIngrese una expresion en el cuadro de texto y presione el botón "Evaluate" para obtener el resultado.""")
    expression = st.text_area('Expresion', '(+) :: N->N->N')  # \\x->(+) 2 x

    if 'type_df' not in st.session_state:
        st.session_state.type_df = load_type_df()

    # Create columns for the buttons
    col1, col2 = st.columns(2)

    with col1:
        evaluate_button = st.button('Evaluate')
    
    with col2:
        reset_button = st.button('Reset')

    if evaluate_button:
        input_stream = InputStream(expression)  # Utiliza InputStream en lugar de FileStream
        lexer = hmLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = hmParser(token_stream)
        
        tree = parser.evaluate()
        visitor = hmVisitor()
        visitor.type_df = st.session_state.type_df  # Load cached DataFrame
        
        if parser.getNumberOfSyntaxErrors() != 0:
            st.error(f"Se encontraron {parser.getNumberOfSyntaxErrors()} error(es) de sintaxis")
        else:
            try:
                semantic_tree = visitor.visitEvaluate(tree)
                st.session_state.type_df = visitor.getTable()  # Update cached DataFrame
                df = st.session_state.type_df
                st.table(df)
                if visitor.evaluateType == 'typeAssign':
                    st.success("Tipo asignado correctamente")
                else:
                    visitor.generate_dot(semantic_tree)
                    dot_representation = visitor.get_graph()
                    st.graphviz_chart(dot_representation)
                    result = visitor.infer_types()
                    if not result:
                        st.error("Error en la inferencia de tipos")
                    else:
                        visitor.generate_new_dot()
                        dot_representation = visitor.get_graph()
                        st.graphviz_chart(dot_representation)
                        st.table(visitor.inference_change_table)
                        st.success("Expresion evaluada correctamente")
            except TypeInferenceError as e:
                st.error(f"Error en la inferencia de tipos:{e.message}")

    if reset_button:
        st.cache_data.clear()
        st.session_state.type_df = load_type_df()

if __name__ == '__main__':
    main()
