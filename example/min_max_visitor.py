import ast


def main():
    with open("min_max.py", "r") as source:
        tree = ast.parse(source.read())
    print(ast.dump(tree.body[0]))
    exec(compile(tree, filename="<ast>", mode="exec"))
    mutate_max(tree.body[0])
    print(ast.dump(tree.body[0]))
    exec(compile(tree, filename="<ast>", mode="exec"))
    # print(tree.__dict__)
    # analyzer = Analyzer()
    # analyzer.visit(tree)


def mutate_max(node):
    if hasattr(node, "value"):
        intermediate = getattr(node, "value")
        if hasattr(intermediate, "func"):
            intermediate_2 = getattr(intermediate, "func")
            if hasattr(intermediate_2, "id"):
                intermediate_3 = getattr(intermediate_2, "id")
                if intermediate_3 == 'max':
                    setattr(intermediate_2, "id", "min")


if __name__ == "__main__":
    main()
