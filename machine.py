from parser import Parser
from scanner import Scanner
from file_processing_error import FileProcessingException

class Machine:
    def __init__(self, tokens: list[str]) -> None:
        self._tokens = tokens 
        self._transition_table: dict[(str, dict[(str, tuple)])] = dict()

    def build_transition_table(self) -> None:
        current_state: str = ""
        i = 0
        while i < len(self._tokens):
            token: str = self._tokens[i]
            if token == "STATE":
                current_state = self._tokens[i + 1]
                if not self._transition_table.get(current_state):
                    self._transition_table[current_state] = dict()


            if token == "LOOP":
                while token != "}":
                    if token == "STATEMENT":
                        transition: str = self._tokens[i + 1]
                        next_state: str = self._tokens[i + 3]
                        read_char: str = transition[1]
                        write_char: str = transition[3]
                        move_dir: str = transition[5]

                        self._transition_table[current_state][read_char] = (write_char, move_dir, current_state)
                    i += 1
                    token = self._tokens[i]


            if token == "STATEMENT":
                transition: str = self._tokens[i + 1]
                next_state: str = self._tokens[i + 3]
                read_char: str = transition[1]
                write_char: str = transition[3]
                move_dir: str = transition[5]
                self._transition_table[current_state][read_char] = (write_char, move_dir, next_state)

            i += 1

    def out_transition_table(self) -> None:
        for state, transitions in self._transition_table.items():
            print(f"State: {state}")
            for read_char, transition in transitions.items():
                print(f"  {read_char} -> {transition}")
            print()

def main():
    scanner: Scanner = Scanner()
    scanner.load_source_code("language.txt")
    tokens = None
    try:
        scanner.tokenize()
        scanner.output_tokens()
        tokens = scanner.get_tokens()
    except FileProcessingException as e:
        print(e)

    print()
    
    parser: Parser = Parser(tokens)
    parser.parse()
    parser.output_stack()

    print()

    machine: Machine = Machine(tokens)
    machine.build_transition_table()
    machine.out_transition_table()

if __name__ == "__main__":
    main()