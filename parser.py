from queue import LifoQueue

class Parser:
    def __init__(self, tokens: list[str]) -> None:
        self._tokens: list[str] = tokens
        self._stack: LifoQueue[str] = LifoQueue()


    def parse(self) -> None:
        pass

    def shift(self, token: str) -> None:
        self._stack.put(token)