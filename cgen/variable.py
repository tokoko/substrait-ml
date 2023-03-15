from cgen.statement import Statement
from cgen.type import Type
from cgen.expression import Expression


class Variable(Expression):
    def __init__(self, data_type: Type, name: str):
        self.data_type = data_type
        self.name = name
        super().__init__(name)

    # TODO CHANGE TO EXPR
    def at(self, expr: Expression):
        return Variable(self.data_type, self.name+f'[{expr.render()}]')

    def field(self, field):
        return Variable(self.data_type, self.name + f'.{field}')

    def declare(self, value: Expression = None, size=None) -> Statement:
        declare_str = f'{self.data_type.render()} {self.name}'

        if size is not None:
            if type(size) == int:
                declare_str += f'[{size}]'
            else:
                declare_str += f'[{size.name}]'

        if value is not None:
            return Statement(f'{declare_str} = {value.render()};')
        else:
            return Statement(f'{declare_str};')

    def assign(self, value: Expression) -> Statement:
        return Statement(f'{self.name} = {value.render()};')
