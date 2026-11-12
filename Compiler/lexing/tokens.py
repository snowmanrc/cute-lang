from enum import Enum, auto
from typing import Union

from Compiler.lexing.defintions import SymbolType, KeywordType, SYMBOL_MAP, KEYWORD_MAP

class TokenType(Enum):
	Int = auto()
	Hex = auto()
	Bin = auto()
	Float = auto()
	Bool = auto()
	Word = auto()
	String = auto()
	Char = auto()
	Symbol = auto()
	Keyword = auto()
	EOL = auto()
	EOF = auto()


TokenValue = Union[int, float, bool, str, SymbolType, KeywordType, None]


class Token:
	"The smallest meaningful unit in the source."

	def __init__(self, token_type: TokenType, value: TokenValue = None):
		self.type = token_type
		self.value = value


	def extract[T](self, value_type: type[T]) -> T:
		"Get the value of the token if it is of the expected type"
		if not isinstance(self.value, value_type):
			raise ValueError(
				f"Expected token value of type {value_type.__name__}, got {type(self.value).__name__}"
			)
		return self.value


	def __repr__(self):
		return f"Token({self.type.name}, {self.value!r})"
