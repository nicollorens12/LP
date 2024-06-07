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
    root: Union['ApplicationNode','FunctionNode']
    expression: Union['AbstractionNode', 'FunctionNode', 'ApplicationNode','AtomNode']
    element: str 

@dataclass
class AbstractionNode:
    variable: str
    expression: Union['AbstractionNode', 'ApplicationNode','AtomNode']
    element: str  

@dataclass
class FunctionNode:
    element: str

@dataclass
class AtomNode:
    element: Union[int, str]

@dataclass
class VariableType:
    type: str
    polymorphic: bool
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
        if ctx.expression():
            self.evaluateType = 'expression'
            for index, row in self.type_df.iterrows():
                element = row['Elemento']
                tipo = row['Tipo']
                self.variable_types[element] = VariableType(type=tipo, polymorphic=self.is_polymorphic(tipo) ,assigned_by_user=True)
        else:
            self.evaluateType = "Error!"
            
        self.root_node = self.visit(input)
        return self.root_node

    def visitTypeAssign(self, ctx:hmParser.TypeAssignContext):
        self.evaluateType = 'typeAssign'
        [element, _, type_expression] = list(ctx.getChildren())
        if element.getText() in self.type_df['Elemento'].values:
            matching_rows = self.type_df.loc[self.type_df['Elemento'] == element.getText()]
            if not matching_rows.empty:
                if matching_rows.iloc[0]['Tipo'] != type_expression.getText():
                    raise TypeInferenceError(f"{element.getText()} already has a different type assigned")
                else:
                    return
        else:
            elem = element.getText()
            type_exp = self.visit(type_expression)
            new_row = pd.DataFrame({'Elemento': [elem], 'Tipo': [type_exp]})
            self.type_df = pd.concat([self.type_df, new_row], ignore_index=True)
            self.variable_types[elem] = VariableType(type=type_exp, polymorphic=self.is_polymorphic(type_exp) , assigned_by_user=True)
            
    def visitTypeExpressionBasic(self, ctx: hmParser.TypeExpressionBasicContext):
        type_text = ctx.VARIABLE().getText()
        if ctx.typeExpression():
            type_expression = self.visit(ctx.typeExpression())
            return f"{type_text}->{type_expression}"
        else:
            return type_text
        
    def visitTypeExpressionParenthesis(self, ctx: hmParser.TypeExpressionParenthesisContext):
        [_,type_expression,_] = list(ctx.getChildren())
        return f"({self.visit(type_expression)})"


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

    # Visit a parse tree produced by hmParser#functionArithmetic.
    def visitFunctionArithmetic(self, ctx:hmParser.FunctionArithmeticContext):
        element = ctx.getText()
        self.get_or_assign_type(element)
        return FunctionNode(element=element)


    # Visit a parse tree produced by hmParser#functionVariable.
    def visitFunctionVariable(self, ctx:hmParser.FunctionVariableContext):
        element = ctx.getText()
        self.get_or_assign_type(element)
        return FunctionNode(element=element)
    
    def get_or_assign_type(self,element):
        element_str = str(element).strip()
   
        if element_str in self.type_df['Elemento'].values:
            type_value = self.type_df.loc[self.type_df['Elemento'] == element_str, 'Tipo'].values[0]
            if element_str not in self.variable_types:
                self.variable_types[element_str] = VariableType(type=type_value, assigned_by_user=True)
            return type_value

        elif element_str in self.variable_types:
            return self.variable_types[element_str].type
        else:
            
            while self.check_type_availability():
                self.current_type = chr(ord(self.current_type) + 1)
            if self.current_type == 'z':
                raise TypeInferenceError("Cannot infer more types")
            assigned_type = self.current_type
            self.current_type = chr(ord(self.current_type) + 1)
            self.variable_types[element_str] = VariableType(type=assigned_type, polymorphic=False ,assigned_by_user=False)
            return assigned_type
        
    def check_type_availability(self):
        return any(self.current_type in var_type.type for var_type in self.variable_types.values())

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

            if parent_aux.type != result[0]:
                self.variable_types[node.element].assigned_by_user = True
                self.inference_change_table = pd.concat([self.inference_change_table, pd.DataFrame([[parent_aux.type, result[0]]], columns=['Old type', 'New type'])])
            if left_child.type != result[2]:
                self.variable_types[node.variable].assigned_by_user = True
                self.inference_change_table = pd.concat([self.inference_change_table, pd.DataFrame([[left_child.type, result[2]]], columns=['Old type', 'New type'])])
            if right_child.type != result[1]:
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
            if isinstance(node.root, ApplicationNode):
                result_aux = self.infer_application_type(node.root)
                if not result_aux:
                    return False
                left_child = self.variable_types[node.root.element]
            elif isinstance(node.root, FunctionNode):
                left_child = self.variable_types[node.root.element]

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

            parent_aux = self.variable_types[node.element]     
            result = self.eq_union(left_child, right_child, parent_aux)

            if parent_aux.type != result[2]:
                self.variable_types[node.element].assigned_by_user = True
                self.inference_change_table = pd.concat([self.inference_change_table, pd.DataFrame([[parent_aux.type, result[2]]], columns=['Old type', 'New type'])])
            if left_child.type != result[0]:
                self.variable_types[node.expression.element].assigned_by_user = True
                self.inference_change_table = pd.concat([self.inference_change_table, pd.DataFrame([[left_child.type, result[0]]], columns=['Old type', 'New type'])])
            if right_child.type != result[1]:
                self.variable_types[str(node.root.element)].assigned_by_user = True
                self.inference_change_table = pd.concat([self.inference_change_table, pd.DataFrame([[right_child.type, result[1]]], columns=['Old type', 'New type'])])
           
            self.variable_types[node.element].type = result[2]
            self.variable_types[str(node.expression.element)].type = result[1]
            self.variable_types[str(node.root.element)].type = result[0]
            return True
        else:
            return False
       
    def eq_union(self, typeleft, type1, type2):

        if typeleft.type.startswith('(') and typeleft.type.endswith(')'):
            typeleft.type = typeleft.type[1:-1]

        if typeleft.assigned_by_user and not type1.assigned_by_user and not type2.assigned_by_user:
            if not typeleft.polymorphic:
                if '->' in typeleft.type:
                    last_arrow_index = self.find_last_arrow_outside_parentheses(typeleft.type)
                    type2_aux = typeleft.type[:last_arrow_index]
                    type1_aux = typeleft.type[last_arrow_index + 2:]
                    return (typeleft.type, type1_aux, type2_aux)
                raise TypeInferenceError(f" Impossible to infer type for {typeleft.type} vs {type1.type} and {type2.type}")
            else:
                result = self.infer_polymorphic_type_simple(typeleft.type)
                type1.type = result[1]
                type1.polymorphic = True
                type2.type = result[2]
                type2.polymorphic = True
                return (typeleft.type, type1.type, type2.type)
            
        
        elif typeleft.assigned_by_user and type1.assigned_by_user and not type2.assigned_by_user:
            if not typeleft.polymorphic:
                if typeleft.type.startswith(type1.type):
                    remaining = typeleft.type[len(type1.type):]
                    if remaining.startswith("->"):
                        remaining = remaining[2:]
                    return (typeleft.type, type1.type, remaining)
                raise TypeInferenceError(f" Cannot infer: {typeleft.type.split('->')[0]} vs {type1.type.split('->')[0]}")
            else:
                result = self.infer_polymorphic_type(typeleft.type,type1.type)
                
                return result
        elif typeleft.assigned_by_user and not type1.assigned_by_user and type2.assigned_by_user:
            if typeleft.type.endswith(type2.type):
                remaining = typeleft.type[:-len(type2.type)]
                if remaining.endswith("->"):
                    remaining = remaining[:-2]
                return (typeleft.type, remaining, type2.type)
            raise TypeInferenceError(f"{typeleft.type.split('->')[0]} vs {type2.type.split('->')[0]}")
            
        
        elif not typeleft.assigned_by_user and type1.assigned_by_user and type2.assigned_by_user:
            return(type1.type + '->' + type2.type, type1.type, type2.type)
        
        elif not typeleft.assigned_by_user and not type1.assigned_by_user and not type2.assigned_by_user:
            return (typeleft.type, type1.type, type2.type)
        
        elif not typeleft.assigned_by_user and not type1.assigned_by_user and type2.assigned_by_user:
            return(type1.type + '->' + type2.type, type1.type, type2.type)
        
        elif not typeleft.assigned_by_user and type1.assigned_by_user and not type2.assigned_by_user:
            if typeleft.polymorphic:
                return self.infer_polymorphic_type(typeleft.type, type1.type)
            else:
                return (type1.type + '->' + type2.type, type1.type, type2.type)

                
    def find_last_arrow_outside_parentheses(self,type_string):
        parenthesis_count = 0
        for i in range(len(type_string) - 1, -1, -1):
            if type_string[i] == ')':
                parenthesis_count += 1
            elif type_string[i] == '(':
                parenthesis_count -= 1
            elif type_string[i:i + 2] == '->' and parenthesis_count == 0:
                return i
        return -1

    def infer_polymorphic_type(self,polymorphic_type, concrete_type):
        poly_parts = polymorphic_type.split('->')
        concrete_parts = concrete_type.split('->')
        if len(poly_parts) < len(concrete_parts):
            raise TypeInferenceError(f"Cannot infer type for {polymorphic_type} vs {concrete_type}")
        var_map = {}
        for i in range(len(concrete_parts)):
            if poly_parts[i][0].islower():
                var_map[poly_parts[i]] = concrete_parts[i]
            elif poly_parts[i] != concrete_parts[i]:
                raise TypeInferenceError(f"Cannot infer type for {polymorphic_type} vs {concrete_type}")
        remaining_type = '->'.join(poly_parts[len(concrete_parts):])
        for key, value in var_map.items():
            remaining_type = remaining_type.replace(key, value)
        return (polymorphic_type, concrete_type, remaining_type)
    
    def infer_polymorphic_type_simple(self, polymorphic_type):
        type_parts = polymorphic_type.split('->')
        type1 = type_parts[0]
        type2 = '->'.join(type_parts[1:])
        return (polymorphic_type, type1, type2)

    
    def is_polymorphic(self, type_string):
        return any([char.islower() for char in type_string])
