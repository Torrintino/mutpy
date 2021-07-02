import ast


def main():
    with open("open.py", "r") as source:
        tree = ast.parse(source.read())
    exec(compile(tree, filename="<ast>", mode="exec"))

    analyzer = Analyzer()
    tree = analyzer.visit(tree)
    exec(compile(tree, filename="<ast>", mode="exec"))


class Analyzer(ast.NodeTransformer):

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id == "open":
                print(node.__dict__)
            if len(node.args) >= 2:
                mode = node.args[1]
                if isinstance(mode, ast.Constant):
                    self.modify_mode(mode)
            elif node.keywords:
                for kw in node.keywords:
                    if kw.arg == "mode":
                        self.modify_mode(kw.value)
        return node

    def modify_mode(self, mode):
        if mode.value == "w":
            mode.value = "r"
        elif mode.value == "r":
            mode.value = "w"
                        


if __name__ == "__main__":
    main()
