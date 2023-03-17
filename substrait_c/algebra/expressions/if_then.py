from ibis_substrait.proto.substrait.ibis.algebra_pb2 import Expression as ExpressionProto
from ibis_substrait.proto.substrait.ibis.type_pb2 import NamedStruct
from ibis_substrait.proto.substrait.ibis.extensions.extensions_pb2 import SimpleExtensionDeclaration
from typing import List
from cgen.variable import Variable
import random
import string
from cgen.ternary import Ternary


class IfThen:
    def __init__(self,
                 plan: ExpressionProto.IfThen,
                 root_struct: NamedStruct,
                 extensions: List[SimpleExtensionDeclaration]
                 ):
        from substrait_c import expr
        self.if_pair_expressions = [
            (expr(getattr(clause, 'if'), root_struct, extensions),
             expr(clause.then, root_struct, extensions)) for clause in plan.ifs
        ]

        self.else_expr = expr(getattr(plan, 'else'), root_struct, extensions)

        self._name = 'IfThen' + ''.join(random.choice(string.digits) for _ in range(6))

    def name(self):
        return self._name

    def substrait_type(self):
        return self.else_expr.substrait_type()

    def to_c(self, base_field_reference: Variable):
        else_c = self.else_expr.to_c(base_field_reference)
        for pair in self.if_pair_expressions[::-1]:
            else_c = Ternary(pair[0].to_c(base_field_reference),
                             pair[1].to_c(base_field_reference),
                             else_c)

        return else_c
