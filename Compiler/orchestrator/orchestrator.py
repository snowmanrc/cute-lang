import sys

from Compiler.lexer.lexer import Lexer
from Compiler.parser.parser import Parser
from Compiler.resolver.resolver import Resolver
from Compiler.checker.checker import TypeChecker
from Compiler.codegen.generator import CodeGenerator


class Orchestrator:


	def __init__(self) -> None:
		pass


	def compile(self, filepath: str, outpath: str):

		with open(filepath) as file:
			content = file.read()
		
		lexer = Lexer()
		tokens = lexer.tokenize(content)
		
		parser = Parser()
		program = parser.parse(tokens)
		
		resolver = Resolver()
		resolver.visit(program)
			
		checker = TypeChecker()
		checker.visit(program)
		
		gen = CodeGenerator(outpath)
		gen.visit(program)


	def run(self):
		filepath = sys.argv[1]
		outpath = filepath.removesuffix(".ct") + ".cute"

		self.compile(filepath, outpath)
		
			