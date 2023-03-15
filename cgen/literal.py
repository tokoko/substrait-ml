from cgen.expression import Expression
from cgen.type import Type


class Literal(Expression):
    def __init__(self, content, data_type: Type = None):
        if type(content) == str:
            content = f'"{content}"'
        elif type(content) == bool:
            content = 'true' if content else 'false'
        elif type(content) == int:
            content = str(content)

        super().__init__(content)
