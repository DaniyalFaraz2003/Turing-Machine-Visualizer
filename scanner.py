import re
from string import ascii_letters, digits
from file_processing_error import FileProcessingException


class SymbolTable:
    def __init__(self) -> None:
        self._KEYWORDS: list[str] = ["start", "halt", "state", "loop", "statement", "insert", "delete"]
    
    def authorize_token(self, token: str) -> bool:
        if token.lower() in self._KEYWORDS:
            return True
        
        if re.match(r"^\([a-zA-Z0-9],[a-zA-Z0-9],[lr]\)$", token):
            return True
        
        if token in list(ascii_letters + digits + "*$/"): 
            return True
        
        if token.isnumeric():
            return True
        
        if token == "->":
            return True
    
        return False
        


class Scanner:
    def __init__(self) -> None:
        self._source_code: str = ""
        self._filename: str = ""
        self._tokens: list[str] = []
        self._current_idx: int = 0
        self.symbol_table: SymbolTable = SymbolTable()

    def load_source_code(self, file_path: str) -> None:
        self._filename = file_path
        with open(self._filename, "r") as file:
            self._source_code = file.read().strip()

    def get_next_character(self) -> str:
        if self._current_idx >= len(self._source_code):
            return ""
        character: str = self._source_code[self._current_idx]
        self._current_idx += 1
        return character
    
    def output_source_code(self) -> None:
        print(self._source_code)

    def tokenize(self) -> None:
        lineno: int = 1
        current_token: str = ""
        while True:
            character: str = self.get_next_character()
            if character == "":
                break

            if character in [" ", "\n", ";", "}", "{"]:
                if character == "\n": lineno += 1
                if current_token:
                    if self.symbol_table.authorize_token(current_token):
                        self._tokens.append(current_token)
                        current_token = ""
                    else:
                        raise FileProcessingException("SYNTAX ERROR", self._filename, lineno)
                
                if character != " " and character != "\n":
                    self._tokens.append(character)
                continue

            current_token += character

        if current_token:
            if self.symbol_table.authorize_token(current_token):
                self._tokens.append(current_token)
                current_token = ""
            else:
                raise FileProcessingException("SYNTAX ERROR", self._filename, lineno)

    def get_tokens(self) -> list[str]:
        return self._tokens

    def output_tokens(self) -> None:
        print(self._tokens)


def main():
    scanner: Scanner = Scanner()
    scanner.load_source_code("language.txt")
    try:
        scanner.tokenize()
        scanner.output_tokens()
    except FileProcessingException as e:
        print(e)

if __name__ == "__main__":
    main()