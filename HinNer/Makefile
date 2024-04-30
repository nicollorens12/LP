file = hm

run:
	streamlit run --server.runOnSave true $(file).py

all:
	antlr4 -Dlanguage=Python3 -no-listener -visitor $(file).g4
novisitor:
	antlr4 -Dlanguage=Python3 -no-listener $(file).g4