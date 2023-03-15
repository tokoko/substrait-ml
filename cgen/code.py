from cgen.statement import Statement
from cgen.code_state import active_code


class Code:
    def __init__(self):
        self.statements = []

    # @staticmethod
    # def get_active_code():
    #     global active_code
    #     return active_code[-1] if active_code else None

    def add(self, *statement, speculative=False):
        for st in statement:
            if not speculative:
                st._set_has_parent()
            self.statements.append(st)

    def render(self):
        return '\n'.join([statement.render() for statement in self.statements])

    def __enter__(self):
        global active_code
        active_code.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        global active_code
        active_code.pop()
        # print([st.content for st in self.statements])
        self.statements = [st for st in self.statements if not st.has_parent]

        for st in self.statements:
            st._set_has_parent()

    def to_statement(self):
        return Statement(self.render())
