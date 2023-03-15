from ibis_substrait.proto.substrait.ibis.algebra_pb2 import Expression
from substrait_c.algebra.expressions.literal import Literal


def test_boolean():
    assert Literal(Expression.Literal(boolean=True)).to_c().render() == 'true'
    assert Literal(Expression.Literal(boolean=False)).to_c().render() == 'false'


def test_i32():
    assert Literal(Expression.Literal(i32=199)).to_c().render() == '199'
    assert Literal(Expression.Literal(i32=-199)).to_c().render() == '-199'
