from ibis_substrait.proto.substrait.ibis.algebra_pb2 import ReadRel
from ibis_substrait.proto.substrait.ibis.type_pb2 import NamedStruct
from substrait_c.schema import Schema
from cgen.function import Function, Parameter
from cgen.code import Code
from cgen import type
from cgen.loop import loop_until, LOOP_ITERATOR
from substrait_c.algebra.expressions import FieldReference


class ReadRelation:
    def __init__(self, read_plan: ReadRel):
        self.read_plan = read_plan
        schema: NamedStruct = self.read_plan.base_schema
        self.expressions = [FieldReference(i, schema) for i in range(len(schema.names))]

    def input_schema(self):
        return Schema('st_read_in', self.read_plan.base_schema)

    def output_schema(self):
        return Schema('st_read_out', self.read_plan.base_schema)

    def exposed_structs(self):
        return [
            self.input_schema(),
            self.output_schema()
        ]

    def exposed_functions(self):
        param_input_data = Parameter(self.input_schema().to_c_struct().pointer(), 'inputData')
        param_output_data = Parameter(self.output_schema().to_c_struct().pointer(), 'outputData')
        param_input_size = Parameter(type.INT, 'input_size')

        with Code() as fn_main_code:

            with Code() as loop_body:
                for e in self.expressions:
                    param_output_data.at(LOOP_ITERATOR) \
                        .field(e.name()) \
                        .assign(e.to_c(param_input_data.at(LOOP_ITERATOR)))  # TODO bind here instead

            loop_until(param_input_size, loop_body)

        return [Function('fn_read', type.VOID, fn_main_code, parameters=[
                param_input_data,
                param_output_data,
                param_input_size
            ])]
