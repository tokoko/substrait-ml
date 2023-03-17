from cgen.expression import Expression


class Ternary(Expression):
    def __init__(self, cond_expr: Expression, if_expr: Expression, else_expr: Expression):
        self.cond_expr = cond_expr
        self.if_expr = if_expr
        self.else_expr = else_expr

    def render(self):
        return f'({self.cond_expr.render()} ? {self.if_expr.render()} : {self.else_expr.render()})'

