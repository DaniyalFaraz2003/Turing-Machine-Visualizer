from queue import LifoQueue
from string import digits, ascii_letters

PARSE_TABLE = {
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

class Parser:
    def __init__(self, tokens: list[str]) -> None:
        self._tokens: list[str] = tokens
        self._stack: LifoQueue[str] = LifoQueue()


    def parse(self) -> None:
        pass

    def shift(self, token: str) -> None:
        self._stack.put(token)


    def reduce(self, rule: str) -> None:
        pass



if __name__ == "__main__":
    print(PARSE_TABLE)
