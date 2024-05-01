# Generated from hm.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .hmParser import hmParser
else:
    from hmParser import hmParser
from dataclasses import dataclass
from typing import Union, List
import pydot

@dataclass
class ApplicationNode:
    abstraction: Union['AbstractionNode', 'FunctionNode']
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

    def visitEvaluate(self, ctx:hmParser.EvaluateContext):
        print("visitEvaluate")
        print("Children: ", ctx.children)
        [expression,_] = list(ctx.getChildren())
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
        node = ApplicationNode(abstraction=self.visit(aplication), atom=self.visit(atom))
        print(node)
        return node

    def visitApplicationSimple(self, ctx:hmParser.ApplicationSimpleContext):
        print("visitApplicationSimple")
        [_,function,_,atom] = list(ctx.getChildren())
        node = ApplicationNode(abstraction=self.visit(function), atom=self.visit(atom))
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
        if isinstance(node, ApplicationNode):
            self.graph.add_node(pydot.Node("@"))
            if node.abstraction:
                abstraction_node = self.generate_dot(node.abstraction)
                if abstraction_node:
                    self.graph.add_edge(pydot.Edge("@", abstraction_node))
            if node.atom:
                atom_node = self.generate_dot(node.atom)
                if atom_node:
                    self.graph.add_edge(pydot.Edge("@", atom_node))
        elif isinstance(node, AbstractionNode):
            abstraction_node = pydot.Node("ʎ")
            self.graph.add_node(abstraction_node)
            expression_node = self.generate_dot(node.expression)
            if expression_node:
                self.graph.add_edge(pydot.Edge(abstraction_node, expression_node))
            return abstraction_node
        elif isinstance(node, FunctionNode):
            function_node = pydot.Node(f"({node.operator})")
            self.graph.add_node(function_node)
            return function_node
        elif isinstance(node, AtomNode):
            atom_node = pydot.Node(f"{node.value}")
            self.graph.add_node(atom_node)
            return atom_node

    def get_graph(self):
        return self.graph.to_string()

del hmParser