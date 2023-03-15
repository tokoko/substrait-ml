from ibis_substrait.proto.substrait.ibis.algebra_pb2 import ProjectRel
from cgen.code import Code
from cgen.function import Function, Parameter
from cgen import type as ctype
from cgen.variable import Variable
from cgen.literal import Literal
from substrait_c import expr, rel
from substrait_c.schema import Schema
from cgen.loop import loop_until, LOOP_ITERATOR
import random
import string
from typing import List
from ibis_substrait.proto.substrait.ibis.extensions.extensions_pb2 import SimpleExtensionDeclaration


class ProjectRelation:
    def __init__(self, plan: ProjectRel, extensions: List[SimpleExtensionDeclaration], root_child=False, names=None):
        self.plan = plan
        self.input_rel = rel(self.plan.input, extensions)

        self.expressions = [
            expr(e, self.input_rel.output_schema().plan, extensions) for e in plan.expressions
        ]

        if names:
            for e, n in zip(self.expressions, names):
                e._name = n

        self.named_struct_output = Schema.to_named_struct(self.expressions, names)
        if root_child:
            self.name = 'output'
        else:
            self.name = 'project' + ''.join(random.choice(string.digits) for _ in range(6))

    def input_schema(self):
        return self.input_rel.input_schema()

    def output_schema(self):
        return Schema(f'st_{self.name}_out', self.named_struct_output)

    def exposed_structs(self):
        ret = self.input_rel.exposed_structs()
        ret.append(self.output_schema())
        return ret

    def exposed_functions(self):
        from_input = self.input_rel.exposed_functions()
        param_input_data = Parameter(self.input_schema().to_c_struct().pointer(), 'inputData')
        param_output_data = Parameter(self.output_schema().to_c_struct().pointer(), 'outputData')
        param_input_size = Parameter(ctype.INT, 'input_size')
        var_child_output = Variable(self.input_rel.output_schema().to_c_struct(), 'childOutputData')

        with Code() as fn_main_code:
            # var_child_output.declare(size=param_input_size)
            var_child_output.declare(size=1)
            from_input[-1].call(param_input_data, var_child_output, param_input_size)

            with Code() as loop_body:
                for e in self.expressions:
                    param_output_data.at(LOOP_ITERATOR) \
                        .field(e.name()) \
                        .assign(e.to_c(var_child_output.at(LOOP_ITERATOR)))

            loop_until(param_input_size, loop_body)

        project_func = Function(f'fn_{self.name}', ctype.VOID, fn_main_code, parameters=[
            param_input_data,
            param_output_data,
            param_input_size
        ])

        from_input.append(project_func)
        return from_input
