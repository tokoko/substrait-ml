import ibis
from ibis_substrait.compiler.core import SubstraitCompiler
from substrait_c.algebra.relations.root import RootRelation
from ibis import literal

t = ibis.table([("Col1", "int64"), ("Col2", "int64")],"t",)
t = t.select(t['Col2'], literal(10, type='int64').name('Lit10'), literal(2).name('Anon1'))

t= t.select(
    ibis.case().when(t['Col2'] < t['Lit10'], literal(2))\
        .when(t['Col2'] > t['Lit10'], literal(1))\
        .else_(literal(-1)).end().name('NamedSwitch')
)

# t = t.select((t['Col2'] / t['Anon1']).name('Col3'))
# t = t.select(t['Col2'] + t['Anon1'])

plan = SubstraitCompiler().compile(t)
root = RootRelation(plan.relations[0].root, plan.extensions)
root.compile_cffi('substrait_example')

inp = {'Col1': 100, 'Col2': 1010}
print(f'Called with {inp}')
res = root.execute_cffi(inp)
print(f'Returned {res}')
