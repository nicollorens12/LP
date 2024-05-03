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
        root_node = None
        if isinstance(node, ApplicationNode):
            root_node = pydot.Node(f"apl_{str(self.aplicationCount)}", label="@")
            self.aplicationCount += 1
            self.graph.add_node(root_node)
            
            if node.expression:
                expression_node = self.generate_dot(node.expression)
                if expression_node:
                    
                    self.graph.add_edge(pydot.Edge(root_node, expression_node))
            if node.atom:
                atom_node = self.generate_dot(node.atom)

                if atom_node:
                    
                    self.graph.add_edge(pydot.Edge(root_node, atom_node))
            
        elif isinstance(node, AbstractionNode):
            abstraction_node = pydot.Node(f"abs_{str(self.aplicationCount)}" ,label="ʎ" )
            self.abstractionCount += 1
            self.graph.add_node(abstraction_node)
            
            # Add node for variable
            if node.variable:
                variable_node = pydot.Node(f"var_{str(self.atomCount)}",label=f"{node.variable}")
                self.atomCount += 1
                self.graph.add_node(variable_node)
                
                self.graph.add_edge(pydot.Edge(abstraction_node, variable_node))
                
            
            expression_node = self.generate_dot(node.expression)
            if expression_node:
                # Create a new node for each abstraction
                
                self.graph.add_node(expression_node)
                self.graph.add_edge(pydot.Edge(abstraction_node, expression_node))
                
            root_node = abstraction_node
        elif isinstance(node, FunctionNode):
            function_node = pydot.Node(f"func_{str(self.functionCount)}",label=f"({node.operator})")
            self.functionCount += 1
            
            self.graph.add_node(function_node)
            root_node = function_node
        elif isinstance(node, AtomNode):
            
            atom_node = pydot.Node(f"atom_{str(self.atomCount)}",label=f"{node.value}")
            self.atomCount += 1
            self.graph.add_node(atom_node)
            root_node = atom_node
        
        return root_node

    def generateTypeTable(self, node):
        type_df = pd.DataFrame(columns=['Elemento', 'Tipo'])
    
        def assign_type(node, type_df):
            if isinstance(node, FunctionNode):
                if node.operator.isdigit():
                    new_row = pd.DataFrame({'Elemento': [node.operator], 'Tipo': ['N->N->N']})
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
    
        type_df = assign_type(node, type_df)
    
        return type_df








    def getTable(self):
        return self.generateTypeTable(self.root_node)

    def get_graph(self):
        return self.graph.to_string()

del hmParser