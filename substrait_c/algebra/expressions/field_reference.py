from ibis_substrait.proto.substrait.ibis.algebra_pb2 import Expression
from ibis_substrait.proto.substrait.ibis.type_pb2 import NamedStruct
from substrait_c.schema import Schema
from cgen.variable import Variable
from typing import Union


class FieldReference:
    def __init__(self,
                 plan: Union[Expression.FieldReference, int],
                 root_struct: NamedStruct
                 ):
        if type(plan) == int:
            col_index = plan
        else:
            reference_type = plan.WhichOneof('reference_type')
            root_type = plan.WhichOneof('root_type')

            if root_type != 'root_reference':
                raise Exception('only root_reference allowed in FieldReference')

            if reference_type == 'direct_reference':
                col_index = plan.direct_reference.struct_field.field

            elif reference_type == 'masked_reference':
                raise Exception('masked_reference in FieldReference')

        schema = Schema(None, root_struct)
        self._name = schema.field_name(col_index)
        self.col_type = schema.field_type(col_index)

    def name(self):
        return self._name

    def substrait_type(self):
        return self.col_type

    def to_c(self, base_field_reference: Variable):
        return base_field_reference.field(self._name)

    def __repr__(self):
        return f'FieldReference ({self._name}, {self.col_type.WhichOneof("kind")})'

