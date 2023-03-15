from substrait_c.algebra.expressions.scalar_function import ScalarFunction
from ibis_substrait.proto.substrait.ibis.algebra_pb2 import Expression
from ibis_substrait.proto.substrait.ibis.algebra_pb2 import FunctionArgument
from ibis_substrait.proto.substrait.ibis.type_pb2 import Type
from ibis_substrait.proto.substrait.ibis.extensions.extensions_pb2 import SimpleExtensionDeclaration


def test_add():
    func = Expression.ScalarFunction(
        function_reference=1,
        arguments=[
            FunctionArgument(
                value=(Expression(literal=Expression.Literal(i32=100)))
            ),
            FunctionArgument(
                value=(Expression(literal=Expression.Literal(i32=200)))
            )
        ],
        output_type= Type(
            i32=Type.I32()
        )
    )

    extend_with_add = [
        SimpleExtensionDeclaration(
            extension_function=SimpleExtensionDeclaration.ExtensionFunction(
                extension_uri_reference=1,
                function_anchor=1,
                name="add"
            )
        )
    ]

    assert ScalarFunction(func, extensions=extend_with_add).to_c().render() == '(100 + 200)'
