DIGITS = '0123456789'
TT_INT = 'TT_INT'
TT_FLOAT = 'TT_FLOAT'
TT_PLUS = 'TT_PLUS'
TT_MINUS = 'TT_MINUS'
TT_DIV = 'TT_DIV'
TT_MUL = 'TT_MUL'
TT_LPAREN = 'TT_LPAREN'
TT_RPAREN = 'TT_RPAREN'
TT_WHITESPACE = 'TT_WHITESPACE'

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn 
        self.ftxt = ftxt
        
    def advance(self, currentChar):
        self.idx += 1
        self.col += 1
        if currentChar == '\n':
            self.ln += 1
            self.col = 0
        return self
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)
        
class Error:
    def __init__(self, pos_start, pos_end, error_name,details):
        self.error_name = error_name
        self.details = details
        self.pos_start = pos_start
        self.pos_end = pos_end
        
    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f' At file {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result

class IllegalCharError(Error):
    def __init__(self,pos_start, pos_end, details):
        super().__init__(pos_start, pos_end,'Illegal Character', details)
        
class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
        
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

class Lexer:
    def __init__(self, fn, text):
        self.text = text
        self.fn = fn
        self.pos = Position(-1,0,-1,fn,text)
        self.currentChar = None
        self.advance()
    
    def advance(self):
        self.pos.advance(self.currentChar)
        self.currentChar = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        
    def make_tokens(self):
        tokens = []
        while self.currentChar != None:
            if self.currentChar in '\t':
                self.advance()
            elif self.currentChar in DIGITS:
                tokens.append(self.make_number())
                
            elif self.currentChar == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.currentChar == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.currentChar == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.currentChar == '/':
                tokens.append(Token(TT_DIV))
                self.advance()    
            elif self.currentChar == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.currentChar == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            elif self.currentChar == ' ':
                tokens.append(Token(TT_WHITESPACE))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.currentChar
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'"+char+"'")
        return tokens, None
    
    def make_number(self):
        num_str = ''
        dot_count = 0
        while self.currentChar != None and self.currentChar in DIGITS + '.':
            if self.currentChar == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.currentChar
            self.advance()
        
        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))
         
def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    return tokens, error    
    