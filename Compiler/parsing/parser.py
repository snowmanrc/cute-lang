from Compiler.lexing.lexer import Lexer
from Compiler.lexing.stream import TokenStream
from Compiler.lexing.tokens import KeywordType, SymbolType, Token, TokenType

from Compiler.defs.nodes import Node
from Compiler.parsing.rules import Rules


class Parser:


	def __init__(self) -> None:
		self._tokens: TokenStream


	def parse(self, tokens: TokenStream):

		self._tokens = tokens

		nodes = []

		while True:

			self._eat_stmt_enders()

			if self._tokens.expect_keyword(KeywordType.Func):
				self._tokens.backtrack()
				func = self._parse_func()
				nodes.append(func)
				continue

			if self._tokens.expect_keyword(KeywordType.Container):
				self._tokens.backtrack()
				func = self._parse_container()
				nodes.append(func)
				continue

			if self._tokens.expect_keyword(KeywordType.Impl):
				self._tokens.backtrack()
				func = self._parse_impl()
				nodes.append(func)
				continue

			if self._tokens.peek().type == TokenType.EOF:
				break

			raise ValueError(f"Unexpected token: {self._tokens.peek()}")

		program = Node.Program(nodes)

		return program


	def _eat_stmt_enders(self):
		while self._tokens.peek().type == TokenType.EOL or self._tokens.expect_symbol(SymbolType.Semicolon):
			self._tokens.advance()


	def _parse_statement(self) -> Node.Statement:

		self._eat_stmt_enders()

		handlers: dict = {
			KeywordType.Let:     self._parse_decl,
			KeywordType.If:      self._parse_if,
			KeywordType.While:   self._parse_while,
			KeywordType.For:     self._parse_for,
			KeywordType.Return:  self._parse_return,
			KeywordType.Builtin: self._parse_builtin,
			SymbolType.LBrace:   self._parse_block,
		}

		current_token = self._tokens.peek()

		if current_token.value in handlers:
			node = handlers[current_token.value]()
		else:
			node = self._parse_expression()

		self._eat_stmt_enders()

		return node


	def _parse_expression(self, prev_bp: float = 0) -> Node.Expression:

		symbol_token = self._tokens.expect_token(TokenType.Symbol)

		if symbol_token is None:
			lhs = self._parse_atom()

		elif symbol_token.value == SymbolType.LParen:
			lhs = self._parse_expression()
			if self._tokens.expect_symbol(SymbolType.RParen) is None:
				raise ValueError("Unterminated paran.")

		elif symbol_token.value in Rules.UNARY_OP_MAPPING:
			unary = Rules.UNARY_OP_MAPPING[symbol_token.value]
			l_bp, r_bp = Rules.OPERATOR_BINDING_POWER[unary]
			lhs = self._parse_expression(r_bp)
			lhs = Node.UnaryOp(
				unary,
				lhs
			)

		else:
			raise ValueError(f"Unexpected token {self._tokens.peek()}")

		while True:

			if self._tokens.expect_token(TokenType.EOL) or self._tokens.expect_token(TokenType.EOF):
				self._tokens.backtrack()
				return lhs

			if self._tokens.peek().value in Rules.STATEMENT_ENDERS:
				return lhs

			symbol_token = self._tokens.expect_token(TokenType.Symbol)

			if symbol_token is None:
				raise ValueError("Expected symbol.")

			if symbol_token.value == SymbolType.LParen:
				self._tokens.backtrack()
				if prev_bp >= Rules.PARENTHESIS_INFIX_BP:
					return lhs
				lhs = self._parse_call(lhs)
				continue

			operation = Rules.BINARY_OPERATOR_MAPPING.get(symbol_token.extract(SymbolType))

			if operation is None:
				raise ValueError(f"Unknown token: {self._tokens.peek()}")

			l_bp, r_bp = Rules.OPERATOR_BINDING_POWER[operation]

			if prev_bp > l_bp:
				self._tokens.backtrack()
				return lhs

			lhs = Node.BinaryOp(
				operation,
				lhs,
				self._parse_expression(r_bp)
			)


	def _parse_atom(self) -> Node.Expression:
		token = self._tokens.advance()

		if token.type in (TokenType.Int, TokenType.Hex, TokenType.Bin):
			return Node.Literal("int", token.extract(int))

		elif token.type == TokenType.Float:
			return Node.Literal("float", token.extract(float))

		elif token.type == TokenType.Bool:
			return Node.Literal("bool", token.extract(bool))

		elif token.type == TokenType.Char:
			return Node.Literal("char", token.extract(str))

		elif token.type == TokenType.String:
			return Node.Literal("string", token.extract(str))

		elif token.type == TokenType.Word:
			return Node.Identifier(token.extract(str))

		else:
			raise ValueError(f"Expected atomic expression! Got {token}")


	def _parse_call(self, callee: Node.Expression) -> Node.Call:

		token = self._tokens.expect_symbol(SymbolType.LParen)

		if token is None: raise ValueError("Expected Left Paren")

		args = []

		while self._tokens.expect_symbol(SymbolType.RParen) is None:
			args.append(self._parse_expression())
			if not self._tokens.expect_symbol(SymbolType.Comma):
				token = self._tokens.expect_symbol(SymbolType.RParen)
				if token is None: raise ValueError("Expected Right Paren")
				break

		return Node.Call(
			callee,
			args
		)


	def _parse_block(self) -> Node.Block:

		self._tokens.expect_symbol(SymbolType.LBrace)

		stmts = []
		while self._tokens.expect_symbol(SymbolType.RBrace) is None:
			stmts.append(self._parse_statement())

		return Node.Block(stmts)


	def _parse_decl(self, *, type_must_be_specified: bool = False, let_required: bool = True, no_value: bool = False) -> Node.Declaration:

		token = self._tokens.expect_keyword(KeywordType.Let)

		if let_required and token is None: raise ValueError("Expected keyword")

		name_token = self._tokens.expect_token(TokenType.Word)
		if name_token is None: raise ValueError()
		name = name_token.extract(str)

		if self._tokens.expect_symbol(SymbolType.Colon):
			decl_type_token = self._tokens.expect_token(TokenType.Word)
			if decl_type_token is None: raise ValueError()
			decl_type = decl_type_token.extract(str)
		else:
			if type_must_be_specified:
				raise ValueError("Type must be specified for this declaration.")
			decl_type = None

		if self._tokens.expect_symbol(SymbolType.Equal) and not no_value:
			value = self._parse_expression()
		else:
			value = None

		return Node.Declaration(name, Node.Identifier(decl_type) if decl_type else None, value)


	def _parse_if(self) -> Node.If:

		token = self._tokens.expect_keyword(KeywordType.If)
		if token is None: raise ValueError()

		condition = self._parse_expression()

		then_block = self._parse_block()

		if self._tokens.expect_keyword(KeywordType.Else) is not None:
			else_stmt = self._parse_statement()
		else:
			else_stmt = None

		return Node.If(condition, then_block, else_stmt)


	def _parse_while(self) -> Node.While:

		token = self._tokens.expect_keyword(KeywordType.While)
		if token is None: raise ValueError()

		condition = self._parse_expression()

		block = self._parse_block()

		return Node.While(condition, block)


	def _parse_for(self) -> Node.For:

		token = self._tokens.expect_keyword(KeywordType.For)
		if token is None: raise ValueError()

		init = self._parse_statement()
		token = self._tokens.expect_symbol(SymbolType.Comma)
		if token is None: raise ValueError()
		condition = self._parse_expression()
		token = self._tokens.expect_symbol(SymbolType.Comma)
		if token is None: raise ValueError()
		step = self._parse_expression()

		block = self._parse_block()

		return Node.For(init, condition, step, block)


	def _parse_return(self) -> Node.Return:

		token = self._tokens.expect_keyword(KeywordType.Return)
		if token is None: raise ValueError()

		if self._tokens.expect_symbol(SymbolType.Semicolon) or self._tokens.peek().type == TokenType.EOL:
			return Node.Return()

		value = self._parse_expression()

		return Node.Return(value)


	def _parse_func(self) -> Node.Function:

		token = self._tokens.expect_keyword(KeywordType.Func)
		if token is None:
			raise ValueError("Expected keyword Func")

		name_token = self._tokens.expect_token(TokenType.Word)
		if name_token is None:
			raise ValueError("Expected function name")
		name = name_token.extract(str)

		token = self._tokens.expect_symbol(SymbolType.LParen)
		if token is None:
			raise ValueError("Expected left parenthesis")

		params = []

		while True:
			if self._tokens.expect_symbol(SymbolType.RParen):
				break
			params.append(self._parse_decl(type_must_be_specified=True, let_required=False))
			self._tokens.expect_symbol(SymbolType.Comma)

		token = self._tokens.expect_symbol(SymbolType.Arrow)
		if token is None:
			raise ValueError("Expected arrow")

		return_type_token = self._tokens.expect_token(TokenType.Word)
		if return_type_token is None:
			raise ValueError("Expected return type")
		return_type = return_type_token.extract(str)

		self._eat_stmt_enders()

		body = self._parse_block()

		return Node.Function(name, params, body, Node.Identifier(return_type))


	def _parse_builtin(self) -> Node.BuiltinCommand:

		token = self._tokens.expect_keyword(KeywordType.Builtin)
		if token is None:
			raise ValueError("Expected keyword Builtin")

		args: list[Node.Identifier] = []

		while not (self._tokens.expect_symbol(SymbolType.Semicolon) or self._tokens.expect_token(TokenType.EOL)):
			token = self._tokens.expect_token(TokenType.Word)
			if token is None:
				raise ValueError("Expected word argument")
			args.append(Node.Identifier(token.extract(str)))

		return Node.BuiltinCommand(args)


	def _parse_container(self) -> Node.Container:

		token = self._tokens.expect_keyword(KeywordType.Container)
		if token is None:
			raise ValueError("Expected keyword Container")

		name_token = self._tokens.expect_token(TokenType.Word)
		if name_token is None:
			raise ValueError("Expected container name")
		name = name_token.extract(str)

		if self._tokens.expect_symbol(SymbolType.Star):
			return Node.Container(
				name,
				True,
				[]
			)

		self._tokens.expect_symbol(SymbolType.LBrace)
		fields = []

		while not self._tokens.expect_symbol(SymbolType.RBrace):
			self._eat_stmt_enders()
			fields.append(self._parse_decl(type_must_be_specified=True, let_required=False, no_value=True))

			if self._tokens.expect_symbol(SymbolType.Comma):
				continue

			self._eat_stmt_enders()
			if self._tokens.expect_symbol(SymbolType.RBrace):
				break

		return Node.Container(
			name,
			False,
			fields
		)


	def _parse_impl(self) -> Node.ContainerImpl:

		token = self._tokens.expect_keyword(KeywordType.Impl)
		if token is None:
			raise ValueError("Expected keyword Impl")

		name_token = self._tokens.expect_token(TokenType.Word)
		if name_token is None:
			raise ValueError("Expected implementation name")
		name = name_token.extract(str)

		token = self._tokens.expect_symbol(SymbolType.LBrace)
		if token is None:
			raise ValueError("Expected left brace")

		methods = []

		while not self._tokens.expect_symbol(SymbolType.RBrace):
			self._eat_stmt_enders()

			method = self._parse_func()
			methods.append(method)

			self._eat_stmt_enders()

		return Node.ContainerImpl(
			name,
			methods
		)