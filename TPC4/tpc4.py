import ply.lex as lex

reserved_keywords = {
    'SELECT': 'SELECT',
    'FROM': 'FROM',
    'WHERE': 'WHERE'
}

tokens = (
    'VARIABLE',
    'COMMA',
    'GREATER',
    'LESSER',
    'GREATER_EQUAL',
    'LESSER_EQUAL',
    'EQUAL',
    'NUM'
) + tuple(reserved_keywords.values())

t_SELECT = r'[Ss][Ee][Ll][Ee][Cc][Tt]'
t_WHERE = r'[Ww][Hh][Ee][Rr][Ee]'
t_FROM = r'[Ff][Rr][Oo][Mm]'

def t_VARIABLE(t):
    r'[A-Za-z_][A-Za-z0-9-_]*'
    t.type = reserved_keywords.get(t.value.upper(), 'VARIABLE')
    return t

t_COMMA = r'\,'
t_GREATER_EQUAL = r'\>\='
t_LESSER_EQUAL = r'\<\='
t_GREATER = r'\>'
t_LESSER = r'\<'
t_EQUAL = r'\='

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere não suportado '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def test_lexer(data):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

test_lexer('Select id, nome, salario From empregados Where salario >= 820')
