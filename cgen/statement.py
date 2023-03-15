from cgen.expression import Expression
from cgen.code_state import get_active_code

class Statement:
    def __init__(self, content):
        if type(content) == Expression:
            self.content = content.render()
        else:
            self.content = content
        self.has_parent = False
        active_code = get_active_code()
        if active_code:
            # print(content)
            # print(active_code)
            active_code.add(self, speculative=True)

    def render(self):
        return f'{self.content}'

    def _set_has_parent(self):
        self.has_parent = True
