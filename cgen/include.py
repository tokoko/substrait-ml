from cgen.statement import Statement


class Include:
    def __init__(self, content):
        self.content = content

    def include(self):
        return Statement(f'#include {self.content}')


STDIO = Include('<stdio.h>')
