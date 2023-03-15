from cgen.code import Code
from cgen.statement import Statement
from cgen.expression import Expression
from cgen.variable import Variable
from cgen import type as ctype
from cgen.literal import Literal


class For(Statement):
    def __init__(self,
                 initializer_block: Code,
                 comparison_block: Code,
                 increment_block: Code,
                 code_block: Code
                 ):
        body = '\n'.join([f'    {line}' for line in code_block.render().split('\n')])
        content = f'for ({initializer_block.render()} {comparison_block.render()}; {increment_block.render()[:-1]}) {{\n{body}\n}}'
        super().__init__(content)


LOOP_ITERATOR = Variable(ctype.INT, 'i')


def loop_until(expr: Expression, loop_body: Code):

    with Code() as initializer:
        LOOP_ITERATOR.declare(Literal(0))

    with Code() as comparison:
        Statement(LOOP_ITERATOR < expr)

    with Code() as increment:
        LOOP_ITERATOR.assign(LOOP_ITERATOR + Literal(1))

    For(initializer, comparison, increment, loop_body)
