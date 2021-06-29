import ast


def main():
    with open("elif.py", "r") as source:
        tree = ast.parse(source.read())
    exec(compile(tree, filename="<ast>", mode="exec"))
    tree.body[1] = mutate_If(tree.body[1])
    exec(compile(tree, filename="<ast>", mode="exec"))
    # print(tree.__dict__)
    # analyzer = Analyzer()
    # analyzer.visit(tree)


def mutate_If(node):
    level = 0
    parent_node = None
    orelse = node
    while hasattr(orelse, "orelse"):
        level += 1
        if level == 2:
            parent = node
        elif level > 2:
            parent = node.orelse[0]
        orelse = orelse.orelse[0]
    if parent:
        parent.orelse = [orelse]
    return node
        
        

if __name__ == "__main__":
    main()
