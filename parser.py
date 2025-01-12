from queue import LifoQueue, Empty
from string import digits, ascii_letters


class ParseTable:
    def __init__(self) -> None:
        self._PARSE_TABLE: dict[str, list[str]] = {
            'S': ["QZ", "QEZ"],
            'Q': [r"STATE START {TL}", "STATE START INSERT C -> B;", "STATE START DELETE -> B;"],
            'Z': [r"STATE HALT {}"],
            'E': ["EE", r"STATE N {T}", r"STATE N {TL}", r"STATE N {LT}", r"STATE N {TLT}", "STATE N INSERT C -> B;", "STATE N DELETE -> B;"],
            'L': [r"LOOP {T}"],
            'T': ["TT", "STATEMENT (C,C,X) -> B;"],
            'N': [str(digit) + 'D' for digit in digits[1:]] + list(digits),
            'D': ["DD"] + list(digits),
            'C': ['/', '$', '*'] + list(ascii_letters) + list(digits),
            'X': ['l', 'r'],
            'B': ['N', "START", "HALT"],
        }

    def inverse_production(self, production: str) -> str:
        for key, value in self._PARSE_TABLE.items():
            if production in value:
                return key

        return ""

class Parser:
    def __init__(self, tokens: list[str]) -> None:
        self._tokens: list[str] = tokens
        self._stack: LifoQueue[str] = LifoQueue()
        self._parse_table: ParseTable = ParseTable()

    def validate(self) -> bool:
        try:
            if self._stack.get(block=False) == 'S':
                return True
        except Empty:
            pass
        
        return False

    def parse(self) -> None:
        pass

    def shift(self, token: str) -> None:
        self._stack.put(token)


    def reduce(self, rule: str) -> bool:
        pass


def main():
    parser: Parser = Parser(['STATE', 'START', '{', 'STATEMENT', '(a,b,l)', '->', '1', ';', 'STATEMENT', '(a,a,r)', '->', '2', ';', '}', 'STATE', '0', '{', 'STATEMENT', '(a,b,l)', '->', '1', ';', 'STATEMENT', '(a,a,r)', '->', '2', ';', 'LOOP', '{', 'STATEMENT', '(b,a,r)', '->', '0', ';', 'STATEMENT', '(a,a,l)', '->', '0', ';', '}', 'STATEMENT', '(b,b,l)', '->', 'HALT', ';', '}', 'STATE', 'HALT', '{', '}'])

    parser.parse()
    print(parser.validate())


if __name__ == "__main__":
    main()
