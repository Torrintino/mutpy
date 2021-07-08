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
