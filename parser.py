import ply.yacc as yacc
from lexer import tokens
import sys
from SymbolTable import *
from MachineCode import *
from Expression import *

symbol_table = SymbolTable()
code = MachineCode();

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)


def p_program_declaration(p):
    'program : DECLARE declarations BEGIN commands END'


def p_program_begin(p):
    'program : BEGIN commands END'


def p_declarations_declarations_pidentifier(p):
    'declarations : declarations COMMA pidentifier'
    symbol_table.add_variable(p[3])


def p_declarations_declarations_pidentifier_num(p):
    'declarations : declarations COMMA pidentifier LPAREN num COLON num RPAREN'
    symbol_table.add_table(p[3], p[5], p[7])


def p_declarations_pidentifier(p):
    'declarations : pidentifier'
    symbol_table.add_variable(p[1])


def p_declarations_pidentifier_num(p):
    'declarations : pidentifier LPAREN num COLON num RPAREN'
    symbol_table.add_table(p[1], p[3], p[5])


def p_commands_commands_command(p):
    'commands : commands command'
    if p[1] is None:
        p[1] = Command(0)
    p[1] = Command(p[1].counter + p[2].counter)
    p[0] = p[1]


def p_commands_command(p):
    'commands : command'
    p[0] = Command(p[1].counter)


def p_command_identifier_expression(p):
    'command : identifier ASSIGN expression SEMICOLON'
    s1 = len(code.code)
    code.assign(p[3].register, p[1])
    if isinstance(p[1], list):
        p[1][0]['value'] = 0
    else:
        p[1]['value'] = 0
    s2 = len(code.code)
    p[0] = Command(s2-s1+p[3].counter)


def p_command_if_else(p):
    'command : IF condition THEN commands ELSE commands ENDIF'
    s1 = len(code.code)
    s2 = len(code.code)
    p[0] = Command(s2-s1)
    #print("IF_ELSE: ", p[4].counter, p[6].counter)


def p_command_if(p):
    'command : IF condition THEN commands ENDIF'
    s1 = len(code.code)
    s2 = len(code.code)
    p[0] = Command(s2 - s1)


def p_command_while(p):
    'command : WHILE condition DO commands ENDWHILE'
    s1 = len(code.code)
    s2 = len(code.code)
    p[0] = Command(s2 - s1)


def p_command_repeat_until(p):
    'command : REPEAT commands UNTIL condition SEMICOLON'
    s1 = len(code.code)
    s2 = len(code.code)
    p[0] = Command(s2 - s1)


def p_command_for(p):
    'command : FOR pidentifier FROM value TO value DO commands ENDFOR'
    s1 = len(code.code)
    s2 = len(code.code)
    p[0] = Command(s2 - s1)


def p_command_for_downto(p):
    'command : FOR pidentifier FROM value DOWNTO value DO commands ENDFOR'
    s1 = len(code.code)
    s2 = len(code.code)
    p[0] = Command(s2 - s1)


def p_read(p):
    'command : READ identifier SEMICOLON'
    s1 = len(code.code)
    code.read(p[2])
    p[2][0]['is_in_memory'] = 1
    p[2][0]['value'] = 0
    s2 = len(code.code)
    p[0] = Command(s2 - s1)


def p_write(p):
    'command : WRITE value SEMICOLON'
    s1 = len(code.code)
    code.write(p[2])
    if isinstance(p[2], list):
        p[2] = p[2][0]
    p[2]['is_in_memory'] = 1
    s2 = len(code.code)
    p[0] = Command(s2 - s1)


def p_expression_value(p):
    'expression : value'
    s1 = len(code.code)
    reg = code.expression_1(p[1])
    s2 = len(code.code)
    p[0] = Expression(reg, s2-s1)


def p_expression_plus(p):
    'expression : value PLUS value'
    s1 = len(code.code)
    reg = code.expression_plus_minus(p[1], p[3], p[2])
    s2 = len(code.code)
    p[0] = Expression(reg, s2-s1)


def p_expression_minus(p):
    'expression : value MINUS value'
    s1 = len(code.code)
    reg = code.expression_plus_minus(p[1], p[3], p[2])
    s2 = len(code.code)
    p[0] = Expression(reg, s2-s1)


def p_expression_times(p):
    'expression : value TIMES value'
    s1 = len(code.code)
    reg = code.expression_times(p[1], p[3])
    s2 = len(code.code)
    p[0] = Expression(reg, s2-s1)


def p_expression_divide(p):
    'expression : value DIVIDE value'
    s1 = len(code.code)
    reg = code.expression_divide(p[1], p[3])
    s2 = len(code.code)
    p[0] = Expression(reg, s2-s1)


def p_expression_modulo(p):
    'expression : value MODULO value'
    s1 = len(code.code)
    reg = code.expression_modulo(p[1], p[3])
    s2 = len(code.code)
    p[0] = Expression(reg, s2-s1)


def p_condition_equal(p):
    'condition : value EQUALS value'


def p_condition_not_equal(p):
    'condition : value NOTEQUALS value'


def p_condition_lesser(p):
    'condition : value LESSER value'


def p_condition_greater(p):
    'condition : value GREATER value'


def p_condition_leq(p):
    'condition : value LEQ value'


def p_condition_geq(p):
    'condition : value GEQ value'


def p_value_num(p):
    'value : num'
    p[0] = symbol_table.get_num(p[1])


def p_value_identifier(p):
    'value : identifier'
    p[0] = p[1]


def p_identifier_pidentifier(p):
    'identifier : pidentifier'
    p[0] = symbol_table.get_variable(p[1])


def p_identifier_pidentifier_pidentifier(p):
    'identifier : pidentifier LPAREN pidentifier RPAREN'
    p[0] = symbol_table.get_table_on_position_pidentifier(p[1], p[3])


def p_identifier_pidentifier_num(p):
    'identifier : pidentifier LPAREN num RPAREN'
    p[0] = symbol_table.get_table_on_position_num(p[1], p[3])


def p_error(p):
    if p:
        print("Syntax error at token", p.type)
    else:
        print("Syntax error at EOF")
    exit(5)


def main():
    inputFile = "test.imp"
    # outFile = sys.argv[2]
    parser = yacc.yacc()
    with open(inputFile, "r") as file:
        parser.parse(file.read())
    c=0
    for i in code.code:
        print(c, i)
        c += 1
    """
    for i in symbol_table.table:
        print(i)
    """


if __name__ == "__main__":
    main()