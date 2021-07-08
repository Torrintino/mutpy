import ast

from mutpy.operators import copy_node, MutationOperator, MutationResign


class OneIterationLoop(MutationOperator):
    def one_iteration(self, node):
        node.body.append(ast.Break(lineno=node.body[-1].lineno + 1))
        return node

    @copy_node
    def mutate_For(self, node):
        return self.one_iteration(node)

    @copy_node
    def mutate_While(self, node):
        return self.one_iteration(node)


class ReverseIterationLoop(MutationOperator):
    @copy_node
    def mutate_For(self, node):
        old_iter = node.iter
        node.iter = ast.Call(
            func=ast.Name(id=reversed.__name__, ctx=ast.Load()),
            args=[old_iter],
            keywords=[],
            starargs=None,
            kwargs=None,
        )
        return node


class ZeroIterationLoop(MutationOperator):
    def zero_iteration(self, node):
        node.body = [ast.Break(lineno=node.body[0].lineno)]
        return node

    @copy_node
    def mutate_For(self, node):
        return self.zero_iteration(node)

    @copy_node
    def mutate_While(self, node):
        return self.zero_iteration(node)


class RangeStepIncrement(MutationOperator):

    @classmethod
    def name(cls):
        return 'RSI'

    @copy_node
    def mutate_Call(self, node):
        mutated = False
        if isinstance(node.func, ast.Name):
            if node.func.id != "range":
                raise MutationResign()
        else:
            raise MutationResign()

        if node.keywords:
            for kw in node.keywords:
                if kw.arg == "step":
                    kw.value.value += 1
                    mutated = True
            if not mutated:
                node.keywords.append(
                    ast.keyword(arg="step", value=ast.Constant(2)))
                mutated = True
        if not mutated:
            node.keywords = [
                ast.keyword(arg="step", value=ast.Constant(2))]
        return node


class GenericLoopSkip(MutationOperator):

    @classmethod
    def name(cls):
        return 'GLS'

    def construct_ast(self, offset):
        return ast.If(
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

    def inc_lineno(self, body):
        for node in body:
            if hasattr(node, "body"):
                for node in node.body:
                    node.body = self.inc_lineno(node.body)
            node.lineno += 8
        return body

    def prepend_loop(self, node):
        if_ast = self.construct_ast(node.lineno)
        node.body = [if_ast] + self.inc_lineno(node.body)
        return node

    @copy_node
    def mutate_For(self, node):
        return self.prepend_loop(node)

    @copy_node
    def mutate_While(self, node):
        return self.prepend_loop(node)
