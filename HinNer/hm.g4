grammar HinNer;

expression : atom                                 #atomExpression
           | application                          #applicationExpression
           | abstraction                          #abstractionExpression
           | '(' expression ')' ;

atom : NUMBER                                     #numberAtom
     | VARIABLE                                   #variableAtom ;

application : '(' function atom ')'               #application ;

abstraction : LAMBDA VARIABLE ARROW expression    #abstraction ;

function : '+' | '-' | '*' | '/' | '%' ;

NUMBER : [0-9]+ ;
VARIABLE : [a-zA-Z][a-zA-Z0-9_]* ;
LAMBDA: '\\';
ARROW: '->';
WS : [ \t\r\n]+ -> skip ;
