from antlr4 import InputStream, CommonTokenStream
from hmLexer import hmLexer
from hmParser import hmParser
from hmVisitor import hmVisitor
from antlr4.error.ErrorListener import ErrorListener
import streamlit as st

class SyntaxErrorListener(ErrorListener):
    def __init__(self):
        super(SyntaxErrorListener, self).__init__()
        self.syntax_errors = 0

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.syntax_errors += 1

def main():
    st.markdown("""## HiNer Interpreter Nico Llorens\nIngrese una expresion en el cuadro de texto y presione el botón "Evaluate" para obtener el resultado.""")
    expression = st.text_area('Expresion')

    if st.button('Evaluate'):
        try:
            input_stream = InputStream(expression)  # Utiliza InputStream en lugar de FileStream
            lexer = hmLexer(input_stream)
            token_stream = CommonTokenStream(lexer)
            parser = hmParser(token_stream) 
            parser.removeErrorListeners()  # Eliminar los listeners de errores predeterminados
            error_listener = SyntaxErrorListener()
            parser.addErrorListener(error_listener)  # Agregar nuestro propio listener de errores
            
            tree = parser.expression()
            visitor = hmVisitor()
            visitor.visit(tree)
            
            if error_listener.syntax_errors > 0:
                st.error(f"Se encontraron {error_listener.syntax_errors} error(es) de sintaxis")
            else:
                st.success("Expresion evaluada correctamente")
        except Exception as e:
            st.error(f"Error de análisis: {e}")
    

if __name__ == '__main__':
    main()
