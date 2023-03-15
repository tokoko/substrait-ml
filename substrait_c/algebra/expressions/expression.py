class Expression:
    def __init__(self):
        pass

    def name(self):
        raise NotImplementedError

    def substrait_type(self):
        raise NotImplementedError

    def to_c(self):
        raise NotImplementedError
