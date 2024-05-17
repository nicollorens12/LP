# Generated from hm.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .hmParser import hmParser
else:
    from hmParser import hmParser
from dataclasses import dataclass
from typing import Union
import pydot
import pandas as pd

@dataclass
class ApplicationNode:
    expression: Union['AbstractionNode', 'FunctionNode', 'ApplicationNode']
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

class hmVisitor(ParseTreeVisitor):

    def __init__(self):
        self.graph = pydot.Dot(graph_type='graph')
        self.aplicationCount = 0
        self.abstractionCount = 0
        self.functionCount = 0
        self.atomCount = 0
        self.root_node = None
        self.type_df = pd.DataFrame(columns=['Elemento', 'Tipo'])
        self.variable_types = {}
        self.current_type = 'a'
        self.evaluateType = None

    def visitEvaluate(self, ctx: hmParser.EvaluateContext):
        print("Visiting evaluate")
        [input, _] = list(ctx.getChildren())
        rule_index = ctx.getRuleIndex()
        if ctx.typeAssign():
            self.evaluateType = 'typeAssign'
        elif ctx.expression():
            self.evaluateType = 'expression'
        else:
            self.evaluateType = "Error!"

        self.root_node = self.visit(input)
        print(input.getText())
        return self.root_node

    def visitTypeAssign(self, ctx: hmParser.TypeAssignContext):
        self.evaluateType = 'typeAssign'
        [element, _, type_expression] = list(ctx.getChildren())
        elem = element.getText()
        print("Type exp is:", type_expression.getText())
        type_exp = self.visit(type_expression)
        new_row = pd.DataFrame({'Elemento': [elem], 'Tipo': [type_exp]})
        self.type_df = pd.concat([self.type_df, new_row], ignore_index=True)

    def visitTypeExpressionBasic(self, ctx: hmParser.TypeExpressionBasicContext):
        print("Visiting type expression basic")
        type_text = ctx.VARIABLE().getText()
        if ctx.typeExpression():
            type_expression = self.visit(ctx.typeExpression())
            return f"{type_text}->{type_expression}"
        else:
            return type_text

    def visitTypeExpressionParenthesis(self, ctx: hmParser.TypeExpressionParenthesisContext):
        print("Visiting type expression parenthesis")
        type_expression1 = self.visit(ctx.typeExpression(0))
        type_expression2 = self.visit(ctx.typeExpression(1))
        return f"({type_expression1})->{type_expression2}"

    def visitExpressionAtom(self, ctx: hmParser.ExpressionAtomContext):
        print("Visiting expression atom")
        [atom] = list(ctx.getChildren())
        return self.visit(atom)

    def visitExpressionApplication(self, ctx: hmParser.ExpressionApplicationContext):
        print("Visiting expression application")
        [application] = list(ctx.getChildren())
        return self.visit(application)

    def visitExpressionAbstraction(self, ctx: hmParser.ExpressionAbstractionContext):
        print("Visiting expression abstraction")
        [abstraction] = list(ctx.getChildren())
        return self.visit(abstraction)

    def visitExpressionParenthesis(self, ctx: hmParser.ExpressionParenthesisContext):
        print("Visiting expression parenthesis")
        [_, expression, _] = list(ctx.getChildren())
        return self.visit(expression)

    def visitAtomNumber(self, ctx: hmParser.AtomNumberContext):
        value = int(ctx.NUMBER().getText())
        return AtomNode(value=value)

    def visitAtomVariable(self, ctx: hmParser.AtomVariableContext):
        variable = ctx.VARIABLE().getText()
        return AtomNode(value=variable)

    def visitApplicationComposed(self, ctx: hmParser.ApplicationComposedContext):
        [aplication, atom] = list(ctx.getChildren())
        node = ApplicationNode(expression=self.visit(aplication), atom=self.visit(atom))
        return node

    def visitApplicationSimple(self, ctx: hmParser.ApplicationSimpleContext):
        [function, atom] = list(ctx.getChildren())
        node = ApplicationNode(expression=self.visit(function), atom=self.visit(atom))
        return node

    def visitAbstractionAnonimous(self, ctx: hmParser.AbstractionAnonimousContext):
        [_, variable, _, expression] = list(ctx.getChildren())
        variable_name = variable.getText()
        abstraction_node = AbstractionNode(variable=variable_name, expression=self.visit(expression))
        return abstraction_node

    def visitFunction(self, ctx: hmParser.FunctionContext):
        operator = ctx.getText()
        return FunctionNode(operator=operator)

    def generate_dot(self, node):
        def get_or_assign_type(element):
            element_str = str(element).strip()  # Asegurarse de que el elemento sea una cadena sin espacios adicionales

            # Verificar si el elemento está en type_df
            if element_str in self.type_df['Elemento'].values:
                print("Para el elemento", element_str, "entro en type_df")
                return self.type_df.loc[self.type_df['Elemento'] == element_str, 'Tipo'].values[0]
            # Verificar si el elemento está en variable_types
            elif element_str in self.variable_types:
                print("Para el elemento", element_str, "entro en variable_types")
                return self.variable_types[element_str]
            else:
                assigned_type = self.current_type
                self.current_type = chr(ord(self.current_type) + 1)
                self.variable_types[element_str] = assigned_type
                return assigned_type

        root_node = None

        if isinstance(node, ApplicationNode):
            label = f"@\n{get_or_assign_type(f'apl_{self.aplicationCount}')}"
            root_node = pydot.Node(f"apl_{str(self.aplicationCount)}", label=label)
            self.aplicationCount += 1
            self.graph.add_node(root_node)
            
            if node.expression:
                expression_node = self.generate_dot(node.expression)
                self.graph.add_edge(pydot.Edge(root_node, expression_node))
            if node.atom:
                atom_node = self.generate_dot(node.atom)
                self.graph.add_edge(pydot.Edge(root_node, atom_node))

        elif isinstance(node, AbstractionNode):
            label = f"ʎ\n{get_or_assign_type(f'abs_{self.abstractionCount}')}"
            abstraction_node = pydot.Node(f"abs_{str(self.abstractionCount)}", label=label)
            self.abstractionCount += 1
            self.graph.add_node(abstraction_node)

            if node.variable:
                variable_type = get_or_assign_type(node.variable)
                variable_node = pydot.Node(f"var_{str(self.atomCount)}", label=f"{node.variable}\n{variable_type}")
                self.atomCount += 1
                self.graph.add_node(variable_node)
                self.graph.add_edge(pydot.Edge(abstraction_node, variable_node))

            if node.expression:
                expression_node = self.generate_dot(node.expression)
                self.graph.add_edge(pydot.Edge(abstraction_node, expression_node))

            root_node = abstraction_node

        elif isinstance(node, FunctionNode):
            label = f"({node.operator})\n{get_or_assign_type(node.operator)}"
            function_node = pydot.Node(f"func_{str(self.functionCount)}", label=label)
            self.functionCount += 1
            self.graph.add_node(function_node)
            root_node = function_node

        elif isinstance(node, AtomNode):
            label = f"{node.value}\n{get_or_assign_type(node.value)}"
            atom_node = pydot.Node(f"atom_{str(self.atomCount)}", label=label)
            self.atomCount += 1
            self.graph.add_node(atom_node)
            root_node = atom_node

        return root_node

    def getTable(self):
        return self.type_df

    def get_graph(self):
        return self.graph.to_string()

del hmParser
