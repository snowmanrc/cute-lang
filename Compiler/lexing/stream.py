from Compiler.lexing.defintions import KeywordType, SymbolType
from Compiler.lexing.tokens import Token, TokenType, TokenValue


class TokenStream:
    "Token Stream for easier manipulation of tokens."

    def __init__(self, tokens: list[Token]) -> None:
        self._tokens = tokens
        self._pos = 0

    def peek(self, offset: int = 0) -> Token:
        idx = self._pos + offset
        if idx >= len(self._tokens):
            return Token(TokenType.EOF)
        return self._tokens[idx]


    def advance(self, steps: int = 1) -> Token:
        tok = self.peek()
        self._pos += steps
        return tok


    def backtrack(self, steps: int = 1):
        self._pos -= steps


    def expect_token(self, type: TokenType) -> Token | None:
        if self.peek().type == type:
            return self.advance()


    def expect_keyword(self, kw: KeywordType) -> Token | None:
        if self.peek().type == TokenType.Keyword and self.peek().value == kw:
            return self.advance()


    def expect_symbol(self, sym: SymbolType) -> Token | None:
        if self.peek().type == TokenType.Symbol and self.peek().value == sym:
            return self.advance()
