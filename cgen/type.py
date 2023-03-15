class Type:
    def __init__(self, name, is_struct=False):
        self.name = name
        self.is_struct = is_struct

    def render(self):
        if self.is_struct:
            return f'struct {self.name}'
        else:
            return self.name

    def pointer(self):
        return Type(f'{self.name}*', self.is_struct)


UNSIGNED_CHAR = Type('unsigned char')
CHAR = Type('char')
SIGNED_CHAR = Type('signed char')
INT = Type('int')
UNSIGNED_INT = Type('unsigned int')
SIGNED_INT = Type('signed int')
SHORT = Type('short')
SIGNED_SHORT = Type('signed short')
UNSIGNED_SHORT = Type('unsigned short')
VOID = Type('void')
FLOAT = Type('float')
DOUBLE = Type('double')