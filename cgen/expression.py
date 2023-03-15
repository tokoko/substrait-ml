
class Expression:
    def __init__(self, content):
        self.content = content

    def render(self):
        return self.content

    def __add__(self, other):
        return Expression(f'({self.content} + {other.content})')

    def __sub__(self, other):
        return Expression(f'({self.content} - {other.content})')

    def __mul__(self, other):
        return Expression(f'({self.content} * {other.content})')

    def __truediv__(self, other):
        return Expression(f'({self.content} / {other.content})')

    def __lt__(self, other):
        return Expression(f'({self.content} < {other.content})')

    def __gt__(self, other):
        return Expression(f'({self.content} > {other.content})')