class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children else []

root = Node(5, [
    Node(3, [
        Node(1),
        Node(4)
    ]),
    Node(2, [
        Node(6),
        Node(0)
    ])
])

def tree_valid(node):
    
    if node.value < 0:
        return False
    
    for child in node.children:
        if not tree_valid(child):
            return False
    
    return True

print(tree_valid(root))