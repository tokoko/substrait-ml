
class Expression:
    def __init__(self, content):
        self.content = content

    def render(self):
        return self.content

    def __add__(self, other):
        return Expression(f'({self.render()} + {other.render()})')

    def __sub__(self, other):
        return Expression(f'({self.render()} - {other.render()})')

    def __mul__(self, other):
        return Expression(f'({self.render()} * {other.render()})')

    def __truediv__(self, other):
        return Expression(f'({self.render()} / {other.render()})')

    def __lt__(self, other):
        return Expression(f'({self.render()} < {other.render()})')

    def __gt__(self, other):
        return Expression(f'({self.render()} > {other.render()})')

    def __and__(self, other):
        return Expression(f'({self.render()} & {other.render()})')
