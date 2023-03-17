from .algebra.expressions import Literal, FieldReference, ScalarFunction, IfThen
from ibis_substrait.proto.substrait.ibis.algebra_pb2 import Expression as ExpressionProto
from ibis_substrait.proto.substrait.ibis.extensions.extensions_pb2 import SimpleExtensionDeclaration
from ibis_substrait.proto.substrait.ibis.type_pb2 import NamedStruct
from typing import List
from ibis_substrait.proto.substrait.ibis.algebra_pb2 import Rel


def rel(plan: Rel, extensions: List[SimpleExtensionDeclaration], root_child=False, names_override=None):
    import substrait_c.algebra.relations as c
    rel_type = plan.WhichOneof('rel_type')
    if rel_type == 'read':
        return c.ReadRelation(plan.read)
    elif rel_type == 'project':
        return c.ProjectRelation(plan.project, extensions, root_child, names_override)
    else:
        raise Exception(f'Unknown Relation Type {rel_type}')


def expr(plan: ExpressionProto,
         root_struct: NamedStruct,
         extensions: List[SimpleExtensionDeclaration]
         # base_field_reference: Variable
         ):

    rex_type = plan.WhichOneof('rex_type')
    if rex_type == 'literal':
        return Literal(plan.literal)
    elif rex_type == 'selection':
        return FieldReference(plan.selection, root_struct)
    elif rex_type == 'scalar_function':
        return ScalarFunction(plan.scalar_function, root_struct, extensions)
    elif rex_type == 'if_then':
        return IfThen(plan.if_then, root_struct, extensions)
    else:
        raise Exception(f'Unknown rex_type {rex_type}')


__all__ = [
    expr
]