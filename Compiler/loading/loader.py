from Compiler.lexing.lexer import Lexer
from Compiler.parsing.parser import Parser
from Compiler.defs.nodes import Node

class Loader:

    def __init__(self) -> None:
        self.lexer = Lexer()
        self.parser = Parser()

    def load(self, filepath: str) -> Node.Program:
        "Loads the source from a file. Will recursively load every file of the source."

        with open(filepath) as file:
            content = file.read()

        stream = self.lexer.tokenize(content)
        program = self.parser.parse(stream)

        return program