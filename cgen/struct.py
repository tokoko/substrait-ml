from typing import List
from cgen.type import Type
from cgen.statement import Statement
from cgen.loop import loop_until, LOOP_ITERATOR
from cgen.function import PRINTF
from cgen.variable import Variable
from cgen.literal import Literal
from cgen.expression import Expression
from cgen.type import INT
from cgen.code import Code


class StructField:
    def __init__(self, data_type: Type, name):
        self.data_type = data_type
        self.name = name


class Struct(Type):
    def __init__(self, name: str, fields: List[StructField]):
        super().__init__(name, is_struct=True)
        self.fields = fields

    def define(self):
        fields_body = '\n'.join([f'    {p.data_type.render()} {p.name};' for p in self.fields])
        ret = f'struct {self.name} {{\n'
        ret += fields_body
        ret += '\n};'
        return Statement(ret)

    def print_formatted(self, var: Variable, size: Expression):
        literal_map = {
            INT: "%d"
        }

        with Code() as body:
            PRINTF.call(
                Literal(';'.join([f'{field.name}: {literal_map[field.data_type]}' for field in self.fields]) + '\\n'),
                *[var.at(LOOP_ITERATOR).field(field.name) for field in self.fields]
            )

        loop_until(size, body)

        # var = Variable()
        # PRINTF.call(Literal('%d\\n'), var_child_output.at(Literal(0)).field('Col2'))
