from ibis.expr.types import Table
from ibis import literal
import ibis
import functools


def dot(table: Table, vec):
    result_columns = []
    for i in range(vec.shape[1]):
        exprs = [table[col] * col_coef for col, col_coef in zip(table.columns, vec[:, i])]
        expr = functools.reduce(lambda a, b: a + b, exprs)
        result_columns.append(expr.name(f'col_{i}'))

    return table.select(*result_columns)


def argmax(table: Table):
    exprs = [table[col] for col in table.columns]

    search_max_expr = ibis.case()

    for i, expr in enumerate(exprs):
        cond = None
        for j, other in enumerate(exprs):
            if i != j:
                if cond is not None:
                    cond = cond & (expr > other)
                else:
                    cond = (expr > other)

        search_max_expr = search_max_expr.when(cond, literal(i))

    search_max_expr = search_max_expr.else_(literal(-1))

    return table.select(search_max_expr.end())


def add(table: Table, vec):
    exprs = []

    for col, const in zip(table.columns, vec):
        exprs.append(table[col] + const)

    return table.select(*exprs)


def subtract(table: Table, vec):
    exprs = []

    for col, const in zip(table.columns, vec):
        exprs.append((table[col] - const).name(col))

    return table.select(*exprs)


def division(table: Table, vec):
    exprs = []

    for col, const in zip(table.columns, vec):
        exprs.append((table[col] / const).name(col))

    return table.select(*exprs)


def multiply(table: Table, vec):
    exprs = []

    for col, const in zip(table.columns, vec):
        exprs.append(table[col] * const)

    return table.select(*exprs)
