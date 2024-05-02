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


    def visitEvaluate(self, ctx:hmParser.EvaluateContext):
        print("visitEvaluate")
        print("Children: ", ctx.children)
        [expression,_] = list(ctx.getChildren())
        self.root_node = self.visit(expression)
        return self.visit(expression)

    def visitExpressionAtom(self, ctx:hmParser.ExpressionAtomContext):
        print("visitExpressionAtom")
        [atom] = list(ctx.getChildren())
        return self.visit(atom)

    def visitExpressionApplication(self, ctx:hmParser.ExpressionApplicationContext):
        print("visitExpressionApplication")
        [application] = list(ctx.getChildren())
        return self.visit(application)

    def visitExpressionAbstraction(self, ctx:hmParser.ExpressionAbstractionContext):
        print("visitExpressionAbstraction")
        [abstraction] = list(ctx.getChildren())
        return self.visit(abstraction)

    def visitExpressionParenthesis(self, ctx:hmParser.ExpressionParenthesisContext):
        print("visitExpressionParenthesis")
        [_,expression,_] = list(ctx.getChildren())
        return self.visit(expression)
    
    def visitAtomNumber(self, ctx:hmParser.AtomNumberContext):
        print("visitAtomNumber")
        value = int(ctx.NUMBER().getText())
        print(AtomNode(value=value))
        return AtomNode(value=value)

    def visitAtomVariable(self, ctx:hmParser.AtomVariableContext):
        print("visitAtomVariable")
        variable = ctx.VARIABLE().getText()
        print(AtomNode(value=variable))
        return AtomNode(value=variable)

    def visitApplicationComposed(self, ctx:hmParser.ApplicationComposedContext):
        print("visitApplicationComposed")
        [aplication,atom] = list(ctx.getChildren())
        node = ApplicationNode(expression=self.visit(aplication), atom=self.visit(atom))
        print(node)
        return node

    def visitApplicationSimple(self, ctx:hmParser.ApplicationSimpleContext):
        print("visitApplicationSimple")
        [_,function,_,atom] = list(ctx.getChildren())
        node = ApplicationNode(expression=self.visit(function), atom=self.visit(atom))
        print(node)
        return node

    def visitAbstractionAnonimous(self, ctx:hmParser.AbstractionAnonimousContext):
        print("visitAbstractionAnonimous")
        [_, variable, _, expression] = list(ctx.getChildren())
        variable_name = variable.getText()
        abstraction_node = AbstractionNode(variable=variable_name, expression=self.visit(expression))
        print(abstraction_node)
        return abstraction_node

    def visitFunction(self, ctx:hmParser.FunctionContext):
        print("visitFunction")
        operator = ctx.getText()
        print(FunctionNode(operator=operator))
        return FunctionNode(operator=operator)
    
    def generate_dot(self, node):
        root_node = None
        if isinstance(node, ApplicationNode):
            root_node = pydot.Node(f"apl_{str(self.aplicationCount)}", label="@")
            self.aplicationCount += 1
            self.graph.add_node(root_node)
            print("Adding abstraction")
            if node.expression:
                expression_node = self.generate_dot(node.expression)
                if expression_node:
                    print("adding edge abstraction expresion")
                    self.graph.add_edge(pydot.Edge(root_node, expression_node))
            if node.atom:
                atom_node = self.generate_dot(node.atom)

                if atom_node:
                    print("adding edge abstraction atom")
                    self.graph.add_edge(pydot.Edge(root_node, atom_node))
            
        elif isinstance(node, AbstractionNode):
            abstraction_node = pydot.Node(f"abs_{str(self.aplicationCount)}" ,label="ʎ" )
            self.abstractionCount += 1
            self.graph.add_node(abstraction_node)
            print("Adding abstraction")
            # Add node for variable
            if node.variable:
                variable_node = pydot.Node(f"var_{str(self.atomCount)}",label=f"{node.variable}")
                self.atomCount += 1
                self.graph.add_node(variable_node)
                print("adding abstraction atom")
                self.graph.add_edge(pydot.Edge(abstraction_node, variable_node))
                print("addgin edge abstraction atom")
            
            expression_node = self.generate_dot(node.expression)
            if expression_node:
                # Create a new node for each abstraction
                print("adding abstraction expresion node")
                self.graph.add_node(expression_node)
                self.graph.add_edge(pydot.Edge(abstraction_node, expression_node))
                print("adding abstraction expresion edge")
            root_node = abstraction_node
        elif isinstance(node, FunctionNode):
            function_node = pydot.Node(f"func_{str(self.functionCount)}",label=f"({node.operator})")
            self.functionCount += 1
            print("Adding node function")
            self.graph.add_node(function_node)
            root_node = function_node
        elif isinstance(node, AtomNode):
            print("adding node atom")
            atom_node = pydot.Node(f"atom_{str(self.atomCount)}",label=f"{node.value}")
            self.atomCount += 1
            self.graph.add_node(atom_node)
            root_node = atom_node
        
        return root_node

    def generateTypeTable(self, node):
        type_table = {}
    
        def assign_type(node):
            nonlocal type_counter
            if isinstance(node, ApplicationNode) or isinstance(node, AbstractionNode):
                type_table[node] = type_counter
                type_counter = chr(ord(type_counter) + 1)
    
                if node.expression:
                    assign_type(node.expression)
                if node.atom:
                    assign_type(node.atom)
            elif isinstance(node, FunctionNode):
                type_table[node] = 'N->N->N'
            elif isinstance(node, AtomNode):
                # Omitir Atomos Variable
                pass
            
        type_counter = 'a'
        assign_type(node)
    
        # Convertir el diccionario en DataFrame de Pandas
        type_df = pd.DataFrame.from_dict(type_table, orient='index', columns=['Tipo']).reset_index()
        type_df = type_df.rename(columns={'index': 'Elemento'})
    
        return type_df


    def getTable(self):
        return self.generateTypeTable(self.root_node)

    def get_graph(self):
        return self.graph.to_string()

del hmParser