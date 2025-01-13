from string import digits, ascii_letters
import re

class ParseTable:
    def __init__(self) -> None:
        self._PARSE_TABLE: dict[str, list[str]] = {
            'S': ["Q Z", "Q E Z", "Q E Z E", "E Q Z E", "E Q E Z E", "E Q E Z"],
            'Q': [r"STATE START { T L }", r"STATE START { L T }", r"STATE START { T L T }", r"STATE START { T }", "STATE START INSERT C -> B ;", "STATE START DELETE -> B ;"],
            'Z': [r"STATE HALT { }"],
            'E': ["E E", r"STATE B { T }", r"STATE B { T L }", r"STATE B { L T }", r"STATE B { T L T }", "STATE B INSERT C -> B ;", "STATE B DELETE -> B ;"],
            'L': [r"LOOP { T }"],
            'T': ["T T", "STATEMENT (C,C,X) -> B ;"],
            'B': ['N', "START", "HALT"],
        }

    def get_vars(self) -> list[str]:
        return list(self._PARSE_TABLE.keys())

    def inverse_production(self, production: str) -> str:
        if re.match(r"^\d+$", production):
            return "B"
        for key, values in self._PARSE_TABLE.items():
            for value in values:
                if value == production:
                    return key

        return ""

class Parser:
    def __init__(self, tokens: list[str]) -> None:
        self._tokens: list[str] = tokens
        self._stack: list[str] = []
        self._parse_table: ParseTable = ParseTable()

    def validate(self) -> bool:
        if len(self._stack) > 0:
            if self._stack[-1] == 'S':
                return True

        return False

    def parse(self) -> None:
        token_idx: int = 0
        while token_idx < len(self._tokens):
            token: str = self._tokens[token_idx]
            look_ahead: str = self._tokens[token_idx + 1] if token_idx + 1 < len(self._tokens) else ""
            if look_ahead == "{" and (token == "START" or token == "HALT"):
                if re.match(r"^\([a-zA-Z0-9],[a-zA-Z0-9],[lr]\)$", token):
                    self.shift("(C,C,X)")
                else:
                    self.shift(token)
                token_idx += 1
                continue

            if re.match(r"^\([a-zA-Z0-9],[a-zA-Z0-9],[lr]\)$", token):
                self.shift("(C,C,X)")
            else:
                self.shift(token)
            token_idx += 1

            # reductions here
            reduce_idx: int = 1
            while reduce_idx <= len(self._stack) and reduce_idx <= 7:
                rule: str = ' '.join(self._stack[len(self._stack) - reduce_idx:])
                
                while self.reduce(rule):
                    reduce_idx = 1
                    rule: str = ' '.join(self._stack[len(self._stack) - reduce_idx:])
                    
                    continue
                reduce_idx += 1

                

    def output_stack(self) -> None:
        print(self._stack)

    def shift(self, token: str) -> None:
        self._stack.append(token)


    def reduce(self, rule: str) -> bool:

        non_terminal: str = self._parse_table.inverse_production(rule)
        if non_terminal == "":
            return False

        pop_count: int = len(rule.split(' '))
        for _ in range(pop_count):
            self._stack.pop()

        self._stack.append(non_terminal)
        return True



def main():
    parser: Parser = Parser(['STATE', 'START', '{', 'STATEMENT', '(a,b,l)', '->', '1', ';', 'STATEMENT', '(a,a,r)', '->', '2', ';', '}', 'STATE', '0', '{', 'STATEMENT', '(a,b,l)', '->', '1', ';', 'STATEMENT', '(a,a,r)', '->', '2', ';', 'LOOP', '{', 'STATEMENT', '(b,a,r)', '->', '0', ';', 'STATEMENT', '(a,a,l)', '->', '0', ';', '}', 'STATEMENT', '(b,b,l)', '->', 'HALT', ';', '}', 'STATE', 'HALT', '{', '}'])

    parser.parse()
    parser.output_stack()


if __name__ == "__main__":
    main()
