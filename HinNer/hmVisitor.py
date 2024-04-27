# Generated from hm.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .hmParser import hmParser
else:
    from hmParser import hmParser

# This class defines a complete generic visitor for a parse tree produced by hmParser.

class hmVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by hmParser#expressionAtom.
    def visitExpressionAtom(self, ctx:hmParser.ExpressionAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by hmParser#expressionApplication.
    def visitExpressionApplication(self, ctx:hmParser.ExpressionApplicationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by hmParser#expressionAbstraction.
    def visitExpressionAbstraction(self, ctx:hmParser.ExpressionAbstractionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by hmParser#expressionParenthesis.
    def visitExpressionParenthesis(self, ctx:hmParser.ExpressionParenthesisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by hmParser#atomNumber.
    def visitAtomNumber(self, ctx:hmParser.AtomNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by hmParser#atomVariable.
    def visitAtomVariable(self, ctx:hmParser.AtomVariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by hmParser#application.
    def visitApplication(self, ctx:hmParser.ApplicationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by hmParser#abstractionAnonimous.
    def visitAbstractionAnonimous(self, ctx:hmParser.AbstractionAnonimousContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by hmParser#abstractionFunction.
    def visitAbstractionFunction(self, ctx:hmParser.AbstractionFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by hmParser#function.
    def visitFunction(self, ctx:hmParser.FunctionContext):
        return self.visitChildren(ctx)



del hmParser