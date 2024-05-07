# Generated from hm.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .hmParser import hmParser
else:
    from hmParser import hmParser
from dataclasses import dataclass
from typing import Union, List
import pydot
import pandas as pd

@dataclass
class ApplicationNode:
    expression: Union['AbstractionNode', 'FunctionNode','ApplicationNode']
    atom: Union['AtomNode']

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

# This class defines a complete generic visitor for a parse tree produced by hmParser.

class hmVisitor(ParseTreeVisitor):

    def __init__(self):
        self.graph = pydot.Dot(graph_type='graph')
        self.aplicationCount = 0
        self.abstractionCount = 0
        self.functionCount = 0
        self.atomCount = 0
        self.root_node = None
        self.type_df = pd.DataFrame(columns=['Elemento', 'Tipo'])
        self.varTypeMap = dict()
        self.current_type = 'a'


    def visitEvaluate(self, ctx:hmParser.EvaluateContext):
        
        [expression,_] = list(ctx.getChildren())
        self.root_node = self.visit(expression)
        return self.visit(expression)

    def visitExpressionAtom(self, ctx:hmParser.ExpressionAtomContext):
        
        [atom] = list(ctx.getChildren())
        return self.visit(atom)

    def visitExpressionApplication(self, ctx:hmParser.ExpressionApplicationContext):
        
        [application] = list(ctx.getChildren())
        return self.visit(application)

    def visitExpressionAbstraction(self, ctx:hmParser.ExpressionAbstractionContext):
        
        [abstraction] = list(ctx.getChildren())
        return self.visit(abstraction)

    def visitExpressionParenthesis(self, ctx:hmParser.ExpressionParenthesisContext):
        
        [_,expression,_] = list(ctx.getChildren())
        return self.visit(expression)
    
    def visitAtomNumber(self, ctx:hmParser.AtomNumberContext):
        
        value = int(ctx.NUMBER().getText())
        
        return AtomNode(value=value)

    def visitAtomVariable(self, ctx:hmParser.AtomVariableContext):
        
        
        variable = ctx.VARIABLE().getText()
        
        return AtomNode(value=variable)

    def visitApplicationComposed(self, ctx:hmParser.ApplicationComposedContext):
        
        [aplication,atom] = list(ctx.getChildren())
        node = ApplicationNode(expression=self.visit(aplication), atom=self.visit(atom))
        
        return node

    def visitApplicationSimple(self, ctx:hmParser.ApplicationSimpleContext):
        
        [_,function,_,atom] = list(ctx.getChildren())
        node = ApplicationNode(expression=self.visit(function), atom=self.visit(atom))
        
        return node

    def visitAbstractionAnonimous(self, ctx:hmParser.AbstractionAnonimousContext):
        
        [_, variable, _, expression] = list(ctx.getChildren())
        variable_name = variable.getText()
        abstraction_node = AbstractionNode(variable=variable_name, expression=self.visit(expression))
        
        return abstraction_node

    def visitFunction(self, ctx:hmParser.FunctionContext):
        
        operator = ctx.getText()
        
        return FunctionNode(operator=operator)
    
    def generate_dot(self, node):
        print("entro a generate dot, varTypeMap es", self.varTypeMap, "y el nodo es", node)
        root_node = None
        if isinstance(node, ApplicationNode):
            root_node = pydot.Node(f"apl_{str(self.aplicationCount)}", label=f"@\n{self.current_type}")
            self.current_type = chr(ord(self.current_type)+1)
            self.aplicationCount += 1
            self.graph.add_node(root_node)
            
            if node.expression:
                expression_node = self.generate_dot(node.expression)
                self.graph.add_edge(pydot.Edge(root_node, expression_node))
            if node.atom:
                print("Voy a generar el nodo atom", node.atom)
                atom_node = self.generate_dot(node.atom)
                self.graph.add_edge(pydot.Edge(root_node, atom_node))
            
        elif isinstance(node, AbstractionNode):
            abstraction_node = pydot.Node(f"abs_{str(self.aplicationCount)}" ,label=f"ʎ\n{self.current_type}" )
            self.current_type = chr(ord(self.current_type)+1)
            self.abstractionCount += 1
            self.graph.add_node(abstraction_node)

            if node.variable:
                variable_node = pydot.Node(f"var_{str(self.atomCount)}",label=f"{node.variable}\n{self.current_type}")
                self.current_type = chr(ord(self.current_type)+1)
                self.atomCount += 1
                self.graph.add_node(variable_node)
                self.graph.add_edge(pydot.Edge(abstraction_node, variable_node))
            if node.expression:
                expression_node = self.generate_dot(node.expression)
                self.graph.add_node(expression_node)
                self.graph.add_edge(pydot.Edge(abstraction_node, expression_node))
            root_node = abstraction_node

        elif isinstance(node, FunctionNode):
            function_node = pydot.Node(f"func_{str(self.functionCount)}",label=f"({node.operator})\n(N->(N->N))")
            self.functionCount += 1
            self.graph.add_node(function_node)
            root_node = function_node

        elif isinstance(node, AtomNode):
            if isinstance(node.value, int):
                atom_node = pydot.Node(f"atom_{str(self.atomCount)}",label=f"{node.value}\nN")
            else:
                print("Tengo un node value", node.value, "y el mapa de tipos es", self.varTypeMap)
                if node.value in self.varTypeMap:
                    print("Encontre el tipo en el mapa de tipos")
                    node_type = self.varTypeMap[node.value]
                    atom_node = pydot.Node(f"atom_{str(self.atomCount)}",label=f"{node.value}\n{node_type}")
                else:
                    print("No encontre el tipo en el mapa de tipos")
                    self.varTypeMap[node.value] = self.current_type
                    print("Ahora el mapa de tipos es", self.varTypeMap)
                    atom_node = pydot.Node(f"atom_{str(self.atomCount)}",label=f"{node.value}\n{self.current_type}")
                    self.current_type = chr(ord(self.current_type)+1)
                
            self.atomCount += 1
            self.graph.add_node(atom_node)
            root_node = atom_node
        
        return root_node

    def generateTypeTable(self, node):
        
        def assign_type(node, type_df):
            if isinstance(node, FunctionNode):
                new_row = pd.DataFrame({'Elemento': [node.operator], 'Tipo': ['(N->(N->N))']})
                type_df = pd.concat([type_df, new_row], ignore_index=True)
            elif isinstance(node, AtomNode) and isinstance(node.value, int):
                new_row = pd.DataFrame({'Elemento': [str(node.value)], 'Tipo': ['N']})
                type_df = pd.concat([type_df, new_row], ignore_index=True)
            elif isinstance(node, ApplicationNode):
                type_df = assign_type(node.expression, type_df)
                type_df = assign_type(node.atom, type_df)
            elif isinstance(node, AbstractionNode):
                type_df = assign_type(node.expression, type_df)
            return type_df

        self.type_df = assign_type(node, self.type_df)
    
        return self.type_df

    def getTable(self):
        return self.generateTypeTable(self.root_node)

    def get_graph(self):
        return self.graph.to_string()
    
    

del hmParser