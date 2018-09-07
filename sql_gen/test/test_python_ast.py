import ast

def children(node):
    result=[]
    for child in ast.iter_child_nodes(node):
        result.append(child)
    return result

def child(node, index):
    return children(node)[index]

def number_of_children(node):
    return len(children(node))


class FunctionCallVisitor(ast.NodeVisitor):
    def visit_Call(self, node):
        print ("hollllllaa" +ast.dump(node))
    def visit_Name(self,node):
        print("visiting name class"+ast.dump(node))

    def visit_Compare(self,node):
        print("visiting Compare class"+ast.dump(node))
        self.generic_visit(node)

code = "a < b"
tree = ast.parse(code)


def draw(tree, spacer):
    if number_of_children(tree) ==0:
        print (spacer + ast.dump(tree))
        return
    
    print(spacer + ast.dump(tree))
    spacer += "  "
    for node in ast.iter_child_nodes(tree):
        draw(node,spacer)

draw(tree,"")

print("***manuall***")
iterator = ast.iter_child_nodes(tree.body[0])
for node in iterator:
    print("direct child:"+ ast.dump(node))
    for node2 in ast.iter_child_nodes(node):
        print("second children: " + ast.dump(node2))
        for node3 in ast.iter_child_nodes(node2):
            print("third children: " + ast.dump(node3))

print("***visitor***")
iterator = ast.iter_child_nodes(tree.body[0])
print (FunctionCallVisitor().visit(tree))
#
