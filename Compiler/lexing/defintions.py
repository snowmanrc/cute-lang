from enum import Enum


class KeywordType(Enum):
	"List of Keywords in cute-lang"
	Func = "func"
	Return = "return"
	Let = "let"
	Container = "container"
	Impl = "impl"
	BoolTrue = "true"
	BoolFalse = "false"
	While = "while"
	For = "for"
	If = "if"
	Else = "else"
	Builtin = "__builtin__"


class SymbolType(Enum):
	"List of symbols in cute-lang"
	Plus = "+"
	Minus = "-"
	Star = "*"
	Slash = "/"
	LParen = "("
	RParen = ")"
	LBracket = "["
	RBracket = "]"
	LBrace = "{"
	RBrace = "}"
	Bang = "!"
	Equal = "="
	DEqual = "=="
	NEqual = "!="
	Gte = ">="
	Lte = "<="
	Lt = "<"
	Gt = ">"
	DoubleLt = "<<"
	DoubleGt = ">>"
	Percent = "%"
	Caret = "^"
	Amp = "&"
	Pipe = "|"
	DAmp = "&&"
	DPipe = "||"
	Colon = ":"
	Semicolon = ";"
	Comma = ","
	Dot = "."
	Hashtag = "#"
	Arrow = "->"


KEYWORD_MAP = {k.value: k for k in KeywordType}
SYMBOL_MAP = {s.value: s for s in SymbolType}