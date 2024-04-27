grammar hm;

expression : atom                                 #expressionAtom
             | application                        #expressionApplication
             | abstraction                        #expressionAbstraction
             | '(' expression ')'                 #expressionParenthesis 
             ;
           

atom : NUMBER                                     #atomNumber
     | VARIABLE                                   #atomVariable
     ;

application : '(' abstraction atom ')';            


abstraction : LAMBDA VARIABLE ARROW expression    #abstractionAnonimous 
            | function atom                       #abstractionFunction 
            | '(' function ')' atom               #abstractionFunctionParenthesis
            ;

function : '+' | '-' | '*' | '/' | '%' ;

NUMBER : [0-9]+ ;
VARIABLE : [a-zA-Z][a-zA-Z0-9_]* ;
LAMBDA: '\\';
ARROW: '->';
WS : [ \t\r\n]+ -> skip ;
