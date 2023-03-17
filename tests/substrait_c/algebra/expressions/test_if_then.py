# from substrait_c.algebra.expressions import IfThen
# from ibis_substrait.proto.substrait.ibis.algebra_pb2 import Expression
# from ibis_substrait.proto.substrait.ibis.algebra_pb2 import FunctionArgument
# from ibis_substrait.proto.substrait.ibis.type_pb2 import Type
# from ibis_substrait.proto.substrait.ibis.extensions.extensions_pb2 import SimpleExtensionDeclaration
#
#
# def test_add():
#     if_else = Expression.IfThen()
#
#
#     setattr(if_else, 'else', Expression(literal=Expression.Literal(i32=300)))
#     # else_attr = Expression(literal=Expression.Literal(i32=300))
#     # setattr(if_else, 'else', Expression(literal=Expression.Literal(i32=300)))
#     # if_else.ifs = [
#     #         Expression.IfThen.IfClause(
#     #             Expression(literal=Expression.Literal(boolean=True)),
#     #             Expression(literal=Expression.Literal(i32=200))
#     #         )
#     #     ]
#     # print(if_else)
#
#     extend_with_add = [
#         SimpleExtensionDeclaration(
#             extension_function=SimpleExtensionDeclaration.ExtensionFunction(
#                 extension_uri_reference=1,
#                 function_anchor=1,
#                 name="add"
#             )
#         )
#     ]
#
#     assert if_else is None
#
#     # assert IfThen(if_else, None, extend_with_add).to_c(None).render() == ''
#
#     # assert ScalarFunction(func, root_struct=None, extensions=extend_with_add).to_c(None).render() == '(100 + 200)'
