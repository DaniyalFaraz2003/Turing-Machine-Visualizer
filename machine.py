
class Machine:
    def __init__(self, tokens: list[str]) -> None:
        self._tokens = tokens 
        self._transition_table: dict[(str, dict[(str, tuple)])] = dict()

    def build_transition_table(self) -> None:
        current_state: str = ""
        for i in range(len(self._tokens)):
            token: str = self._tokens[i]
            if token == "STATE":
                current_state = self._tokens[i + 1]
                if not self._transition_table.get(current_state):
                    self._transition_table[current_state] = dict()
                    # to be continued