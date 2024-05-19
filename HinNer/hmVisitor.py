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
import re

@dataclass
class ApplicationNode:
    expression: Union['AbstractionNode', 'FunctionNode', 'ApplicationNode']
    atom: Union['AtomNode']
    element: str  # Nuevo campo para almacenar el elemento asociado al nodo

@dataclass
class AbstractionNode:
    variable: str
    expression: Union['AbstractionNode', 'FunctionNode']
    element: str  # Nuevo campo para almacenar el elemento asociado al nodo

@dataclass
class FunctionNode:
    element: str

@dataclass
class AtomNode:
    element: Union[int, str]



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
        self.inference_change_table = None

    def visitEvaluate(self, ctx: hmParser.EvaluateContext):
        [input, _] = list(ctx.getChildren())
        if ctx.typeAssign():
            self.evaluateType = 'typeAssign'
        elif ctx.expression():
            self.evaluateType = 'expression'
            for index, row in self.type_df.iterrows():
                element = row['Elemento']
                tipo = row['Tipo']
                self.variable_types[element] = tipo

        else:
            self.evaluateType = "Error!"

        self.root_node = self.visit(input)
        return self.root_node

    def visitTypeAssign(self, ctx: hmParser.TypeAssignContext):
        self.evaluateType = 'typeAssign'
        [element, _, type_expression] = list(ctx.getChildren())
        elem = element.getText()
        type_exp = self.visit(type_expression)
        new_row = pd.DataFrame({'Elemento': [elem], 'Tipo': [type_exp]})
        self.type_df = pd.concat([self.type_df, new_row], ignore_index=True)
        self.variable_types[elem] = type_exp

    def visitTypeExpressionBasic(self, ctx: hmParser.TypeExpressionBasicContext):
        type_text = ctx.VARIABLE().getText()
        if ctx.typeExpression():
            type_expression = self.visit(ctx.typeExpression())
            return f"{type_text}->{type_expression}"
        else:
            return type_text

    def visitTypeExpressionParenthesis(self, ctx: hmParser.TypeExpressionParenthesisContext):
        [_,type_expression1,_,_,type_expression2] = list(ctx.getChildren())
        vtype_expression1 = self.visit(type_expression1)
        vtype_expression2 = self.visit(type_expression2)
        return f"({vtype_expression1})->{vtype_expression2}"

    def visitExpressionAtom(self, ctx: hmParser.ExpressionAtomContext):
        [atom] = list(ctx.getChildren())
        return self.visit(atom)

    def visitExpressionApplication(self, ctx: hmParser.ExpressionApplicationContext):
        [application] = list(ctx.getChildren())
        return self.visit(application)

    def visitExpressionAbstraction(self, ctx: hmParser.ExpressionAbstractionContext):
        [abstraction] = list(ctx.getChildren())
        return self.visit(abstraction)

    def visitExpressionParenthesis(self, ctx: hmParser.ExpressionParenthesisContext):
        [_, expression, _] = list(ctx.getChildren())
        return self.visit(expression)

    def visitAtomNumber(self, ctx: hmParser.AtomNumberContext):
        value = int(ctx.NUMBER().getText())
        self.get_or_assign_type(value)
        return AtomNode(element=value)

    def visitAtomVariable(self, ctx: hmParser.AtomVariableContext):
        variable = ctx.VARIABLE().getText()
        self.get_or_assign_type(variable)
        return AtomNode(element=variable)

    def visitApplicationComposed(self, ctx: hmParser.ApplicationComposedContext):
        [aplication, atom] = list(ctx.getChildren())
        element = f"apl_{self.aplicationCount}"
        self.aplicationCount += 1
        self.get_or_assign_type(element)
        node = ApplicationNode(expression=self.visit(aplication), atom=self.visit(atom), element=element)
        return node

    def visitApplicationSimple(self, ctx: hmParser.ApplicationSimpleContext):
        [function, atom] = list(ctx.getChildren())
        element = f"apl_{self.aplicationCount}"
        self.aplicationCount += 1
        self.get_or_assign_type(element)
        node = ApplicationNode(expression=self.visit(function), atom=self.visit(atom), element=element)
        return node

    def visitAbstractionAnonimous(self, ctx: hmParser.AbstractionAnonimousContext):
        [_, variable, _, expression] = list(ctx.getChildren())
        variable_name = variable.getText()
        element = f"abs_{self.abstractionCount}"
        self.abstractionCount += 1
        self.get_or_assign_type(element)
        abstraction_node = AbstractionNode(variable=variable_name, expression=self.visit(expression), element=element)
        return abstraction_node

    def visitFunction(self, ctx: hmParser.FunctionContext):
        element = ctx.getText()
        self.get_or_assign_type(element)
        return FunctionNode(element=element)

    def get_or_assign_type(self,element):
            element_str = str(element).strip()  # Asegurarse de que el elemento sea una cadena sin espacios adicionales
            # Verificar si el elemento está en type_df
            if element_str in self.type_df['Elemento'].values:
                return self.type_df.loc[self.type_df['Elemento'] == element_str, 'Tipo'].values[0]
            # Verificar si el elemento está en variable_types
            elif element_str in self.variable_types:
                return self.variable_types[element_str]
            else:
                assigned_type = self.current_type
                self.current_type = chr(ord(self.current_type) + 1)
                self.variable_types[element_str] = assigned_type
                return assigned_type

    def generate_dot(self, node):
        root_node = None
        if isinstance(node, ApplicationNode):
            label = f"@\n{self.get_or_assign_type(node.element)}"
            root_node = pydot.Node(f"{node.element}", label=label)
            self.aplicationCount += 1
            self.graph.add_node(root_node)
            
            if node.expression:
                expression_node = self.generate_dot(node.expression)
                self.graph.add_edge(pydot.Edge(root_node, expression_node))
            if node.atom:
                atom_node = self.generate_dot(node.atom)
                self.graph.add_edge(pydot.Edge(root_node, atom_node))

        elif isinstance(node, AbstractionNode):
            label = f"ʎ\n{self.get_or_assign_type(node.element)}"
            abstraction_node = pydot.Node(f"{node.element}", label=label)
            self.abstractionCount += 1
            self.graph.add_node(abstraction_node)

            if node.variable:
                variable_type = self.get_or_assign_type(node.variable)
                variable_node = pydot.Node(f"var_{str(self.atomCount)}", label=f"{node.variable}\n{variable_type}")
                self.atomCount += 1
                self.graph.add_node(variable_node)
                self.graph.add_edge(pydot.Edge(abstraction_node, variable_node))

            if node.expression:
                expression_node = self.generate_dot(node.expression)
                self.graph.add_edge(pydot.Edge(abstraction_node, expression_node))

            root_node = abstraction_node

        elif isinstance(node, FunctionNode):
            label = f"({node.element})\n{self.get_or_assign_type(node.element)}"
            function_node = pydot.Node(f"func_{str(self.functionCount)}", label=label)
            self.functionCount += 1
            self.graph.add_node(function_node)
            root_node = function_node

        elif isinstance(node, AtomNode):
            label = f"{node.element}\n{self.get_or_assign_type(node.element)}"
            atom_node = pydot.Node(f"atom_{str(self.atomCount)}", label=label)
            self.atomCount += 1
            self.graph.add_node(atom_node)
            root_node = atom_node

        return root_node
    
    def generate_new_dot(self):
        self.graph = pydot.Dot(graph_type='graph')
        self.generate_dot(self.root_node)

    def getTable(self):
        return self.type_df

    def get_graph(self):
        return self.graph.to_string()
    
    def infer_type(self):
        if isinstance(self.root_node, ApplicationNode):
            return self.infer_application_type(self.root_node)
        elif isinstance(self.root_node, AbstractionNode):
            return self.infer_abstraction_type(self.root_node)

    def infer_abstraction_type(self,node):
        print(f"Variable types: {self.variable_types}")
        if isinstance(node, AbstractionNode):
            
            if isinstance(node.expression, ApplicationNode):
                self.infer_application_type(node.expression)
                right_child_type = self.variable_types[node.expression.element]
            elif isinstance(node.expression, AbstractionNode):
                self.infer_abstraction_type(node.expression)
                right_child_type = self.variable_types[node.expression.element]
            else:
                right_child_type = self.variable_types[node.expression.element]
            parent_type_aux = self.variable_types[node.element]
            left_child_type = self.variable_types[node.variable]
            result = self.eq_union(parent_type_aux, left_child_type, right_child_type)

            if result[0]:
                self.variable_types[node.element] = result[1]
                self.variable_types[node.expression.element] = result[2]
                self.variable_types[node.variable] = result[3]

                if parent_type_aux != result[3]:
                    self.inference_change_table = pd.concat([self.inference_change_table, pd.DataFrame([[parent_type_aux, result[3]]], columns=['Old type', 'New type'])])
                if left_child_type != result[1]:
                    self.inference_change_table = pd.concat([self.inference_change_table, pd.DataFrame([[left_child_type, result[1]]], columns=['Old type', 'New type'])])
                if right_child_type != result[2]:
                    self.inference_change_table = pd.concat([self.inference_change_table, pd.DataFrame([[right_child_type, result[2]]], columns=['Old type', 'New type'])])
                return True
            else:
                return False
        else:
            return True
        
    def infer_application_type(self,node):
        if isinstance(node, ApplicationNode):
            right_child_type = self.variable_types[str(node.atom.element)]
            if isinstance(node.expression, ApplicationNode):
                self.infer_application_type(node.expression)
                left_child_type = self.variable_types[node.expression.element]
            elif isinstance(node.expression, AbstractionNode):
                left_child_type = self.variable_types[node.expression.element]
            else:
                left_child_type = self.variable_types[node.expression.element]
            parent_type_aux = self.variable_types[node.element]
            result = self.eq_union(left_child_type, right_child_type, parent_type_aux)

            if result[0]:
                self.variable_types[node.element] = result[3]
                self.variable_types[node.expression.element] = result[1]
                self.variable_types[node.atom.element] = result[2]

                if parent_type_aux != result[3]:
                    self.inference_change_table = pd.concat([self.inference_change_table, pd.DataFrame([[parent_type_aux, result[3]]], columns=['Old type', 'New type'])])
                if left_child_type != result[1]:
                    self.inference_change_table = pd.concat([self.inference_change_table, pd.DataFrame([[left_child_type, result[1]]], columns=['Old type', 'New type'])])
                if right_child_type != result[2]:
                    self.inference_change_table = pd.concat([self.inference_change_table, pd.DataFrame([[right_child_type, result[2]]], columns=['Old type', 'New type'])])
                return True
            else:
                return False
        else:
            return True
                
            
    def eq_union(self, typeleft, type1, type2):
        print(f"Typeleft: {typeleft}, Type1: {type1}, Type2: {type2}")
        # Caso cuando typeleft es exactamente la concatenación de type1 y type2
        if typeleft == type1 + '->' + type2:
            print("Equal thing")
            return (True,typeleft, type1, type2)
        
        elif len(typeleft) == (len(type1) + 2 + len(type2)) :
            print("Equal size")
            # Verificar si typeleft contiene '->' en alguna parte
            if '->' in typeleft:
                print("FLAG")
                # Encontrar la última aparición de '->' en typeleft
                last_arrow_index = typeleft.rindex('->')
                # Extraer type1 hasta antes del último '->'
                type1 = typeleft[:last_arrow_index]
                # Extraer type2 desde después del último '->'
                type2 = typeleft[last_arrow_index + 2:]
                print(f"Type1: {type1}, Type2: {type2}")
                return (True,typeleft, type1, type2)
            return (False, typeleft, type1, type2)
            
        # Caso cuando el largo de typeleft es mayor que la suma de los largos de type1 y type2
        elif len(typeleft) > (len(type1) + 2 + len(type2)):
            print("Greater than")
            # Verificar si typeleft empieza con type1
            if typeleft.startswith(type1):
                # Extraer el resto de typeleft después de type1
                remaining = typeleft[len(type1):]
                if remaining.startswith("->"):
                    remaining = remaining[2:]
                print(f"Remaining: {remaining}")
                return (True,typeleft, type1, remaining)

            # Verificar si typeleft termina con type2
            if typeleft.endswith(type2):
                # Extraer el inicio de typeleft antes de type2
                remaining = typeleft[:-len(type2)]
                print(f"Remaining: {remaining}")
                if remaining.endswith("->"):
                    remaining = remaining[:-2]
                return (True,typeleft, remaining, type2)
            return (False, typeleft, type1, type2)
        elif len(typeleft) == 1:
            typeleft = type1 + '->' + type2
            return (True,typeleft, type1, type2)
        
        print("ELSE")
        return (False,type1, type1, type2)


        

del hmParser
