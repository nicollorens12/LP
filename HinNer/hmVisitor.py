# Generated from hm.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .hmParser import hmParser
else:
    from hmParser import hmParser

# This class defines a complete generic visitor for a parse tree produced by hmParser.

class hmVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by hmParser#evaluate.
    def visitEvaluate(self, ctx:hmParser.EvaluateContext):
        return self.visitChildren(ctx)
        # Visit a parse tree produced by hmParser#evaluate.
    def visitEvaluate(self, ctx:hmParser.EvaluateContext):
        print("visitEvaluate")
        return self.visitChildren(ctx)
    # Visit a parse tree produced by hmParser#expressionAtom.
    def visitExpressionAtom(self, ctx:hmParser.ExpressionAtomContext):
        print("visitExpressionAtom")
        return self.visitChildren(ctx)
    # Visit a parse tree produced by hmParser#expressionApplication.
    def visitExpressionApplication(self, ctx:hmParser.ExpressionApplicationContext):
        print("visitExpressionApplication")
        return self.visitChildren(ctx)
    # Visit a parse tree produced by hmParser#expressionAbstraction.
    def visitExpressionAbstraction(self, ctx:hmParser.ExpressionAbstractionContext):
        print("visitExpressionAbstraction")
        return self.visitChildren(ctx)
    # Visit a parse tree produced by hmParser#expressionParenthesis.
    def visitExpressionParenthesis(self, ctx:hmParser.ExpressionParenthesisContext):
        print("visitExpressionParenthesis")
        return self.visitChildren(ctx)
    # Visit a parse tree produced by hmParser#atomNumber.
    def visitAtomNumber(self, ctx:hmParser.AtomNumberContext):
        print("visitAtomNumber")
        return self.visitChildren(ctx)
    # Visit a parse tree produced by hmParser#atomVariable.
    def visitAtomVariable(self, ctx:hmParser.AtomVariableContext):
        print("visitAtomVariable")
        return self.visitChildren(ctx)
    # Visit a parse tree produced by hmParser#applicationComposed.
    def visitApplicationComposed(self, ctx:hmParser.ApplicationComposedContext):
        print("visitApplicationComposed")
        return self.visitChildren(ctx)
    # Visit a parse tree produced by hmParser#applicationSimple.
    def visitApplicationSimple(self, ctx:hmParser.ApplicationSimpleContext):
        print("visitApplicationSimple")
        return self.visitChildren(ctx)
    # Visit a parse tree produced by hmParser#abstractionAnonimous.
    def visitAbstractionAnonimous(self, ctx:hmParser.AbstractionAnonimousContext):
        print("visitAbstractionAnonimous")
        return self.visitChildren(ctx)
    # Visit a parse tree produced by hmParser#abstractionFunction.
    def visitAbstractionFunction(self, ctx:hmParser.AbstractionFunctionContext):
        print("visitAbstractionFunction")
        return self.visitChildren(ctx)
    # Visit a parse tree produced by hmParser#function.
    def visitFunction(self, ctx:hmParser.FunctionContext):
        print("visitFunction")
        return self.visitChildren(ctx)


del hmParser