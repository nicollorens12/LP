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
    root: Union['ApplicationNode','FunctionNode']
    expression: Union['AbstractionNode', 'FunctionNode', 'ApplicationNode','AtomNode']
    element: str 

@dataclass
class AbstractionNode:
    variable: str
    expression: Union['AbstractionNode', 'FunctionNode']
    element: str  

@dataclass
class FunctionNode:
    element: str

@dataclass
class AtomNode:
    element: Union[int, str]

# Clase para manejar los tipos de las variables
@dataclass
class VariableType:
    type: str
    assigned_by_user: bool


class TypeInferenceError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

        
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
                self.variable_types[element] = VariableType(type=tipo, assigned_by_user=True)

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
        self.variable_types[elem] = VariableType(type=type_exp, assigned_by_user=True)

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
        [root,expression] = list(ctx.getChildren())
        element = f"apl_{self.aplicationCount}"
        self.aplicationCount += 1
        self.get_or_assign_type(element)
        node = ApplicationNode(expression=self.visit(expression), root=self.visit(root), element=element)
        return node

    def visitApplicationSimple(self, ctx: hmParser.ApplicationSimpleContext):
        [root, expression] = list(ctx.getChildren())
        element = f"apl_{self.aplicationCount}"
        self.aplicationCount += 1
        self.get_or_assign_type(element)
        node = ApplicationNode(expression=self.visit(expression), root=self.visit(root), element=element)
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
        element_str = str(element).strip()  # Asegurarse de que el elemento sea un string sin espacios adicionales
   
        if element_str in self.type_df['Elemento'].values:
            type_value = self.type_df.loc[self.type_df['Elemento'] == element_str, 'Tipo'].values[0]
            if element_str not in self.variable_types:
                self.variable_types[element_str] = VariableType(type=type_value, assigned_by_user=True)
            return type_value

        elif element_str in self.variable_types:
            return self.variable_types[element_str].type
        else:
            assigned_type = self.current_type
            self.current_type = chr(ord(self.current_type) + 1)
            self.variable_types[element_str] = VariableType(type=assigned_type, assigned_by_user=False)
            return assigned_type

    def generate_dot(self, node):
        root_node = None
        if isinstance(node, ApplicationNode):
            label = f"@\n{self.get_or_assign_type(node.element)}"
            root_node = pydot.Node(f"{node.element}", label=label)
            self.aplicationCount += 1
            self.graph.add_node(root_node)
            if node.root:
                aux_node = self.generate_dot(node.root)
                self.graph.add_edge(pydot.Edge(root_node, aux_node))
            if node.expression:
                expression_node = self.generate_dot(node.expression)
                self.graph.add_edge(pydot.Edge(root_node, expression_node))
            

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
    
    def infer_types(self):
        if isinstance(self.root_node, ApplicationNode):
            return self.infer_application_type(self.root_node)
        elif isinstance(self.root_node, AbstractionNode):
            return self.infer_abstraction_type(self.root_node)

    def infer_abstraction_type(self,node):
        if isinstance(node, AbstractionNode):
            if isinstance(node.expression, ApplicationNode):
                result_aux = self.infer_application_type(node.expression)
                if not result_aux:
                    return False
                right_child = self.variable_types[node.expression.element]
            elif isinstance(node.expression, AbstractionNode):
                result_aux =self.infer_abstraction_type(node.expression)
                if not result_aux:
                    return False
                right_child = self.variable_types[node.expression.element]
            else:
                right_child = self.variable_types[node.expression.element]
            parent_aux = self.variable_types[node.element]
            left_child = self.variable_types[node.variable]
            result = self.eq_union(parent_aux, left_child, right_child)
            print("This is an abstraction node")
            print(f"Elements are: {node.element}, {node.variable}, {node.expression.element}")
            print(f"eq: {left_child.type} = {right_child.type} -> {parent_aux.type}")
            print("Results are:", result)

            if parent_aux.type != result[0]:
                print(f"Assigning to {node.element} the type {result[0]}")
                self.variable_types[node.element].assigned_by_user = True
                self.inference_change_table = pd.concat([self.inference_change_table, pd.DataFrame([[parent_aux.type, result[0]]], columns=['Old type', 'New type'])])
            if left_child.type != result[2]:
                print(f"Assigning to {node.variable} the type {result[2]}")
                self.variable_types[node.variable].assigned_by_user = True
                self.inference_change_table = pd.concat([self.inference_change_table, pd.DataFrame([[left_child.type, result[2]]], columns=['Old type', 'New type'])])
            if right_child.type != result[1]:
                print(f"Assigning to {node.expression.element} the type {result[1]}")
                self.variable_types[node.expression.element].assigned_by_user = True
                self.inference_change_table = pd.concat([self.inference_change_table, pd.DataFrame([[right_child.type, result[1]]], columns=['Old type', 'New type'])])
            
            self.variable_types[node.element].type = result[0]
            self.variable_types[node.expression.element].type = result[1]
            self.variable_types[node.variable].type = result[2]

            return True
            
        else:
            return False
        
    def infer_application_type(self,node): #Pending remake for two cases function expression or application atom
        if isinstance(node, ApplicationNode):
            left_child = None
            right_child = None
            parent_aux = None
            print(f"Infering types for {node.element}")
            if isinstance(node.root, ApplicationNode):
                result_aux = self.infer_application_type(node.root)
                if not result_aux:
                    return False
                left_child = self.variable_types[node.root.element]
            elif isinstance(node.root, FunctionNode):
                left_child = self.variable_types[node.root.element]
                
            print(f"left_child {str(node.root.element)}", left_child)
            if isinstance(node.expression, ApplicationNode):
                result_aux = self.infer_application_type(node.expression)
                if not result_aux:
                    return False
                right_child = self.variable_types[node.expression.element]
            elif isinstance(node.expression, AbstractionNode):
                result_aux = self.infer_abstraction_type(node.expression)
                if not result_aux:
                    return False
                right_child = self.variable_types[node.expression.element]
            elif isinstance(node.expression, FunctionNode):
                right_child  = self.variable_types[node.expression.element]
            elif isinstance(node.expression, AtomNode):
                right_child = self.variable_types[str(node.expression.element)]

            print(f"right_child {node.expression.element}", right_child)
            parent_aux = self.variable_types[node.element]
            print(f"parent_aux {node.element}", parent_aux)
            
            result = self.eq_union(left_child, right_child, parent_aux)
            print("This is an application node")
            print(f"elements are: {node.element}, {node.expression.element}, {node.root.element}")
            print(f"eq: {left_child.type} = {right_child.type} -> {parent_aux.type}")
            print("Results are:", result)
            
            if parent_aux.type != result[2]:
                print(f"Assigning to {node.element} the type {result[2]}")
                self.variable_types[node.element].assigned_by_user = True
                self.inference_change_table = pd.concat([self.inference_change_table, pd.DataFrame([[parent_aux.type, result[2]]], columns=['Old type', 'New type'])])
            if left_child.type != result[0]:
                print(f"Assigning to {node.expression.element} the type {result[0]}")
                self.variable_types[node.expression.element].assigned_by_user = True
                self.inference_change_table = pd.concat([self.inference_change_table, pd.DataFrame([[left_child.type, result[0]]], columns=['Old type', 'New type'])])
            if right_child.type != result[1]:
                print(f"Assigning to {node.root.element} the type {result[1]}")
                self.variable_types[str(node.root.element)].assigned_by_user = True
                self.inference_change_table = pd.concat([self.inference_change_table, pd.DataFrame([[right_child.type, result[1]]], columns=['Old type', 'New type'])])
            print(f"Assigning to {node.expression.element} the type {result[1]}")
            print(f"Variable type is {self.variable_types}")
            
                
            self.variable_types[node.element].type = result[2]
            self.variable_types[str(node.expression.element)].type = result[1]
            self.variable_types[str(node.root.element)].type = result[0]
            return True
        else:
            return False
       
    def eq_union(self, typeleft, type1, type2):
        if typeleft.assigned_by_user and not type1.assigned_by_user and not type2.assigned_by_user:
            print("FLAG!")
            if '->' in typeleft.type:
                last_arrow_index = typeleft.type.rindex('->')
                type1_aux = typeleft.type[:last_arrow_index]
                type2_aux = typeleft.type[last_arrow_index + 2:]
                print(f"I'm returning {typeleft.type} = {type1_aux} , {type2_aux}")
                return (typeleft.type, type1_aux, type2_aux)
            raise TypeInferenceError(f"Impossible to infer type for {typeleft.type} vs {type1.type} and {type2.type}")
        elif typeleft.assigned_by_user and type1.assigned_by_user and not type2.assigned_by_user:
            if typeleft.type.startswith(type1.type):
                remaining = typeleft.type[len(type1.type):]
                if remaining.startswith("->"):
                    remaining = remaining[2:]
                return (typeleft.type, type1.type, remaining)
            raise TypeInferenceError(f"{typeleft.type.split('->')[0]} vs {type1.type.split('->')[0]}")
        
        elif typeleft.assigned_by_user and not type1.assigned_by_user and type2.assigned_by_user:
            if typeleft.type.endswith(type2.type):
                remaining = typeleft.type[:-len(type2.type)]
                if remaining.endswith("->"):
                    remaining = remaining[:-2]
                return (typeleft.type, remaining, type2.type)
            raise TypeInferenceError(f"{typeleft.type.split('->')[0]} vs {type2.type.split('->')[0]}")
        
        elif not typeleft.assigned_by_user and type1.assigned_by_user and type2.assigned_by_user:
            #make typeleft.assign_by_user = True??
            return(type1.type + '->' + type2.type, type1.type, type2.type)
        
        elif not typeleft.assigned_by_user and not type1.assigned_by_user and not type2.assigned_by_user:
            return (typeleft.type, type1.type, type2.type)
        
        raise TypeInferenceError("Unknown error in type inference")
