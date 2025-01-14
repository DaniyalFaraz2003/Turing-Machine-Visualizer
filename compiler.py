from scanner import Scanner
from parser import Parser
from machine import Machine
from file_processing_error import FileProcessingException

class Compiler:
    def __init__(self) -> None:
        self._scanner: Scanner = Scanner()
        self._parser: Parser = None
        self._machine: Machine = None

    def compile(self, file_path: str) -> None:
        self._scanner.load_source_code(file_path)
        tokens = None
        try:
            self._scanner.tokenize()
            self._scanner.output_tokens()
            tokens = self._scanner.get_tokens()
        except FileProcessingException as e:
            print(e)

        print()
        
        self._parser = Parser(tokens)
        self._parser.parse()
        self._parser.output_stack()
        
        try:
            if not self._parser.validate():
                raise FileProcessingException("SYNTAX ERROR", self._scanner.get_filename(), 0)
            else:
                self._machine = Machine(tokens)
                self._machine.build_transition_table()
                self._machine.out_transition_table()
        except FileProcessingException as e:
            print(e)
