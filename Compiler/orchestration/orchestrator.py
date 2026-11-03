import sys

from Compiler.lexing.lexer import Lexer
from Compiler.parsing.parser import Parser
from Compiler.resolution.resolver import Resolver
from Compiler.checking.checker import TypeChecker
from Compiler.codegen.generator import CodeGenerator


class Orchestrator:


	def __init__(self) -> None:
		pass


	def compile(self, filepath: str, outpath: str):

		with open(filepath) as file:
			content = file.read()
		
		lexer = Lexer(content)
		tokens = lexer.tokenize()
		
		parser = Parser()
		program = parser.parse(tokens)
		
		resolver = Resolver()
		resolver.visit(program)
			
		checker = TypeChecker()
		checker.visit(program)
		
		gen = CodeGenerator(outpath)
		gen.visit(program)


	def run(self):

		if len(sys.argv) <= 1:
			print("usage: cute [filepath] (outpath)")
		elif len(sys.argv) == 2:
			filepath = sys.argv[1]
			outpath = filepath.removesuffix(".ct") + ".cute"
		else:
			filepath = sys.argv[1]
			outpath = sys.argv[2]

		self.compile(filepath, outpath)
		
			