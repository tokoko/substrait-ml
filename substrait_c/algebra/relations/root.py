from ibis_substrait.proto.substrait.ibis.algebra_pb2 import RelRoot
from substrait_c.algebra.relations.read import ReadRelation
from substrait_c.algebra.relations.project import ProjectRelation
from cgen.code import Code
from cgen.include import STDIO
from cgen.variable import Variable
from cgen.literal import Literal
from substrait_c import rel
from cgen import type as ctype
from cgen.function import Function, Parameter
from cgen.function import PRINTF
from typing import List
from ibis_substrait.proto.substrait.ibis.extensions.extensions_pb2 import SimpleExtensionDeclaration


class RootRelation:
    def __init__(self, plan: RelRoot, extensions: List[SimpleExtensionDeclaration]):
        self.plan = plan
        self.input_rel = rel(self.plan.input, extensions, root_child=True, names_override=plan.names)
        # print(plan.names)

    def input_schema(self):
        return self.input_rel.input_schema()

    def output_schema(self):
        return self.input_rel.output_schema()

    def exposed_structs(self):
        return self.input_rel.exposed_structs()

    def exposed_functions(self):
        return self.input_rel.exposed_functions()

    def render(self, input_data: list = []):
        with Code() as code:
            STDIO.include()
            from_input = self.exposed_functions()

            for struct in self.exposed_structs():
                struct.to_c_struct().define()

            for func in from_input:
                func.define()

            with Code() as fn_main_code:
                var_size = Variable(ctype.INT, 'size')
                var_size.declare(Literal(len(input_data)))

                var_child_input = Variable(self.input_schema().to_c_struct(), 'childInputData')
                # var_child_input.declare(size=var_size)
                var_child_input.declare(size=1)

                for i, row in enumerate(input_data):
                    for k, v in row.items():
                        var_child_input.at(Literal(i)).field(k).assign(Literal(v))

                var_child_output = Variable(self.input_rel.output_schema().to_c_struct(), 'childOutputData')
                # var_child_output.declare(size=var_size)
                var_child_output.declare(size=1)
                from_input[-1].call(var_child_input, var_child_output, var_size)
                # self.output_schema().to_c_struct().print_formatted(var_child_output, var_size)

            Function('main', ctype.INT, fn_main_code, parameters=[
                Parameter(ctype.INT, 'argc'),
                Parameter(ctype.CHAR, 'argv')# pointer
            ]).define()

        return code.render()

    def render_header(self):
        with Code() as code:
            self.input_schema().to_c_struct().define()
            self.output_schema().to_c_struct().define()
            self.exposed_functions()[-1].signature()

        return code.render()

    def compile_cffi(self, module_name):
        import cffi

        self.cffi_module_name = module_name
        ffi = cffi.FFI()

        ffi.cdef(self.render_header())
        ffi.set_source(module_name, self.render())
        ffi.compile()

    def execute_cffi(self, fields):
        import importlib
        cffi_module = importlib.import_module(self.cffi_module_name)

        _ffi = cffi_module.ffi
        _lib = cffi_module.lib

        st_input = _ffi.new("struct st_read_in *")
        st_output = _ffi.new("struct st_output_out *")

        for k, v in fields.items():
            setattr(st_input[0], k, v)

        _lib.fn_output(st_input, st_output, 1)

        ret = {}
        for field in self.output_schema().plan.names:
            ret[field] = getattr(st_output[0], field)

        return ret
