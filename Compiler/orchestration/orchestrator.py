import sys

from Compiler.loading.loader import Loader
from Compiler.resolution.resolver import Resolver
from Compiler.checking.checker import TypeChecker
from Compiler.codegen.generator import CodeGenerator


class Orchestrator:


	def __init__(self) -> None:
		pass


	def compile(self, filepath: str, outpath: str):

		loader = Loader()
		program = loader.load(filepath)

		resolver = Resolver()
		resolver.visit(program)
			
		checker = TypeChecker()
		checker.visit(program)

		print(program.dump())

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
		
			