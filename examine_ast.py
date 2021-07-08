import ast
from mutpy.utils import create_ast
from mutpy import codegen


with open("example/for.py") as f:
    code = f.read()

code_ast = create_ast(code)
offset = code_ast.body[0].lineno
constructed_ast = ast.If(
    test=ast.Compare(
        left=ast.Constant("unique_mutation_var"), ops=[ast.In()],
        comparators=[
            ast.Call(func=ast.Name("locals"), args=[], keywords=[])
        ]),
    body=[
        ast.If(
            test=ast.Name("unique_mutation_var"),
            body=[
                ast.Assign(
                    targets=[ast.Name("unique_mutation_var")],
                    value=ast.Constant(0),
                    lineno=offset+3),
                ast.Continue(lineno=offset+4),
            ],
            orelse=[
                ast.Assign(
                    targets=[ast.Name("unique_mutation_var")],
                    value=ast.Constant(1),
                    lineno=offset+6)
            ],
            lineno=offset+2)
    ],
    orelse=[
        ast.Assign(
            targets=[ast.Name("unique_mutation_var")],
            value=ast.Constant(1),
            lineno=offset+8)
    ],
    lineno=offset+1)

code_ast.body[0].body = [constructed_ast] + code_ast.body[0].body
#print(code_ast.body[0].body)
print(codegen.to_source(code_ast))
