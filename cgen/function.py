from typing import List
from cgen.code import Code
from cgen.type import Type
from cgen.statement import Statement
from cgen.variable import Variable


class Parameter(Variable):
    def __init__(self, data_type: Type, name):
        self.data_type = data_type
        self.name = name
        self.content = name

    # def as_variable(self):
    #     return Variable(self.data_type, self.name)


class Function:
    def __init__(self,
                 name: str,
                 return_type: Type = None,
                 body: Code = None,
                 parameters: List[Parameter] = []
                 ):
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.body = body

    def define(self):
        params_signature = ', '.join([f'{p.data_type.render()} {p.name}' for p in self.parameters])
        ret = f'{self.return_type.render()} {self.name}({params_signature}){{\n'
        ret += '\n'.join([f'    {line}' for line in self.body.render().split('\n')])
        ret += '\n}'
        return Statement(ret)

    def call(self, *expressions):
        return Statement(f'{self.name}({", ".join(expr.render() for expr in expressions)});')

    def signature(self):
        params_signature = ', '.join([f'{p.data_type.render()} {p.name}' for p in self.parameters])
        ret = f'{self.return_type.render()} {self.name}({params_signature});'
        return Statement(ret)


PRINTF = Function('printf')
