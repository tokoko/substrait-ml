from ibis_substrait.proto.substrait.ibis.algebra_pb2 import Expression as ExpressionProto
from ibis_substrait.proto.substrait.ibis.extensions.extensions_pb2 import SimpleExtensionDeclaration
from ibis_substrait.proto.substrait.ibis.type_pb2 import NamedStruct
from typing import List
from cgen.variable import Variable
import random
import string


class ScalarFunction:
    def __init__(self,
                 plan: ExpressionProto.ScalarFunction,
                 root_struct: NamedStruct,
                 extensions: List[SimpleExtensionDeclaration]
                 ):
        function_reference = plan.function_reference

        self._substrait_type = plan.output_type

        for e in extensions:
            if e.extension_function.function_anchor == function_reference:
                self.function_name = e.extension_function.name

        self.arguments = plan.arguments
        self.extensions = extensions
        self.root_struct = root_struct
        self._name = 'Scalar' + ''.join(random.choice(string.digits) for _ in range(6))

    def name(self):
        return self._name

    def substrait_type(self):
        return self._substrait_type

    def to_c(self, base_field_reference: Variable):
        from substrait_c import expr
        arg_expressions = [
            expr(arg.value,
                 root_struct=self.root_struct,
                 extensions=self.extensions).to_c(base_field_reference)
            for arg in self.arguments
        ]

        if self.function_name == 'add':
            return arg_expressions[0] + arg_expressions[1]
        elif self.function_name == 'subtract':
            return arg_expressions[0] - arg_expressions[1]
        elif self.function_name == 'multiply':
            return arg_expressions[0] * arg_expressions[1]
        elif self.function_name == 'divide':
            return arg_expressions[0] / arg_expressions[1]
        elif self.function_name == 'gt':
            return arg_expressions[0] > arg_expressions[1]
        elif self.function_name == 'lt':
            return arg_expressions[0] < arg_expressions[1]
        elif self.function_name == 'and':
            return arg_expressions[0] & arg_expressions[1]
        raise Exception(f'Unknown function {self.function_name}')
