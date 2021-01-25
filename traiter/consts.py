"""Shared constants."""

CLOSE = '  ) ] '.split()
COLON = ' :'.split()
COMMA = ' , '.split()
CROSS = ' x × '.split()
DASH = ' – - –– -- '.split()
DOT = ' . '.split()
EQ = ' = '.split()
OPEN = ' ( [ '.split()
PLUS = ' + '.split()
SEMICOLON = ' ; '.split()
SLASH = ' / '.split()
QUOTE = ' “ ” " \' '.split()
LETTERS = list('abcdefghijklmnopqrstuvwxyz')

DASH_RE = '(' + '|'.join(DASH) + ')'
FLOAT_RE = r'\d+\.?\d*'
INT_RE = r'\d+'

FLOAT_TOKEN_RE = f'^{FLOAT_RE}$'
INT_TOKEN_RE = r'^\d+$'

DASH_CHAR = [d for d in DASH if len(d) == 1]