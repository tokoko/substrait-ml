from ibis_substrait.proto.substrait.ibis.type_pb2 import Type, NamedStruct
from cgen.struct import Struct, StructField
from cgen.type import INT, SHORT, DOUBLE
from typing import List
from substrait_c.algebra.expressions import Expression


# TODO conversion between Type objects instead of here

def substrait_type_to_c_type(substrait_type: Type):
    substrait_kind = substrait_type.WhichOneof('kind')
    if substrait_kind == 'i64':
        return INT
    elif substrait_kind == 'i16':
        return SHORT
    elif substrait_kind == 'i8':
        return SHORT
    elif substrait_kind == 'fp64':
        return DOUBLE
    elif substrait_kind == 'bool':
        return INT
    else:
        raise Exception(f'Unknown type: {substrait_kind}')

def substrait_type_to_c(substrait_type: Type):
    substrait_kind = substrait_type.WhichOneof('kind')
    if substrait_kind == 'i64':
        return 'int'
    elif substrait_kind == 'i16':
        return 'short' # TODO
    elif substrait_kind == 'i8':
        return 'short' # TODO
    elif substrait_kind == 'fp64':
        return 'float'
    elif substrait_kind == 'bool':
        return 'int'
    else:
        raise Exception(f'Unknown type: {substrait_kind}')


class Schema:
    def __init__(self, name, plan: NamedStruct):
        self.name = name
        self.c_schema = [
            (name, substrait_type_to_c(substrait_type), substrait_type, substrait_type_to_c_type(substrait_type))
            for name, substrait_type in zip(plan.names, plan.struct.types)
        ]
        self.plan = plan

    def to_c_struct(self) -> Struct:
        return Struct(self.name, fields=[StructField(c_type, name) for name, type, _, c_type in self.c_schema])

    def field_type(self, index):
        return self.c_schema[index][2]

    def field_name(self, index):
        return self.c_schema[index][0]

    @staticmethod
    def to_named_struct(expressions: List[Expression], names_override=None):
        names = [i.name() for i in expressions]

        return NamedStruct(
            names=names if not names_override else names_override,
            struct=Type.Struct(
                types=[i.substrait_type() for i in expressions]
            )
        )
