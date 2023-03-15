from ibis_substrait.proto.substrait.ibis.algebra_pb2 import Expression as ExpressionProto
from ibis_substrait.proto.substrait.ibis.type_pb2 import Type
from cgen.literal import Literal as LiteralC
from substrait_c.algebra.expressions import Expression
import random
import string


class Literal(Expression):
    def __init__(self, plan: ExpressionProto.Literal):
        super().__init__()
        self.literal_type = plan.WhichOneof('literal_type')

        if self.literal_type == 'boolean':
            self.literal_c = LiteralC(plan.boolean)
        elif self.literal_type == 'i8':
            self.literal_c = LiteralC(plan.i8)
            self._substrait_type = Type(i8=Type.I8())
        elif self.literal_type == 'i16':
            self.literal_c = LiteralC(plan.i16)
            self._substrait_type = Type(i16=Type.I16())
        elif self.literal_type == 'i32':
            self.literal_c = LiteralC(plan.i32)
            self._substrait_type = Type(i32=Type.I32())
        elif self.literal_type == 'i64':
            self.literal_c = LiteralC(plan.i64)
            self._substrait_type = Type(i64=Type.I64())
        elif self.literal_type == 'fp64':
            self.literal_c = LiteralC(plan.fp64)
            self._substrait_type = Type(fp64=Type.FP64())
        else:
            raise Exception(f'Unknown Type -> {self.literal_type}')

        self._name = 'Anon' + ''.join(random.choice(string.digits) for _ in range(6))

    def name(self):
        return self._name

    def substrait_type(self):
        return self._substrait_type

    def to_c(self, base_field_reference=None):
        return self.literal_c

    def __repr__(self):
        return f'Literal (UNKNOWN, {self.literal_type})'
