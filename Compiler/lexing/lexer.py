from typing import List, Optional

from Compiler.lexing.tokens import Token, TokenType
from Compiler.lexing.defintions import SymbolType, KeywordType, KEYWORD_MAP, SYMBOL_MAP


class Lexer:
	"Class for lexing the source code into tokens."

	def __init__(self, source: str):
		self.source = source
		self.length = len(self.source)
		self.pos = 0


	def setSource(self, source: str):
		"Update the current source and resetting the lexer."
		self.source = source
		self.length = len(self.source)
		self.pos = 0


	def tokenize(self) -> List[Token]:
		"Start the tokenization of the current source."

		tokens = []
		while self.pos < self.length:
			ch = self._peek()

			# skip whitespace
			if ch in " \t\r": 
				self._advance()
				continue

			# newline counts as a statement ender
			if ch == "\n":
				self._advance()
				tokens.append(Token(TokenType.EOL, "\n"))
				continue

			if ch == "/" and self._peek(1) == "/":
				self._skip_comments()
				continue

			if ch == '"':
				tokens.append(self._lex_string())
				continue

			if ch == "'":
				tokens.append(self._lex_char())
				continue

			if ch.isdigit():
				tokens.append(self._lex_number())
				continue

			if ch.isalpha() or ch == "_":
				tokens.append(self._lex_word_or_keyword_or_bool())
				continue

			symbol_token = self._lex_symbol()
			if symbol_token:
				tokens.append(symbol_token)
				continue

			raise ValueError(f"Unexpected character '{ch}' at index {self.pos}")

		tokens.append(Token(TokenType.EOF, None))
		return tokens


	def _peek(self, offset: int = 0) -> str:
		"Peek at the next character."
		idx = self.pos + offset
		if idx >= self.length:
			return ""
		return self.source[idx]


	def _advance(self, steps: int = 1) -> str:
		"Advance the character pointer by some steps."
		ch = self._peek()
		self.pos += steps
		return ch
	

	def _skip_comments(self):
		"Handle single and multi-line comments."

		if self._peek(0) == "/" and self._peek(1) == "/" and self._peek(2) == "/":
			self._advance(3)
			while self.pos < self.length:
				if self._peek(0) == "/" and self._peek(1) == "/" and self._peek(2) == "/":
					self._advance(3)
					break
				self._advance()
		else:
			self._advance(2)
			while self.pos < self.length and self._peek() != "\n":
				self._advance()


	def _lex_number(self) -> Token:
		"""
		Tokenize a number.
		Can tokenize integars, floating numbers, hexadecimal (0x) and binary (0b)
		"""
		start = self.pos

		if self._peek() == "0":
			next_ch = self._peek(1).lower()

			if next_ch == "x":
				self._advance(2)
				while self.pos < self.length and (self._peek().isdigit() or self._peek().lower() in "abcdef"):
					self._advance()
				val = int(self.source[start:self.pos], 16)
				return Token(TokenType.Hex, val)

			elif next_ch == "b":
				self._advance(2)
				while self.pos < self.length and self._peek() in "01":
					self._advance()
				val = int(self.source[start:self.pos], 2)
				return Token(TokenType.Bin, val)

		is_float = False

		while self.pos < self.length:
			if self._peek().isdigit():
				self._advance()
			elif self._peek() == "." and not is_float and self._peek(1).isdigit():
				is_float = True
				self._advance()
			else:
				break

		num_str = self.source[start:self.pos]

		if is_float:
			return Token(TokenType.Float, float(num_str))

		return Token(TokenType.Int, int(num_str))


	def _lex_string(self) -> Token:
		"Tokenize a string and process escape sequences."
		self._advance()
		chars = []

		while self.pos < self.length:
			ch = self._peek()
			if ch == '"':
				break
			if ch == '\\':
				self._advance() 
				if self.pos >= self.length:
					raise ValueError("Unterminated string literal")
				
				escaped = self._peek()
				if escaped == 'n':
					chars.append('\n')
				elif escaped == 't':
					chars.append('\t')
				elif escaped == 'r':
					chars.append('\r')
				elif escaped == '\\':
					chars.append('\\')
				elif escaped == '"':
					chars.append('"')
				else:
					chars.append(escaped)
				
				self._advance()
				continue

			chars.append(ch)
			self._advance()

		if self.pos >= self.length:
			raise ValueError("Unterminated string literal")

		self._advance()
		return Token(TokenType.String, "".join(chars))


	def _lex_char(self) -> Token:
		"Tokenize a character literal, handling escape sequences."
		self._advance()

		if self.pos >= self.length:
			raise ValueError("Unterminated char literal")

		ch = self._peek()
		if ch == '\\':
			self._advance()
			if self.pos >= self.length:
				raise ValueError("Unterminated char literal")

			escaped = self._peek()
			if escaped == 'n':
				val = '\n'
			elif escaped == 't':
				val = '\t'
			elif escaped == 'r':
				val = '\r'
			elif escaped == '\\':
				val = '\\'
			elif escaped == "'":
				val = "'"
			else:
				val = escaped
			self._advance()
		else:
			val = ch
			self._advance()

		if self.pos >= self.length or self._peek() != "'":
			raise ValueError("Unterminated or multi-character char literal")

		self._advance() 
		return Token(TokenType.Char, val)


	def _lex_word_or_keyword_or_bool(self) -> Token:

		start = self.pos
		while self.pos < self.length and (self._peek().isalnum() or self._peek() == "_"):
			self._advance()
		text = self.source[start:self.pos]

		if text == KeywordType.BoolTrue.value:
			return Token(TokenType.Bool, True)
		if text == KeywordType.BoolFalse.value:
			return Token(TokenType.Bool, False)
		if text in KEYWORD_MAP:
			return Token(TokenType.Keyword, KEYWORD_MAP[text])
		return Token(TokenType.Word, text)


	def _lex_symbol(self) -> Optional[Token]:

		if self.pos + 1 < self.length:
			two_char = self.source[self.pos:self.pos + 2]
			if two_char in SYMBOL_MAP:
				self._advance(2)
				return Token(TokenType.Symbol, SYMBOL_MAP[two_char])

		one_char = self._peek()
		if one_char in SYMBOL_MAP:
			self._advance(1)
			return Token(TokenType.Symbol, SYMBOL_MAP[one_char])

		return None
