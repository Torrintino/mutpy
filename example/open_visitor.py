import ast


def main():
    with open("open.py", "r") as source:
        tree = ast.parse(source.read())
    exec(compile(tree, filename="<ast>", mode="exec"))

    analyzer = Analyzer()
    analyzer.visit(tree)


class Analyzer(ast.NodeVisitor):

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id == "open":
                print(node.__dict__)
            if len(node.args) >= 2:
                mode = node.args[1]
                if isinstance(mode, ast.Constant):
                    if mode.value == "w":
                        mode.value = "r"
                    elif mode.value == "r":
                        mode.value = "w"
            elif node.keywords:
                pass


if __name__ == "__main__":
    main()
