grammar hm;

evaluate : (expression | typeAssign) EOF;

typeAssign : (atom|function) '::' typeExpression;

typeExpression : VARIABLE ('->' typeExpression)?                     #typeExpressionBasic
               | '(' typeExpression ')' ('->' typeExpression)*        #typeExpressionParenthesis
               ;

expression : atom                                                #expressionAtom
             | application                                       #expressionApplication
             | abstraction                                       #expressionAbstraction
             | '(' expression ')'                                #expressionParenthesis 
             ;           

atom : NUMBER                                                    #atomNumber
     | VARIABLE                                                  #atomVariable
     ;              

application : application expression                             #applicationComposed
            | function expression                                #applicationSimple
            ;            

abstraction : LAMBDA VARIABLE ARROW application                  #abstractionAnonimous
            ;


function : '(' ('+' | '-' | '*' | '/' | '%') ')' ;

NUMBER : [0-9]+ ;
VARIABLE : [a-zA-Z][a-zA-Z0-9_]* ;
TYPE : [a-zA-Z][a-zA-Z0-9_]* ;
LAMBDA: '\\';
ARROW: '->';
WS : [ \t\r\n]+ -> skip ;
