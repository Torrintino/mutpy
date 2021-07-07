import ast

from mutpy import utils
from mutpy.operators.arithmetic import AbstractArithmeticOperatorReplacement
from mutpy.operators.base import MutationOperator, MutationResign, copy_node


class AssignmentOperatorReplacement(AbstractArithmeticOperatorReplacement):
    def should_mutate(self, node):
        return isinstance(node.parent, ast.AugAssign)

    @classmethod
    def name(cls):
        return 'ASR'


class BreakContinueReplacement(MutationOperator):
    def mutate_Break(self, node):
        return ast.Continue()

    def mutate_Continue(self, node):
        return ast.Break()


class ConstantReplacement(MutationOperator):
    FIRST_CONST_STRING = 'mutpy'
    SECOND_CONST_STRING = 'python'

    def mutate_Num(self, node):
        return ast.Num(n=node.n + 1)

    def mutate_Str(self, node):
        if utils.is_docstring(node):
            raise MutationResign()

        if node.s != self.FIRST_CONST_STRING:
            return ast.Str(s=self.FIRST_CONST_STRING)
        else:
            return ast.Str(s=self.SECOND_CONST_STRING)

    def mutate_Str_empty(self, node):
        if not node.s or utils.is_docstring(node):
            raise MutationResign()

        return ast.Str(s='')

    @classmethod
    def name(cls):
        return 'CRP'


class OpenModeReplacement(MutationOperator):

    @copy_node
    def mutate_Call(self, node):
        mutated = False
        
        if isinstance(node.func, ast.Name):
            if node.func.id != "open":
                raise MutationResign()
            
            if len(node.args) >= 2:
                mode = node.args[1]
                if isinstance(mode, ast.Constant):
                    self.modify_mode(mode)
                    mutated = True
            elif node.keywords:
                for kw in node.keywords:
                    if kw.arg == "mode":
                        self.modify_mode(kw.value)
                        mutated = True

        if not mutated:
            raise MutationResign()
        return node

    def modify_mode(self, mode):
        if mode.value == "w":
            mode.value = "r"
        elif mode.value == "r":
            mode.value = "w"
        elif mode.value == "x":
            mode.value = "r"
        elif "b" in mode.value:
            mode.value = mode.value.replace("b", "t")
        else:
            mode.value += "b"

    @classmethod
    def name(cls):
        return 'OMR'

class OpenEncodingReplacement:

    @copy_node    
    def mutate_Call(self, node):
        mutated = False
        
        if isinstance(node.func, ast.Name):
            if node.func.id != "open":
                raise MutationResign()

            if node.keywords:
                for kw in node.keywords:
                    if kw.arg == "encoding":
                        if kw.value.value == "windows-1252":
                            kw.value.value = "utf-8"
                        else:
                            kw.value.value = "windows-1252"
                        mutated = True
        if not mutated:
            raise MutationResign()
        return node

    @classmethod
    def name(cls):
        return 'OER'

class SliceIndexRemove(MutationOperator):
    def mutate_Slice_remove_lower(self, node):
        if not node.lower:
            raise MutationResign()

        return ast.Slice(lower=None, upper=node.upper, step=node.step)

    def mutate_Slice_remove_upper(self, node):
        if not node.upper:
            raise MutationResign()

        return ast.Slice(lower=node.lower, upper=None, step=node.step)

    def mutate_Slice_remove_step(self, node):
        if not node.step:
            raise MutationResign()

        return ast.Slice(lower=node.lower, upper=node.upper, step=None)


class SelfVariableDeletion(MutationOperator):
    def mutate_Attribute(self, node):
        try:
            if node.value.id == 'self':
                return ast.Name(id=node.attr, ctx=ast.Load())
            else:
                raise MutationResign()
        except AttributeError:
            raise MutationResign()


class StatementDeletion(MutationOperator):
    def mutate_Assign(self, node):
        return ast.Pass()

    def mutate_Return(self, node):
        return ast.Pass()

    def mutate_Expr(self, node):
        if utils.is_docstring(node.value):
            raise MutationResign()
        return ast.Pass()

    @classmethod
    def name(cls):
        return 'SDL'
